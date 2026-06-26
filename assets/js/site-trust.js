/* Populates trust signals from live Google Business Profile data (cached JSON)
 * with fallbacks from SC_SITE_CONFIG. Updates JSON-LD aggregateRating too. */

(function () {
  const cfg = window.SC_SITE_CONFIG || {};
  const CACHE_KEY = 'sc_gbp_reviews_v1';
  const CACHE_MS = 60 * 60 * 1000; // 1 hour in sessionStorage

  function reviewsDataUrl() {
    if (cfg.googleReviewsDataUrl) return cfg.googleReviewsDataUrl;
    return location.pathname.includes('/pages/')
      ? '../assets/data/google-reviews.json'
      : 'assets/data/google-reviews.json';
  }

  function readCache() {
    try {
      const raw = sessionStorage.getItem(CACHE_KEY);
      if (!raw) return null;
      const parsed = JSON.parse(raw);
      if (!parsed || !parsed.updatedAt) return null;
      const age = Date.now() - new Date(parsed.updatedAt).getTime();
      if (age > CACHE_MS) return null;
      return parsed;
    } catch (_) {
      return null;
    }
  }

  function writeCache(data) {
    try {
      sessionStorage.setItem(CACHE_KEY, JSON.stringify(data));
    } catch (_) { /* ignore quota */ }
  }

  function fallbackStats() {
    return {
      rating: cfg.googleReviewRating != null ? Number(cfg.googleReviewRating) : 5,
      reviewCount: cfg.googleReviewCount != null ? Number(cfg.googleReviewCount) : 5,
      reviewUrl: (cfg.googleReviewUrl || '').trim(),
      source: 'config',
    };
  }

  async function loadLiveStats() {
    const cached = readCache();
    if (cached) return cached;

    try {
      const res = await fetch(reviewsDataUrl(), { cache: 'no-cache' });
      if (!res.ok) throw new Error('fetch failed');
      const data = await res.json();
      if (data && data.rating > 0 && data.reviewCount > 0) {
        writeCache(data);
        return data;
      }
    } catch (_) { /* use fallback */ }

    return fallbackStats();
  }

  function reviewLabel(rating, count) {
    const r = Number(rating).toFixed(1);
    const n = count === 1 ? '1 Review' : count + ' Reviews';
    return r + ' \u2605 on Google \u00b7 ' + n;
  }

  function ratingStars(rating) {
    const value = Math.max(0, Math.min(5, Math.round(Number(rating))));
    return '\u2605'.repeat(value) + (value < 5 ? '\u2606'.repeat(5 - value) : '');
  }

  function applyStats(stats) {
    const rating = stats.rating > 0 ? stats.rating : fallbackStats().rating;
    const count = stats.reviewCount > 0 ? stats.reviewCount : fallbackStats().reviewCount;
    const url = (stats.reviewUrl || cfg.googleReviewUrl || '').trim();
    const label = reviewLabel(rating, count);

    document.querySelectorAll('[data-sc-google-review]').forEach((el) => {
      const html = '<i class="fa-brands fa-google" aria-hidden="true"></i> ' + label;

      if (el.tagName === 'A') {
        if (url) {
          el.href = url;
          el.target = '_blank';
          el.rel = 'noopener';
        }
        el.setAttribute('aria-label', label);
        el.innerHTML = html;
        return;
      }

      if (url) {
        const a = document.createElement('a');
        a.className = el.className;
        a.href = url;
        a.target = '_blank';
        a.rel = 'noopener';
        a.setAttribute('aria-label', label);
        a.innerHTML = html;
        el.replaceWith(a);
      } else {
        el.innerHTML = html;
      }
    });

    document.querySelectorAll('[data-sc-google-rating]').forEach((el) => {
      const display = el.dataset.scGoogleRatingFormat === 'stars'
        ? ratingStars(rating)
        : Number(rating).toFixed(1) + '\u2605';
      el.textContent = display;
      el.setAttribute('aria-label', Number(rating).toFixed(1) + ' out of 5 stars on Google');
    });

    document.querySelectorAll('[data-sc-google-review-count]').forEach((el) => {
      el.textContent = count === 1 ? '1 Review' : count + ' Reviews';
    });

    document.querySelectorAll('[data-sc-google-rating-pill]').forEach((el) => {
      el.innerHTML = '<i class="fa-solid fa-star"></i> ' + Number(rating).toFixed(1) + '-Star Rated';
    });

    document.querySelectorAll('script[type="application/ld+json"]').forEach((script) => {
      try {
        const data = JSON.parse(script.textContent);
        const graphs = data['@graph'] || (data['@type'] ? [data] : []);
        let changed = false;
        graphs.forEach((node) => {
          if (node['@type'] === 'LocalBusiness' && node.aggregateRating) {
            node.aggregateRating.reviewCount = String(count);
            node.aggregateRating.ratingValue = String(rating);
            changed = true;
          }
        });
        if (changed) script.textContent = JSON.stringify(data, null, 2);
      } catch (_) { /* ignore */ }
    });
  }

  document.querySelectorAll('[data-sc-response-promise]').forEach((el) => {
    const promise = (cfg.estimateResponsePromise || '').trim();
    if (promise) el.textContent = promise + '.';
  });

  loadLiveStats().then(applyStats);
})();
