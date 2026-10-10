#!/usr/bin/env python3
"""Collect human-written GitHub comments for the baseline. Standard library plus the gh CLI.

    python3 collect_github.py [--out data/human_github.jsonl] [--seed 2026] [--until 2026-10-07]
    python3 collect_github.py --control        # pre-LLM control corpus, see below

Read-only: every request is a GET through `gh api`. For each repo it draws a few random three-day
windows from the period, reads the PR review comments and the issue-tracker comments created in
them (the latter cover both PR conversation comments and issue comments), drops bots and comments
that label themselves as AI-generated, then samples a fixed number per kind with a per-author and
per-thread cap. Usernames are never written; @mentions inside the text become "@user"; bot command
lines such as /retest or @rustbot are removed.

Default period: 2025-01-01 up to four days before --until (default: today). With --control the
period is 2021-01-01 to 2022-09-30, before LLM-assisted commenting was common, and the repo list
drops repos that did not exist yet. The control exists to measure how far the recent sample has
drifted from how people wrote before assistants.
"""
import argparse
import json
import random
import re
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlencode

DATA = Path(__file__).parent / "data"
ISO = "%Y-%m-%dT%H:%M:%SZ"

REPOS = [
    "vercel/next.js", "facebook/react", "microsoft/vscode", "rust-lang/rust", "golang/go",
    "kubernetes/kubernetes", "astral-sh/uv", "tailwindlabs/tailwindcss", "denoland/deno",
    "ollama/ollama", "oven-sh/bun", "sveltejs/svelte", "zed-industries/zed",
    "home-assistant/core", "godotengine/godot", "python/cpython", "pytorch/pytorch",
    "vuejs/core", "nodejs/node", "vitejs/vite", "huggingface/transformers",
    "microsoft/TypeScript", "grafana/grafana", "langchain-ai/langchain",
]
NOT_IN_2021 = {"astral-sh/uv", "ollama/ollama", "oven-sh/bun", "zed-industries/zed", "langchain-ai/langchain"}
CONTROL_REPOS = [r for r in REPOS if r not in NOT_IN_2021]
CONTROL_PERIOD = ("2021-01-01", "2022-09-30")
RECENT_FROM = "2025-01-01"

TARGETS = {"pr_review": 12, "pr_comment": 10, "issue_comment": 12}  # per repo
WINDOWS_PER_REPO = 6
WINDOW_DAYS = 3
PAGES_PER_WINDOW = 2     # 100 comments per page, per stream
MAX_PER_AUTHOR = 4       # per repo, across kinds
MAX_PER_THREAD = 2
MAX_CHARS = 4000

BOT_EXACT = {"bors", "stale", "welcome", "github-actions", "dependabot", "renovate", "codecov",
             "vercel", "netlify", "coderabbitai", "gopherbot", "linux-foundation-easycla"}
BOT_PARTS = ("dependabot", "renovate", "codecov", "coderabbit", "github-actions", "netlify",
             "changeset", "easycla", "cla-", "copilot", "claude", "gemini-code", "sonar", "snyk",
             "mergify", "greptile", "graphite", "ellipsis", "sourcery", "codspeed",
             "pre-commit-ci", "allcontributors", "imgbot", "dosu", "k8s-ci", "k8s-triage",
             "fejta", "rust-log-analyzer", "rust-timer", "highfive", "vercel[", "gopherbot")

PROW = ("lgtm approve retest test hold unhold assign unassign cc uncc close reopen kind area sig "
        "triage priority label remove-label remove-kind remove-area remove-sig remove-priority "
        "remove-lifecycle lifecycle ok-to-test override retitle milestone wg committee "
        "good-first-issue help help-wanted cherrypick cherry-pick merge rebase squash retry rerun "
        "check skip").split()
