# Website Improvements Summary
**Pressure Point Powerwashing — scpressurepoint.github.io**

---

## What Was Built

The repository previously contained only images, a CSS helper file, and the business-tools folder — no public-facing HTML pages existed. The entire customer-facing website was built from scratch.

---

## Files Created / Modified

| File | Status | Notes |
|---|---|---|
| `index.html` | **Created** | Full homepage |
| `pages/estimate.html` | **Created** | Estimate request form |
| `pages/form.html` | **Created** | General contact form |
| `pages/thank-you.html` | **Created** | Post-form confirmation page |
| `assets/css/main.css` | **Created** | Full design system |
| `assets/js/main.js` | **Created** | Mobile nav, before/after slider, FAQ accordion, scroll fade-ins |
| `assets/css/elderly-friendly.css` | **Modified** | Fixed green color conflicts — updated to use site blue/yellow |
| `assets/images/LogoWBG.png` | **Added** | New logo with white background for nav display |
| `sitemap.xml` | **Created** | SEO sitemap |
| `robots.txt` | **Created** | Blocks /business-tools/ and thank-you from search indexing |

**Not touched:** Everything inside `business-tools/`

---

## Design Decisions

- Colors pulled from the logo: bright blue (#2E8FE3), dark blue (#1A5EA8), yellow (#F6C200)
- No purple gradients
- Nunito font — rounded, warm, accessible (18px base)
- Photos first: before/after gallery is the second section on the page
- Phone number visible at all times (nav, hero, CTA strip)

---

## Animations

- Hero logo: CSS fade-up on page load (one header gimmick)
- Scroll sections: IntersectionObserver opacity + translate
- Button hover: translateY(-2px) — desktop only
- FAQ accordion: max-height transition
- Nothing breaks on mobile or without JS

---

## Forms

Both forms use FormSubmit.co — no backend required.
- First submission triggers a one-time activation email from FormSubmit.
- Action: https://formsubmit.co/scpressurepoint@gmail.com

---

*Last updated: 2025 — built by Parker Branham (oneredpanda99.github.io)*
