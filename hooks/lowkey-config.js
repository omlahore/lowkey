// Shared helpers for the lowkey hooks: where state lives, which levels exist,
// and how to read the ruleset out of SKILL.md for one level.

const fs = require('fs');
const os = require('os');
const path = require('path');

const LEVELS = ['auto', 'lite', 'full', 'brainrot'];
const DEFAULT_LEVEL = 'auto';

function claudeDir() {
  return process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), '.claude');
}

function flagPath() {
  return path.join(claudeDir(), '.lowkey-mode');
}

function voicePath() {
  return path.join(claudeDir(), 'lowkey', 'voice.md');
}

function isMode(m) {
  return m === 'off' || LEVELS.includes(m);
}

function defaultMode() {
  const env = (process.env.LOWKEY_DEFAULT_MODE || '').trim().toLowerCase();
  return isMode(env) ? env : DEFAULT_LEVEL;
}

function readMode() {
  try {
    const m = fs.readFileSync(flagPath(), 'utf8').trim().toLowerCase();
    return isMode(m) ? m : null;
  } catch (e) {
    return null;
  }
}

// Write to a temp file and rename over the flag, so a symlink planted at the
// flag path is replaced rather than followed.
function writeMode(mode) {
  const p = flagPath();
  try {
    fs.mkdirSync(path.dirname(p), { recursive: true });
    const tmp = `${p}.${process.pid}.tmp`;
    fs.writeFileSync(tmp, mode);
    fs.renameSync(tmp, p);
  } catch (e) {
    // best effort, a hook must never fail the session
  }
}

function skillPath() {
  const candidates = [];
  if (process.env.CLAUDE_PLUGIN_ROOT) {
    candidates.push(path.join(process.env.CLAUDE_PLUGIN_ROOT, 'skills', 'lowkey', 'SKILL.md'));
  }
  candidates.push(path.join(__dirname, '..', 'skills', 'lowkey', 'SKILL.md'));
  return candidates.find((c) => fs.existsSync(c)) || null;
}

// SKILL.md marks level-specific blocks with <!-- level: a, b --> ... <!-- /level -->.
// Keep the blocks that list the active level, drop the others and the frontmatter.
function rulesFor(level, skillText) {
  const body = skillText.replace(/^---\n[\s\S]*?\n---\n/, '');
  const out = [];
  let keep = true;
  for (const line of body.split('\n')) {
    const open = line.match(/^<!--\s*level:\s*([a-z, ]+?)\s*-->$/);
    if (open) {
      keep = open[1].split(/[\s,]+/).includes(level);
      continue;
    }
    if (/^<!--\s*\/level\s*-->$/.test(line)) {
      keep = true;
      continue;
    }
    if (keep) out.push(line);
  }
  return out.join('\n').replace(/\n{3,}/g, '\n\n').trim();
}

function voiceProfile() {
  try {
    const v = fs.readFileSync(voicePath(), 'utf8').trim();
    return v ? v : '';
  } catch (e) {
    return '';
  }
}

function fullRuleset(level) {
  const p = skillPath();
  if (!p) return '';
  let text = `LOWKEY ACTIVE, level: ${level}\n\n${rulesFor(level, fs.readFileSync(p, 'utf8'))}`;
  const examples = path.join(path.dirname(p), 'examples.md');
  if (fs.existsSync(examples)) text = text.replace('`examples.md` next to this file', `\`${examples}\``);
  const voice = voiceProfile();
  if (voice) {
    text += `\n\n## The user's own voice (wins over the defaults above)\n\n${voice}`;
  }
  return text;
}

function readStdin() {
  try {
    if (process.stdin.isTTY) return {};
    const raw = fs.readFileSync(0, 'utf8');
    return raw ? JSON.parse(raw) : {};
  } catch (e) {
    return {};
  }
}

module.exports = {
  LEVELS,
  claudeDir,
  defaultMode,
  flagPath,
  fullRuleset,
  isMode,
  readMode,
  readStdin,
  rulesFor,
  voicePath,
  writeMode,
};
