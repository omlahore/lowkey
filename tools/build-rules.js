#!/usr/bin/env node
// Builds the rule copies other agents read (AGENTS.md, Cursor, Windsurf,
// Cline, Copilot, Kiro, Gemini, Codex) from skills/lowkey/SKILL.md, so there
// is one source of truth. `node tools/build-rules.js --check` exits 1 when a
// copy is stale.

const fs = require('fs');
const path = require('path');
const { rulesFor } = require('../hooks/lowkey-config');

const root = path.join(__dirname, '..');
const skill = fs.readFileSync(path.join(root, 'skills', 'lowkey', 'SKILL.md'), 'utf8');
const plugin = JSON.parse(fs.readFileSync(path.join(root, '.claude-plugin', 'plugin.json'), 'utf8'));
const repo = plugin.repository;

const rules = rulesFor('auto', skill)
  .replace('auto and full (the user typed lowercase):', 'A person (the user typed lowercase, so mirror it):')
  .replace('More by venue: `examples.md` next to this file.', `More by venue: ${repo}/blob/main/skills/lowkey/examples.md`)
  .replace(/ Active every reply until "stop lowkey" or "normal mode"\. Still active if unsure\./, ' Applies to every reply written for people.')
  .replace(/\n\| \*\*(lite|full|brainrot)\*\* \|[^\n]*/g, '')
  .replace(/## Levels\n\n\| level \| does \|\n\|---\|---\|\n\| \*\*auto\*\* \|[^\n]*\n\n/, '');

const description = 'lowkey: write like a person in the conversation, not an assistant. Mirror the thread, drop AI tells, keep code exact.';

const files = {
  'AGENTS.md': `${rules}\n`,
  '.cursor/rules/lowkey.mdc': `---\ndescription: ${description}\nglobs:\nalwaysApply: true\n---\n\n${rules}\n`,
  '.windsurf/rules/lowkey.md': `---\ntrigger: always_on\n---\n\n${rules}\n`,
  '.clinerules/lowkey.md': `${rules}\n`,
  '.github/copilot-instructions.md': `${rules}\n`,
  '.kiro/steering/lowkey.md': `---\ntitle: lowkey, talk like the room\ninclusion: always\n---\n\n${rules}\n`,
  'gemini-extension.json': `${JSON.stringify({
    name: plugin.name,
    version: plugin.version,
    description: plugin.description,
    contextFileName: 'AGENTS.md',
  }, null, 2)}\n`,
  '.codex-plugin/plugin.json': `${JSON.stringify({
    name: plugin.name,
    version: plugin.version,
    description: plugin.description,
    author: plugin.author,
    homepage: plugin.homepage,
    repository: plugin.repository,
    license: plugin.license,
    keywords: plugin.keywords,
    skills: './skills/',
    interface: {
      displayName: 'lowkey',
      shortDescription: 'Talk like the room, not like an assistant',
      developerName: plugin.author.name,
      category: 'Productivity',
      capabilities: ['Instructions'],
      websiteURL: plugin.homepage,
      defaultPrompt: ['Use lowkey for this reply.', 'Draft my reply to this review in lowkey.'],
      brandColor: '#b5c858',
      composerIcon: './assets/icon.png',
      logo: './assets/icon.png',
    },
  }, null, 2)}\n`,
  '.agents/plugins/marketplace.json': `${JSON.stringify({
    name: plugin.name,
    interface: { displayName: 'lowkey' },
    plugins: [{
      name: plugin.name,
      source: { source: 'url', url: `${repo}.git`, ref: 'main' },
      policy: { installation: 'AVAILABLE', authentication: 'ON_INSTALL' },
      category: 'Productivity',
    }],
  }, null, 2)}\n`,
};

const check = process.argv.includes('--check');
let stale = [];
for (const [rel, content] of Object.entries(files)) {
  const p = path.join(root, rel);
  const current = fs.existsSync(p) ? fs.readFileSync(p, 'utf8') : null;
  if (current === content) continue;
  if (check) {
    stale.push(rel);
  } else {
    fs.mkdirSync(path.dirname(p), { recursive: true });
    fs.writeFileSync(p, content);
    console.log(`wrote ${rel}`);
  }
}
if (stale.length) {
  console.error(`stale, run node tools/build-rules.js: ${stale.join(', ')}`);
  process.exit(1);
}
