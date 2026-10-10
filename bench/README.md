# Texting-style benchmark

Scores how close an agent's chat messages are to the way people actually type, using plain text statistics measured against a human baseline. There is no model-as-judge and nothing to install: the scripts use the Python 3 standard library only (self-test passes on 3.9, 3.12 and 3.14), plus the `gh` CLI for the GitHub collection.

There are two parts. The **human baseline** is real GitHub and Hacker News comments, collected by the scripts in this folder. The **prompt set** is 40 situations where an agent has to write a message for a person. The comparison runs the prompts through the agent with and without the skill, then scores both sets of replies with the same script, next to the baseline.

## Contents

| path | what it is |
|---|---|
| `style_stats.py` | The metrics. Prints a table per corpus plus a comparison table, and can write JSON or markdown. |
| `collect_github.py` | Collects the GitHub baseline through `gh api`, GET requests only. `--control` collects the pre-LLM control corpus. |
| `collect_hn.py` | Collects the Hacker News baseline from the public HN Search API. |
| `prompts.jsonl` | 40 prompts for the agent runs. |
| `data/` | The collected corpora, and next to each a `.meta.json` with parameters, per-repo counts and drop counts. |
| `results/` | `human_baseline.md` and `human_baseline.json`. |

## Reproduce

```sh
cd bench
python3 style_stats.py --selftest

python3 collect_github.py --until 2026-10-11     # needs `gh auth login`, read-only
python3 collect_github.py --control
python3 collect_hn.py --until 2026-10-11

python3 style_stats.py data/human_github.jsonl data/human_github_pre2023.jsonl data/human_hn.jsonl \
  --min-words 10 --json results/human_baseline.json --md results/human_baseline.md
```

Collection reads live data, so running it again draws a new sample and the numbers move a little. The files committed in `data/` are the reference: `style_stats.py` is deterministic, so running the last command on them reproduces `results/` exactly. `--until` pins the end of the sampling period (the control has a fixed one); the committed samples used `2026-10-11`.

## Human baseline

| corpus | file | comments | repos | created |
|---|---|---|---:|---|
| GitHub 2025-26 | `data/human_github.jsonl` | 789 (271 PR review, 230 PR conversation, 288 issue) | 24 | 2025-01 to 2026-09 |
| GitHub 2021-22 control | `data/human_github_pre2023.jsonl` | 615 (205 PR review, 182 PR conversation, 228 issue) | 19 | 2021-01 to 2022-09 |
| Hacker News | `data/human_hn.jsonl` | 504 | n/a | 2025-03 to 2026-09 |

Repos in the 2025-26 set: `vercel/next.js`, `facebook/react`, `microsoft/vscode`, `rust-lang/rust`, `golang/go`, `kubernetes/kubernetes`, `astral-sh/uv`, `tailwindlabs/tailwindcss`, `denoland/deno`, `ollama/ollama`, `oven-sh/bun`, `sveltejs/svelte`, `zed-industries/zed`, `home-assistant/core`, `godotengine/godot`, `python/cpython`, `pytorch/pytorch`, `vuejs/core`, `nodejs/node`, `vitejs/vite`, `huggingface/transformers`, `microsoft/TypeScript`, `grafana/grafana`, `langchain-ai/langchain`. The control uses the same list minus `astral-sh/uv`, `langchain-ai/langchain`, `ollama/ollama`, `oven-sh/bun`, `zed-industries/zed`, which did not exist yet or were not public. `golang/go` contributes fewer comments because its pull requests are reviewed on Gerrit.

Key numbers (full tables for every metric and corpus are in `results/human_baseline.md`; the `10+ words` columns keep only messages of at least 10 words, which removes replies like "thanks!" or "lgtm" so the comparison is with messages of agent-like length):

