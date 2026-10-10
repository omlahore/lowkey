#!/usr/bin/env python3
"""Style statistics for chat-style messages. Standard library only.

    python3 style_stats.py FILE [FILE ...] [--min-words N] [--json OUT] [--md OUT]
    python3 style_stats.py --selftest

FILE is a JSON array or a JSONL file whose items are strings or objects with a
"text" field. Each FILE is reported as its own corpus. Fenced code, inline code,
URLs, quoted lines (starting with ">") and markdown image/link syntax are removed
before anything is measured. Link text is kept, images are dropped.

With --min-words N every corpus is reported twice: once in full and once
restricted to messages of at least N words (after cleaning). Use it to compare
against agent output, which is rarely shorter than a sentence or two.
"""
import argparse
import html
import json
import re
import statistics
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Word lists. Extend freely. Matching is case-insensitive; curly apostrophes
# are normalised to straight ones before matching.
# ---------------------------------------------------------------------------

ASSISTANT_TELLS = [
    "great question", "good question", "excellent question",
    "i hope this helps", "hope this helps", "let me know if",
    "happy to help", "happy to assist", "i'd be happy to", "i would be happy to",
    "certainly", "absolutely", "you're absolutely right",
    "it's worth noting", "it is worth noting", "worth noting that",
    "in summary", "in conclusion", "to summarize",
    "feel free to", "don't hesitate to",
    "delve", "delves", "delving", "delved",
    "here's a", "here is a", "comprehensive",
    "i apologize", "apologies for the confusion", "as an ai",
    "thank you for your", "i appreciate your",
]

# Regex fragments, matched as whole words (not inside paths, locales or domains).
CASUAL_MARKERS = [
    r"lol+", r"lmf?ao+", r"(?:ha){2,}h?", r"he(?:he)+",
    "tbh", "ngl", "imo", "imho", "idk", "kinda", "lowkey", "fr", "nvm", "tho",
    # "rn" also means React Native ("the rn app"), so skip it after a determiner or before a noun
    r"(?<!\bthe\s)(?<!\ba\s)(?<!\ban\s)(?<!\bour\s)(?<!\bmy\s)(?<!\bthis\s)(?<!\bthat\s)(?<!\bin\s)"
    r"(?<!\bof\s)(?<!\bfor\s)(?<!\bwith\s)(?<!\bon\s)(?<!\bto\s)rn"
    r"(?!\s+(?:app|apps|bridge|core|internal|internals|side|project|build|builds|code|docs|version|"
    r"package|packages|module|modules|library|renderer)\b)",
]

# Sentence-initial past-tense verbs that leave out the subject ("Fixed the bug.").
SUBJECTLESS_VERBS = set("""
added adjusted aligned applied backported benchmarked bumped built bundled cached
changed checked cleaned cleared closed committed compared configured confirmed
converted copied created debugged deleted deployed disabled dropped enabled ensured
exported extended extracted fixed flipped formatted found generated handled hardened
implemented imported improved inlined installed introduced investigated kept landed
limited linted looked made marked merged migrated moved normalized noticed opened
optimized patched pinned profiled pulled pushed ran rebased rechecked reduced
refactored regenerated removed renamed reordered replaced reported reproduced
resolved restarted restored retested reran reverted reviewed rewrote rolled saw
scanned sent shipped simplified skipped split squashed started stopped switched
synced tested took tightened tried tweaked unpinned updated upgraded used verified
wrapped wrote
""".split())

ABBREVIATIONS = {"e.g", "i.e", "etc", "vs", "cf", "approx", "eg", "ie", "mr", "mrs",
                 "ms", "dr", "st", "fig", "incl", "esp", "al"}

# ---------------------------------------------------------------------------
# Cleaning
# ---------------------------------------------------------------------------

PH = "\U0000E000"  # stands in for stripped code, URLs and images

