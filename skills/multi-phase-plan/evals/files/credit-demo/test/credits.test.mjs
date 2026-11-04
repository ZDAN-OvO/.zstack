import test from 'node:test';
import assert from 'node:assert/strict';
import { issue, state } from '../credits.mjs';
test('issues positive credits', () => {
  state.balance = 0; state.entries = [];
  assert.deepEqual(issue(10), { balance: 10, entries: 1 });
});
test('rejects invalid credits', () => assert.throws(() => issue(0), /invalid/));
