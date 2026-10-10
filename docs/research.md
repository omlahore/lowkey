# How people actually type online, 2025 to 2026

The research behind lowkey. Every rule in [SKILL.md](../skills/lowkey/SKILL.md) traces back to a finding here.

Research for a texting-style skill (SKILL.md) that makes an agent's messages read like real chat, comment-thread and GitHub writing instead of tidy assistant prose.

Compiled 2026-10-11. Sources: peer-reviewed papers, preprints, named-pollster surveys, official platform docs, and one measurement I ran myself on about 8,500 public GitHub comments pulled on 2026-10-11 (method in section 14).

## Evidence tags used below

| Tag | Meaning |
|---|---|
| PEER | Peer-reviewed journal or conference paper |
| PREPRINT | arXiv or similar, not confirmed peer reviewed by me |
| SURVEY | Survey with a named pollster or named organization |
| MEASURED | My own count on public GitHub data, 2026-10-11 |
| VENDOR | Company analytics, not independent |
| STUDENT | Student paper, poster or thesis. Small samples, treat as directional |
| PRESS | Journalism, blog or book commentary. Not a data source |
| FOLK | Widely repeated, no data found |

No em dashes are used anywhere in this file. Where a source title contains one, I replaced it with a comma.

---

## Summary: 15 rules for the skill

Each rule says what to do, what supports it, and how much I trust it.

**1. Mirror the thread before applying any style.** Read the last 3 to 5 messages and match case, end punctuation, length, emoji and slang. Registers differ sharply by venue: in public GitHub review comments only 14% start with a lowercase letter and 55% end with a period (MEASURED, section 8), while in friend chat lowercase and dropped periods are common (OnePoll, Lucey, Abirou et al.). A 2025 study of LLM replies on X, Bluesky and Reddit found that concrete style examples and retrieved context cut detectability by 2 to 6 points and 2 to 10 more points, while abstract persona descriptions and fine-tuning did little or made it worse (PREPRINT, Pagan et al.). So the skill should carry real example messages and tell the agent to copy the thread, not just list rules. Confidence: high on mirroring, medium on the exact numbers.

**2. On GitHub, Slack and other work threads, default to plain sentence case with contractions.** In 4,843 public PR review comments: 86% of comments that start with a letter start uppercase, 30% contain a contraction versus 14% a spelled-out form, and 0.0% to 0.5% contain imo, tbh, ngl, iirc, lol, idk or rn (MEASURED). Go lowercase and drop final periods only when the thread already does (Neovim and Next.js review threads do: 42% and 49% lowercase starts). Confidence: high.

**3. In chat, do not end a short reply with a period.** One-word and short text replies with a period are rated less sincere and more negative than the same reply without (PEER: Gunraj et al. 2016, Houghton et al. 2018). A 2025 replication with 200 people found the effect for 1-word and 3-to-4-word replies and no significant effect at 6-to-8 words (PEER: Kemp et al.). So "ok" or "sure, see you at 6", not "Ok." or "Sure." Confidence: high for short replies in chat. Not applicable to full sentences or GitHub prose.

**4. Treat register as a bundle and do not mix.** Lowercase start + no final period + contractions is one bundle. Sentence case + period is the other. In PR review comments of 20 words or fewer, 61% of lowercase-start comments have no terminal punctuation and only 15% end with a period, while 47% of sentence-case comments end with a period (MEASURED). A lowercase message with a perfect final period, or a formal paragraph with "ngl" in it, reads as forced. Confidence: medium (observational).

**5. Be short and answer first.** The median PR review comment is 21 words and 13% are 5 words or fewer (MEASURED). In public WhatsApp groups 14% of messages are one word and 75% are 16 words or fewer (PREPRINT). Mobile dating chat had a median of 8 words (PREPRINT). No preamble, no recap, no "let me know if". Over-long answers are a measurable AI trait: RLHF reward models favor length (PEER: Singhal et al.) and LLM replies on social platforms are wordier than human ones (PREPRINT: Pagan et al., Dawkins et al.). Confidence: high.

**6. Split a thought across lines in chat. Do not split it on Slack or GitHub.** In chat the message boundary replaces the period: in a 2007 college sample, sentences inside a multi-sentence message got final punctuation 54% (texts) and 78% (IM) of the time, but only 29% and 35% of messages ended with a mark (PEER: Ling and Baron). Slack's own guidance is the opposite: one message, use shift+return for line breaks, never a lone "hey" (official Slack blog, 2025). GitHub: one comment per point, no bursts. Double texting rules are FOLK, I found no survey. Confidence: medium.

**7. Use at most one exclamation mark, and use it for warmth.** A final "!" reads as the most sincere ending in texts (PEER: Gunraj et al.). In a 122-person college survey, "sure!" made 23% uncomfortable versus 61% for "sure." and 76% for "sure..." (STUDENT: Lucey). In professional discussion lists, exclamation points mostly marked friendliness, not excitement (PEER: Waseleski 2006). On GitHub "!" appears in 4.9% of review comments and 15.8% of issue comments, mostly "Thanks!"; stacked "!!" in about 0.1% (MEASURED). Confidence: high for one, medium for the rest.

**8. Avoid "..." and a bare "?" unless you mean doubt.** "sure..." was the most uncomfortable variant (76%) and a question mark reads as tentative (STUDENT: Lucey). Age effects on ellipses are widely claimed but no representative age-comparison study exists (FOLK with weak support). On GitHub, ellipses are in about 2% of comments (MEASURED). Confidence: medium.

**9. Use "lol" and "haha" as tone softeners in informal chat only.** Linguists treat "lol" as a discourse marker that softens or signals attitude, not laughter (PEER: Schneebeli 2020; PRESS/PEER: McWhorter, McSweeney, Tagliamonte and Denis 2008). 92% of Lucey's respondents used "haha" as a tone particle. On GitHub the lol family is in 0.2% of comments (MEASURED). In work threads skip it unless peers use it. Confidence: medium-high.

**10. Emoji: at most one, at the end, from the safe set. Prefer reactions to reply messages.** On GitHub, reactions in my sample were 65% thumbs up, 12% heart, 8% eyes, 6% thumbs down, 3% laugh, 2% rocket, 2% party (MEASURED). Slack's guidance: eyes for "looking", check mark for "done", reactions instead of "I agree" (official). Emoji sit at the end of 67% of emoji-containing sentences in GitHub issue comments (PREPRINT: Lu et al.). Risks: a 273-person US study found younger readers rate messages ending in a smile emoji as more passive-aggressive (significant) and thumbs up too (marginal), and older readers rate fire and bomb emoji more negatively (PEER: Zhukova and Herring 2024); smileys lower perceived competence in first formal contact (PEER: Glikson et al. 2018); only 26% of workers find emoji acceptable with new clients versus 65% with long-known ones (SURVEY: Censuswide). Confidence: high on risk, medium on exact effect sizes.

**11. Hedge opinions, not facts. Phrase requests as questions or label them.** About 24% of PR review comments contain a hedge (I think, maybe, seems, not sure) and 5% are "could we / can you" style requests (MEASURED). Labels like nit, optional and non-blocking are official practice at Google and in Conventional Comments. Polite comment tone correlates with faster issue resolution (PEER: Destefanis et al., observational), and negative review interactions cost real time (PEER: Egelman et al., Google). Do not hedge things you verified. Confidence: high.

**12. Keep "I" for opinions and first-person experience. Drop it for status replies.** "I think" appears 581 times versus 2 bare "Think ..."; "I guess" 95 versus 0; "I tried" 31 versus 7; "I checked" 38 versus 6. But "Fixed" is bare 190 times versus "I fixed" 7, "Added" 119 versus 51, "Sorry" 62 versus "I'm sorry" 8 (MEASURED). So "i ran this" is right and "Fixed in abc123" is also right. See section 10. Confidence: high.

**13. Never casualize a literal.** Identifiers, flags, paths, versions, error strings and product names keep exact case, in backticks: 51% of PR review comments contain a backtick span (MEASURED). Lowercase style applies to prose only. Confidence: high.

**14. Use only stable dev shorthand. Skip meme slang.** In 8,526 GitHub comments: nit 1.2%, imo 0.5%, btw 0.2%, fwiw 0.1%, tbh/ngl 0.1%, idk 0.06%, rn 0.01%, "no cap", "fr", "ong", "lowkey" 0 (MEASURED). 74% of US adults say brands try too hard to act cool online, and Gen Z is split (42% like, 32% dislike) on brands using slang (SURVEY: CivicScience 2026, Morning Consult 2024). If you use slang at all, use it rarely: the persona prompt that made GPT-4.5 pass a Turing test allowed "fr" and "ngl" but told the model not to use them in every other word (PREPRINT: Jones and Bergen). Confidence: high.

**15. Remove AI tells by changing behavior, not by search and replace, and do not fake typos.** Tells with evidence: em dashes (esp. spaced), "Great question", "You're absolutely right", "I hope this helps", "Certainly!", "not X but Y", rule of three, Title Case headings, bold inline headers, emoji as bullets, clerk-like politeness, over-complete answers (section 9). Wikipedia's own guide warns against treating its signs as the problems to fix. Models are also changing: em dash overuse is being suppressed in some models, and the Economist found only Claude still over-used them as of mid 2026. Typo evidence is mixed: uncorrected typos made a bot seem less human (PEER: Westerman et al.), corrected typos made it seem more human and warmer (PEER: Bluvstein et al. 2024), and Turing-test judges cited typos as a human sign (PREPRINT: Jones and Bergen). Do not inject any. Confidence: high on tells, medium on typos.

### How to use this in SKILL.md

- Ship an example bank (section 11) and tell the agent to mirror the last few messages of the thread. Examples beat rules (rule 1).
- Give per-venue presets: chat/DM, Discord help, Slack, GitHub review, GitHub issue (section 8 table).
- Add a short tells checklist (section 12) as a final pass.
- Keep a hard exemption for code, identifiers and quoted text (rule 13).
- "Keep the subject" is right for opinions and experience reports, but dropping it is the norm for status replies on GitHub (rule 12, section 10).

---

## 1. Punctuation

### 1.1 The sentence-final period