FENCE = re.compile(r"^[ \t]*(`{3,}|~{3,})[^\n]*\n.*?(?:^[ \t]*\1[`~]*[ \t]*$|\Z)", re.S | re.M)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
QUOTE_LINE = re.compile(r"^[ \t]{0,3}>.*$", re.M)
TABLE_ROW = re.compile(r"^[ \t]*\|.*\|[ \t]*$", re.M)
EMAIL_QUOTE_HEADER = re.compile(r"^On .{3,200} wrote:[ \t]*$", re.M)
IMAGE = re.compile(r"!\[[^\]\n]*\]\([^)\n]*\)|!\[[^\]\n]*\]\[[^\]\n]*\]")
LINK = re.compile(r"\[([^\]\n]+)\]\((?:[^()\s]|\([^()\s]*\))*(?:\s+\"[^\"]*\")?\)")
REF_LINK = re.compile(r"\[([^\]\n]+)\]\[[^\]\n]*\]")
INLINE_CODE = re.compile(r"(`+)(?!`)(.+?)(?<!`)\1(?!`)")
URL = re.compile(r"<?\b(?:https?://|www\.)[^\s<>]*[^\s<>.,;:!?'\")\]}]>?")
BR = re.compile(r"<br\s*/?>", re.I)
HTML_TAG = re.compile(
    r"</?(?:a|abbr|b|blockquote|br|code|details|div|em|h[1-6]|hr|i|img|kbd|li|ol|p|"
    r"picture|pre|s|source|span|strong|sub|summary|sup|table|tbody|td|th|thead|tr|u|ul)"
    r"(?:\s[^>\n]*)?/?>", re.I)


def clean_text(text):
    t = html.unescape(text).replace("\r\n", "\n").replace("\r", "\n")
    t = FENCE.sub("\n", t)
    t = HTML_COMMENT.sub("", t)
    t = QUOTE_LINE.sub("", t)
    t = TABLE_ROW.sub("", t)
    t = EMAIL_QUOTE_HEADER.sub("", t)
    t = IMAGE.sub(PH, t)
    t = LINK.sub(r"\1", t)
    t = REF_LINK.sub(r"\1", t)
    t = INLINE_CODE.sub(PH, t)
    t = URL.sub(PH, t)
    t = BR.sub("\n", t)
    return HTML_TAG.sub("", t)


# ---------------------------------------------------------------------------
# Emoji (Unicode ranges, no external libraries)
# ---------------------------------------------------------------------------

_ALWAYS_EMOJI = (
    "\U0001F300-\U0001F64F\U0001F680-\U0001F6FF\U0001F7E0-\U0001F7EB\U0001F7F0"
    "\U0001F900-\U0001F9FF\U0001FA70-\U0001FAFF"
    "\U0001F004\U0001F0CF\U0001F18E\U0001F191-\U0001F19A\U0001F201\U0001F21A\U0001F22F"
    "\U0001F232-\U0001F236\U0001F238-\U0001F23A\U0001F250-\U0001F251"
    "\U0000231A\U0000231B\U000023E9-\U000023EC\U000023F0\U000023F3\U000025FD\U000025FE\U00002614\U00002615\U00002648-\U00002653\U0000267F"
    "\U00002693\U000026A1\U000026AA\U000026AB\U000026BD\U000026BE\U000026C4\U000026C5\U000026CE\U000026D4\U000026EA\U000026F2\U000026F3"
    "\U000026F5\U000026FA\U000026FD\U00002705\U0000270A\U0000270B\U00002728\U0000274C\U0000274E\U00002753-\U00002755\U00002757"
    "\U00002795-\U00002797\U000027B0\U000027BF\U00002B1B\U00002B1C\U00002B50\U00002B55"
)
# Text-default symbols: emoji only when followed by the emoji variation selector.
_NEEDS_VS16 = ("\U000000A9\U000000AE\U0000203C\U00002049\U00002122\U00002139\U00002190-\U000021FF\U00002300-\U000023FF"
               "\U000025A0-\U000025FF\U00002600-\U000027BF\U00002900-\U0000297F\U00002B00-\U00002BFF\U00003030\U0000303D\U00003297\U00003299")
