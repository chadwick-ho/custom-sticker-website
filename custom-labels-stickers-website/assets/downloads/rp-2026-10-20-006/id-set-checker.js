(function () {
  'use strict';
  const states = ['shipped', 'rejected', 'retained', 'unprinted'];
  const lines = value => String(value || '').split(/\r?\n/).map(x => x.trim()).filter(Boolean);
  const duplicates = values => {
    const seen = new Set(), repeated = new Set();
    values.forEach(id => { if (seen.has(id)) repeated.add(id); seen.add(id); });
    return [...repeated];
  };
  function reconcile(input) {
    const allocated = lines(input.allocated), expected = new Set(allocated);
    const groups = Object.fromEntries(states.map(state => [state, lines(input[state])]));
    const all = states.flatMap(state => groups[state]), observed = new Set(all);
    const crossState = [...observed].filter(id => states.filter(state => groups[state].includes(id)).length > 1);
    const report = {
      counts: Object.fromEntries([['allocated', allocated.length], ...states.map(state => [state, groups[state].length])]),
      duplicateAllocated: duplicates(allocated),
      duplicateFinal: duplicates(all),
      crossState,
      missing: [...expected].filter(id => !observed.has(id)),
      unexpected: [...observed].filter(id => !expected.has(id)),
      emptyAllocation: allocated.length === 0
    };
    report.consistent = !report.emptyAllocation && ['duplicateAllocated', 'duplicateFinal', 'crossState', 'missing', 'unexpected'].every(key => report[key].length === 0);
    return report;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = { reconcile };
  if (typeof document === 'undefined') return;
  const demo = bad => ({
    allocated: Array.from({length: 8}, (_, i) => 'DEMO-' + String(i + 1).padStart(4, '0')).join('\n'),
    shipped: (bad ? ['DEMO-0001','DEMO-0001','DEMO-0003','DEMO-0004','DEMO-0005'] : ['DEMO-0001','DEMO-0002','DEMO-0003','DEMO-0004','DEMO-0005']).join('\n'),
    rejected: 'DEMO-0006', retained: 'DEMO-0007', unprinted: 'DEMO-0008'
  });
  const form = document.querySelector('form');
  const result = document.getElementById('result');
  function run() {
    const input = Object.fromEntries(['allocated', ...states].map(key => [key, form.elements[key].value]));
    const report = reconcile(input);
    result.textContent = (report.consistent ? 'Supplied ID sets are internally consistent. Physical shipment and approval still need independent evidence.\n' : 'Resolve the supplied ID-set discrepancies before release.\n') + JSON.stringify(report, null, 2);
  }
  form.addEventListener('submit', event => { event.preventDefault(); run(); });
  for (const [id, bad] of [['valid-example', false], ['duplicate-example', true]]) {
    document.getElementById(id).addEventListener('click', () => {
      for (const [key, value] of Object.entries(demo(bad))) form.elements[key].value = value;
      run();
    });
  }
  document.getElementById('clear').addEventListener('click', () => { form.reset(); result.textContent = 'Cleared. Enter one exact identifier per line.'; });
})();