COMMAND_LINE = re.compile(
    r"^(?:/(?:%s)(?:\s.*)?|@(?:rust-timer|rustbot|bors|[\w-]*bot)\b.*|bors\b.*|r\? @.*)$" % "|".join(PROW),
    re.I)
AI_LABEL = re.compile(
    r"generated (?:with|by) \W{0,4}(?:claude|chatgpt|copilot|gemini|cursor|codex|gpt)"
    r"|co-authored-by:\s*(?:claude|copilot|chatgpt|gemini|gpt)"
    r"|\U0001F916 generated"
    r"|(?:written|drafted|composed) (?:with|by) (?:the help of )?(?:claude|chatgpt|copilot|gemini|gpt)"
    r"|as an ai (?:language )?model", re.I)
MENTION = re.compile(r"(?<![\w`/])@[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})(?:/[\w.-]+)?")
CRUDE_CODE = re.compile(r"```.*?```|!\[[^\]]*\]\([^)]*\)|https?://\S+|<[^>]+>", re.S)

api_calls = 0


def gh_get(endpoint, params):
    global api_calls
    url = f"{endpoint}?{urlencode(params)}"
    for attempt in range(5):
        api_calls += 1
        p = subprocess.run(["gh", "api", "--method", "GET", url], capture_output=True, text=True)
        if p.returncode == 0:
            return json.loads(p.stdout)
        msg = (p.stderr + p.stdout).lower()
        if "404" in msg or "not found" in msg:
            raise LookupError(url)
        time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"gh api kept failing for {url}: {p.stderr.strip()[:200]}")


def is_bot(user):
    if not user or user.get("type") != "User":
        return True
    login = user["login"].lower()
    return (login in BOT_EXACT or login.endswith("bot") or login.endswith("robot")
            or any(part in login for part in BOT_PARTS))


