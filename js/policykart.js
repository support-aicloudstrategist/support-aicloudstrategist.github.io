const form = document.getElementById('policykartForm');
const band = document.getElementById('resultBand');
const message = document.getElementById('resultMessage');
const scoreValue = document.getElementById('scoreValue');
const gapList = document.getElementById('gapList');
const submitStatus = document.getElementById('submitStatus');
function trackPolicyKartEvent(name, props = {}) {
  if (window.plausible) {
    window.plausible(name, { props });
  }
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const checked = [...form.querySelectorAll('input[type="checkbox"]:checked')];
  const score = checked.reduce((total, item) => total + Number(item.dataset.score || 0), 0);
  const gaps = checked.map((item) => item.dataset.gap).slice(0, 5);
  const formData = new FormData(form);
  const email = String(formData.get('email') || '').trim();
  const website = String(formData.get('website') || '').trim();

  let result = 'Low Immediate Risk';
  let copy = 'Your current answers suggest a simpler readiness profile. Keep your privacy evidence updated and review it as workflows expand.';

  if (score >= 13) {
    result = 'High Readiness Priority';
    copy = 'Your answers indicate that a structured DPDP readiness snapshot would be useful. Prioritize data mapping, rights/grievance workflows, vendor evidence, and breach readiness.';
  } else if (score >= 6) {
    result = 'Medium Readiness Gap';
    copy = 'Your answers suggest meaningful documentation or workflow gaps. A focused review can clarify the priority risks and next actions.';
  }

  band.textContent = result;
  message.textContent = copy;
  scoreValue.textContent = score;
  gapList.innerHTML = '';

  const items = gaps.length ? gaps : ['No major risk indicators selected.'];
  for (const gap of items) {
    const li = document.createElement('li');
    li.textContent = gap;
    gapList.appendChild(li);
  }

  if (!submitStatus) return;

  trackPolicyKartEvent('PolicyKart Result Calculated', {
    band: result,
    score: String(score)
  });

  submitStatus.className = 'form-status';
  if (!email && !website) {
    submitStatus.textContent = 'Result calculated locally. Add a business email or website if you want us to follow up.';
    return;
  }

  submitStatus.textContent = 'Assessment calculated locally. For follow-up, use the Free Business Review form so the request goes through the approved AICS lead pipeline.';
  submitStatus.classList.add('success');
});