**Core studies (PEER).**
- Gunraj, Drumm-Hewitt, Dashow, Upadhyay, Klin (2016), "Texting insincerely: The role of the period in text messaging", Computers in Human Behavior 55:1067-1075. 126 undergraduates rated short exchanges shown as text messages or as handwritten notes. One-word affirmative replies ("Sure", "Yep") ended with a period or not. Text replies with a period were rated less sincere. Handwritten notes showed no such effect, so the effect belongs to the medium. An exclamation point made replies seem more sincere. The authors conclude punctuation is a cue senders use and receivers understand to carry pragmatic and social meaning. Klin's own gloss: in a chatty medium a period can feel stuffy. Links: https://researchconnect.suny.edu/en/publications/texting-insincerely-the-role-of-the-period-in-text-messaging/ and https://www.nbcnews.com/tech/mobile/drop-dot-periods-makes-text-messages-less-sincere-study-finds-n477331
- Houghton, Upadhyay, Klin (2018), "Punctuation in text messages may convey abruptness. Period", Computers in Human Behavior 80:112-121 (DOI 10.1016/j.chb.2017.10.044, metadata confirmed via Crossref). Indexed highlights say one-word texts with periods were understood as more negative than the same texts without, and that the period may be perceived as abrupt. I did not retrieve the full abstract, so the sample size is unconfirmed.
- Kemp, Kovacic, Beyersmann (2025), "Is the period really 'pissed'? The effect of punctuation and message length on perceptions in digital communication", Telematics and Informatics 97:102241. 200 Australian undergraduates read 30 fictitious exchanges (positive, neutral, negative). Each ended with a short (1 word), medium (3 to 4 words) or long (6 to 8 words) reply, with a final period in half. Periods lowered ratings of how the friend felt for short and medium replies, in every emotional tone. For long replies the period made no significant difference. https://researchers.mq.edu.au/en/publications/is-the-period-really-pissed-the-effect-of-punctuation-and-message/

