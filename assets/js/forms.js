/* Quote, estimate & survey forms — Forminit email delivery */

(function () {

  const cfg = window.SC_FORM_CONFIG || {

    forminitFormId: '',

    forminitEstimateFormId: '',

    forminitSurveyFormId: '',

    thankYouPath: 'pages/thank-you.html',

    phone: '8032728118'

  };



  const FORMINIT_SDK = 'https://forminit.com/sdk/v1/forminit.js';



  let sdkPromise = null;



  function thankYouUrl() {

    const path = cfg.thankYouPath || 'pages/thank-you.html';

    if (path.startsWith('http')) return path;

    const onSubpage = /\/pages\//.test(window.location.pathname);

    const rel = onSubpage ? 'thank-you.html' : path;

    return new URL(rel, window.location.href).href;

  }



  function formIdFor(type) {

    if (type === 'estimate') return (cfg.forminitEstimateFormId || cfg.forminitFormId || '').trim();

    if (type === 'survey') return (cfg.forminitSurveyFormId || cfg.forminitFormId || '').trim();

    return (cfg.forminitFormId || '').trim();

  }



  function toE164(phone) {

    const digits = String(phone || '').replace(/\D/g, '');

    if (!digits) return '';

    if (digits.length === 10) return '+1' + digits;

    if (digits.length === 11 && digits.startsWith('1')) return '+' + digits;

    if (String(phone).trim().startsWith('+')) return String(phone).trim();

    return '+' + digits;

  }



  function loadForminitSdk() {

    if (!sdkPromise) {

      sdkPromise = new Promise((resolve, reject) => {

        if (window.Forminit) {

          resolve(new window.Forminit());

          return;

        }

        const script = document.createElement('script');

        script.src = FORMINIT_SDK;

        script.async = true;

        script.onload = () => {

          if (window.Forminit) resolve(new window.Forminit());

          else reject(new Error('Form handler failed to initialize.'));

        };

        script.onerror = () => reject(new Error('Could not load form handler.'));

        document.head.appendChild(script);

      });

    }

    return sdkPromise;

  }



  function clearFormError(form) {

    const existing = form.querySelector('.form-delivery-error');

    if (existing) existing.remove();

  }



  function formatPhoneDisplay(phone) {

    const d = String(phone || '').replace(/\D/g, '');

    if (d.length === 10) return '(' + d.slice(0, 3) + ') ' + d.slice(3, 6) + '-' + d.slice(6);

    return phone || '';

  }



  function showFormError(form, message) {

    clearFormError(form);

    const phone = cfg.phone || '8032728118';

    const tel = phone.replace(/\D/g, '');

    const display = formatPhoneDisplay(phone);

    const el = document.createElement('div');

    el.className = 'form-delivery-error';

    el.setAttribute('role', 'alert');

    el.innerHTML =

      '<p><strong>Something went wrong.</strong> ' + message + '</p>' +

      '<p>Please try again in a moment, or reach us directly: ' +

      '<a href="tel:' + tel + '">call ' + display + '</a> · ' +

      '<a href="sms:' + tel + '">text us</a></p>';

    const anchor = form.querySelector('.form-submit') || form.lastElementChild;

    if (anchor && anchor.parentNode === form) {

      form.insertBefore(el, anchor.nextSibling);

    } else {

      form.appendChild(el);

    }

    el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

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



  function appendText(fd, name, value) {

    const v = value == null ? '' : String(value).trim();

    if (v) fd.append('fi-text-' + name, v);

  }



  function buildForminitData(form, meta) {

    const src = new FormData(form);

    const fd = new FormData();

    const SENDER_KEYS = ['name', 'customer_name', 'email', 'customer_email',

      'phone', 'customer_phone', 'address', 'customer_address',

      'first_name', 'last_name'];



    const full = (src.get('name') || src.get('customer_name') || '').toString().trim();

    const first = (src.get('first_name') || '').toString().trim();

    const last = (src.get('last_name') || '').toString().trim();



    if (full) {

      fd.append('fi-sender-fullName', full);

    } else if (first || last) {

      if (first) fd.append('fi-sender-firstName', first);

      if (last) fd.append('fi-sender-lastName', last);

      const combined = [first, last].filter(Boolean).join(' ').trim();

      if (combined) fd.append('fi-sender-fullName', combined);

    }



    const email = (src.get('email') || src.get('customer_email') || '').toString().trim();

    if (email) fd.append('fi-sender-email', email);



    const phone = toE164(src.get('phone') || src.get('customer_phone'));

    if (phone) fd.append('fi-sender-phone', phone);



    const address = (src.get('address') || src.get('customer_address') || '').toString().trim();

    if (address) fd.append('fi-sender-address', address);



    for (const [key, value] of src.entries()) {

      if (key.startsWith('_') || value instanceof File) continue;

      if (SENDER_KEYS.includes(key)) continue;



      const str = String(value).trim();

      if (!str) continue;



      if (key.endsWith('_rating') || key === 'overall_rating') {

        const num = parseInt(str, 10);

        if (num >= 1 && num <= 5) fd.append('fi-rating-' + key.replace(/_rating$/, ''), String(num));

        else appendText(fd, key, str);

        continue;

      }



      appendText(fd, key, str);

    }



    appendText(fd, 'form_type', meta.formType || 'website');

    if (meta.subject) appendText(fd, 'subject', meta.subject);



    return fd;

  }



  async function submitToForminit(formId, formData) {

    const client = await loadForminitSdk();

    const { data, error } = await client.submit(formId, formData);

    if (error) throw new Error(error.message || 'Submission was rejected.');

    return data;

  }



  async function handleSubmit(form, options) {

    const btn = form.querySelector('button[type="submit"], input[type="submit"]');

    clearFormError(form);

    setSubmitting(btn, true);



    const formId = formIdFor(options.formType || 'quote');

    if (!formId) {

      showFormError(form, 'Form delivery is not configured yet.');

      setSubmitting(btn, false);

      return false;

    }



    try {

      const payload = options.formData || buildForminitData(form, options);

      await submitToForminit(formId, payload);

      window.location.href = thankYouUrl();

      return true;

    } catch (err) {

      showFormError(form, err.message || 'We could not send your message.');

      setSubmitting(btn, false);

      return false;

    }

  }



  document.querySelectorAll('form[data-sc-form]').forEach((form) => {

    form.addEventListener('submit', (e) => {

      e.preventDefault();

      handleSubmit(form, {

        formType: form.dataset.formType || 'quote',

        subject: form.dataset.formSubject || 'SC Pressure Point — Website Form'

      });

    });

  });



  window.SC_submitForm = handleSubmit;

  window.SC_buildForminitData = buildForminitData;

  window.SC_submitToForminit = submitToForminit;

  window.SC_formIdFor = formIdFor;

  window.SC_showFormError = showFormError;

  window.SC_clearFormError = clearFormError;

  window.SC_thankYouUrl = thankYouUrl;

  window.SC_setSubmitting = setSubmitting;

  window.SC_toE164 = toE164;

})();