| metric | GitHub 2025-26 | same, 10+ words | GitHub 2021-22 control | same, 10+ words | Hacker News | same, 10+ words |
|---|---:|---:|---:|---:|---:|---:|
| messages scored | 788 | 589 | 615 | 454 | 497 | 454 |
| sentences starting with a capital letter | 86.0% | 87.6% | 87.1% | 88.8% | 95.1% | 95.1% |
| messages with no capitalised sentence start | 12.6% | 8.0% | 10.2% | 6.0% | 2.8% | 2.9% |
| non-empty lines ending with a full stop | 43.8% | 47.3% | 43.7% | 47.7% | 69.9% | 71.7% |
| messages with no line ending in a full stop | 47.2% | 37.4% | 47.3% | 37.9% | 24.9% | 21.6% |
| em dashes per 1,000 words | 1.31 | 1.37 | 0.11 | 0.12 | 0.20 | 0.21 |
| en dashes per 1,000 words | 0.00 | 0.00 | 0.00 | 0.00 | 0.12 | 0.12 |
| messages with at least one emoji | 5.5% | 5.4% | 5.7% | 5.3% | 0.0% | 0.0% |
| words per message | 31.88 (med 19) | 40.84 (med 27) | 29.42 (med 20) | 37.94 (med 26) | 49.52 (med 33) | 53.65 (med 36) |
| lines per message | 1.90 (med 1) | 2.19 (med 1) | 1.70 (med 1) | 1.92 (med 1) | 1.83 (med 1) | 1.91 (med 1) |
| words per line | 16.76 (med 12) | 18.69 (med 14) | 17.28 (med 13) | 19.73 (med 16) | 27.02 (med 22) | 28.16 (med 23) |
| messages with an assistant-tell phrase | 2.3% | 3.1% | 1.0% | 1.3% | 2.6% | 2.9% |
| messages with header, bold or list | 6.3% | 8.5% | 3.1% | 4.2% | 1.0% | 1.1% |
| messages with a casual marker | 0.9% | 1.2% | 2.0% | 2.4% | 1.4% | 1.5% |
| sentences starting with a subjectless verb | 2.3% | 2.0% | 1.4% | 0.9% | 0.0% | 0.0% |

**What the control shows.** Compare the `10+ words` columns of the two GitHub corpora. Em dashes go from 0.12 to 1.37 per 1,000 words, messages with a header, bold text or a list from 4.2% to 8.5%, and messages with an assistant-tell phrase from 1.3% to 3.1%. "let me know if", "thank you for your" and "i appreciate your" appear 12 times in the 2025-26 set and 0 times in the 2021-22 one. Sentence-initial capitals (88.8% vs 87.6%), lines ending in a full stop (47.7% vs 47.3%), emoji (5.3% vs 5.4% of messages) and median length (26 vs 27 words) did not move. So for dashes, markdown and tell phrases the 2021-22 column is the better target, and for capitalisation, full stops, emoji and length the two eras agree.

**What the baseline says about the style.** In human GitHub comments 12 to 14% of sentences start in lowercase, but only 6 to 13% of messages are lowercase throughout: most messages capitalise normally and a minority drop capitals. 37 to 47% of messages have no line ending in a full stop. Emoji appear in about 5% of messages and casual markers (lol, tbh, ngl and the rest of the list) in 2% or less. Hacker News has no emoji at all and capitalises 95.1% of sentences.

A cell like `32.5 (med 18)` is the mean with the median after it. Everything else is a pooled share or rate over all sentences, lines, words or messages in the corpus.

### How the corpora were collected

**GitHub, 2025 to 2026** (`data/human_github.jsonl`, `collect_github.py`). For each repo the script picks six random three-day windows between 2025-01-01 and four days before `--until`, and reads up to 200 PR review comments and 200 issue-tracker comments from the start of each window (`GET /repos/{repo}/pulls/comments` and `GET /repos/{repo}/issues/comments`, sorted by update time with `since`). Issue-tracker comments are split into PR conversation comments and issue comments by the `/pull/` in their URL. Then it removes:

- bots: user type `Bot`, logins ending in `[bot]`, `bot` or `robot`, and a list of known automation accounts (dependabot, renovate, codecov, vercel, coderabbit, github-actions, netlify, changesets, CLA bots, k8s-ci-robot, rustbot, gopherbot and similar)
- comments created outside the window, longer than 4,000 characters, or exact duplicates of another collected comment (case-insensitive)
- comments that label themselves as AI-generated ("Generated with Claude Code", "Co-Authored-By: Claude", "as an AI language model" and similar)
- bot command lines inside human comments (`/lgtm`, `/retest`, `@rustbot ready`, `bors r+`), and whole comments that were only commands

