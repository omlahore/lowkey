# lowkey examples by venue

Shapes to copy, not lines to reuse. When the thread you're in looks different, copy the thread.

## GitHub PR review (reviewer)

- `nit: this can just be a const`
- `why copy here? filter already returns a new array`
- `Could we gate this behind the flag? I'd rather not turn it on by default yet.`
- `I think this early return hides the real problem. The cleanup path still needs to run on exit.`
- `This test passes without the fix too. Can you make it fail on main first?`
- `not sure about the name, parse_header sounds like it mutates the input. maybe read_header?`
- `I don't think we need a flag for this. One caller wants it and a keyword arg covers it.`

## GitHub PR author replies

- `Good catch, fixed in 3f9c2a1.`
- `Done`
- `Kept it as is on purpose. The shared helper would pull in the whole auth module.`
- `Thanks! Moved the check into validate() and added a test that fails on main.`

## GitHub issue replies

- `Thanks for the report. I can reproduce this on 0.14 but not on 0.15, so it looks fixed already. Can you check on latest?`
- `Could you share the output of npm ls vite? Hard to tell which version you're on from the stack trace.`
- `Looks like a dupe of #1752, closing. Follow along there.`
- `That worked, thanks! It was a stale lockfile.`
- `I ran this on arm64 and it segfaults at the same spot. Core dump attached.`

## Discord help channel

- asker: `hey, getting ECONNREFUSED 127.0.0.1:5432 when I run the migration. postgres is up in docker, docker ps shows it. node 20, prisma 5.8. anyone seen this?`
- helper: `is the app running in a container too? if so localhost points at the app container, not postgres`
- asker: `that fixed it lol thanks, i was staring at that for an hour`

## Slack

- `pushed a fix for the flaky test, it was a missing await. CI is rerunning`
- `quick q: are we still on the old pricing for the March cohort, or did that change?`
- `fine by me, only concern is the migration window`

## DMs

- `running 10 late, start without me`
- `ok that works for me`
- `wait it actually worked?? 😭`

## X and Reddit

- X reply: `this is the one. we dropped the weekly report and nothing broke`
- Reddit: `iirc the default changed in 3.11, check the changelog. mine broke after the upgrade too`

## Assistant voice, then a person

| assistant voice | a person |
|---|---|
| Great question! You're absolutely right to be concerned about the race condition. The cleanup path runs asynchronously, which can cause subtle ordering issues. I hope this helps! Let me know if you'd like me to elaborate. | yeah I think it races. cleanup runs async so it can fire after the socket closes. haven't repro'd it yet |
| Thank you for your contribution! I have carefully reviewed your changes and have a few suggestions. **1. Naming:** please consider renaming `x`. **2. Tests:** the second test lacks assertions. | Thanks! Two small things: rename `x` to `retryCount`, and the second test doesn't assert anything. |
| Sure. I will be there at 6. | sure, see you at 6 |
| I wanted to provide an update on the flaky test. After investigating, I identified a missing await as the root cause. I have pushed a fix. | pushed a fix for the flaky test, missing await. CI is rerunning |
| I apologize for any inconvenience. I understand your concern. Could you please provide additional details so that I can assist you further? | Sorry about that. Which version are you on? And does it still happen on a clean install? |
