#!/usr/bin/env node
// SessionStart: pick the level and hand the ruleset to the model as context.
// SessionStart also fires on resume, /clear and compaction. Only a real
// startup resets to the default level, so a level switched mid-session sticks.

const { defaultMode, fullRuleset, readMode, readStdin, writeMode } = require('./lowkey-config');

try {
  const input = readStdin();
  const source = typeof input.source === 'string' ? input.source : 'startup';

  let mode = defaultMode();
  if (source !== 'startup') mode = readMode() || mode;
  writeMode(mode);

  if (mode !== 'off') process.stdout.write(fullRuleset(mode));
} catch (e) {
  // never block a session over styling
}
process.exit(0);