It then samples, per repo, up to 12 PR review comments, 10 PR conversation comments and 12 issue comments, with at most 4 comments per author per repo and 2 per thread, using a seeded shuffle. Rows hold `text`, `repo`, `kind` (`pr_review`, `pr_comment`, `issue_comment`) and `created_at`. No author fields are stored, `@mentions` inside the text become `@user`, and URLs inside the text are left as written.

**GitHub, pre-LLM control** (`data/human_github_pre2023.jsonl`, `collect_github.py --control`). The same procedure over windows between 2021-01-01 and 2022-09-30, before assistant-written comments were common, on the repos from the list above that existed then. It is there to answer one question: how much of the 2025 to 2026 profile is people drifting toward assistant style rather than a stable human baseline.

**Hacker News** (`data/human_hn.jsonl`, `collect_hn.py`). 18 random 20-minute windows between 2025-01-01 and the day before `--until`, up to 28 comments per window, at most 2 per author and 3 per story, from the HN Search API (`hn.algolia.com/api`, 18 requests). Rows hold `text`, `source` and `created_at`. HTML is converted to text, with code blocks fenced so the metrics skip them.

**Reddit was left out on purpose.** Its robots.txt disallows automated access to the site (`User-agent: * / Disallow: /`) and points to a Public Content Policy with access and use restrictions, so reading the `.json` endpoints is not terms-respecting, and committing the text to a public repo would be redistribution. If you have approved API access, a collector only needs to write `{"text": ...}` lines for `style_stats.py` to score them.

The texts are other people's public comments. They are here so the statistics can be reproduced, not as a general dataset.

## Metrics

`style_stats.py FILE...` takes JSON arrays or JSONL files whose items are strings or objects with a `text` field. Each file is a corpus. Before measuring, it removes fenced code blocks (an unclosed fence runs to the end), inline code, URLs, quoted lines starting with `>`, markdown image and link syntax (link text is kept), markdown table rows, HTML comments and tags, and `On ... wrote:` lines. Inline code, URLs and images leave a placeholder that is not a word, so "`foo` is broken" is not scored as a sentence starting with a lowercase "is".

| metric | definition |
|---|---|
| sentences starting with a capital letter | Sentence starts are the start of every non-empty line and the word after `.`, `!` or `?` plus whitespace (not after `...`, `e.g.`, `etc.` and similar, or a single letter). Leading quotes, brackets, emphasis marks, emoji and `@mentions` are skipped. Only starts whose first token is a plain word count, so versions, paths, commands, numbers and code are ignored. Share = uppercase / (uppercase + lowercase), pooled over all sentences; mean and median are per message. |
| messages with no capitalised sentence start | Among messages with at least one counted sentence start, the share where none starts with a capital. This is the message-level view of lowercase style: the pooled share above hides whether lowercase is spread thinly over many messages or concentrated in a few. |
| non-empty lines ending with a full stop | A line counts as ending with a full stop if its last character is `.`, ignoring trailing closing quotes or brackets, emphasis marks and emoji. `...` does not count. |
| messages with no line ending in a full stop | Share of messages in which no line ends with a full stop. |
| em / en dashes per 1,000 words | U+2014 and U+2013 in the cleaned text, divided by words. Also reported: share of messages with either. |
| emoji per message, share with an emoji | Unicode ranges: pictographs, ZWJ sequences, skin tones, flags, keycaps, and symbols followed by the emoji variation selector. GitHub `:shortcodes:` count too. Text emoticons such as `:)` do not. |
| words per line, lines per message, words per message | A word is a whitespace-separated token with a letter or digit in it; list markers and header hashes are not words. A line is a non-empty line left after cleaning. Reported as mean and median. |
| messages with an assistant-tell phrase | Any phrase from `ASSISTANT_TELLS` in the script ("great question", "i hope this helps", "let me know if", "happy to help", "certainly", "absolutely", "it's worth noting", "in summary", "feel free to", "delve", "here's a", "comprehensive" and others). The per-phrase counts are in the output. Plenty of humans write these words too; the point is the comparison, not zero. |
| messages with a markdown header, bold text, a list | Header = a line starting with 1 to 6 `#` and a space. Bold = `**x**` or `__x__`. List = 2 or more bullet or numbered items. |
| messages with a casual marker | lol, haha, tbh, ngl, imo, idk, kinda, lowkey, fr, rn, plus lmao, lmfao, hehe, imho, nvm, tho (`CASUAL_MARKERS`). Whole-word matches only, so locales like `fr-FR` and paths do not count, and `rn` is skipped when it means React Native ("the rn app"). |
| sentences starting with a subjectless verb | The first word is a past-tense verb that drops its subject ("Fixed", "Ran", "Updated", "Added", "Checked"; the list is `SUBJECTLESS_VERBS`). Imperatives and "Looks good" are not counted. |

