/* Populates trust signals from SC_SITE_CONFIG (review link, response promise, JSON-LD). */

(function () {
  const cfg = window.SC_SITE_CONFIG || {};
  const rating = cfg.googleReviewRating != null ? Number(cfg.googleReviewRating) : 5;
  const count = cfg.googleReviewCount != null ? Number(cfg.googleReviewCount) : 5;
  const url = (cfg.googleReviewUrl || '').trim();
  const promise = (cfg.estimateResponsePromise || '').trim();

  function reviewLabel() {
    const r = rating.toFixed(1);
    const n = count === 1 ? '1 Review' : count + ' Reviews';
    return r + ' \u2605 on Google \u00b7 ' + n;
  }

  document.querySelectorAll('[data-sc-google-review]').forEach((el) => {
    const label = reviewLabel();
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

  document.querySelectorAll('[data-sc-response-promise]').forEach((el) => {
    if (promise) el.textContent = promise + '.';
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
})();
