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

/* ---- Scroll Reveals (staggered + variants) ---- */
const prefersReducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

function getStaggerDelay(el) {
  if (el.dataset.delay) return Number(el.dataset.delay) || 0;
  const group = el.closest('[data-stagger]');
  if (!group) return 0;
  const items = Array.from(group.querySelectorAll('.fade-in'));
  const idx = Math.max(0, items.indexOf(el));
  const step = Number(group.dataset.staggerStep || 70);
  const max = Number(group.dataset.staggerMax || 420);
  return Math.min(idx * step, max);
}

function reveal(el) {
  const delay = getStaggerDelay(el);
  el.style.transitionDelay = delay ? `${delay}ms` : '0ms';
  el.classList.add('visible');
}

if (prefersReducedMotion) {
  document.querySelectorAll('.fade-in').forEach(el => el.classList.add('visible'));
} else {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        reveal(e.target);
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -10% 0px' });

  document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
}

/* ---- Rolling Reviews Marquee ----
   Add reviews in HTML as <div class="review-card" data-review>...</div>
   We'll duplicate the cards for a seamless loop and compute a slow duration. */
function initReviewsMarquee() {
  const marquee = document.querySelector('.reviews-marquee');
  if (!marquee) return;
  const track = marquee.querySelector('[data-reviews-track]');
  if (!track) return;
  const originals = Array.from(track.querySelectorAll('[data-review]'));
  if (originals.length < 2) return;

  // Measure original width before cloning
  const originalWidth = track.scrollWidth;
  const containerWidth = marquee.clientWidth || 1;

  // Clone enough to cover at least 2x the viewport
  let safety = 0;
  while (track.scrollWidth < containerWidth * 2.2 && safety < 12) {
    originals.forEach(node => track.appendChild(node.cloneNode(true)));
    safety += 1;
  }

  // Distance to travel equals the original set width
  const distance = originalWidth || track.scrollWidth / 2;

  // Speed: px per second (lower is slower)
  const pxPerSec = 22; // smooth, slow
  const duration = Math.max(28, Math.round(distance / pxPerSec));

  track.style.setProperty('--reviews-distance', `${distance}px`);
  track.style.setProperty('--reviews-duration', `${duration}s`);
}

initReviewsMarquee();
window.addEventListener('resize', () => {
  // Re-run after resize for consistent loop
  // (simple debounce)
  clearTimeout(window.__ppReviewsResize);
  window.__ppReviewsResize = setTimeout(() => {
    const marquee = document.querySelector('.reviews-marquee');
    const track = marquee && marquee.querySelector('[data-reviews-track]');
    if (!marquee || !track) return;
    // Reset to originals (first N) if we can detect duplicates
    // Easiest: reload by removing all clones beyond first set length
    const originals = Array.from(track.querySelectorAll('[data-review]'));
    if (originals.length) {
      // Keep only the first block of reviews up to the first repeated author+text set
      // Practical: keep first 12 nodes to avoid ballooning if resized repeatedly
      const keep = Math.min(12, originals.length);
      track.innerHTML = '';
      originals.slice(0, keep).forEach(n => track.appendChild(n));
    }
    initReviewsMarquee();
  }, 220);
});

// Note: No scroll snapping / scroll capture / scroll spy.
// Only reveal animations are applied to keep scrolling feeling natural.
