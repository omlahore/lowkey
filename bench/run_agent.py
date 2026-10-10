#!/usr/bin/env python3
"""Run bench/prompts.jsonl through Claude Code headless, with and without lowkey.

    python3 bench/run_agent.py --arm baseline --model haiku
    python3 bench/run_agent.py --arm lowkey --model haiku
    python3 bench/run_agent.py --arm lowkey --level lite --model haiku

Each run uses an empty working directory, no user or project settings, and a
throwaway HOME, so your own CLAUDE.md, plugins and hooks can't leak into
either arm. The lowkey arm loads this repo with --plugin-dir, so the real
hooks run exactly as they would after installing the plugin.
Writes bench/results/agent_<arm>[_<level>]_<model>.jsonl.
"""
import argparse
import concurrent.futures as cf
import json
import os
import pathlib
import subprocess
import tempfile

BENCH = pathlib.Path(__file__).resolve().parent
ROOT = BENCH.parent


def run_one(prompt, args, home):
    cmd = [
        "claude", "-p", prompt["prompt"],
        "--model", args.model,
        "--no-session-persistence",
        "--setting-sources", "",
        "--output-format", "json",
    ]
    if args.arm == "lowkey":
        cmd += ["--plugin-dir", str(ROOT)]
    env = dict(os.environ)
    if args.isolate_home:
        env["HOME"] = home
    if args.level:
        env["LOWKEY_DEFAULT_MODE"] = args.level
    with tempfile.TemporaryDirectory() as cwd:
        p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=300)
    if p.returncode != 0:
        return {"id": prompt["id"], "error": (p.stderr or p.stdout).strip()[:500]}
    out = json.loads(p.stdout)
    text = out.get("result", "").strip()
    return {
        "id": prompt["id"],
        "category": prompt["category"],
        "channel": prompt["channel"],
        "text": text,
        # the reply kept every fact the prompt says it must mention
        "facts_ok": all(m.lower() in text.lower() for m in prompt.get("must_mention", [])),
        "cost_usd": out.get("total_cost_usd"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=["baseline", "lowkey"], required=True)
    ap.add_argument("--level", choices=["auto", "lite", "full", "brainrot"])
    ap.add_argument("--model", default="haiku")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--no-isolate-home", dest="isolate_home", action="store_false")
    args = ap.parse_args()

    prompts = [json.loads(l) for l in (BENCH / "prompts.jsonl").read_text().splitlines() if l.strip()]
    if args.limit:
        prompts = prompts[: args.limit]
    name = "_".join(x for x in ["agent", args.arm, args.level, args.model] if x)
    out_path = BENCH / "results" / f"{name}.jsonl"

    with tempfile.TemporaryDirectory() as home:
        # macOS keeps Claude Code's login in the keychain, so a fresh HOME still
        # authenticates while hiding ~/.claude (CLAUDE.md, plugins, hooks).
        with cf.ThreadPoolExecutor(args.jobs) as pool:
            rows = list(pool.map(lambda pr: run_one(pr, args, home), prompts))

    errors = [r for r in rows if "error" in r]
    with out_path.open("w") as f:
        for r in rows:
            if "error" not in r:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    ok = [r for r in rows if "error" not in r]
    kept = sum(r["facts_ok"] for r in ok)
    print(f"{len(ok)} replies -> {out_path}")
    print(f"kept every required fact in {kept}/{len(ok)} replies")
    for e in errors[:5]:
        print("error", e["id"], e["error"])


if __name__ == "__main__":
    main()
