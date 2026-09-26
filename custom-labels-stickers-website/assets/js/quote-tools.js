/* Keep geometric estimates independent of the page so units and edge cases can be checked. */
function calculateLabelFit(values) {
  const factor = values.unit === 'in' ? 25.4 : 1;
  const diameter = Number(values.diameter) * factor;
  const wall = Number(values.wall) * factor;
  const clearance = Number(values.clearance) * factor;
  const seam = Number(values.seam) * factor;
  if (![diameter, wall, clearance, seam].every(Number.isFinite) || diameter <= 0 || wall <= 0 || clearance < 0 || seam < 0) {
    throw new Error('Enter positive bottle measurements and non-negative clearance and seam values.');
  }
  const circumference = Math.PI * diameter;
  const width = circumference + (values.mode === 'overlap' ? seam : -seam);
  const height = wall - 2 * clearance;
  if (height <= 0) throw new Error('Top and bottom clearance must leave some usable label height.');
  if (width <= 0) throw new Error('The gap must be smaller than the bottle circumference.');
  return { circumference, width, height };
}

if (typeof module !== 'undefined' && module.exports) module.exports = { calculateLabelFit };

if (typeof document !== 'undefined') {
  const draftKey = 'rp-label-planner-v1';
  const email = 'ruishengmao05@gmail.com';
  function downloadBrief(text) {
    const url = URL.createObjectURL(new Blob([text], { type: 'text/plain;charset=utf-8' }));
    const link = document.createElement('a');
    link.href = url;
    link.download = 'rp-label-quote-brief.txt';
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  async function copyBrief(text, status) {
    try {
      await navigator.clipboard.writeText(text);
      status.textContent = 'Brief copied. Paste it into your email or WhatsApp message.';
    } catch {
      status.textContent = 'Copy is unavailable. Select the brief text or download it instead.';
    }
  }
  const planner = document.querySelector('[data-label-planner]');
  if (planner) {
    planner.querySelector('[type="submit"]').disabled = false;
    const output = document.getElementById('planner-result');
    const error = document.getElementById('planner-error');
    const brief = document.getElementById('planner-brief');
    const status = document.getElementById('planner-status');
    const unit = planner.elements.unit;
    let previousUnit = unit.value;
    unit.addEventListener('change', () => {
      const factor = previousUnit === 'mm' ? 1 / 25.4 : 25.4;
      ['diameter', 'wall', 'clearance', 'seam'].forEach(name => {
        const input = planner.elements[name];
        if (input.value !== '') input.value = String(Number((Number(input.value) * factor).toFixed(4)));
      });
      previousUnit = unit.value;
    });
    planner.addEventListener('input', () => {
      output.hidden = true;
      status.textContent = '';
      error.textContent = '';
    });
    planner.addEventListener('submit', event => {
      event.preventDefault();
      output.hidden = true;
      error.textContent = '';
      try {
        const values = Object.fromEntries(new FormData(planner));
        const fit = calculateLabelFit(values);
        const size = `${fit.width.toFixed(1)} x ${fit.height.toFixed(1)} mm`;
        document.getElementById('fit-width').textContent = `${fit.width.toFixed(1)} mm`;
        document.getElementById('fit-height').textContent = `${fit.height.toFixed(1)} mm`;
        document.getElementById('fit-inch').textContent = `${(fit.width / 25.4).toFixed(3)} x ${(fit.height / 25.4).toFixed(3)} in`;
        document.getElementById('fit-formula').textContent = `Circumference ${fit.circumference.toFixed(2)} mm; width = circumference ${values.mode === 'overlap' ? '+' : '-'} seam. Height = straight wall - 2 x clearance.`;
        brief.value = [
          'RP CUSTOM LABEL QUOTE BRIEF',
          `Product: ${values.product}`, `Quantity: ${values.quantity} pcs`,
          `Bottle outside diameter: ${values.diameter} ${values.unit}`,
          `Straight-wall height: ${values.wall} ${values.unit}`,
          `Top and bottom clearance (each): ${values.clearance} ${values.unit}`,
          `Seam: ${values.seam} ${values.unit} ${values.mode}`,
          `Estimated finished label size: ${size} (geometric estimate; sample fit required)`,
          `Material: ${values.material}`, `Application: ${values.application}`,
          'Please confirm adhesive, material, final dieline, quantity per artwork, roll specs and price.',
          'Source: https://rplabels.com/label-quote-planner'
        ].join('\n');
        output.hidden = false;
        status.textContent = 'Estimated finished label size: ' + size + '. Your quote brief is ready below.';
      } catch (problem) {
        error.textContent = problem.message;
      }
    });
    document.getElementById('planner-copy').addEventListener('click', () => copyBrief(brief.value, status));
    document.getElementById('planner-download').addEventListener('click', () => downloadBrief(brief.value));
    document.getElementById('planner-contact').addEventListener('click', event => {
      try {
        sessionStorage.setItem(draftKey, JSON.stringify({
          product: planner.elements.product.value,
          quantity: planner.elements.quantity.value,
          material: planner.elements.material.value,
          size: document.getElementById('fit-width').textContent + ' x ' + document.getElementById('fit-height').textContent + ' (estimate)',
          application: planner.elements.application.value,
          message: brief.value
        }));
      } catch {
        event.preventDefault();
        status.textContent = 'Browser storage is unavailable. Copy or download the brief, then open Contact from the menu.';
      }
    });
  }

  const inquiry = document.querySelector('[data-inquiry-form]');
  if (inquiry) {
    inquiry.querySelector('[type="submit"]').disabled = false;
    const result = document.getElementById('inquiry-result');
    const brief = document.getElementById('inquiry-brief');
    const status = document.getElementById('inquiry-status');
    try {
      const draft = JSON.parse(sessionStorage.getItem(draftKey) || 'null');
      if (draft && typeof draft === 'object') {
        ['product', 'quantity', 'material', 'size', 'application', 'message'].forEach(name => {
          if (typeof draft[name] === 'string') inquiry.elements[name].value = draft[name];
        });
        sessionStorage.removeItem(draftKey);
      }
    } catch { /* Manual entry remains available when browser storage is disabled. */ }
    inquiry.addEventListener('input', () => {
      result.hidden = true;
      status.textContent = '';
    });
    inquiry.addEventListener('submit', event => {
      event.preventDefault();
      const values = Object.fromEntries(new FormData(inquiry));
      const fields = [['product','Product'],['size','Label size'],['quantity','Quantity'],['material','Material'],['finish','Finish'],['application','Package / application'],['artwork','Artwork status'],['whatsapp','WhatsApp'],['email','Reply email'],['country','Shipping country'],['message','Project details']];
      brief.value = 'RP CUSTOM LABEL INQUIRY\n\n' + fields.map(([name, label]) => `${label}: ${String(values[name] || '').trim() || 'To confirm'}`).join('\n');
      const mail = document.getElementById('inquiry-email');
      const mailto = `mailto:${email}?subject=${encodeURIComponent('Custom label quote: ' + values.product)}&body=${encodeURIComponent(brief.value)}`;
      mail.href = mailto;
      mail.hidden = mailto.length > 1800;
      document.getElementById('inquiry-long').hidden = mailto.length <= 1800;
      result.hidden = false;
      status.textContent = 'Your brief is ready. It has not been sent. Choose email, or copy it and open WhatsApp. Attach artwork in that conversation.';
    });
    document.getElementById('inquiry-copy').addEventListener('click', () => copyBrief(brief.value, status));
    document.getElementById('inquiry-download').addEventListener('click', () => downloadBrief(brief.value));
  }
}