# Common text-default symbols that render as emoji on GitHub even without the selector.
_USUALLY_EMOJI = "\U00002764\U000026A0\U00002714\U00002716\U00002611"
_MODIFIER = "[\U0001F3FB-\U0001F3FF]"
_UNIT = (f"(?:[{_ALWAYS_EMOJI}]|[{_NEEDS_VS16}]\U0000FE0F|[{_USUALLY_EMOJI}]){_MODIFIER}?\U0000FE0F?")
EMOJI = re.compile(
    "[\U0001F1E6-\U0001F1FF]{2}"          # flags
    r"|[0-9#*]\U0000FE0F?\U000020E3"              # keycaps
    f"|{_UNIT}(?:\U0000200D{_UNIT})*"         # single emoji and ZWJ sequences
)
SHORTCODE = re.compile(r"(?<![\w:]):[a-z0-9_+\-]{2,}:(?![\w:])")  # :tada: :+1:


def emoji_count(text):
    return len(EMOJI.findall(text)) + len(SHORTCODE.findall(text))


# ---------------------------------------------------------------------------
# Matchers
# ---------------------------------------------------------------------------

TELLS_RE = re.compile(r"\b(" + "|".join(
    re.escape(p) for p in sorted(ASSISTANT_TELLS, key=len, reverse=True)) + r")\b")
CASUAL_RE = re.compile(r"(?<![\w/.\-])(?:" + "|".join(CASUAL_MARKERS) + r")(?![\w/\-]|\.\w)")
LEAD = re.compile(r"^\s*(?:#{1,6}\s+|(?:[-*+]|\d{1,3}[.)])\s+(?:\[[ xX]\]\s+)?)")
HEADER_LINE = re.compile(r"#{1,6}\s+\S")
LIST_LINE = re.compile(r"(?:[-*+]|\d{1,3}[.)])\s+\S")
BOLD = re.compile(r"\*\*[^\s*][^*\n]*?\*\*|__[^\s_][^_\n]*?__")
BOUNDARY = re.compile(r"([.!?]+)[\"')\]*_]*\s+")
SKIP_LEAD = re.compile(
    "^(?:[\\s\"'\U0000201C\U0000201D\U00002018\U00002019(\\[{<*_~]|@[\\w\\-/]+[,:]?(?=\\s|$)|" + EMOJI.pattern + ")+")
FIRST_TOKEN = re.compile(r"\S+")
PLAIN_WORD = re.compile(r"[^\W\d_]+(?:['\U00002019\-][^\W\d_]+)*")
TRAILING = re.compile(rf"(?:\s|{EMOJI.pattern}|[)\]}}\"'\U0000201D\U00002019*_~])+$")


def has_content(p):
    return any(c.isalnum() for c in p) or emoji_count(p) > 0


def count_words(p):
    return sum(1 for tok in p.split() if any(c.isalnum() for c in tok))


def ends_with_period(p):
    core = TRAILING.sub("", p)
    return core.endswith(".") and not core.endswith("..")


def first_word(head):
    """First token of a sentence if it is a plain word (not a version, path, command or number)."""
    m = FIRST_TOKEN.match(SKIP_LEAD.sub("", head))
    tok = m.group(0).rstrip(".,;:!?)]}\"'\U0000201D\U00002019*_~") if m else ""
    return tok if PLAIN_WORD.fullmatch(tok) else None


def sentence_heads(line):
    heads = [line]
    for m in BOUNDARY.finditer(line):
        punct = m.group(1)
        if punct.endswith(".."):
            continue
        if punct == ".":
            tok = re.search(r"(\S+)$", line[:m.start(1)])
            word = tok.group(1).lower().strip("([\"'") if tok else ""
            if word in ABBREVIATIONS or len(re.sub(r"\W", "", word)) == 1:
                continue
        heads.append(line[m.end():])
    return heads


# ---------------------------------------------------------------------------
# Per-message analysis and corpus summary
# ---------------------------------------------------------------------------