All word lists live at the top of `style_stats.py`. The same code and lists score every corpus.

`--min-words N` adds, for every corpus, a second corpus restricted to messages of at least N words after cleaning.

## Prompts

`prompts.jsonl` has 40 lines. Each prompt describes a real-looking situation with concrete code names and results, never says anything about style, and ends with the same output instruction ("Reply with only the message text, nothing else.").

| field | meaning |
|---|---|
| `id` | category plus index, e.g. `pr_review_change_03` |
| `category` | one of the eight below |
| `channel` | where the message would be posted: `github_pr_review`, `github_pr_comment`, `github_issue`, `slack`, `slack_dm`, `discord`, `text_message` |
| `prompt` | the text given to the agent |
| `must_mention` | strings a faithful message should contain verbatim (identifiers, flags, numbers). Empty when a prompt has none worth checking. It is a guard against a style rewrite dropping the technical content. |

| category | prompts | what the agent writes |
|---|---:|---|
| `pr_review_approve` | 4 | an approving review comment |
| `pr_review_change` | 6 | a review comment asking for a change |
| `pr_review_test_result` | 4 | an explanation of a test, CI, benchmark or coverage result |
| `issue_reply` | 6 | a reply to an issue reporter |
| `maintainer_reply` | 6 | a reply to a maintainer's review of the author's PR |
| `chat_help` | 6 | a Slack or Discord help reply |
| `status_update` | 4 | a short status update to a teammate |
| `casual_friend` | 4 | a casual reply to a friend |

## Running the agent arms

The runner is not part of this folder yet. What `style_stats.py` expects from it: one JSONL file per arm, one line per reply, `{"id": "pr_review_approve_01", "text": "..."}`. Run every prompt several times per arm (5 is a reasonable start), because 40 messages per arm is too few to separate small differences. Then:

```sh
python3 style_stats.py results/arm_default.jsonl results/arm_skill.jsonl \
  data/human_github_pre2023.jsonl data/human_github.jsonl --min-words 10 --md results/comparison.md
```

Check `must_mention` separately so a style win does not hide lost content.

## Read the numbers with these in mind

- **The 2025 to 2026 GitHub sample is not purely human.** Bot accounts and comments that label themselves as AI-generated are removed, but only a handful of comments carry such a label (6 candidates in the whole 2025-26 pull), and people paste or lightly edit assistant output without saying so. Compare the two GitHub columns: the 2021 control predates that, so gaps between them show how far current GitHub text has moved. Treat 2021 as the cleaner picture of human typing and 2025 to 2026 as what a reader meets on GitHub today.
- **Hacker News is long-form discussion, not chat.** It is a useful casual-prose baseline with almost no emoji or markdown, but nothing in this folder measures Slack, Discord or texting directly. Do not make claims about those registers from these numbers alone.
- **GitHub comments are technical and public.** Casual markers and emoji are rarer there than in private chat, so this baseline cannot say how many a Slack or friend message should have.
- **Agent messages are longer than human ones.** That is why every table has a `10+ words` variant.
- **The heuristics are simple.** Sentence splitting, the subjectless-verb list, the assistant-tell list and the casual-marker list are approximations, applied identically to every corpus. About 1 to 2 percent of GitHub messages are hard-wrapped at a fixed column, which adds a few false lowercase sentence starts, and indented code blocks and unfenced stack traces are not detected as code.
- **Sampling error.** Shares from 40 messages carry roughly plus or minus 15 points. Use more runs per prompt before reading anything into a small gap.
- **Style only.** None of this says whether a message is correct or useful.