**Mechanism (PRESS/linguistics).** Mark Liberman: the default way to end a casual electronic message is simply to stop, with no mark, so adding a period adds meaning the reader has to interpret (Language Log, 2015, https://languagelog.ldc.upenn.edu/nll/?p=21548). Ben Crair made the same point in The New Republic (25 Nov 2013): line breaks replaced punctuation, so a period now stands out (https://newrepublic.com/article/115726/period-our-simplest-punctuation-mark-has-become-sign-anger). Gretchen McCulloch's book *Because Internet* (2019) calls this "typographical tone of voice" and notes periods can feel passive-aggressive because they add formality to an informal setting (summary: https://en.wikipedia.org/wiki/Because_Internet, NPR via WUSF https://www.wusf.org/2019-08-20/ironic-informal-and-expressive-new-rules-of-language-evolve-online).

**Who uses periods (SURVEY).** OnePoll survey of 2,000 people reported by StudyFinds (12 Sep 2023): 16% of Gen Z always end sentences with a period versus 28% of millennials; less than a quarter of Gen Z use periods, commas and quotation marks in casual communication. https://studyfinds.com/grammar-young-adults-spelling/

**Older data on how often marks appear (PEER).** Ling and Baron (2007), US college students, 191 texts (2005) versus 191 instant messages (2003): only 29% of text messages and 35% of IMs ended with any final punctuation, and total sentence-final punctuation was 39% for texts and 45% for IMs. https://nl.ijs.si/janes/wp-content/uploads/2014/09/lingbaron07.pdf

**On GitHub the period is normal (MEASURED).** 54.7% of inline PR review comments end with a period, and 25% end with no terminal mark. Among comments of 20 words or fewer, 40.5% end with a period and 33.7% with no mark. The no-period convention is a chat convention, not a GitHub one. Per repo it varies from 30% (Next.js) to 88% (Deno).

### 1.2 Exclamation marks

- Gunraj et al. (above): exclamation points read as most sincere.
- Lucey (2013), "Is she mad at me? Tone and conversation in text messaging", Lingua Frankly 1(1), Boston College undergraduate linguistics journal, n = 122 college-aged respondents (STUDENT). Respondents ranked positivity as CAPS > "!" > no mark > "." > "?" > "...". For the word "sure", the share made uncomfortable was: "sure..." 76%, "sure." 61%, "sure" 56%, "sure!" 23%, "Sure haha" 27%. 79% said they use exclamation points. 88%, 93% and 70% said that small punctuation variants of the same words did not mean the same thing. https://ejournals.bc.edu/index.php/lingua/article/view/9457
- Waseleski (2006), JCMC 11(4):1012-1024, content analysis of 200 exclamation points in two professional electronic discussion groups: exclamations rarely signaled excitability and more often signaled friendly interaction (PEER). https://academic.oup.com/jcmc/article/11/4/1012/4617714
- McCulloch (informal Twitter polls, June 2018, no vote counts reported): three exclamation marks was the most popular signal of genuine enthusiasm; she told The Atlantic that "!" now works as a sincerity marker and suggested people may be tiring of it (PRESS). https://interaksyon.philstar.com/breaking-news/2018/06/29/129630/how-many-exclamation-points-for-sincerity-poll-linguist/amp/
- Abirou, Kerrigan, Michell, Wade (2024, PEER): in a matched-guise experiment on SMS, one exclamation point read as more extroverted, image-oriented, laidback, queer and feminine than none, and two read as particularly trendy and tech-savvy. https://repository.upenn.edu/handle/20.500.14332/59864
- GitHub (MEASURED): "!" appears in 4.9% of PR review comments and 15.8% of issue/PR conversation comments. Most are "Thanks!" or a short congratulation. "!!" appears in 0.0% to 0.2%.

### 1.3 Ellipses

- Lucey (STUDENT): ellipses were read as incompleteness, uncertainty and discomfort, the most negative mark in the ranking (76% uncomfortable for "sure...").
- A Leiden University student thesis (123 respondents of many ages and countries) reports ellipses can be read very negatively and that interpretation of some punctuation depends on age and native language. I could not open the thesis text, only a search summary, so treat as STUDENT and unverified. https://studenttheses.universiteitleiden.nl/access/item%3A2658676/view
- McCulloch (Electric Literature piece, 2020): ellipses were informal thought separators in letters and early email, so some older writers use them neutrally; younger readers may read hesitation or menace; some people use them ironically to parody older users (PRESS). https://electricliterature.com/why-ok-is-the-most-terrifying-text-you-could-ever-receive/
- Glassdoor Community poll (2 to 5 June 2025, over 1,000 US professionals, informal): among four options the ellipsis was ranked most passive-aggressive and the thumbs-up second (SURVEY, not a random sample). https://api.glassdoor.com/blog/emojis-at-work-industries-guide/
- Age-by-age ellipsis perception: I found no representative poll. "Boomer ellipses" is FOLK with weak support.
- GitHub (MEASURED): ellipsis or the ellipsis character appears in 1.8% of PR review comments and 2.4% of issue comments.

### 1.4 Question marks

- Lucey (STUDENT): a question mark on a statement signals tentativeness ("a tentative agreement", "I guess so").
- Ling and Baron (PEER, 2007): 73% of texted semantic questions ended with "?" while only 30% of other sentences got any final mark; in IM, 100% of questions got "?".
- Mobile dating chat (PREPRINT: Zhang and Yasseri 2016): 37% of messages contained a question mark and 21% an exclamation mark. https://arxiv.org/pdf/1607.03320
- GitHub (MEASURED): 23.7% of PR review comments contain "?" and 12.9% end with it. Requests phrased as "could/can/should/would we or you ...?" are 4.9% of review comments, "why not / what about / any reason" 1.1%.

### 1.5 Commas versus line breaks

- Ling and Baron: punctuation inside a message is kept far more than at its end (sentences not at the end of a multi-sentence text had final marks 54% of the time, in IM 78%, versus 29% and 35% at message end). The message boundary does the period's job. See rule 6.
- Chat writers segment on purpose: the sender chooses when to press send, so a message break is a deliberate act (conversation-analysis literature, e.g. Hutchby and Tanna 2008, not read in full, https://emcawiki.net/Hutchby-Tanna2008 ; a German conversation-analytic study of dyadic SMS and WhatsApp dialogues reports that adjacency-pair parts are often sent as separate messages, https://www.revue-tranel.ch/article/view/2971, read via search summary only).
- I found no peer-reviewed study that treats the message break as a formal punctuation mark. The line-break-as-period idea rests on the Ling and Baron counts, Liberman and Crair.

---

## 2. Capitalization

**Lowercase as a social signal (PEER).** Abirou, Kerrigan, Michell, Wade (2024), "New and Changing Social Evaluations of All-lowercase and Exclamation Points", Penn Working Papers in Linguistics 30.1:1-10. Matched-guise test on SMS: all-lowercase was associated with a younger, trendier, more online texter and rated more feminine and queer; the authors describe the stance as carefully calibrated casualness. Ratings were stronger among younger participants. https://repository.upenn.edu/handle/20.500.14332/59864

**Lowercase as deliberate (PRESS).** McCulloch links all-lowercase texting to a reaction against phones that auto-capitalize, so it takes effort and means something; early internet users also typed lowercase by default, which gives it a retro, ironic edge (Electric Literature, link in 1.3). *Because Internet* describes lowercase as "minimalist typography" that can read as deadpan. I found no usage data on how many people turn auto-capitalization off. That is FOLK.

**Who writes it (SURVEY, PRESS).** OnePoll (2,000 people, 2023): a quarter of 18 to 24 year olds use capital letters correctly versus 61% of seniors (https://studyfinds.com/grammar-young-adults-spelling/). Fortune (29 Jan 2026) reports internal messages in the Musk v. OpenAI dispute show Sam Altman typing all lowercase even in high-stakes moments, contrasted with Nadella and Bret Taylor; Altman has said he capitalizes by hand but typing capitals reminds him of school. The article's point is that the same habit costs a 22-year-old more than a CEO (https://www.fortune.com/2026/01/29/openai-ceo-sam-altman-types-all-lowercase-like-gen-z-but-could-be-career-chatgpt-boss, read via search summary).

**Register bundle (FOLK, widely reblogged).** A popular linguistics-Tumblr thread contrasts "i am mad" (neutral), "I Am Mad" (self-aware exaggeration) and "I am mad." (formal, standoffish). Useful as intuition, no data. https://allthingslinguistic.com/tagged/typographical%20register

**ALL CAPS.** In Lucey's college data CAPS sits at the top of the positivity ladder (HAHA above haha), and 61% said they use CAPS. A 2021 Penn working-paper acoustic study found all-caps text is produced with higher loudness, pitch and duration but across many emotions, not only anger (https://repository.upenn.edu/pwpl/vol27/iss1/10, via search summary only). So caps mean intensity, and the "yelling" reading is one of several.

**Pronoun "i".** On GitHub even lowercase-style writers capitalize I: lowercase "i" is 3.5% of first-person uses before common verbs (I think, I was, I have ...) in PR review comments and 6.8% in issue comments (MEASURED).

**GitHub capitalization varies by community (MEASURED, PR review comments that start with a letter).** Next.js 49% lowercase starts, Neovim 42%, PyTorch 22%, Kubernetes 20%, Rust 16%, React 15%, Deno 4%, Django 5%, Tokio 5%. Pick by repo.

---

## 3. Message structure and length

**Length measurements.**
| Source | Medium | Finding |
|---|---|---|
| Ling and Baron 2007 (PEER) | US college SMS, 2005 | 7.7 words per text, about 35 characters; IM transmissions 6.0 words but conversational turns (several IMs in a row) were longer |
| Chang 2020 (PREPRINT) | Public WhatsApp groups, Venezuelan refugee crisis | 14.1% of messages exactly one word, 25% three words or fewer, 75% sixteen words or fewer. https://arxiv.org/pdf/2005.05883 |
| Zhang and Yasseri 2016 (PREPRINT) | Mobile dating chat | median 8 words per message, mean 11.6 |
| MEASURED | GitHub PR review comments | median 21 words, 13% five or fewer, 49% twenty or fewer, 21% over fifty |
| MEASURED | GitHub issue/PR conversation | median 24 words, 18% five or fewer, 27% over fifty |

Self-reported lengths in surveys run higher than logged lengths, so I use logged numbers only.

**Splitting a thought.** Ling and Baron found IM users often send consecutive transmissions that form one turn. Conversation analysis treats a message as one unit of a turn the sender builds by pressing send. Evidence for any "ideal" number of bursts: none found. Double texting etiquette is FOLK; the only data I found is Hinge platform data about reply rates after a second message, via a secondary article (https://www.globaldatinginsights.com/news/sending-second-message-to-matches-who-dont-reply-can-actually-improve-your-chances-of-a-reply/), which says nothing about how it reads.

**Slack (official).** Matt Haughey, Slack blog, 21 March 2025: do not send a DM that only says "hey" or "hello", put the whole message in the first line, and use shift+return for line breaks so a multi-paragraph message goes out as one message, because each message triggers its own notification. Keep discussion in threads, reply with reactions instead of "I agree" messages, use eyes for "looking" and check mark for "done". https://slack.com/intl/en-us/blog/collaboration/etiquette-tips-in-slack

**Discord help channels (community norm, no measured data).** "Don't ask to ask": state the actual problem with details instead of "any Java experts around?" https://dontasktoask.com/

**GitHub.** Bullets appear in 2.6% of PR review comments and 7.7% of issue comments, bold in 1.7% and 6.1%, headers in 0.0% and 1.7% (MEASURED). Conversational replies are plain paragraphs. Use a list only for parallel items.

---

## 4. Emoji and emoticons

### 4.1 Generational meaning

**Best data (PEER).** Zhukova and Herring (2024), "Benign or Toxic? Differences in Emoji Interpretation by Gender, Generation, and Emoji Type", Language@Internet. 273 US adults (Gen Z 97, Millennials 94, Gen X 44, Boomers 38; 159 women, 71 men, 33 non-binary, 10 undisclosed) rated short messages ending in one of four emoji (bomb, fire, thumbs up, smiling face with smiling eyes) on friendliness, playfulness, sarcasm, passive-aggression, offensiveness and threat. Findings:
- Non-binary and Gen Z respondents rated emoji messages as more sarcastic, passive-aggressive and threatening overall.
- Gen Z rated the smile emoji (the 😊 face, not 🙂) as more passive-aggressive than Millennials did (p < .05); Boomers rated it as significantly less passive-aggressive than younger groups (p < .001).
- For thumbs up, the generational gradient (Gen Z and Millennials more passive-aggressive than Gen X, Gen X more than Boomers) was only marginal (p < .06).
- Older generations rated fire and bomb emoji more negatively.
- Caution: the stimuli were short messages that included veiled threats ("You're going to regret that"). Applying the result to a casual 🙂 in a review comment is an extrapolation.
https://homes.luddy.indiana.edu/herring/zhukova.herring.pdf

**Smiley at work (PEER).** Glikson, Cheshin, van Kleef (2018), Social Psychological and Personality Science 9(5):614-625: three experiments, 549 participants from 29 countries read work emails from strangers. Smileys did not raise perceived warmth and lowered perceived competence, which reduced willingness to share information; the effect depended on formality and perceived message appropriateness. Authors: avoid smileys in initial interactions. https://cris.haifa.ac.il/en/publications/the-dark-side-of-a-smiley-effects-of-smiling-emoticons-on-virtual/

**Workplace surveys (SURVEY).**
- Censuswide for Mailsuite, 2,013 US office workers, published 30 Sep 2024: thumbs up is the most-used work emoji (54% have used it); 56% of emoji users say it is to be friendly and 41% to soften communication; 26% of recipients say emoji make an email unprofessional; 6% admit using one to be passive-aggressive. Acceptable with long-known clients: 82% Gen Z, 60% Gen X, 58% Boomers (65% overall). Acceptable with new clients: 26% overall. https://mailsuite.com/blog/how-americans-use-emojis-in-work-emails/
- Atlassian Teamwork Lab with YouGov, 10,000 knowledge workers in the US, France, Germany, India and Australia, 27 May 2025: 88% of Gen Z find emoji useful at work, fewer than half of Boomers and Gen X (heise reports 51% of Gen X and Boomers say not helpful at work, and 61% of Gen Z more likely to read a message with one or two emoji). https://www.atlassian.com/blog/teamwork/digital-body-language and https://heise.de/-10491329
- Glassdoor Community poll, 2 to 5 June 2025, over 1,000 US professionals: 37% have questioned whether an emoji at work was professional (41% of workers aged 21 to 25). Informal poll. https://api.glassdoor.com/blog/emojis-at-work-industries-guide/

**Weak or unverified (do not lean on).**
- Perspectus Global (UK, April 2021, 2,000 people aged 16 to 29) ranked emoji that make you look "officially old": thumbs up, red heart, OK hand, check mark, poo, loudly crying face, monkey covering eyes, clapping hands, kiss mark, grimacing face. I found percentages (24%, 22%, 20%, 17%, 17%, 16%, 15%, 10%, 10%, 9%) only in reprints, not an English original. Note 😭 appears on the "old" list, which complicates "😭 means laughing for Gen Z". https://au.news.yahoo.com/emojis-make-you-look-old-to-gen-z-125933332.html
- Frog Recruitment (NZ) via HCA Mag: 64% read 🙂 as pleased and 21% as passive-aggressive, the latter mostly Gen Z and Millennials. https://hcamag.com/nz/specialisation/employee-engagement/how-many-kiwis-use-emojis-in-the-workplace/491196 (search summary only).
- UCLA student project, 20 respondents: no meaningful difference between Gen Z and Gen Alpha laughter markers. https://languagedlife.ucla.edu/sociolinguistics/lol-vs-%F0%9F%98%82-how-digital-laughter-varies-across-generations/
- "💀 or 😭 means laughing" and "😂 is dated" for Gen Z: widely reported in the press (e.g., CNN 2021), no survey with numbers found. On GitHub 😂 ranked 21st of emoji versus 1st on Twitter (Lu et al. 2018, PREPRINT). FOLK.

### 4.2 Frequency and position

- Share of posts containing emoji (PREPRINT: Lu, Ai, Chen, Cao, Mei, arXiv 2102.05737, 62.9M GitHub posts): 5.53% overall; issues 3.34%, issue comments 3.37%, pull requests 4.14%, PR comments 14.0%, PR review comments 2.92%, commit comments 6.09%. Twitter in 2018: 17.98%. https://arxiv.org/abs/2102.05737
- Earlier (PREPRINT: Lu, Cao, Chen, Liu 2018, arXiv 1812.04863, data 2012 to June 2017): in June 2017 0.58% of issues, 0.75% of PRs, 1.32% of issue comments and 3.23% of PR comments had emoji. 66.77% of emoji-containing sentences in issue comments end with an emoji. In issues and PRs emoji mostly sit mid-post; in comments they sit at the end. Top GitHub emoji (by their table) are thumbs up, smiling faces, check marks and party popper; only one of the top 10 overlaps Twitter's top 10. Single-emoji posts are led by thumbs up (26.3%), ship (23.8%), OK hand (16.7%), clapping hands (16.1%), rocket (15.2%), 100 (13.2%), check mark (12.5%) and party popper (10.8%). https://arxiv.org/abs/1812.04863
- Zhou, Lu, Gao, Mei, Ai (2024), ICWSM, "Emoji Promotes Developer Participation and Issue Resolution on GitHub" (PEER): 1.71% of issues contained emoji in June 2021. With matching, issues with emoji were about 4 percentage points more likely to receive comments and 3.3 to 3.8 points more likely to be closed within 30 to 180 days (observational). https://arxiv.org/abs/2308.16360
- MEASURED (2026-10-11): 2.6% of PR review comments and 4.1% of issue comments contain emoji (about 3.2% overall; 2.4% and 3.5% if check-mark, cross and warning glyphs from checklists are excluded). That matches the 2.92% review-comment rate Lu et al. report for 2021. Conversational emoji counts in 8,526 comments: 👍 36, 🤔 21, 🙏 17, 😅 14, 🙂 11, 🤷 9, 😄 7, 🎉 7, 😆 6, 😭 6. ASCII emoticons appear in about 1% of comments, almost all ":)" (59) and ":-)" (13).

### 4.3 Reactions and "safe" emoji

- GitHub reactions are fixed at 8: 👍 👎 😄 😕 ❤️ 🎉 🚀 👀 (docs: https://docs.github.com/en/rest/reactions/reactions). In my sample of 8,983 human comments, reactions totalled 1,935: 👍 1,259 (65%), ❤️ 240 (12%), 👀 162 (8%), 👎 120 (6%), 😄 63 (3%), 🚀 47 (2%), 🎉 36 (2%), 😕 8 (0.4%) (MEASURED).
- Slack reactions (VENDOR: Cultivate, 83,055 messages from four enterprises over 180 days to 10 June 2020): thumbs up 30% of reactions, heart 8.1%, laughing face 6.4%, fire 4.6%, party popper 4.4%; negative emoji very rare (the most common, mask face, 0.27%); 71% of users used fewer than ten different emoji. https://www.informationweek.com/data-management/what-emoji-use-at-work-can-tell-us-about-team-dynamics
- Slack official: 👀 for "reviewing", ✅ for "done".
- Synthesis (my reading of the numbers above, not a measured result). Safe in a semi-professional thread: 👍 ✅ 👀 🎉 🚀 ❤️ 🙏, and 😅 or 🤔 for a rueful or thinking beat. Riskier: 🙂 and bare 👍 as a reply to a disagreement or a request for help, 😂 💀 😭 (age-split reading), 🔥 and 💣 (older readers read threat), 👎 (harsh), any smiley in a first message to a stranger.
- Emoji function (PEER): emoji act as digital gestures that accompany text (Gawne and McCulloch 2019, Language@Internet 17, https://scholarworks.iu.edu/journals/index.php/li/article/view/37786); emoticons mark illocutionary force, like punctuation, for example a smiley softening a complaint into a description (Dresner and Herring 2010, Communication Theory 20:248-269, https://homes.luddy.indiana.edu/herring/Dresner_Herring.pdf).

---

## 5. Discourse markers and softeners

### 5.1 lol, haha, lmao

- Tagliamonte and Denis (2008), "Linguistic ruin? LOL! Instant messaging and teen language", American Speech 83(1):3-34 (PEER): over a million words of teen IM. Abbreviations were far rarer than media hype; per 100,000 words: lol 195, omg 107, brb 31, ttyl 30, btw 22, nvm 7, gtg 5, np 4, nm 3, lmao 2 (University of Toronto summary, https://magazine.utoronto.ca/?p=3266). Teen-language work also reports lol functioning as a signal of interlocutor involvement, like "mm-hm" (secondary summary, not checked against the paper).
- Schneebeli (2020), "Where lol Is: Function and Position of lol Used as a Discourse Marker in YouTube Comments", Discours 27, DOI 10.4000/discours.10900 (PEER): 886 non-lexical uses of lol in 20,287 YouTube comments. Function depends on position; clause-final lol acts more as a pragmatic marker (attitude, softening) and standalone lol more often means simple amusement. https://journals.openedition.org/discours/10900 and https://www.vice.com/en/article/akvqgk/why-we-use-lol-so-much
- McSweeney (Columbia), *The Pragmatics of Text Messaging* (Routledge): treats lol as an illocutionary-force marker that can soften criticism or signal agreement and understanding. Via secondary coverage only. https://www.hola.com/us/lifestyle/20240425359258/how-millennials-helped-to-the-evolution-of-lol/
- McWhorter (TED, 2013, via UBC summary): lol is no longer "laughing out loud", it is a marker of empathy and shared stance, like "you know" or "I mean". https://blogs.ubc.ca/englishlanguagestudies/?p=168
- McCulloch (Because Internet): lol rarely signals real laughter; it signals irony or goodwill. Citing McSweeney, she adds that it can offer plausible deniability ("you look good in red lol"). https://en.wikipedia.org/wiki/Because_Internet
- Lucey (STUDENT): 92% of respondents used "haha" as a text particle; "lol" self-reported by 35%. Respondents described "haha" as a flavor or filler particle that makes the text taken less seriously, and said an added "lol so don't worry" made a heads-up message ("I have two questions for you at some point") less intimidating. The same "haha" could mean laughter, discomfort or sarcasm depending on context (forced choice of laughing, uncomfortable, sarcastic or other: 66% read "I mean it's your decision...haha" as uncomfortable, 76% read "I hope you are having a wonderful car ride back lol" as sarcastic, 81% read "HAHA you know they were laughing when they wrote that" as laughing).
- GitHub (MEASURED): lol/lmao/haha/hehe in 0.1% of PR review comments and 0.3% of issue comments.

### 5.2 Hedges, boosters, tags

- Theory: hedges soften commitment and manage face (Lakoff 1973; Brown and Levinson 1987; Hyland 1998). Hedges and hesitations affect perceived authority and sociability (Hosman 1989, Human Communication Research, https://aquila.usm.edu/fac_pubs/16291).
- Code review specifically: a Polish thesis on "hedge phrases in feedback" in free-software code review treats comments as face-threatening acts that hedges can soften (STUDENT/early work, https://digespedi.us.edu.pl/?p=636). Politeness in issue comments tracked faster fixes across 22 JIRA projects (PEER: Destefanis, Ortu, Counsell, Swift, Marchesi, Tonelli 2016, PeerJ Computer Science 2:e73, correlational, https://peerj.com/articles/cs-73). Google's 1,317-developer survey found "pushback" in review is rare but costly (PEER: Egelman et al., ICSE 2020, https://research.google/pubs/predicting-developers-negative-feelings-about-code-review/).
- Official practice: Google's code review guide says comment on the code not the developer, explain why, and label severity with Nit, Optional or FYI (https://google.github.io/eng-practices/review/reviewer/comments.html). Conventional Comments defines labels (praise, nitpick, suggestion, issue, todo, question, thought, chore, note) and decorations (non-blocking, blocking, if-minor), and says a bare comment is less clear than a labeled one (https://conventionalcomments.org/). Go's review guide defines LGTM, SGTM and PTAL (https://go.googlesource.com/wiki/+/refs/heads/master/CodeReview.md). Kubernetes asks for polite, respectful discussion, says pushing back is fine, and treats /lgtm and /approve as process signals (https://www.kubernetes.dev/docs/guide/pull-requests/).
- GitHub (MEASURED): about 24% of PR review comments and 22% of issue comments contain at least one hedge or softener from a broad list. "I think" 7.8% and 5.7%, maybe/perhaps 3.7% and 2.6%, please 2.4% and 6.3%, sorry/my bad 1.0% and 1.8%, imo 0.5% and 0.4%, "nit" 2.4% of review comments.
- Question tags ("right?", "no?"): functions are confirmation seeking, softening, or confrontation (https://en.wikipedia.org/wiki/Tag_question). "right?" is the common invariant tag in US English; "no?" is typical of some non-native varieties. On GitHub they are rare: "right?" 0.26%, "no?" 0.08% (MEASURED).

### 5.3 Tone indicators (/j /s /srs /gen)

- What they are: slash-suffixed tags such as /j (joking), /s (sarcasm), /srs (serious), /gen or /genq (genuine) that spell out intended tone; common among neurodivergent users; /s traces to Reddit annotation habits (https://en.wikipedia.org/wiki/Tone_indicator, Khodak, Saunshi, Vodrahalli 2018, LREC, "A Large Self-Annotated Corpus for Sarcasm", https://aclanthology.org/L18-1102/). I found no peer-reviewed study of their effectiveness. Community guides stress they do not excuse rude content (e.g., https://tonetaglist.carrd.co).
- GitHub (MEASURED): 1 comment in 8,526 uses one. Use only in a community that already does.

---

## 6. Slang and abbreviations, 2024 to 2026

**What is stable.** Abbreviations that have lasted decades and are fine in dev contexts: btw, fyi, imo/imho, iirc, afaik, fwiw, tbh, idk, nit, lgtm, ptal, wdyt, ymmv. They are low-frequency even in friendly dev threads (MEASURED, GitHub): btw 0.20%, fyi 0.12%, imo 0.49%, iirc 0.1%, afaik 0.1%, fwiw 0.08%, tbh/ngl 0.14%, idk 0.06%, nit 1.2%, thx/ty 0.29%. Plain casual words are far more common: yeah/yep/nope 1.38%, ok/okay 1.67%, hmm 0.49%, "oh/ah" openers 0.90%, gonna/wanna/kinda 0.28%.

**Effectively absent on GitHub (MEASURED, 8,526 comments).** rn 0.01%, bc/cuz 0.01%, w/ 0.02%, wtf/omg/smh 0.01%. Zero hits for lowkey, highkey, "no cap", fr, ong, "it's giving", bussin, rizz, skibidi, sigma, delulu, slay, cooked and bet ("mid" appears only inside compounds like mid-session, "vibe" four times, mostly "vibe coding"). So rn, bc, w/ and the 2020s meme set are chat-only.

**Classification (my judgment from the evidence in this section; no per-term aging data exists, so treat it as a default, not a finding).**

| Bucket | Terms | Why |
|---|---|---|
| Fine in dev threads | btw, fyi, imo, imho, iirc, afaik, fwiw, tbh, idk, nit, lgtm, ptal, wdyt, ymmv, yeah, yep, nope, hmm | decades old, present in GitHub comments at roughly 0.05% to 1.7% |
| Chat only | rn, bc, cuz, w/, ngl, fr, ong, lowkey, highkey, bet, no cap, lol, lmao, haha | zero or near zero on GitHub, fine with friends who write that way |
| Skip, dated or forced for most writers | it's giving, cooked, mid, rizz, skibidi, sigma, delulu, slay, bussin, 6-7 | meme-cycle words, several AAVE-derived and read as appropriation from outsiders and brands, zero hits on GitHub |

**Abbreviations are rarer than folk belief.** Ling and Baron: under 5% of words in the US texting sample were abbreviated, versus nearly 19% in a British sample from an earlier study. Teen IM abbreviations were a few percent at most (Tagliamonte and Denis).

**Which ones age badly or sound forced.**
- Brand and "fellow kids" use (SURVEY): CivicScience (published 31 Mar 2026): 74% of US adults agree brands try too hard to act cool on social media (77% in 2024); about 60% say Gen Z or Gen Alpha slang in ads has no effect on how they feel about the product; among those affected 26% react negatively and 15% positively; Gen Z (18 to 29) is the most likely to react positively (29%, up from 19% in 2024); only 2% of adults 55 and over react positively. https://civicscience.com/does-gen-z-coded-marketing-actually-work/ Morning Consult (Sep 26 to Oct 8, 2024; 2,205 US adult social media users and 1,002 Gen Zers aged 13 to 27): 71% of Gen Z saw brands using internet slang or trends in the past month versus 37% of all users; Gen Z liked it 42% and disliked it 32%; Gen Z was 14 points more likely than millennials to call it cringe, millennials 6 points more likely to call it cool. https://intel.morningconsult.com/mc-content/analysis/brands-social-media-trends
- Meme-cycle churn (PRESS): Oxford's 2025 word of the year was "rage bait" (announced 1 Dec 2025, 30,000+ votes, https://corp.oup.com/?p=5721); Dictionary.com's was "67" (29 Oct 2025, https://www.dictionary.com/e/word-of-the-year-2025/). A Preply survey reported by Vice (March 2026) names "6-7" and "skibidi" as Gen Z's most disliked slang, but the article's ranking is internally inconsistent, so treat as weak. https://www.vice.com/en/article/gen-z-hates-these-popular-words-for-being-insanely-cringe/
- Origins and appropriation (PRESS/reference): the page says much Gen Z and Gen Alpha slang comes from AAVE and Black queer ballroom culture (it traces "no cap" and "bussin" to AAVE) and cites coverage arguing Black English is often misidentified as Gen Z lingo, which is one more reason for outsiders and brands to avoid it. https://en.wikipedia.org/wiki/Gen_Z_slang
- Regional and demographic spread (PEER): new words on Twitter spread along demographic similarity, especially racial demographics, more than distance (Eisenstein et al. 2014, PLOS ONE). https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4237389/

**What worked in a Turing test (PREPRINT).** Jones and Bergen (2025) persona prompt: a 19-year-old, introverted, into internet culture and video games, low world knowledge. Style instructions (paraphrased): never end sentences with a period; no apostrophes in contractions; usually under five words; some slang such as "fr" or "ngl" but not in every other word; dry and a little humorous; sometimes ask a question back but not every turn. GPT-4.5 with this prompt was judged human 73% of the time (69% with undergraduates, 76% on Prolific), versus 36% without it. Caveats: five-minute games, 300-character messages, one message at a time (the humans were constrained too), strangers, no technical content. The prompt is Figure 6 on page 13 of the PDF. https://arxiv.org/abs/2503.23674 (arXiv v1 numbers; a peer-reviewed PNAS version is reported)

---

## 7. Repeated letters, keysmash, stretching

- Expressive lengthening is a systematic written stand-in for spoken lengthening (PEER: Kalman and Gergle 2014, Computers in Human Behavior 34:187-193, about 500,000 Enron emails; letter repetitions often but not always mirror spoken cues and their use grew over time while the link to speech weakened). https://cris.openu.ac.il/en/publications/letter-repetitions-in-computer-mediated-communication-a-unique-li-2/ Stretched words correlate with subjective, sentiment-bearing language (PEER: Brody and Diakopoulos 2011, EMNLP). https://aclanthology.org/D11-1052/ Darics treats it as a written non-verbal signal in its own right. https://research.aston.ac.uk/en/publications/non-verbal-signalling-in-digital-discourse-the-case-of-letter-rep/
- McCulloch: "yesss" style stretching conveys friendly intimacy (NPR via WUSF, link in 1.1).
- Keysmash: Park's San Diego Linguistics Papers study argues keysmashes behave like language, with a right length, repetition and keyboard location needed for them to look well-formed (STUDENT/working paper, https://quote.ucsd.edu/ling/2022/07/); McCulloch observes most people delete and re-smash if it looks wrong, and phone keysmashes differ from keyboard ones (https://www.cjr.org/language_corner/keysmash-qwerty-asdf.php). Dictionary.com lists "keysmash" as a signal of intense emotion.
- When it reads natural: friend chat, reactions to good news, performing warmth or embarrassment, usually one stretched word per message.
- When it reads cringe (FOLK, consistent with the measurements): in work threads, in every message, on technical content. GitHub (MEASURED): stretched words are in 0.2% to 0.3% of comments and "??" in 0.1%.
- Human text also drops apostrophes ("cant", "im"): human tweets omit contraction apostrophes more than LLM text does (PREPRINT: Dawkins, Fraser, Kiritchenko 2025, https://arxiv.org/abs/2506.09975). Ling and Baron: in texts only 31.9% of contractions kept the apostrophe versus 93.9% in IM. On GitHub, writers keep apostrophes.

---

## 8. Register by platform

### 8.1 Summary table

| Venue | Case | End mark on short replies | Typical length | Emoji | Slang | Evidence |
|---|---|---|---|---|---|---|
| iMessage, WhatsApp (friends) | lowercase common, esp. under 25 | none; period reads curt | 1 to 16 words, often several short messages | frequent, end of line | abbreviations and "lol"/"haha" softeners fine | Lucey, Kemp, Ling and Baron, WhatsApp corpus, OnePoll, Abirou (no measured style data for iMessage itself) |
| Discord help channel | mixed, lean casual | none or "?" | problem stated up front with versions and error text | occasional | casual slang fine among peers | dontasktoask (norm); no measured Discord data found. A 2 billion message dataset exists (arXiv 2502.00627) but reports no style stats |
| Slack (work) | sentence case or light lowercase | optional | one message, short, threads for follow-ups | reactions first, 👍 dominant | light, no meme slang | Slack official, Cultivate (VENDOR), Atlassian/YouGov, Censuswide |
| X replies | lowercase and no period common | none | one to two sentences | moderate (17.98% of 2018 tweets had emoji) | topical slang, hashtags | Lu et al. 2022; Pagan et al.: hashtag and emoji counts betray AI replies on X |
| Reddit comments | sentence case, informal | period normal in longer comments | one short paragraph | low | imo, iirc, afaik, tbh native; tone tags in some subs | Pagan et al.: AI replies on Reddit diverge on politics, aggression and tone; no measured frequencies |
| GitHub PR review | sentence case (86%), lowercase in some repos | period 55% overall, 40% on short ones | median 21 words | 2.6% of comments, reactions common | stable shorthand only, nit/imo/btw | MEASURED (section 8.2) |
| GitHub issue/PR conversation | sentence case (90%) | period 49% | median 24 words | 4.1% | none beyond btw/fyi/imo | MEASURED |

Basis: the two GitHub rows are measured. The Slack row rests on official guidance, vendor data and surveys. The iMessage/WhatsApp, Discord, X and Reddit rows are inferred from the cited studies and community norms. I found no measured style data for those four venues, so treat their cells as defaults to check against the thread, not as findings.

### 8.2 GitHub, measured (public data, 2026-10-11)

Sample: 20 active repos, latest up to 300 inline PR review comments and 300 issue/PR conversation comments each, bots removed. PR review n = 4,843, issue/conversation n = 3,594. Code fences removed before measuring. Percentages are of comments.

| Feature | PR review | Issue/conversation |
|---|---|---|
| Median words (mean) | 21 (33.8) | 24 (55.1) |
| 5 words or fewer | 13.0% | 17.5% |
| Over 50 words | 20.8% | 27.4% |
| Starts lowercase (among letter-starting) | 14.4% | 9.7% |
| Ends with period | 54.7% | 48.6% |
| Ends with "?" | 12.9% | 7.6% |
| Ends with "!" | 1.8% | 5.1% |
| No terminal mark | 25.1% | 34.5% |
| Contains emoji | 2.6% | 4.1% |
| Contains "!" anywhere | 4.9% | 15.8% |
| Contains "?" anywhere | 23.7% | 22.3% |
| Contains an em dash | 5.4% | 4.9% |
| Contains backticks | 51.0% | 32.2% |
| Contains bold | 1.7% | 6.1% |
| Contains bullet list | 2.6% | 7.7% |
| Multi-paragraph | 24.4% | 34.3% |
| Contains a suggestion block | 5.9% | n/a |
| "thanks" | 4.5% | 16.1% |
| Starts with hi/hey | 0.2% | 4.4% |

Notes:
- Short review comments (20 words or fewer, n = 2,342): median 10 words, 21% lowercase starts, 40.5% end with a period, 33.7% no terminal mark, 15.2% end with "?", only 0.9% contain an em dash. The em dash is a feature of long comments.
- Capitalization and period go together. PR review, lowercase-start (n = 629): 55% no terminal mark, 23% period, 16% question. Uppercase-start (n = 3,732): 60% period, 19% none, 13% question.
- Repo culture varies a lot (PR review lowercase-start / ends-with-period): Deno 4% / 88%, Next.js 49% / 30%, Neovim 42% / 58%, Rust 16% / 36%, Kubernetes 20% / 47%, Django 5% / 50%.
- Maintainers (MEMBER) versus contributors (PR comments): mean words 35.5 vs 33.0, "thanks" 1.4% vs 6.4%. Maintainers thank less in review comments; contributors thank reviewers.
- Issue replies: the word "thanks" alone 12.1% (16.1% in the table above, which also counts "thank you", "thx", "ty"), "thanks for the report/PR/..." 4.2%, "could/can/would you" 5.0%, "please" 6.3%, closing or duplicate language 3.2%, hi/hey openers 4.3%.
- Caveat: Oct 2026 comments may include AI-assisted writing, and some repos now have "@claude review" style triggers. I cannot separate human from AI-assisted text, so the em dash rate is an upper bound for purely human writing.

### 8.3 What changes from a friend chat to a public GitHub thread

- Periods and case flip from "optional, often dropped" to "normal".
- Slang almost disappears; stable shorthand and plain casual words remain (yeah, hmm, ok, nit, imo).
- Emoji drop from frequent to rare; reactions replace them.
- Hedging is common and structured (nit, optional, "could we ...?", "not sure, but ...").
- Technical precision rises: 51% of review comments quote code. Prose is short and specific.
- Warmth is carried by "Thanks!", "Good catch", "makes sense", not by laughter tokens.
- Some projects restrict AI-written replies in review threads (the Kubernetes contributor guide says responses to review comments must be written without AI tools; Wikipedia's talk page guidelines allow collapsing LLM-generated comments).

---

## 9. What makes AI-written chat messages easy to spot

### 9.1 Documented tells

**Wikipedia, "Signs of AI writing" and "Signs of AI use in comments" (field guide, read 2026-10-11).** It is descriptive and warns that no single sign proves AI use and that fixing surface signs alone is not the goal. Tells it lists:
- Words and phrases: "I hope this helps", "Of course!", "Certainly!", "You're absolutely right!", "Would you like ...", "is there anything else", "let me know", "here is a".
- Customer-service tone in comments: clerk-like assurances ("I have carefully reviewed", "I understand your concern", apologizing for inconvenience), requests for feedback, headings and Markdown inside discussion comments.
- Formatting: Title Case section headings, heavy boldface, inline-header bullets (bold term, colon, description), emoji in front of headings or bullets (now rarer), Markdown in non-Markdown venues, thematic breaks. Curly quotes are typical of ChatGPT and DeepSeek, not of Gemini or Claude.
- Rhetoric: rule of three, "not just X but also Y" and "it's not X, it's Y" parallelisms, vague attributions, summary conclusions, "serves as" in place of "is".
- Vocabulary clusters that shift by model generation (delve, tapestry, underscore, pivotal, showcasing, leverage, multifaceted, and others) and fade over time.
- Em dashes: LLM output uses them more than nonprofessional human writing of the same genre, in places where humans use commas, parentheses or colons, often spaced. The page says this is more common on discussion pages than in articles, that GPT-5.1 suppresses it on request, and that newer models hard-coded to avoid em dashes now show less punctuation variety (that last claim is marked citation-needed on the page).
- Signs of human writing it lists: simple "is/has" phrasing, plain words (wrote, not authored), qualifiers like "very" and "perhaps", superlatives, isolated wordy phrases.
- It warns that perfect grammar, mixed casual and formal register (common in technical writers) and "bland" prose are NOT reliable signs.
https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing and https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_use_in_comments

**Em dashes, numbers (PRESS and PREPRINT).**
- Washington Post analysis (13 Nov 2025) of 328,744 GPT-4o messages of 10 words or more from 37,929 publicly shared English conversations (May 2024 to July 2025): fewer than 1 in 10 responses used an em dash a year earlier, more than half by summer 2025; the not-just-X-but-Y construction appeared in 6% of chats; a check-mark emoji was used 11 times more than by humans; by July 2025 about 70% of messages contained an emoji (read via Boston Globe reprint; shared-conversation sample, so selection bias). https://www.bostonglobe.com/2025/11/13/business/chatgpt-writing-style-clues/
- OpenAI's GPT-5.1 follows a custom instruction to avoid em dashes (Altman, Nov 2025; Ars Technica coverage titled "Sam Altman celebrates ChatGPT finally following em dash formatting rules", 14 Nov 2025). https://arstechnica.com/ai/2025/11/forget-agi-sam-altman-celebrates-chatgpt-finally-following-em-dash-formatting-rules/
- The Economist ("How to spot AI writing", dated 30 July 2026 per Wikipedia's citation): using its own articles as the human baseline (55,940 sentences, 1.2 million words) and asking ChatGPT, Claude, Gemini and Grok to rewrite them, only Claude used more em dashes than the human writers and ChatGPT used markedly fewer; LLM text had fewer commas and semicolons and almost no parentheses, "and" was the most overused word, and bots favored long polysyllabic words, nominalizations and "not only but also". Read via secondary summaries. https://biznews.com/tech/spot-ai-written-text

**Style in grammar (PEER).** Reinhart et al. (2025), "Do LLMs write like humans? Variation in grammatical and rhetorical styles", PNAS (arXiv 2410.16107): GPT-4o used present participial clauses 5.3 times as often as humans, "that" clauses as subjects 2.6 times, nominalizations 2.1 times, phrasal coordination 1.9 times, and agentless passives about half as often. Instruction-tuned models differ from humans more than base models. Corpus: news, academic, blogs, web and subtitle text, not chat. https://arxiv.org/abs/2410.16107

**Word-level overuse (PEER).** Kobak et al. 2025, Science Advances 11(27): excess vocabulary after 2022 in biomedical papers (https://www.science.org/doi/10.1126/sciadv.adt3813, cited by Wikipedia, not read by me). Juzek and Ward 2025, "Why does ChatGPT delve so much?" (https://aclanthology.org/2025.coling-main.426.pdf) and a follow-up on the role of learning from human feedback (https://arxiv.org/abs/2508.01930), both cited by Wikipedia, not read by me. Per Wikipedia and the Washington Post, "delve" has faded since 2024 while other words rose. Takeaway: word lists age fast, so use behavior rules rather than word blacklists.

**Affect and tone on social platforms (PREPRINT).** Pagan, Tornberg, Bail, Hannak, Barrie (arXiv 2511.04195, Nov 2025): classifiers detected AI-written replies on X, Bluesky and Reddit with 70 to 80% accuracy even after calibration. The most persistent differences were affective: positive emotion, affection and optimism over-represented, toxicity under-represented; on X, hashtag and emoji counts; on Bluesky, word count and word length; on Reddit, aggression, politics and power. Instruction-tuned models did worse than base models, and bigger models did not help. Concrete style examples and retrieved context reduced detectability; abstract persona descriptions and fine-tuning did not reliably help. https://arxiv.org/abs/2511.04195

**Social posts (PREPRINT).** Dawkins, Fraser, Kiritchenko (NRC Canada, 2025), 505,159 AI-generated posts: base models wrote longer posts, lower type-token ratio, over-produced hashtags and emoji, and used more adverbs, first-person pronouns, private verbs and contractions than humans. Fine-tuned models were far harder to detect, confirmed in a 250-person human study. https://arxiv.org/abs/2506.09975

### 9.2 Sycophancy and canned openers

- anthropics/claude-code issue #3382, "Claude says 'You're absolutely right!' about everything", opened 12 Jul 2025, closed 22 Aug 2025, 179 comments, 870 thumbs up (verified via the GitHub API). The Register covered it (13 Aug 2025). https://github.com/anthropics/claude-code/issues/3382 and https://www.theregister.com/2025/08/13/claude_codes_copious_coddling_confounds/
- OpenAI rolled back a GPT-4o update on 28 to 29 Apr 2025 because it had become noticeably sycophantic. https://openai.com/index/expanding-on-sycophancy/
- Length is rewarded in training: reward models trained on helpfulness data correlate strongly with length, and a length-only reward reproduced most RLHF gains (PEER: Singhal et al., COLM 2024). https://arxiv.org/abs/2310.03716

### 9.3 Can people spot it?

- Russell, Karpinska, Iyyer (ACL 2025): five annotators who use LLMs for writing, by majority vote, labeled 299 of 300 articles correctly (99.3% true positive, 0% false positive). Nine annotators in total; non-experts averaged 56.7% true positive with about 52% false positive, near chance. Experts cited vocabulary (53% of explanations), sentence structure (36%), grammar and punctuation (25%), originality (24%), clarity (20%). Experts also took informality (contractions, slang, "just", "actually") as a sign of human writing. https://arxiv.org/abs/2501.15654
- Jakesch, Hancock, Naaman (2023), PNAS 120(11):e2208839120: 4,600 participants could not detect AI self-presentations; their heuristics (first-person pronouns, contractions, family topics) were flawed and exploitable. https://doi.org/10.1073/pnas.2208839120
- Implication: the reader group matters. Developers who use LLMs daily are the hardest audience. First-person pronouns and contractions mislead casual readers, while heavy users in Russell et al. cited vocabulary, sentence structure, originality and clarity.

### 9.4 Typos and "no mistakes ever"

- Westerman, Cross, Lindmark (2018), Communication Studies: typos in a "chatbot's" replies lowered perceived humanness (PEER). https://doi.org/10.1080/10510974.2018.1557233
- Bluvstein, Zhao, Barasch, Schroeder (2024), "Imperfectly Human: The Humanizing Potential of (Corrected) Errors in Text-Based Communication", Journal of the Association for Consumer Research: five studies, over 3,000 participants; agents that made and corrected typos were rated more human and warmer than agents with no typos or uncorrected typos. The authors do not recommend inserting typos. https://newsroom.haas.berkeley.edu/research/to-err-is-human-and-in-the-age-of-ai-it-may-be-humanizing/
- Jones and Bergen: Turing-test judges named typos and "humanly" language among their reasons; linguistic style was the top reason class (27% of reasons) ahead of interaction dynamics (23%).
- Verdict: mixed. Do not inject typos. Natural informality (fragments, dropped final period, contractions) is the safe part of "imperfection".

---

## 10. What real casual writers still keep

**Technical terms and identifiers in exact case (MEASURED).** 51.0% of PR review comments and 32.2% of issue comments contain backticks. Lowercase and no-period style never touches identifiers, paths, flags, versions, quoted errors or product names. This is a correctness rule, not a style choice.

**The subject of the sentence: it depends on the sentence (MEASURED, n about 8,500 comments).**
- Opinions and beliefs keep "I": "I think" 581 versus bare "Think ..." 2; "I don't think" 144 versus "Don't think" 1; "I'm not sure" 81 versus "Not sure" 36; "I guess" 95 versus 0; "I believe" 56 versus 0; "I agree" 55 versus "Agree" 4; "I wonder" 32 versus 2; "I assume" 25 versus 2.
- First-person experience reports keep "I" more often than not: "I ran" 26 versus bare "Ran" 8; "I tried" 31 versus 7; "I checked" 38 versus 6; "I tested" 24 versus 15.
- Status replies drop it: bare "Fixed" 190 versus "I fixed" 7; "Added" 119 versus 51; "Updated" 53 versus 21; "Pushed" 17 versus 5; "Removed" 30 versus 21; bare "Sorry" 62 versus "I'm sorry" 8. Comments that start with a bare status verb outnumber those starting with "I/we" plus a status verb 7.7 to 1 in PR review comments.
- Linguistics background (PEER): subject pronoun drop is common in informal registers, "diary drop", including text messages and emails: "Should really go to the gym tomorrow", "Don't think I can make it tonight" (Weir 2009, UCL, https://www.isle-linguistics.org/assets/content/documents/hogg/weir2009.pdf; Haegeman and Ihsane on diary style). Rates vary hugely by writer (2% to 92% across diary extracts in Haegeman and Ihsane 1999, per a search summary).
- Rule: keep "I" for opinion, doubt and what you personally tried. Drop it for commit-log style status ("Fixed in abc123", "Added a test") and interjections ("Sorry", "Thanks"). Never drop it in a way that leaves the claim ambiguous about who did or believes what.

**Clarity when it matters.** Casual writers add context only when needed: versions, commands, error text, links to the commit or issue. Short messages are not vague messages: the median GitHub review comment is 21 words and half of review comments quote code.

**Contractions.** In PR review comments 29.6% contain a contraction and 14.3% a spelled-out form; in texts 85% of potential contractions were contracted (Ling and Baron). Heavy LLM users read contractions and informality as human, so they help, but only as part of the whole bundle.

**Typographic basics.** Capital I, capitalized proper nouns and product names (GitHub, not github), straight quotes. Lowercase "i" is 3.5% of first-person uses on GitHub.

---

## 11. Example messages

All paraphrased or written fresh for this file. They show shape, not content to reuse.

**GitHub PR review (reviewer)**
1. `nit: this can just be a const`
2. `why copy here? filter already returns a new array`
3. `Could we gate this behind the flag? I'd rather not turn it on by default yet.`
4. `I think this early return hides the real problem. The cleanup path still needs to run on exit.`
5. `This test passes without the fix too. Can you make it fail on main first?`
6. `not sure about the name, parse_header sounds like it mutates the input. maybe read_header?`
7. `I don't think we need a flag for this. One caller wants it and a keyword arg covers it.`

**GitHub PR author replies**
8. `Good catch, fixed in 3f9c2a1.`
9. `Done`
10. `Kept it as is on purpose. The shared helper would pull in the whole auth module.`

**GitHub issue replies**
11. `Thanks for the report. I can reproduce this on 0.14 but not on 0.15, so it looks fixed already. Can you check on latest?`
12. `Could you share the output of npm ls vite? Hard to tell which version you're on from the stack trace.`
13. `Looks like a dupe of #1752, closing. Follow along there.`
14. `That worked, thanks! It was a stale lockfile.`
15. `I ran this on arm64 and it segfaults at the same spot. Core dump attached.`

**Discord help channel**
16. (asker) `hey, getting ECONNREFUSED 127.0.0.1:5432 when I run the migration. postgres is up in docker, docker ps shows it. node 20, prisma 5.8. anyone seen this?`
17. (helper) `is the app running in a container too? if so localhost points at the app container, not postgres`
18. (asker, later) `that fixed it lol thanks, i was staring at that for an hour`

**Slack**
19. `pushed a fix for the flaky test, it was a missing await. CI is rerunning`
20. `quick q: are we still on the old pricing for the March cohort, or did that change?`
21. `fine by me, only concern is the migration window`

**DM or iMessage**
22. `running 10 late, start without me`
23. `ok that works for me`

**X or Reddit**
24. (X reply) `this is the one. we dropped the weekly report and nothing broke`
25. (Reddit) `iirc the default changed in 3.11, check the changelog. mine broke after the upgrade too`

### Before and after (assistant voice to human voice)

| Assistant voice | Human voice |
|---|---|
| Great question! You're absolutely right to be concerned about the race condition. The cleanup path runs asynchronously, which can cause subtle ordering issues. I hope this helps! Let me know if you'd like me to elaborate. | yeah I think it races. cleanup runs async so it can fire after the socket closes. haven't repro'd it yet |
| Thank you for your contribution! I have carefully reviewed your changes and have a few suggestions. **1. Naming:** please consider renaming `x`. **2. Tests:** the second test lacks assertions. | Thanks! Two small things: rename `x` to `retryCount`, and the second test doesn't assert anything. |
| Sure. I will be there at 6. | sure, see you at 6 |
| I wanted to provide an update on the flaky test. After investigating, I identified a missing await as the root cause. I have pushed a fix. | pushed a fix for the flaky test, missing await. CI is rerunning |
| I apologize for any inconvenience. I understand your concern. Could you please provide additional details so that I can assist you further? | Sorry about that. Which version are you on? And does it still happen on a clean install? |

---

## 12. Things to avoid

**AI tells (final-pass checklist).**
- Em dashes, especially spaced ones. En dashes used as em dashes. A sentence that needs a dash should be split or use a comma.
- Openers and closers: "Great question", "You're absolutely right", "Certainly!", "Of course!", "I hope this helps", "Let me know if ...", "Would you like me to ...", "Happy to help".
- Clerk language: "I apologize for any inconvenience", "I understand your concern", "I have carefully reviewed".
- "Not X but Y", "It's not just X, it's Y", rule-of-three lists, symmetrical paragraph shapes, a tidy closing summary.
- Title Case headings, bold inline headers, bullet lists and emoji bullets in conversational replies, Markdown in a venue that does not render it.
- Over-complete answers: every caveat, every alternative, a recap of the question.
- Uniform politeness and positivity on every message; absence of any blunt or neutral reply.
- Always-perfect sentence rhythm, always the same opener, a trailing emoji on every comment.

**Forced slang and cringe.**
- Meme slang in work threads: "no cap", "fr fr", "it's giving", "bussin", "rizz", "skibidi", "sigma", "delulu", "slay", "cooked", "bet", "6-7". All of these except "6-7" (not tested) had zero hits in 8,526 GitHub comments.
- Brand-voice enthusiasm and "fellow kids" register (74% of US adults dislike brands acting cool).
- Fake typos, fake keysmash, fake "lol" laughter.
- Gen Z-coded emoji (💀 😭) in a thread of older engineers.
- A smiley or 🙂 in a first message to a stranger or in a disagreement.
- Tone tags (/j /s) where nobody else uses them.

**Overuse.**
- "lol", "haha", "tbh", "ngl", "imo" in every message. Use at most one softener per message and not in every message.
- Multiple hedges in one sentence ("I think maybe it might possibly ...").
- Hedging verified facts.
- Stacked punctuation ("!!", "??", "...").
- More than one emoji, or emoji at the start of lines.
- Splitting one thought into three Slack messages.
- Mixed bundles: lowercase with perfect formal sentences; sentence case with "ngl".
- Stripping subjects from opinions ("Think this is wrong") or adding them to status ("I have fixed the issue").
- Casual style applied to identifiers.

---

## 13. Gaps and caveats

- No measured style data for Discord, iMessage or Slack message text. Only a dataset paper (Discord, 2 billion messages, arXiv 2502.00627), vendor emoji counts for Slack, and norms documents.
- No representative survey on ellipsis perception by age, on double texting, on how many people disable auto-capitalization, or on whether 😂 or 💀 are read as dated or as laughter. All FOLK.
- Houghton et al. 2018: I confirmed the paper and its highlights but not the full abstract or sample size.
- Several sources were read through search summaries or secondary articles (Fortune on Altman, the Economist study, the Penn all-caps paper, McSweeney, Frog Recruitment, the Leiden thesis, the Washington Post analysis via Boston Globe). Marked where relevant.
- The Wikipedia guide I read is the live page on 2026-10-11 and contains items I could not independently verify (for example mid-2026 model-era vocabulary and a claim about reduced punctuation variety, marked citation-needed there). It is a field guide for Wikipedia, so some signs may not carry over to chat.
- Jones and Bergen's 73% result used five-minute, 300-character, one-message-at-a-time games. It is evidence for what a style prompt can do in short chat with strangers, not for GitHub review.
- GitHub measurement: 20 repos, latest comments only, bots filtered by account type and name, some AI-assisted text likely included. Percentages from different cuts (n between 8,437 and 8,526) differ by under 1 point. Not a random sample of GitHub.

---

## 14. Method notes for the GitHub measurement

- Pulled 2026-10-11 with `gh api repos/{repo}/pulls/comments` and `.../issues/comments`, three pages of 100 per repo per type, sorted newest first. Read-only.
- Repos: kubernetes/kubernetes, rust-lang/rust, facebook/react, vercel/next.js, vitejs/vite, microsoft/vscode, python/cpython, pytorch/pytorch, home-assistant/core, grafana/grafana, denoland/deno, tokio-rs/tokio, nodejs/node, astral-sh/ruff, godotengine/godot, neovim/neovim, zed-industries/zed, tailwindlabs/tailwindcss, helix-editor/helix, django/django.
- Date span of included comments: 2026-02-19 to 2026-10-10 (slow repos reach further back).
- Filters: dropped bots (account type Bot, names ending in bot, a few known automation accounts), dropped comments empty after removing code fences, HTML comments and quoted lines. Case and end-mark checks used the original body start and the cleaned end.
- Scripts were run with Python 3 in isolated mode. The tables above come from three analysis passes with slightly different filters. Counts for subject-drop, slang, hedges and tags use all human comments (n about 8,500).
- Reactions: summed the `reactions` object of 8,983 human comments.
- Emoji detection: Unicode emoji ranges plus GitHub shortcodes restricted to the official GitHub emoji list (to avoid false positives like `::` paths). An early pass counted any `:word:` as an emoji and overstated rates (4.4% and 7.0%); all emoji figures in this file use the corrected detector.

---

## 15. Sources

### Punctuation and texting
- Gunraj, Drumm-Hewitt, Dashow, Upadhyay, Klin (2016), CHB 55:1067-1075. PEER. https://researchconnect.suny.edu/en/publications/texting-insincerely-the-role-of-the-period-in-text-messaging/ . Texts with a final period rated less sincere, handwritten notes unaffected, 126 undergraduates, exclamation most sincere.
- NBC News on the same study. PRESS. https://www.nbcnews.com/tech/mobile/drop-dot-periods-makes-text-messages-less-sincere-study-finds-n477331
- Binghamton University research news (Dec 2015). PRESS. https://discovere.binghamton.edu/research-in-the-news/klin-6587.html
- Houghton, Upadhyay, Klin (2018), CHB 80:112-121, DOI 10.1016/j.chb.2017.10.044. PEER. https://doi.org/10.1016/j.chb.2017.10.044 . Period read as abrupt and more negative on one-word replies (highlights only).
- Kemp, Kovacic, Beyersmann (2025), Telematics and Informatics 97:102241. PEER. https://researchers.mq.edu.au/en/publications/is-the-period-really-pissed-the-effect-of-punctuation-and-message/ . N = 200, effect for 1 and 3 to 4 words, none at 6 to 8.
- Lucey (2013), Lingua Frankly 1(1). STUDENT. https://ejournals.bc.edu/index.php/lingua/article/view/9457 and https://ejournals.bc.edu/index.php/lingua/article/download/9457/8388/16192 . n = 122, "sure..." 76% uncomfortable.
- Ling and Baron (2007), Text messaging and IM: linguistic comparison of American college data (J. Language and Social Psychology 26(3):291-298, DOI 10.1177/0261927X06303480). PEER. I read the pre-publication manuscript dated 16 Feb 2007, so figures may differ slightly in print. https://nl.ijs.si/janes/wp-content/uploads/2014/09/lingbaron07.pdf . 7.7 words per text, 29% of texts end with a mark.
- Waseleski (2006), JCMC 11(4):1012-1024. PEER. https://academic.oup.com/jcmc/article/11/4/1012/4617714 . 200 exclamations, friendliness over excitability.
- Liberman, Language Log (7 Oct 2015). PRESS. https://languagelog.ldc.upenn.edu/nll/?p=21548 . Default is to end by stopping.
- Crair, The New Republic (25 Nov 2013). PRESS. https://newrepublic.com/article/115726/period-our-simplest-punctuation-mark-has-become-sign-anger
- McCulloch (2019), Because Internet; NPR via WUSF. PRESS. https://www.wusf.org/2019-08-20/ironic-informal-and-expressive-new-rules-of-language-evolve-online ; summary https://en.wikipedia.org/wiki/Because_Internet
- McCulloch exclamation polls via Interaksyon (2018). PRESS. https://interaksyon.philstar.com/breaking-news/2018/06/29/129630/how-many-exclamation-points-for-sincerity-poll-linguist/amp/
- Electric Literature on "Ok." (2020). PRESS. https://electricliterature.com/why-ok-is-the-most-terrifying-text-you-could-ever-receive/
- OnePoll via StudyFinds (12 Sep 2023). SURVEY. https://studyfinds.com/grammar-young-adults-spelling/ . 16% of Gen Z always use periods versus 28% of millennials.
- Leiden thesis on ellipses. STUDENT. https://studenttheses.universiteitleiden.nl/access/item%3A2658676/view
- Zhang and Yasseri (2016), mobile dating chat. PREPRINT. https://arxiv.org/pdf/1607.03320 . Median 8 words, 37% with "?", 21% with "!".
- Chang (2020), public WhatsApp groups. PREPRINT. https://arxiv.org/pdf/2005.05883 . 14.1% one word, 75% 16 words or fewer.

### Capitalization
- Abirou, Kerrigan, Michell, Wade (2024), PWPL 30.1:1-10. PEER. https://repository.upenn.edu/handle/20.500.14332/59864
- Penn 2021, No need to yell, PWPL 27.1. PEER (summary only). https://repository.upenn.edu/pwpl/vol27/iss1/10
- Fortune (29 Jan 2026) on Altman. PRESS. https://www.fortune.com/2026/01/29/openai-ceo-sam-altman-types-all-lowercase-like-gen-z-but-could-be-career-chatgpt-boss
- All Things Linguistic, typographical register reblogs. FOLK. https://allthingslinguistic.com/tagged/typographical%20register

### Emoji
- Zhukova and Herring (2024), Language@Internet. PEER. https://homes.luddy.indiana.edu/herring/zhukova.herring.pdf
- Glikson, Cheshin, van Kleef (2018), SPPS 9(5):614-625. PEER. https://cris.haifa.ac.il/en/publications/the-dark-side-of-a-smiley-effects-of-smiling-emoticons-on-virtual/
- Lu, Cao, Chen, Liu (2018), A first look at emoji usage on GitHub. PREPRINT. https://arxiv.org/abs/1812.04863
- Lu, Ai, Chen, Cao, Mei, Emojis predict dropouts of remote workers (arXiv 2102.05737). PREPRINT. https://arxiv.org/abs/2102.05737
- Zhou, Lu, Gao, Mei, Ai (2024), ICWSM. PEER. https://arxiv.org/abs/2308.16360
- Gawne and McCulloch (2019), Emoji as digital gestures, Language@Internet 17. PEER. https://scholarworks.iu.edu/journals/index.php/li/article/view/37786
- Dresner and Herring (2010), Communication Theory 20:248-269. PEER. https://homes.luddy.indiana.edu/herring/Dresner_Herring.pdf
- Censuswide for Mailsuite (30 Sep 2024). SURVEY. https://mailsuite.com/blog/how-americans-use-emojis-in-work-emails/
- Atlassian Teamwork Lab with YouGov (27 May 2025). SURVEY. https://www.atlassian.com/blog/teamwork/digital-body-language ; heise (17 Jul 2025) https://heise.de/-10491329
- Glassdoor Community poll (June 2025). SURVEY (informal). https://api.glassdoor.com/blog/emojis-at-work-industries-guide/
- Cultivate Slack emoji analysis (2020). VENDOR. https://www.informationweek.com/data-management/what-emoji-use-at-work-can-tell-us-about-team-dynamics
- Perspectus Global (2021) via Yahoo. SURVEY (percentages unverified). https://au.news.yahoo.com/emojis-make-you-look-old-to-gen-z-125933332.html
- Frog Recruitment via HCA Mag. SURVEY (summary only). https://hcamag.com/nz/specialisation/employee-engagement/how-many-kiwis-use-emojis-in-the-workplace/491196
- UCLA student project on laughter markers. STUDENT. https://languagedlife.ucla.edu/sociolinguistics/lol-vs-%F0%9F%98%82-how-digital-laughter-varies-across-generations/
- GitHub REST reactions docs. https://docs.github.com/en/rest/reactions/reactions

### Discourse markers, hedges, politeness
- Tagliamonte and Denis (2008), American Speech 83(1):3-34; summary https://magazine.utoronto.ca/?p=3266 . PEER.
- Schneebeli (2020), Discours 27. PEER. https://journals.openedition.org/discours/10900 ; Vice summary https://www.vice.com/en/article/akvqgk/why-we-use-lol-so-much
- McSweeney, The Pragmatics of Text Messaging (Routledge), via Hola. PRESS. https://www.hola.com/us/lifestyle/20240425359258/how-millennials-helped-to-the-evolution-of-lol/
- McWhorter TED talk via UBC. PRESS. https://blogs.ubc.ca/englishlanguagestudies/?p=168
- Hosman (1989), Human Communication Research. PEER. https://aquila.usm.edu/fac_pubs/16291
- Hedge phrases in code review thesis. STUDENT. https://digespedi.us.edu.pl/?p=636
- Destefanis et al. (2016), PeerJ CS 2:e73. PEER. https://peerj.com/articles/cs-73
- Egelman et al. (2020), ICSE. PEER. https://research.google/pubs/predicting-developers-negative-feelings-about-code-review/
- Google Engineering Practices, comments. https://google.github.io/eng-practices/review/reviewer/comments.html
- Conventional Comments. https://conventionalcomments.org/
- Go code review guide. https://go.googlesource.com/wiki/+/refs/heads/master/CodeReview.md
- Kubernetes pull request guide. https://www.kubernetes.dev/docs/guide/pull-requests/
- Slack etiquette (Haughey, 21 Mar 2025). https://slack.com/intl/en-us/blog/collaboration/etiquette-tips-in-slack
- Don't ask to ask. https://dontasktoask.com/
- Tag questions. PRESS/reference. https://en.wikipedia.org/wiki/Tag_question
- Tone indicators. PRESS/reference. https://en.wikipedia.org/wiki/Tone_indicator ; Khodak et al. (LREC 2018) https://aclanthology.org/L18-1102/ ; tag list https://tonetaglist.carrd.co
- Weir (2009), Subject pronoun drop in informal English. PEER/working paper. https://www.isle-linguistics.org/assets/content/documents/hogg/weir2009.pdf

### Slang
- CivicScience (31 Mar 2026). SURVEY. https://civicscience.com/does-gen-z-coded-marketing-actually-work/
- Morning Consult (Oct 2024). SURVEY. https://intel.morningconsult.com/mc-content/analysis/brands-social-media-trends
- Preply via Vice (Mar 2026). SURVEY (weak). https://www.vice.com/en/article/gen-z-hates-these-popular-words-for-being-insanely-cringe/
- Oxford University Press word of the year 2025. https://corp.oup.com/?p=5721 ; Dictionary.com 2025 https://www.dictionary.com/e/word-of-the-year-2025/
- Gen Z slang reference. PRESS/reference. https://en.wikipedia.org/wiki/Gen_Z_slang
- Eisenstein, O'Connor, Smith, Xing (2014), PLOS ONE. PEER. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4237389/
- Jones and Bergen (2025), Large language models pass the Turing test. PREPRINT. https://arxiv.org/abs/2503.23674 (persona prompt in Figure 6, PDF p. 13)

### Letter repetition, keysmash
- Kalman and Gergle (2014), CHB 34:187-193. PEER. https://cris.openu.ac.il/en/publications/letter-repetitions-in-computer-mediated-communication-a-unique-li-2/
- Brody and Diakopoulos (2011), EMNLP. PEER. https://aclanthology.org/D11-1052/
- Darics, Non-verbal signalling in digital discourse: the case of letter repetition. PEER. https://research.aston.ac.uk/en/publications/non-verbal-signalling-in-digital-discourse-the-case-of-letter-rep/
- Park (2022), keysmashes, San Diego Linguistics Papers 11. STUDENT/working paper. https://quote.ucsd.edu/ling/2022/07/
- CJR Language Corner on keysmash. PRESS. https://www.cjr.org/language_corner/keysmash-qwerty-asdf.php

### AI writing tells
- Wikipedia: Signs of AI writing. https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- Wikipedia: Signs of AI use in comments. https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_use_in_comments
- Russell, Karpinska, Iyyer (ACL 2025). PEER. https://arxiv.org/abs/2501.15654 ; https://aclanthology.org/2025.acl-long.267
- Reinhart et al. (2025), PNAS. PEER. https://arxiv.org/abs/2410.16107
- Pagan, Tornberg, Bail, Hannak, Barrie (2025), Computational Turing test. PREPRINT. https://arxiv.org/abs/2511.04195
- Dawkins, Fraser, Kiritchenko (2025), When detection fails. PREPRINT. https://arxiv.org/abs/2506.09975
- Jakesch, Hancock, Naaman (2023), PNAS. PEER. https://doi.org/10.1073/pnas.2208839120 ; https://arxiv.org/abs/2206.07271
- Washington Post analysis (13 Nov 2025) via Boston Globe. PRESS. https://www.bostonglobe.com/2025/11/13/business/chatgpt-writing-style-clues/
- Economist study of AI writing (2026) via secondary summary. PRESS. https://biznews.com/tech/spot-ai-written-text
- Ars Technica (14 Nov 2025) on em dash instruction handling. PRESS. https://arstechnica.com/ai/2025/11/forget-agi-sam-altman-celebrates-chatgpt-finally-following-em-dash-formatting-rules/
- Kriss, NYT Magazine (3 Dec 2025), cited by Wikipedia, not read (paywalled). https://www.nytimes.com/2025/12/03/magazine/chatbot-writing-style.html
- anthropics/claude-code issue 3382. https://github.com/anthropics/claude-code/issues/3382 ; The Register https://www.theregister.com/2025/08/13/claude_codes_copious_coddling_confounds/
- OpenAI, Expanding on sycophancy (2025). https://openai.com/index/expanding-on-sycophancy/
- Singhal, Goyal, Xu, Durrett (COLM 2024), A long way to go: length correlations in RLHF. PEER. https://arxiv.org/abs/2310.03716
- Westerman, Cross, Lindmark (2018), Communication Studies. PEER. https://doi.org/10.1080/10510974.2018.1557233
- Bluvstein, Zhao, Barasch, Schroeder (2024), JACR, via Berkeley Haas. PEER. https://newsroom.haas.berkeley.edu/research/to-err-is-human-and-in-the-age-of-ai-it-may-be-humanizing/
- Discord Unveiled dataset (2025). PREPRINT. https://arxiv.org/abs/2502.00627
