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

  /* Touch — detect direction before acting.
     Horizontal gesture: move the slider (preventDefault to stop scroll).
     Vertical gesture:   do nothing, let the browser scroll normally.     */
  let touchStartX = 0;
  let touchStartY = 0;
  let touchDir    = null; // 'h' | 'v' | null

  wrap.addEventListener('touchstart', e => {
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;
    touchDir    = null;
    dragging    = false;
  }, { passive: true });

  wrap.addEventListener('touchmove', e => {
    const dx = e.touches[0].clientX - touchStartX;
    const dy = e.touches[0].clientY - touchStartY;

    if (touchDir === null) {
      if (Math.abs(dx) < 4 && Math.abs(dy) < 4) return; // too small to judge yet
      touchDir = Math.abs(dx) > Math.abs(dy) ? 'h' : 'v';
      if (touchDir === 'h') dragging = true;
    }

    if (touchDir === 'h') {
      e.preventDefault(); // block scroll only while dragging horizontally
      setPos(pctFromX(e.touches[0].clientX));
    }
  }, { passive: false });

  window.addEventListener('touchend', () => {
    dragging = false;
    touchDir = null;
  }, { passive: true });
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
