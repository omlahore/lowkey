#!/usr/bin/env node
// UserPromptSubmit: notice level switches (/lowkey lite, "stop lowkey", ...),
// remember them, and give the model a one-line reminder every turn so the
// style doesn't drift after a long session.

const { LEVELS, fullRuleset, readMode, defaultMode, readStdin, writeMode } = require('./lowkey-config');

const OFF = /\b(stop lowkey|lowkey off|turn off lowkey|disable lowkey|normal mode)\b/;
const ON = /\b(lowkey on|start lowkey|enable lowkey|lowkey mode)\b/;

// Returns the requested mode, or null when the prompt doesn't change it.
function parse(prompt) {
  let p = prompt.trim().toLowerCase().replace(/\s+/g, ' ');

  // Slash commands arrive wrapped: <command-name>/lowkey</command-name><command-args>lite</command-args>
  const name = /<command-name>\s*([^<\s]+)\s*<\/command-name>/.exec(p);
  if (name) {
    if (!/^\/lowkey(:lowkey)?$/.test(name[1])) return null;
    const args = /<command-args>\s*([^<]*?)\s*<\/command-args>/.exec(p);
    p = `/lowkey ${args ? args[1] : ''}`.trim();
  }

  const slash = /^\/lowkey(?::lowkey)?(?:\s+(\S+))?\s*$/.exec(p);
  if (slash) {
    const arg = slash[1] || 'auto';
    if (arg === 'off' || arg === 'stop') return 'off';
    return LEVELS.includes(arg) ? arg : null;
  }
  if (name) return null;
  if (OFF.test(p)) return 'off';
  if (ON.test(p)) {
    const cur = readMode();
    return cur && cur !== 'off' ? cur : 'auto';
  }
  return null;
}

const STYLE = {
  auto: 'mirror the person or thread you are answering (case, end punctuation, length, emoji), work register on GitHub and Slack, chat register in DMs',
  lite: 'work register: sentence case, contractions, short, at most one emoji',
  full: 'chat register: lowercase starts, no full stop at line ends, a line per thought, one or two emojis',
  brainrot: 'chat register plus real slang and 💀 😭, never with strangers',
};

function reminder(mode) {
  return `LOWKEY ACTIVE (${mode}): ${STYLE[mode]}. Answer first and short. No em dashes, no assistant openers or closers, no headers or bullets in chat. Code and identifiers stay exact. Plain careful sentences for warnings and destructive steps.`;
}

function main() {
  const input = readStdin();
  const prompt = typeof input.prompt === 'string' ? input.prompt : '';
  if (/<scheduled-task\b/i.test(prompt)) return;

  const before = readMode() || defaultMode();
  const asked = parse(prompt);
  const mode = asked || before;
  if (asked && asked !== before) writeMode(asked);

  let context;
  if (mode === 'off') {
    if (before === 'off') return;
    context = 'lowkey is off now. write normally again.';
  } else if (asked && before !== mode) {
    context = fullRuleset(mode) || reminder(mode);
  } else {
    context = reminder(mode);
  }

  process.stdout.write(JSON.stringify({
    hookSpecificOutput: { hookEventName: 'UserPromptSubmit', additionalContext: context },
  }));
}

if (require.main === module) {
  process.stdin.on('error', () => process.exit(0));
  try {
    main();
  } catch (e) {
    // never block a prompt over styling
  }
  process.exit(0);
}

module.exports = { parse };
