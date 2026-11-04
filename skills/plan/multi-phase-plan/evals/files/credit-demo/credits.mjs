export const state = { balance: 0, entries: [] };
export function issue(credits) {
  if (!Number.isInteger(credits) || credits <= 0) throw new Error('invalid credits');
  state.balance += credits;
  state.entries.push({ credits });
  return { balance: state.balance, entries: state.entries.length };
}
