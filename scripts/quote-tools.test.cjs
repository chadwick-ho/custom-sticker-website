const test = require('node:test');
const assert = require('node:assert/strict');
const { calculateLabelFit, formatInquiryBrief } = require('../custom-labels-stickers-website/assets/js/quote-tools.js');
const sample = { unit: 'mm', diameter: 20, wall: 30, clearance: 1, seam: 2, mode: 'gap' };

test('round bottle uses circumference minus gap and two clearances', () => {
  const fit = calculateLabelFit(sample);
  assert.equal(fit.width, Math.PI * 20 - 2);
  assert.equal(fit.height, 28);
});

test('overlap adds material instead of subtracting it', () => {
  assert.equal(calculateLabelFit({ ...sample, mode: 'overlap' }).width, Math.PI * 20 + 2);
});

test('inch inputs produce the same physical dimensions', () => {
  const inch = { ...sample, unit: 'in' };
  for (const key of ['diameter', 'wall', 'clearance', 'seam']) inch[key] /= 25.4;
  const mmFit = calculateLabelFit(sample);
  const inchFit = calculateLabelFit(inch);
  assert.ok(Math.abs(mmFit.width - inchFit.width) < 1e-10);
  assert.ok(Math.abs(mmFit.height - inchFit.height) < 1e-10);
});

test('invalid measurements do not produce a usable label', () => {
  for (const change of [{diameter: 0}, {diameter: -1}, {wall: 2}, {seam: 70}, {clearance: -1}, {seam: NaN}]) {
    assert.throws(() => calculateLabelFit({ ...sample, ...change }));
  }
});

test('quote brief includes per-design quantity, project stage and copy approval', () => {
  const brief = formatInquiryBrief({ product: 'Supplement Labels', quantity: '500 pcs', skuCount: '3 flavors', orderStage: 'First launch / trial order', copyStatus: 'Draft awaiting buyer approval', email: 'buyer@example.com' });
  assert.match(brief, /Quantity per design: 500 pcs/);
  assert.match(brief, /Number of designs \/ SKUs: 3 flavors/);
  assert.match(brief, /Project stage: First launch \/ trial order/);
  assert.match(brief, /Text \/ code approval: Draft awaiting buyer approval/);
  assert.match(brief, /Reply email: buyer@example.com/);
});
