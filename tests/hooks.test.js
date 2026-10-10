const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');

const root = path.join(__dirname, '..');
const { rulesFor } = require('../hooks/lowkey-config');
const { parse } = require('../hooks/lowkey-mode');
const skill = fs.readFileSync(path.join(root, 'skills', 'lowkey', 'SKILL.md'), 'utf8');

function run(hook, input, env = {}) {
  return execFileSync(process.execPath, [path.join(root, 'hooks', hook)], {
    input: JSON.stringify(input),
    env: { ...process.env, ...env },
    encoding: 'utf8',
  });
}

function tmpConfig() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'lowkey-'));
}

test('rulesFor keeps only the active level blocks and drops frontmatter', () => {
  const lite = rulesFor('lite', skill);
  assert.match(lite, /^# lowkey/);
  assert.match(lite, /\nlite:\n/);
  assert.doesNotMatch(lite, /auto and full/);
  assert.doesNotMatch(lite, /\nbrainrot:\n/);
  assert.doesNotMatch(lite, /<!--/);

  for (const level of ['auto', 'full']) {
    const out = rulesFor(level, skill);
    assert.match(out, /\nauto and full/);
    assert.doesNotMatch(out, /\nlite:\n/);
    assert.doesNotMatch(out, /\nbrainrot:\n/);
  }

  const rot = rulesFor('brainrot', skill);
  assert.match(rot, /\nbrainrot:\n/);
  assert.doesNotMatch(rot, /\nlite:\n/);
});

test('SKILL.md stays under 4 KB, it is injected every session', () => {
  assert.ok(Buffer.byteLength(skill) < 4096, `${Buffer.byteLength(skill)} bytes`);
});

test('the skill never uses the punctuation it bans', () => {
  assert.doesNotMatch(skill, /[–—]/);
});

test('parse reads slash commands, envelopes and plain phrases', () => {
  assert.equal(parse('/lowkey lite'), 'lite');
  assert.equal(parse('/lowkey'), 'auto');
  assert.equal(parse('/lowkey off'), 'off');
  assert.equal(parse('/lowkey:lowkey brainrot'), 'brainrot');
  assert.equal(parse('/lowkey banana'), null);
  assert.equal(parse('<command-name>/lowkey</command-name>\n<command-args>lite</command-args>'), 'lite');
  assert.equal(parse('<command-name>/caveman</command-name><command-args>stop lowkey</command-args>'), null);
  assert.equal(parse('ok stop lowkey for now'), 'off');
  assert.equal(parse('back to normal mode please'), 'off');
  assert.equal(parse('fix the flaky test in ci'), null);
});

test('session start emits the ruleset for the default level', () => {
  const dir = tmpConfig();
  const out = run('lowkey-activate.js', { source: 'startup' }, { CLAUDE_CONFIG_DIR: dir, LOWKEY_DEFAULT_MODE: '' });
  assert.match(out, /^LOWKEY ACTIVE, level: auto/);
  assert.match(out, /\nauto and full/);
  assert.doesNotMatch(out, /\nbrainrot:\n/);
  assert.equal(fs.readFileSync(path.join(dir, '.lowkey-mode'), 'utf8'), 'auto');
});

test('session start respects LOWKEY_DEFAULT_MODE=off', () => {
  const dir = tmpConfig();
  const out = run('lowkey-activate.js', { source: 'startup' }, { CLAUDE_CONFIG_DIR: dir, LOWKEY_DEFAULT_MODE: 'off' });
  assert.equal(out, '');
});

test('resume and compaction keep a level switched mid-session', () => {
  const dir = tmpConfig();
  fs.writeFileSync(path.join(dir, '.lowkey-mode'), 'lite');
  const out = run('lowkey-activate.js', { source: 'compact' }, { CLAUDE_CONFIG_DIR: dir });
  assert.match(out, /^LOWKEY ACTIVE, level: lite/);
});

test('a voice profile is appended after the defaults', () => {
  const dir = tmpConfig();
  fs.mkdirSync(path.join(dir, 'lowkey'));
  fs.writeFileSync(path.join(dir, 'lowkey', 'voice.md'), 'says "haha" a lot');
  const out = run('lowkey-activate.js', { source: 'startup' }, { CLAUDE_CONFIG_DIR: dir });
  assert.match(out, /The user's own voice[\s\S]*says "haha" a lot/);
});

test('prompt hook switches levels, reminds every turn, and goes quiet when off', () => {
  const dir = tmpConfig();
  const env = { CLAUDE_CONFIG_DIR: dir };
  fs.writeFileSync(path.join(dir, '.lowkey-mode'), 'full');

  const ctx = (out) => JSON.parse(out).hookSpecificOutput.additionalContext;

  assert.match(ctx(run('lowkey-mode.js', { prompt: 'why is ci red' }, env)), /^LOWKEY ACTIVE \(full\)/);

  assert.match(ctx(run('lowkey-mode.js', { prompt: '/lowkey lite' }, env)), /^LOWKEY ACTIVE, level: lite/);
  assert.equal(fs.readFileSync(path.join(dir, '.lowkey-mode'), 'utf8'), 'lite');

  assert.match(ctx(run('lowkey-mode.js', { prompt: 'stop lowkey' }, env)), /write normally/);
  assert.equal(run('lowkey-mode.js', { prompt: 'next question' }, env), '');

  assert.equal(run('lowkey-mode.js', { prompt: '<scheduled-task name="x">/lowkey brainrot' }, env), '');
  assert.equal(fs.readFileSync(path.join(dir, '.lowkey-mode'), 'utf8'), 'off');
});

test('hooks survive garbage on stdin', () => {
  const dir = tmpConfig();
  for (const hook of ['lowkey-activate.js', 'lowkey-mode.js']) {
    execFileSync(process.execPath, [path.join(root, 'hooks', hook)], {
      input: '{not json',
      env: { ...process.env, CLAUDE_CONFIG_DIR: dir },
    });
  }
});

test('rule copies for other agents match SKILL.md', () => {
  execFileSync(process.execPath, [path.join(root, 'tools', 'build-rules.js'), '--check']);
});
