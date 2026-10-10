---
name: lowkey-voice
description: >
  Builds a voice profile from the user's own messages so lowkey texts like
  them instead of like a generic template. Reads pasted messages, a file, or
  the user's recent GitHub comments, works out their habits (case, line
  breaks, punctuation, emoji, laughter, softeners, length), and saves a short
  profile to ~/.claude/lowkey/voice.md, which lowkey loads every session. Use
  when the user says "learn my voice", "text like me", "match how i write",
  "lowkey voice", or pastes their own messages and asks for replies in that
  style.
---

# lowkey voice

the goal is a short profile that makes every reply sound like this person, not like an assistant doing an impression

## 1. get real samples

ask for 10 to 40 messages the user actually wrote, from chats, GitHub, Slack, Discord, X or Reddit
a file path or a pasted export is fine
if they want their GitHub comments, read them with the gh CLI (read-only), for example:
`gh api "search/issues?q=commenter:USERNAME&sort=updated&per_page=30" --jq '.items[].comments_url'`
then fetch those comment URLs and keep only the comments where `user.login` is theirs
more samples beats clever analysis, so ask for more if there are fewer than 10

## 2. read them like a linguist, not a fan

note what they really do, with rough counts:
- capital letters at the start of lines, or not
- full stops at line ends, or line breaks instead
- message length and lines per message
- which emojis, how often, and where in the line
- laughter: haha, lol, lmao, 😭, 💀, none
- softeners and fillers they use (tbh, i think, kinda, "no?", "right?") and how often
- how they open (hey, yo, none) and how they close
- how they thank, disagree, and say something is good
- words and habits they never use, which matter as much as what they do use

don't invent habits that aren't in the samples

## 3. save the profile

write `~/.claude/lowkey/voice.md`, about 15 to 40 lines:
- a list of traits, each one concrete ("starts lines lowercase, keeps capital I for names", "ends questions with no?")
- 6 to 12 short sample lines in their style, paraphrased, with names, links, and private details removed

create the folder if it's missing
the lowkey hook adds this file after its own rules every session, and the profile wins where they disagree

## 4. check with them

show the profile and ask what's off
fix it, save again, and use it from this reply on
