#!/usr/bin/env python3
"""Collect Hacker News comments for the second baseline. Standard library only.

    python3 collect_hn.py [--out data/human_hn.jsonl] [--seed 2026] [--until 2026-10-11]

Uses the public HN Search API (https://hn.algolia.com/api), read-only. It samples short time windows
at random between 2025-01-01 and the day before --until (default: today), so the corpus is spread
over the whole period rather than being the newest few hours. Usernames, story titles and ids are never written. HTML is
converted to plain text; code blocks become fenced blocks and links become their full URL.
"""
import argparse
import json
import random
import re
import sys
import time
import urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlencode

API = "https://hn.algolia.com/api/v1/search_by_date"
USER_AGENT = "lowkey-bench/1.0 (style research; github.com/omlahore/lowkey)"
WINDOWS = 18
WINDOW_MINUTES = 20
PER_WINDOW = 28
MAX_PER_AUTHOR = 2
MAX_PER_STORY = 3
MAX_CHARS = 4000
START = datetime(2025, 1, 1, tzinfo=timezone.utc)


class Plain(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.in_link = [], False

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            self.parts.append("\n\n")
        elif tag == "br":
            self.parts.append("\n")
        elif tag == "pre":
            self.parts.append("\n```\n")
        elif tag == "a" and dict(attrs).get("href"):
            self.parts.append(dict(attrs)["href"])
            self.in_link = True

    def handle_endtag(self, tag):
        if tag == "pre":
            self.parts.append("\n```\n")
        elif tag == "a":
            self.in_link = False

    def handle_data(self, data):
        if not self.in_link:
            self.parts.append(data)


def to_text(html):
    p = Plain()
    p.feed(html)
    p.close()
    return re.sub(r"\n{3,}", "\n\n", "".join(p.parts)).strip()


def fetch(t0, t1):
    q = urlencode({"tags": "comment", "hitsPerPage": 1000,
                   "numericFilters": f"created_at_i>={t0},created_at_i<{t1}"})
    req = urllib.request.Request(f"{API}?{q}", headers={"User-Agent": USER_AGENT})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp)["hits"]
        except OSError:
            time.sleep(3 * (attempt + 1))
    raise RuntimeError("HN search API kept failing")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(Path(__file__).parent / "data" / "human_hn.jsonl"))
    ap.add_argument("--seed", default="2026")
    ap.add_argument("--until", help="YYYY-MM-DD; windows end the day before this (default: today)")
    args = ap.parse_args()

    until = (datetime.fromisoformat(args.until).replace(tzinfo=timezone.utc) if args.until
             else datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0))
    rng = random.Random(args.seed)
    span = int((until - timedelta(days=1) - START).total_seconds()) - WINDOW_MINUTES * 60
    starts = sorted(int(START.timestamp()) + rng.randrange(span) for _ in range(WINDOWS))
    rows, seen, per_author, per_story, drops, api_calls = [], set(), Counter(), Counter(), Counter(), 0
    for t0 in starts:
        hits = fetch(t0, t0 + WINDOW_MINUTES * 60)
        api_calls += 1
        rng.shuffle(hits)
        taken = 0
        for h in hits:
            if taken == PER_WINDOW:
                break
            text = to_text(h["comment_text"]) if h.get("comment_text") else ""
            key = text.lower()
            if not text or len(text) > MAX_CHARS or key in seen:
                drops["empty_long_or_duplicate"] += 1
            elif per_author[h["author"]] >= MAX_PER_AUTHOR or per_story[h["story_id"]] >= MAX_PER_STORY:
                drops["capped_while_sampling"] += 1
            else:
                seen.add(key)
                per_author[h["author"]] += 1
                per_story[h["story_id"]] += 1
                rows.append({"text": text, "source": "hn", "created_at": h["created_at"]})
                taken += 1
        print(datetime.fromtimestamp(t0, timezone.utc).strftime("%Y-%m-%d %H:%M"), taken, flush=True)
        time.sleep(0.5)

    rows.sort(key=lambda r: r["created_at"])
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False).replace("\U00002014", "\\u2014") + "\n")
    meta = {"collected_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), "total": len(rows),
            "params": {"windows": WINDOWS, "window_minutes": WINDOW_MINUTES, "per_window": PER_WINDOW,
                       "max_per_author": MAX_PER_AUTHOR, "max_per_story": MAX_PER_STORY,
                       "max_chars": MAX_CHARS, "start": START.isoformat(), "until": until.date().isoformat(),
                       "seed": args.seed},
            "dropped_comments_by_reason": dict(drops), "api_calls": api_calls}
    out.with_suffix(".meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(rows)} comments to {out}")


if __name__ == "__main__":
    sys.exit(main())