def analyze(raw):
    """Raw counts for one message, or None if nothing is left after cleaning."""
    clean = clean_text(raw)
    lines = []
    for ln in clean.split("\n"):
        s = ln.strip()
        p = LEAD.sub("", s).strip()
        if has_content(p):
            lines.append((s, p))
    if not lines:
        return None
    line_words = [count_words(p) for _, p in lines]
    cap = low = sent = subj = 0
    for _, p in lines:
        for head in sentence_heads(p):
            w = first_word(head)
            if w is None:
                continue
            sent += 1
            cap += w[0].isupper()
            low += w[0].islower()
            subj += w.lower() in SUBJECTLESS_VERBS
    norm = clean.replace("\U00002019", "'").lower()
    return {
        "words": sum(line_words),
        "line_words": line_words,
        "period_lines": sum(ends_with_period(p) for _, p in lines),
        "cap": cap, "low": low, "sent": sent, "subj": subj,
        "em": clean.count("\U00002014"), "en": clean.count("\U00002013"),
        "emoji": emoji_count(clean),
        "tells": sorted(set(TELLS_RE.findall(norm))),
        "md_header": any(HEADER_LINE.match(s) for s, _ in lines),
        "md_bold": bool(BOLD.search(clean)),
        "md_list": sum(bool(LIST_LINE.match(s)) for s, _ in lines) >= 2,
        "casual": bool(CASUAL_RE.search(norm)),
    }


def _mean(xs):
    return statistics.fmean(xs) if xs else None


def _median(xs):
    return statistics.median(xs) if xs else None


def _share(flags):
    return sum(flags) / len(flags) if flags else None


def _ratio(num, den):
    return num / den if den else None


def _m(kind, overall=None, per=None):
    per = per or []
    return {"kind": kind, "overall": overall, "mean": _mean(per), "median": _median(per)}


def summarize(recs):
    n = len(recs)
    words = sum(r["words"] for r in recs)
    line_words = [w for r in recs for w in r["line_words"]]
    cap_n = sum(r["cap"] for r in recs)
    low_n = sum(r["low"] for r in recs)
    sent_n = sum(r["sent"] for r in recs)
    lines_n = len(line_words)
    per_cap = [r["cap"] / (r["cap"] + r["low"]) for r in recs if r["cap"] + r["low"]]
    per_subj = [r["subj"] / r["sent"] for r in recs if r["sent"]]
    per_period = [r["period_lines"] / len(r["line_words"]) for r in recs]
    with_sentences = [r for r in recs if r["cap"] + r["low"]]
    flag = lambda key: _m("pct", _share([bool(r[key]) for r in recs]))
    md_any = [r["md_header"] or r["md_bold"] or r["md_list"] for r in recs]
    tell_counts = {}
    for r in recs:
        for t in r["tells"]:
            tell_counts[t] = tell_counts.get(t, 0) + 1
    metrics = {
        "cap_start": _m("pct", _ratio(cap_n, cap_n + low_n), per_cap),
        "lowercase_msgs": _m("pct", _share([r["cap"] == 0 for r in with_sentences])),
        "period_end_lines": _m("pct", _ratio(sum(r["period_lines"] for r in recs), lines_n), per_period),
        "no_period_msgs": _m("pct", _share([r["period_lines"] == 0 for r in recs])),
        "em_dash_per_1k_words": _m("rate", _ratio(1000 * sum(r["em"] for r in recs), words)),
        "en_dash_per_1k_words": _m("rate", _ratio(1000 * sum(r["en"] for r in recs), words)),
        "dash_msgs": _m("pct", _share([bool(r["em"] or r["en"]) for r in recs])),
        "emoji_per_msg": _m("num", None, [r["emoji"] for r in recs]),
        "emoji_msgs": _m("pct", _share([r["emoji"] > 0 for r in recs])),
        "words_per_line": _m("num", None, line_words),
        "lines_per_msg": _m("num", None, [len(r["line_words"]) for r in recs]),
        "words_per_msg": _m("num", None, [r["words"] for r in recs]),
        "assistant_tells": _m("pct", _share([bool(r["tells"]) for r in recs])),
        "md_header": flag("md_header"),
        "md_bold": flag("md_bold"),
        "md_list": flag("md_list"),
        "md_any": _m("pct", _share(md_any)),
        "casual_markers": flag("casual"),
        "subjectless_start": _m("pct", _ratio(sum(r["subj"] for r in recs), sent_n), per_subj),
    }
    return {"messages": n, "words": words, "sentences": sent_n, "lines": lines_n,
            "metrics": metrics,
            "assistant_tell_messages": dict(sorted(tell_counts.items(), key=lambda kv: -kv[1]))}


