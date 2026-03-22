/* Pressure Point Powerwashing — Main JS */

/* ---- Mobile Nav Toggle ---- */
const hamburger = document.getElementById('nav-hamburger');
const drawer    = document.getElementById('nav-drawer');
if (hamburger && drawer) {
  hamburger.addEventListener('click', () => {
    drawer.classList.toggle('open');
  });
  // Close drawer when a link is clicked
  drawer.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => drawer.classList.remove('open'));
  });
}

/* ---- Before/After Sliders ---- */
function initSlider(wrap) {
  const beforePanel = wrap.querySelector('.ba-before');
  const beforeImg   = beforePanel.querySelector('img');
  const divider     = wrap.querySelector('.ba-divider');
  const handle      = wrap.querySelector('.ba-handle');
  let dragging      = false;
  let startPct      = 50;

  /* The before image must always be the full width of the wrap,
     not the clipped panel's width, so it doesn't stretch. */
  function syncImageWidth() {
    const w = wrap.offsetWidth;
    beforeImg.style.width = w + 'px';
  }
  syncImageWidth();
  window.addEventListener('resize', syncImageWidth);

  function setPos(pct) {
    pct = Math.max(2, Math.min(98, pct));
    beforePanel.style.width = pct + '%';
    divider.style.left      = pct + '%';
    handle.style.left       = pct + '%';
  }
  setPos(startPct);

  function pctFromX(clientX) {
    const rect = wrap.getBoundingClientRect();
    return ((clientX - rect.left) / rect.width) * 100;
  }

  /* Mouse */
  wrap.addEventListener('mousedown',   e => { dragging = true; setPos(pctFromX(e.clientX)); });
  window.addEventListener('mousemove', e => { if (dragging) setPos(pctFromX(e.clientX)); });
  window.addEventListener('mouseup',   ()  => { dragging = false; });

  /* Touch */
  wrap.addEventListener('touchstart',  e => { dragging = true; setPos(pctFromX(e.touches[0].clientX)); }, { passive: true });
  window.addEventListener('touchmove', e => { if (dragging) setPos(pctFromX(e.touches[0].clientX)); }, { passive: true });
  window.addEventListener('touchend',  ()  => { dragging = false; });
}
document.querySelectorAll('.ba-wrap').forEach(initSlider);

/* ---- FAQ Accordion ---- */
document.querySelectorAll('.faq-q').forEach(btn => {
  btn.addEventListener('click', () => {
    const item    = btn.parentElement;
    const answer  = item.querySelector('.faq-a');
    const isOpen  = item.classList.contains('open');

    // Close all
    document.querySelectorAll('.faq-item').forEach(i => {
      i.classList.remove('open');
      i.querySelector('.faq-q').setAttribute('aria-expanded', 'false');
      i.querySelector('.faq-a').style.maxHeight = '0';
    });

    // Open clicked (unless it was already open)
    if (!isOpen) {
      item.classList.add('open');
      btn.setAttribute('aria-expanded', 'true');
      answer.style.maxHeight = answer.scrollHeight + 'px';
    }
  });
});

const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      observer.unobserve(e.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
