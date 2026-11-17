/* SC Pressure Point — Main JS */

/* Nav: subtle shrink on scroll */
(function initNavScroll() {
  const nav = document.querySelector('.nav');
  if (!nav) return;
  const onScroll = () => nav.classList.toggle('nav--scrolled', window.scrollY > 20);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
})();

/* Sticky mobile CTA bar (homepage + pages using main.css) */
(function initMobileCtaBar() {
  const bar = document.getElementById('mobile-cta-bar');
  if (!bar) return;
  document.body.classList.add('has-mobile-cta');
})();

/* ---- Mobile Nav Toggle ---- */
const hamburger = document.getElementById('nav-hamburger');
const drawer    = document.getElementById('nav-drawer');
if (hamburger && drawer) {
  hamburger.setAttribute('aria-controls', 'nav-drawer');
  hamburger.setAttribute('aria-expanded', 'false');

  const setDrawer = (open) => {
    drawer.classList.toggle('open', open);
    hamburger.setAttribute('aria-expanded', String(open));
    hamburger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  };

  hamburger.addEventListener('click', () => {
    setDrawer(!drawer.classList.contains('open'));
  });
  // Close drawer when a link is clicked
  drawer.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => setDrawer(false));
  });
  // Close drawer on Escape, returning focus to the toggle
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && drawer.classList.contains('open')) {
      setDrawer(false);
      hamburger.focus();
    }
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
  wrap._setPos = setPos;
  const markTouched = () => { wrap._touched = true; wrap.classList.remove('is-hinting'); };
  wrap.addEventListener('mousedown', markTouched);
  wrap.addEventListener('touchstart', markTouched, { passive: true });

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
  const pxPerSec = 60; // smooth, slow
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

/* Form submit: loading state */
document.querySelectorAll('form').forEach(form => {
  form.addEventListener('submit', () => {
    const btn = form.querySelector('button[type="submit"]');
    if (!btn || btn.classList.contains('is-loading')) return;
    if (!btn.querySelector('.btn-label')) {
      const label = document.createElement('span');
      label.className = 'btn-label';
      label.innerHTML = btn.innerHTML;
      btn.textContent = '';
      btn.appendChild(label);
    }
    btn.classList.add('is-loading');
    btn.setAttribute('aria-busy', 'true');
  });
});

// Note: No scroll snapping / scroll capture / scroll spy.
// Only reveal animations are applied to keep scrolling feeling natural.

/* ---- Image modal helpers (shared) ---- */

function openModal(arg1, arg2) {
  // Backwards-compatible: open modal by id (business-tools) or open image modal via src, alt
  if (typeof arg1 === 'string' && document.getElementById(arg1) && !arg2) {
    const el = document.getElementById(arg1);
    el.removeAttribute('hidden');
    el.classList.add('active');
    return;
  }

  // image modal (src, alt)
  const src = arg1, alt = arg2;
  const modal = document.getElementById('imageModal');
  const modalImage = document.getElementById('modalImage');
  const modalCaption = document.getElementById('modalCaption');
  if (!modal) return;
  modal.classList.add('image-modal-open');
  modalImage.src = src;
  modalImage.alt = alt || '';
  modalCaption.textContent = alt || '';
  document.body.style.overflow = 'hidden';
}

function closeModal(eventOrId) {
  // close by id (business-tools)
  if (typeof eventOrId === 'string') {
    const el = document.getElementById(eventOrId);
    if (!el) return;
    el.setAttribute('hidden', '');
    el.classList.remove('active');
    return;
  }

  // event or direct call: image modal
  if (eventOrId && eventOrId.target && eventOrId.target.id && eventOrId.target.id !== 'imageModal') return;
  const modal = document.getElementById('imageModal');
  if (!modal) return;
  modal.classList.remove('image-modal-open');
  document.body.style.overflow = 'auto';
}

document.addEventListener('keydown', function(event) {
  if (event.key === 'Escape') closeModal();
});

/* ============================================================
   MOTION LAYER: ticker loop, slider hint sweep, stat count-up
   ============================================================ */
(function () {
  const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Ticker: duplicate the items once so translateX(-50%) loops seamlessly */
  document.querySelectorAll('[data-ticker]').forEach(track => {
    if (reduce) return;
    Array.from(track.children).forEach(item => {
      const clone = item.cloneNode(true);
      clone.setAttribute('aria-hidden', 'true');
      clone.querySelectorAll('a').forEach(a => a.setAttribute('tabindex', '-1'));
      track.appendChild(clone);
    });
    // ~60px per second regardless of how much text there is
    track.style.setProperty('--ticker-dur', Math.max(20, track.scrollWidth / 2 / 60) + 's');
  });

  if (reduce || !('IntersectionObserver' in window)) return;

  /* Before/after sliders: one gentle sweep the first time each comes into view,
     so visitors see the photos are draggable. Skipped if they already touched it. */
  const sweep = (wrap) => {
    if (!wrap._setPos || wrap._touched) return;
    wrap.classList.add('is-hinting');
    const steps = [[72, 250], [28, 950], [50, 1650]];
    steps.forEach(([pct, at]) => setTimeout(() => { if (!wrap._touched) wrap._setPos(pct); }, at));
    setTimeout(() => wrap.classList.remove('is-hinting'), 2400);
  };
  const sliderObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      sliderObs.unobserve(e.target);
      const i = Array.from(document.querySelectorAll('.ba-wrap')).indexOf(e.target);
      setTimeout(() => sweep(e.target), 350 + (i % 2) * 200);
    });
  }, { threshold: 0.6 });
  document.querySelectorAll('.ba-wrap').forEach(w => sliderObs.observe(w));

  /* Stat numbers count up when they scroll in */
  const countObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      countObs.unobserve(e.target);
      const el = e.target;
      const to = Number(el.dataset.countTo);
      const suffix = el.dataset.countSuffix || '';
      const dur = 1100;
      const t0 = performance.now();
      const tick = (now) => {
        const p = Math.min(1, (now - t0) / dur);
        const eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(to * eased) + suffix;
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    });
  }, { threshold: 0.6 });
  document.querySelectorAll('[data-count-to]').forEach(el => countObs.observe(el));
})();