LABELS = {
    "cap_start": "sentences starting with a capital letter",
    "lowercase_msgs": "messages with no capitalised sentence start",
    "period_end_lines": "non-empty lines ending with a full stop",
    "no_period_msgs": "messages with no line ending in a full stop",
    "em_dash_per_1k_words": "em dashes per 1,000 words",
    "en_dash_per_1k_words": "en dashes per 1,000 words",
    "dash_msgs": "messages with an em or en dash",
    "emoji_per_msg": "emoji per message",
    "emoji_msgs": "messages with at least one emoji",
    "words_per_line": "words per line",
    "lines_per_msg": "lines per message",
    "words_per_msg": "words per message",
    "assistant_tells": "messages with an assistant-tell phrase",
    "md_header": "messages with a markdown header",
    "md_bold": "messages with bold text",
    "md_list": "messages with a list (2+ items)",
    "md_any": "messages with header, bold or list",
    "casual_markers": "messages with a casual marker",
    "subjectless_start": "sentences starting with a subjectless verb",
}


# ---------------------------------------------------------------------------
# Input and output
# ---------------------------------------------------------------------------

def load_messages(path):
    raw = Path(path).read_text(encoding="utf-8")
    if raw.lstrip().startswith("["):
        items = json.loads(raw)
    else:
        items = [json.loads(ln) for ln in raw.splitlines() if ln.strip()]
    out = []
    for it in items:
        if isinstance(it, str):
            out.append(it)
        elif isinstance(it, dict) and isinstance(it.get("text"), str):
            out.append(it["text"])
        else:
            raise SystemExit(f"{path}: item is neither a string nor an object with a text field: {str(it)[:80]}")
    return out


def build_corpora(paths, min_words):
    corpora = {}
    for path in paths:
        name = Path(path).stem
        while name in corpora:
            name += "_"
        msgs = load_messages(path)
        recs = [r for r in map(analyze, msgs) if r]
        info = {"source": str(path), "dropped_empty": len(msgs) - len(recs)}
        corpora[name] = dict(summarize(recs), **info)
        if min_words:
            keep = [r for r in recs if r["words"] >= min_words]
            corpora[f"{name} (>={min_words} words)"] = dict(summarize(keep), min_words=min_words, **info)
    return corpora


def fmt(kind, x):
    if x is None:
        return "-"
    return f"{x * 100:.1f}%" if kind == "pct" else f"{x:.2f}"


def corpus_rows(c):
    return [(LABELS[k], fmt(m["kind"], m["overall"]), fmt(m["kind"], m["mean"]),
             fmt(m["kind"], m["median"])) for k, m in c["metrics"].items()]


def headline(m):
    if m["overall"] is not None:
        return fmt(m["kind"], m["overall"])
    if m["mean"] is None:
        return "-"
    return f"{m['mean']:.2f} (med {m['median']:g})"


def corpus_title(name, c):
    return (f"{name}: {c['messages']} messages, {c['words']} words, "
            f"{c['sentences']} sentences, {c['lines']} lines")


def text_report(corpora):
    out = []
    for name, c in corpora.items():
        rows = corpus_rows(c)
        w = max(len(r[0]) for r in rows)
        out.append(f"\n== {corpus_title(name, c)}")
        out.append(f"{'metric':<{w}}  {'overall':>9}  {'mean':>9}  {'median':>9}")
        out += [f"{a:<{w}}  {b:>9}  {c_:>9}  {d:>9}" for a, b, c_, d in rows]
        if c["assistant_tell_messages"]:
            top = ", ".join(f"{k} ({v})" for k, v in list(c["assistant_tell_messages"].items())[:6])
            out.append(f"assistant tells by message count: {top}")
    if len(corpora) > 1:
        out.append("\n== comparison (value, or mean with median for per-message counts)")
        names = list(corpora)
        w = max(len(v) for v in LABELS.values())
        out.append(f"{'metric':<{w}}  " + "  ".join(f"{n[:26]:>26}" for n in names))
        for k, label in LABELS.items():
            out.append(f"{label:<{w}}  " + "  ".join(f"{headline(corpora[n]['metrics'][k]):>26}" for n in names))
    return "\n".join(out)


