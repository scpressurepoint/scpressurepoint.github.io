/* Quote & estimate forms — Web3Forms when configured, SMS fallback otherwise */
(function () {
  const cfg = window.SC_FORM_CONFIG || { phone: '8032728118', thankYouPath: 'pages/thank-you.html', web3formsAccessKey: '' };

  function thankYouUrl() {
    const path = cfg.thankYouPath || 'pages/thank-you.html';
    if (path.startsWith('http')) return path;
    const onSubpage = /\/pages\//.test(window.location.pathname);
    const rel = onSubpage ? 'thank-you.html' : path;
    return new URL(rel, window.location.href).href;
  }

  function labelize(name) {
    return name.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
  }

  function buildSmsBody(form, intro, extraLines) {
    const fd = new FormData(form);
    const lines = [intro, ''];
    for (const [key, value] of fd.entries()) {
      if (key.startsWith('_') || key === 'access_key' || key === 'photos') continue;
      if (value instanceof File) continue;
      if (String(value).trim()) lines.push(`${labelize(key)}: ${value}`);
    }
    if (extraLines && extraLines.length) {
      lines.push('', ...extraLines);
    }
    return encodeURIComponent(lines.join('\n'));
  }

  function openSms(form, intro, extraLines) {
    window.location.href = `sms:${cfg.phone}?&body=${buildSmsBody(form, intro, extraLines)}`;
  }

  async function submitWeb3Forms(form, subject) {
    const key = (cfg.web3formsAccessKey || '').trim();
    if (!key) return false;

    const fd = new FormData(form);
    fd.append('access_key', key);
    fd.append('subject', subject);
    const first = fd.get('first_name') || fd.get('customer_name') || fd.get('name');
    if (first && !fd.get('from_name')) fd.append('from_name', first);

    const res = await fetch('https://api.web3forms.com/submit', { method: 'POST', body: fd });
    if (!res.ok) return false;
    const data = await res.json();
    return !!data.success;
  }

  function setSubmitting(btn, on) {
    if (!btn) return;
    if (on) {
      btn.dataset.prevHtml = btn.innerHTML;
      btn.disabled = true;
      btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>&nbsp; Sending...';
    } else {
      btn.disabled = false;
      if (btn.dataset.prevHtml) btn.innerHTML = btn.dataset.prevHtml;
    }
  }

  async function handleSubmit(form, options) {
    const btn = form.querySelector('button[type="submit"], input[type="submit"]');
    setSubmitting(btn, true);
    try {
      const emailed = await submitWeb3Forms(form, options.subject);
      if (emailed) {
        window.location.href = thankYouUrl();
        return;
      }
    } catch (_) { /* SMS fallback below */ }

    openSms(form, options.smsIntro, options.smsExtra);
    setSubmitting(btn, false);
  }

  document.querySelectorAll('form[data-sc-form]').forEach((form) => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      handleSubmit(form, {
        subject: form.dataset.formSubject || 'SC Pressure Point — Website Form',
        smsIntro: form.dataset.smsIntro || 'Hi SC Pressure Point, I would like a quote:',
        smsExtra: (form.dataset.smsExtra || '').split('|').filter(Boolean)
      });
    });
  });

  window.SC_submitForm = handleSubmit;
})();