def prepare(body):
    """Normalise newlines, drop bot-command lines, hide @mentions. Returns None if nothing is left."""
    lines = [ln.rstrip() for ln in body.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    lines = [ln for ln in lines if not COMMAND_LINE.match(ln.strip())]
    text = MENTION.sub("@user", "\n".join(lines)).strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    if not re.search(r"[A-Za-z0-9]", CRUDE_CODE.sub("", text)):
        return None
    return text


def windows_for(repo, seed, start, end):
    """Random WINDOW_DAYS-long windows inside [start, end], deterministic for (repo, seed)."""
    span = (end - start - timedelta(days=WINDOW_DAYS)).total_seconds()
    rng = random.Random(f"{seed}:{repo}:windows")
    starts = sorted(start + timedelta(seconds=rng.random() * span) for _ in range(WINDOWS_PER_REPO))
    return [(s.strftime(ISO), (s + timedelta(days=WINDOW_DAYS)).strftime(ISO)) for s in starts]


def gather(repo, stats, windows):
    """Candidate comments for one repo, grouped by kind."""
    pool = {k: [] for k in TARGETS}
    seen = set()
    streams = [("pr_review", f"repos/{repo}/pulls/comments"), (None, f"repos/{repo}/issues/comments")]
    for lo, hi in windows:
        for fixed_kind, endpoint in streams:
            for page in range(1, PAGES_PER_WINDOW + 1):
                params = {"sort": "updated", "direction": "asc", "since": lo, "per_page": 100, "page": page}
                items = gh_get(endpoint, params)
                for it in items:
                    kind = fixed_kind or ("pr_comment" if "/pull/" in it["html_url"] else "issue_comment")
                    body = it["body"] or ""
                    if is_bot(it.get("user")):
                        stats["bot"] += 1
                    elif not lo <= it["created_at"] < hi:
                        stats["created_outside_window"] += 1
                    elif len(body) > MAX_CHARS:
                        stats["too_long"] += 1
                    elif AI_LABEL.search(body):
                        stats["self_labelled_ai"] += 1
                    else:
                        text = prepare(body)
                        if text is None:
                            stats["empty_or_commands_only"] += 1
                        elif text.lower() in seen:
                            stats["duplicate"] += 1
                        else:
                            seen.add(text.lower())
                            pool[kind].append({
                                "text": text, "repo": repo, "kind": kind, "created_at": it["created_at"],
                                "_author": it["user"]["login"].lower(),
                                "_thread": it.get("pull_request_url") or it["issue_url"],
                            })
                if len(items) < 100 or items[-1]["updated_at"] >= hi:
                    break
    return pool


def sample(pool, rng, stats):
    per_author, per_thread, out = Counter(), Counter(), []
    for kind, target in TARGETS.items():
        cands = pool[kind][:]
        rng.shuffle(cands)
        taken = 0
        for c in cands:
            if taken == target:
                break
            if per_author[c["_author"]] >= MAX_PER_AUTHOR or per_thread[c["_thread"]] >= MAX_PER_THREAD:
                stats["capped_while_sampling"] += 1
                continue
            per_author[c["_author"]] += 1
            per_thread[c["_thread"]] += 1
            out.append({k: v for k, v in c.items() if not k.startswith("_")})
            taken += 1
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--control", action="store_true", help="collect the pre-LLM control corpus instead")
    ap.add_argument("--out", help="default: data/human_github.jsonl, or data/human_github_pre2023.jsonl with --control")
    ap.add_argument("--seed", default="2026")
    ap.add_argument("--until", help="YYYY-MM-DD; the recent period ends four days before this (default: today)")
    ap.add_argument("--repos", nargs="*")
    args = ap.parse_args()

    if args.control:
        start, end = (datetime.fromisoformat(d).replace(tzinfo=timezone.utc) for d in CONTROL_PERIOD)
    else:
        until = datetime.fromisoformat(args.until).replace(tzinfo=timezone.utc) if args.until else datetime.now(timezone.utc)
        start, end = datetime.fromisoformat(RECENT_FROM).replace(tzinfo=timezone.utc), until - timedelta(days=4)
    repos = args.repos or (CONTROL_REPOS if args.control else REPOS)
    out = Path(args.out or DATA / ("human_github_pre2023.jsonl" if args.control else "human_github.jsonl"))

    collected, per_repo, drops = [], {}, Counter()
    for repo in repos:
        stats = Counter()
        try:
            pool = gather(repo, stats, windows_for(repo, args.seed, start, end))
        except LookupError as e:
            print(f"skip {repo}: not found ({e})", file=sys.stderr)
            continue
        rows = sample(pool, random.Random(f"{args.seed}:{repo}"), stats)
        collected += rows
        per_repo[repo] = dict(Counter(r["kind"] for r in rows), total=len(rows))
        drops.update(stats)
        print(f"{repo:28} {len(rows):3}  {dict(Counter(r['kind'] for r in rows))}", flush=True)

    collected.sort(key=lambda r: (r["repo"], r["kind"], r["created_at"]))
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for r in collected:
            f.write(json.dumps(r, ensure_ascii=False).replace("\U00002014", "\\u2014") + "\n")
    meta = {
        "collected_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "total": len(collected), "repos": len(per_repo), "per_repo": per_repo,
        "by_kind": dict(Counter(r["kind"] for r in collected)),
        "period": [start.strftime(ISO), end.strftime(ISO)],
        "params": {"targets_per_repo": TARGETS, "windows_per_repo": WINDOWS_PER_REPO,
                   "window_days": WINDOW_DAYS, "pages_per_window": PAGES_PER_WINDOW,
                   "max_per_author_per_repo": MAX_PER_AUTHOR, "max_per_thread": MAX_PER_THREAD,
                   "max_chars": MAX_CHARS, "seed": args.seed},
        "dropped_comments_by_reason": dict(drops), "api_calls": api_calls,
    }
    out.with_suffix(".meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"\nwrote {len(collected)} comments from {len(per_repo)} repos to {out}")


if __name__ == "__main__":
    main()