def md_report(corpora, command=None):
    out = ["# Style statistics", ""]
    if command:
        out += [f"Generated by `{command}`.", ""]
    if len(corpora) > 1:
        names = list(corpora)
        out += ["## Comparison", "", "Each cell is a pooled share or rate, or `mean (med median)` for per-message counts.", "",
                "| metric | " + " | ".join(names) + " |", "|---|" + "---:|" * len(names)]
        out.append("| messages | " + " | ".join(str(corpora[n]["messages"]) for n in names) + " |")
        out.append("| words | " + " | ".join(str(corpora[n]["words"]) for n in names) + " |")
        for k, label in LABELS.items():
            out.append(f"| {label} | " + " | ".join(headline(corpora[n]["metrics"][k]) for n in names) + " |")
        out.append("")
    for name, c in corpora.items():
        subset = f" Only messages of at least {c['min_words']} words." if c.get("min_words") else ""
        out += [f"## {name}", "", f"Source: `{c['source']}`. {c['messages']} messages, {c['words']} words, "
                f"{c['sentences']} sentences, {c['lines']} lines.{subset} "
                f"Inputs empty after cleaning: {c['dropped_empty']}.", "",
                "| metric | overall | mean | median |", "|---|---:|---:|---:|"]
        out += [f"| {a} | {b} | {c_} | {d} |" for a, b, c_, d in corpus_rows(c)]
        if c["assistant_tell_messages"]:
            top = ", ".join(f"{k} ({v})" for k, v in list(c["assistant_tell_messages"].items())[:8])
            out += ["", f"Assistant-tell phrases by number of messages containing them: {top}."]
        out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def selftest():
    c = clean_text("Fixed in https://x.com/a/b.\n> quoted\n```py\nprint(1)\n```\n"
                   "use `foo()` ![i](http://i.png) see [docs](http://d.com) <!-- hidden -->")
    assert all(s not in c for s in ("quoted", "print", "http", "foo", "hidden")), c
    assert "docs" in c and "Fixed in" in c and c.count(PH) == 3, c
    assert "x" not in clean_text("~~~\nx\n"), "unclosed fence must be stripped"

    r = analyze("Fixed it. then ran tests\nlooks good")
    assert (r["cap"], r["low"], r["sent"], r["subj"]) == (1, 2, 3, 1), r
    r = analyze("@bob Thanks for the fix, e.g. the null check. Well... maybe not! really?")
    assert (r["cap"], r["low"]) == (2, 1), r
    r = analyze("`foo` is broken\nhttps://x.com/y is also broken")
    assert (r["cap"], r["low"], r["sent"]) == (0, 0, 0), r
    r = analyze("v18 works\ncmd+k opens it\nsrc/a.ts is wrong\n3 tests failed\n| a | b |\n&nbsp;&nbsp;")
    assert (r["cap"], r["low"], r["sent"]) == (0, 0, 0) and len(r["line_words"]) == 4, r
    r = analyze("Don't. can't-stop! \"Quoted start\" ok")
    assert (r["cap"], r["low"]) == (2, 1), r
    r = analyze("Thanks! \U0001F642 will do\n\U0001F680 shipped it")
    assert (r["cap"], r["low"], r["subj"]) == (1, 2, 1), r

    r = analyze("done.\nlooks fine\nok. \U0001F642\nwait...")
    assert r["period_lines"] == 2 and len(r["line_words"]) == 4, r
    assert analyze("- one\n- two\n3. three")["line_words"] == [1, 1, 1]

    r = analyze("a \U00002014 b \U00002013 c")
    assert (r["em"], r["en"], r["words"]) == (1, 1, 3), r

    sample = ("ship \U0001F680 \U0001F44D\U0001F3FD \U0001F1EE\U0001F1F3 "
              "\U0001F468\U0000200D\U0001F469\U0000200D\U0001F467 \U00002764\U0000FE0F \U00002705 1\U0000FE0F\U000020E3 :tada:")
    assert analyze(sample)["emoji"] == 8, analyze(sample)
    assert analyze("plain \U00002713 \U00002192 12:30:45 a::b ok")["emoji"] == 0

    assert analyze("Great question! I hope this helps.")["tells"] == ["great question", "i hope this helps"]
    assert analyze("lgtm, ship it")["tells"] == []
    assert analyze("It\U00002019s worth noting that x")["tells"] == ["it's worth noting"]

    r = analyze("## Title\n- a\n- b\nsome **bold** text")
    assert r["md_header"] and r["md_bold"] and r["md_list"], r
    r = analyze("#123 is fixed\n- single item\n2 ** 3")
    assert not (r["md_header"] or r["md_bold"] or r["md_list"]), r

    assert analyze("lol tbh idk")["casual"] and analyze("ngl that's neat")["casual"]
    assert analyze("so haha.")["casual"] and analyze("hahaha ok")["casual"]
    assert not analyze("the fr-FR locale, see fr/index.md and frankly fine")["casual"]
    assert analyze("can't repro rn")["casual"] and analyze("busy rn, will look later")["casual"]
    assert not analyze("the rn app is broken")["casual"] and not analyze("rn bridge crashes")["casual"]

    r = analyze("Fixed the bug. Ran the tests. I added a test.")
    assert (r["sent"], r["subj"]) == (3, 2), r

    assert analyze("```\ncode only\n```") is None and analyze("   ") is None

    s = summarize([analyze("Fixed it.\nlooks good \U0001F642"), analyze("Ran the suite. All green.")])
    m = s["metrics"]
    assert s["messages"] == 2 and m["emoji_msgs"]["overall"] == 0.5
    assert m["cap_start"]["overall"] == 0.75 and m["period_end_lines"]["overall"] == 2 / 3
    assert m["lines_per_msg"]["mean"] == 1.5 and m["subjectless_start"]["overall"] == 0.5

    m = summarize([analyze("Fixed it.\nlooks good"), analyze("Ran the suite. All green."),
                   analyze("nothing capital here. at all"), analyze("12345")])["metrics"]
    assert m["lowercase_msgs"]["overall"] == 1 / 3 and m["no_period_msgs"]["overall"] == 0.5, m

    with tempfile.TemporaryDirectory() as d:
        a, b = Path(d, "a.json"), Path(d, "b.jsonl")
        a.write_text(json.dumps(["one", {"text": "two"}]))
        b.write_text('"three"\n{"text": "four", "repo": "x"}\n')
        assert load_messages(a) == ["one", "two"] and load_messages(b) == ["three", "four"]
        corpora = build_corpora([a, b], 2)
        assert list(corpora) == ["a", "a (>=2 words)", "b", "b (>=2 words)"]
        assert "== comparison" in text_report(corpora) and "## b (>=2 words)" in md_report(corpora)
        json.dumps(corpora)
    print("selftest ok")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", help="JSON or JSONL file(s) of messages")
    ap.add_argument("--min-words", type=int, default=0, help="also report each corpus restricted to messages of at least N words")
    ap.add_argument("--json", metavar="OUT", help="write results as JSON")
    ap.add_argument("--md", metavar="OUT", help="write results as markdown tables")
    ap.add_argument("--selftest", action="store_true", help="run the built-in asserts and exit")
    args = ap.parse_args(argv)
    if args.selftest:
        selftest()
        return 0
    if not args.files:
        ap.error("give at least one FILE, or --selftest")
    corpora = build_corpora(args.files, args.min_words)
    command = "python3 style_stats.py " + " ".join(argv if argv is not None else sys.argv[1:])
    print(text_report(corpora))
    if args.json:
        Path(args.json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json).write_text(json.dumps({"command": command, "corpora": corpora}, indent=2) + "\n", encoding="utf-8")
    if args.md:
        Path(args.md).parent.mkdir(parents=True, exist_ok=True)
        Path(args.md).write_text(md_report(corpora, command), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
