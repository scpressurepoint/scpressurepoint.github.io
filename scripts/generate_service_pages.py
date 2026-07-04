#!/usr/bin/env python3
"""Generate services hub + individual service pages for SC Pressure Point."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERVICES_DIR = ROOT / "services"
PAGES_DIR = ROOT / "pages"

LOCALE_LINKS = """
      <a href="../pressure-washing-columbia-sc.html">Columbia</a>
      <a href="../pressure-washing-lexington-sc.html">Lexington</a>
      <a href="../pressure-washing-irmo-sc.html">Irmo</a>
      <a href="../pressure-washing-west-columbia-sc.html">West Columbia</a>
      <a href="../pressure-washing-forest-acres-sc.html">Forest Acres</a>
      <a href="../pressure-washing-dentsville-sc.html">Dentsville</a>
      <a href="../pressure-washing-blythewood-sc.html">Blythewood</a>
"""

SERVICES = [
    {
        "slug": "driveways",
        "title": "Driveway Pressure Washing",
        "short": "Driveways",
        "icon": "fa-road",
        "description": "Professional driveway pressure washing in Columbia, SC. Oil stains, tire marks, and years of buildup removed from concrete and asphalt.",
        "intro": "Columbia humidity and red clay leave dark algae lines and oil stains on driveways fast. SC Pressure Point restores concrete and asphalt with a measured process: pre-treat, agitate where needed, and rinse without etching the surface.",
        "process": [
            ("Walk-through & quote", "We measure or estimate square footage, note oil stains, expansion joints, and drainage. You get a per-sq-ft price before we start."),
            ("Pre-treatment", "Cleaning solution is applied to break down organic growth, tire marks, and embedded grime. Heavily stained areas get extra dwell time."),
            ("Surface cleaning", "A surface cleaner or appropriate nozzle pattern removes buildup evenly. We adjust pressure for aged or porous concrete."),
            ("Detail & rinse", "Edges, aprons, and garage transitions are finished by hand. We rinse toward drains and confirm even color before we leave."),
        ],
        "pricing_note": "Most driveways: $0.20–$0.40/sq ft. Typical two-car driveway: about $125–$275.",
        "related": ["sidewalks-walkways", "steps-entryways"],
    },
    {
        "slug": "sidewalks-walkways",
        "title": "Sidewalk & Walkway Pressure Washing",
        "short": "Sidewalks & Walkways",
        "icon": "fa-person-walking",
        "description": "Sidewalk and walkway pressure washing in Columbia, SC. Moss, algae, and dirt removed for safer, sharper-looking paths.",
        "intro": "Shaded walkways get slick with algae and moss, especially under tree cover common in Forest Acres, Shandon, and Lexington subdivisions. We clean front walks, side paths, and HOA common areas with the same per-surface pricing you see on our pricing guide.",
        "process": [
            ("Surface check", "We identify slick algae, moss, and uneven pavers or stamped concrete that need lower pressure."),
            ("Plant protection", "Landscaping along the walk is pre-wet and covered when needed before any chemicals are applied."),
            ("Clean & treat", "Solution breaks down organic growth; we use surface-appropriate pressure so mortar and joints stay intact."),
            ("Final rinse", "Walkways are rinsed clear and checked for even brightness from curb to porch."),
        ],
        "pricing_note": "Front walk + steps: often $125–$200 depending on length and buildup.",
        "related": ["driveways", "steps-entryways"],
    },
    {
        "slug": "steps-entryways",
        "title": "Steps & Entryway Pressure Washing",
        "short": "Steps & Entryways",
        "icon": "fa-stairs",
        "description": "Steps and entryway pressure washing in Columbia, SC. First impressions matter — we clean brick, concrete, and stone entryways safely.",
        "intro": "Entry steps collect pollen, mildew, and foot traffic grime faster than flat concrete. We treat brick, concrete, and stone steps with the right pressure and chemistry so mortar and treads stay intact while the entry looks sharp again.",
        "process": [
            ("Material assessment", "Brick, concrete, and natural stone each get a different pressure and chemical plan."),
            ("Pre-soak & apply", "Steps are pre-wet; cleaning solution loosens mildew and ground-in dirt in treads and risers."),
            ("Controlled cleaning", "We work top-to-bottom with fan tips or soft wash methods on delicate brick and mortar."),
            ("Safety check", "Before we leave, steps are rinsed free of residue and checked for even color on all treads."),
        ],
        "pricing_note": "Quoted with your walkway or driveway when possible; standalone entry jobs priced by sq ft.",
        "related": ["sidewalks-walkways", "patios-decks"],
    },
    {
        "slug": "patios-decks",
        "title": "Patio & Deck Pressure Washing",
        "short": "Patios & Decks",
        "icon": "fa-umbrella-beach",
        "description": "Patio and deck pressure washing in Columbia, SC. Concrete, brick, stone, and wood-safe treatments for outdoor living spaces.",
        "intro": "Back patios and pool decks stay wet longer in Midlands humidity, which feeds algae and makes surfaces slippery. We refresh concrete, pavers, brick, and stone patios — and use wood-safe methods when a deck needs cleaning without splintering or furring the grain.",
        "process": [
            ("Layout & furniture", "We confirm what moves off the patio and note paver sand, wood type, or sealed surfaces."),
            ("Pre-treatment", "Organic growth and tannin stains get appropriate dwell time before agitation."),
            ("Surface-appropriate wash", "Concrete and pavers get surface cleaning; wood decks get lower pressure and wood-safe chemistry when applicable."),
            ("Rinse & inspect", "We rinse toward drainage, reset furniture if agreed, and walk the space with you when you are home."),
        ],
        "pricing_note": "Most back patios: about $100–$320 depending on size and condition.",
        "related": ["driveways", "fences"],
    },
    {
        "slug": "house-siding",
        "title": "House Siding Soft Wash",
        "short": "All House Sidings",
        "icon": "fa-house",
        "description": "House siding soft wash in Columbia, SC. Safe cleaning for vinyl, stucco, painted siding, and more — no damage, thorough results.",
        "intro": "Columbia pollen and humidity coat north-facing siding and soffits within a season. SC Pressure Point uses soft wash methods — low pressure at the wall with professional cleaning solution — so vinyl, stucco, fiber cement, and painted siding get clean without the damage high pressure causes.",
        "process": [
            ("Photo-based quote", "Text photos of all elevations. We quote by measurable siding area and note delicate trim or older paint."),
            ("Plant & window prep", "Landscaping is pre-wet and covered; windows and outlets are protected before application."),
            ("Soft wash application", "Cleaning solution is applied from the bottom up, allowed to dwell, then rinsed with low pressure."),
            ("Trim & spot check", "We verify even color on each elevation and touch up tiger stripes or heavy mildew lines as needed."),
        ],
        "pricing_note": "Siding soft wash: $0.20–$0.40/sq ft, quoted after photos.",
        "related": ["soffit-gutters", "windows-ledges"],
    },
    {
        "slug": "soffit-gutters",
        "title": "Soffit & Exterior Gutter Cleaning",
        "short": "Soffit & Exterior Gutters",
        "icon": "fa-water",
        "description": "Soffit and exterior gutter cleaning in Columbia, SC. Tiger stripes, mold, and grime removed from gutters and soffits.",
        "intro": "Overflow streaks and mildew on soffits make a home look older than it is. We brighten exterior gutter faces and clean soffits with methods matched to your material — not the high-pressure blasting that dents aluminum or forces water behind fascia.",
        "process": [
            ("Access plan", "We confirm ladder points or extension reach for second-story runs and note fragile sections."),
            ("Apply & dwell", "Cleaning solution breaks down tiger stripes, mildew, and pollen on gutter exteriors and soffit panels."),
            ("Low-pressure rinse", "Gutters and soffits are rinsed with controlled pressure to avoid forcing water behind trim."),
            ("Final pass", "We check for remaining streaks on downspouts and corners visible from the street."),
        ],
        "pricing_note": "Often bundled with siding soft wash; standalone runs quoted after photos.",
        "related": ["house-siding", "windows-ledges"],
    },
    {
        "slug": "fences",
        "title": "Fence Pressure Washing",
        "short": "Fences",
        "icon": "fa-border-all",
        "description": "Fence pressure washing in Columbia, SC. Wood, vinyl, and aluminum fences cleaned — black streaks, mildew, and weathering removed.",
        "intro": "Fence lines under trees pick up green mildew and black streaks that age the whole yard. We clean wood, vinyl, and aluminum fencing with pressure and chemistry matched to the material so boards and panels brighten without gouging or warping.",
        "process": [
            ("Material ID", "Wood, vinyl, and aluminum each need different pressure limits and cleaning approach."),
            ("Pre-treat", "Mildew and organic growth are treated along rails, posts, and pickets."),
            ("Even pass", "We work in consistent sections so color evens out without lap marks on long runs."),
            ("Rinse & review", "Fence lines are rinsed and checked from multiple angles for missed panels."),
        ],
        "pricing_note": "Quoted by linear feet or total surface area after photos.",
        "related": ["patios-decks", "driveways"],
    },
    {
        "slug": "windows-ledges",
        "title": "Window & Ledge Washing",
        "short": "Windows & Ledges",
        "icon": "fa-window-maximize",
        "description": "Exterior window and ledge washing in Columbia, SC. Streak-free glass and clean ledges — great paired with siding or porch work.",
        "intro": "Pollen and mildew collect on window ledges and frames even when the glass still looks okay from inside. We wash exterior glass and ledges for a streak-free finish, often bundled with siding soft wash or porch cleaning for a full front-elevation refresh.",
        "process": [
            ("Scope check", "We confirm which windows, ledges, and frames are included and note second-story reach."),
            ("Frame & ledge prep", "Ledges and sills are cleaned of pollen, webs, and mildew before glass work."),
            ("Glass wash", "Exterior panes are washed with appropriate tools for streak-free results."),
            ("Final detail", "We wipe drips from frames and confirm sight lines from the street and driveway."),
        ],
        "pricing_note": "Often added to siding or porch jobs; standalone counts quoted after photos.",
        "related": ["house-siding", "soffit-gutters"],
    },
]

SERVICE_BY_SLUG = {s["slug"]: s for s in SERVICES}


def nav_html(depth: str) -> str:
    """depth: 'root' | 'pages' | 'services'"""
    if depth == "root":
        p, s = "pages/", "services/"
    elif depth == "pages":
        p, s = "", "../services/"
    else:
        p, s = "../pages/", ""
    return f"""<nav class="nav">
  <div class="nav-inner">
    <a href="/" class="nav-logo">
      <img src="{'../' if depth != 'root' else ''}assets/images/Logo.png" alt="SC Pressure Point logo">
      <span class="nav-logo-text">
        <span class="brand-top">SC Pressure Point</span>
        <span class="brand-bottom">Pressure Washing</span>
      </span>
    </a>
    <ul class="nav-links">
      <li><a href="{p}gallery.html">Gallery</a></li>
      <li><a href="{p if depth != 'services' else '../pages/'}services.html">Services</a></li>
      <li><a href="{'../' if depth != 'root' else ''}pressure-washing-costs-columbia-sc.html">Pricing</a></li>
      <li><a href="{p}about.html">About</a></li>
      <li><a href="{p}reviews.html">Reviews</a></li>
      <li><a href="{p}contact.html">Contact</a></li>
    </ul>
    <a href="tel:8032728118" class="nav-phone"><i class="fa-solid fa-phone"></i>(803) 272-8118</a>
    <button class="nav-hamburger" id="nav-hamburger" aria-label="Open menu"><span></span><span></span><span></span></button>
  </div>
  <div class="nav-drawer" id="nav-drawer">
    <ul>
      <li><a href="{p}gallery.html">Gallery</a></li>
      <li><a href="{p if depth != 'services' else '../pages/'}services.html">Services</a></li>
      <li><a href="{'../' if depth != 'root' else ''}pressure-washing-costs-columbia-sc.html">Pricing</a></li>
      <li><a href="{p}about.html">About</a></li>
      <li><a href="{p}reviews.html">Reviews</a></li>
      <li><a href="{p}faq.html">FAQ</a></li>
      <li><a href="{p}contact.html">Contact</a></li>
      <li><a href="{p}estimate.html#form">Get a Free Estimate</a></li>
    </ul>
    <div class="drawer-phone">
      <a href="tel:8032728118" class="btn btn-primary btn-lg" style="width:100%; justify-content:center; margin-top:0.75rem;">
        <i class="fa-solid fa-phone"></i>&nbsp; (803) 272-8118
      </a>
    </div>
  </div>
</nav>"""


def head_analytics() -> str:
    return """  <!-- Microsoft Clarity -->
  <script type="text/javascript">
      (function(c,l,a,r,i,t,y){
          c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
          t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
          y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
      })(window, document, "clarity", "script", "w7h964agdu");
  </script>
  <!-- Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-X8BLNTEE52"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-X8BLNTEE52');
  </script>"""


def related_links(slug: str) -> str:
    svc = SERVICE_BY_SLUG[slug]
    items = []
    for rel in svc["related"]:
        r = SERVICE_BY_SLUG[rel]
        items.append(f'<a href="{rel}.html"><i class="fa-solid {r["icon"]}"></i> {r["short"]}</a>')
    return "\n        ".join(items)


def process_html(steps) -> str:
    rows = []
    for i, (title, desc) in enumerate(steps, 1):
        rows.append(f"""        <li class="service-process-step">
          <span class="service-process-num">{i}</span>
          <div>
            <strong>{title}</strong>
            <p>{desc}</p>
          </div>
        </li>""")
    return "\n".join(rows)


def service_page(svc: dict) -> str:
    slug = svc["slug"]
    url = f"https://www.scpressurepoint.com/services/{slug}.html"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{svc['title']} | SC Pressure Point</title>
  <meta name="description" content="{svc['description']} Free estimates. Text (803) 272-8118.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{url}">

  <link rel="icon" href="../favicon.ico" sizes="any">
  <link rel="icon" href="../assets/images/Logo.png" type="image/png">
  <link rel="apple-touch-icon" href="../assets/images/apple-touch-icon.png">

  <meta property="og:type" content="website">
  <meta property="og:title" content="{svc['title']} | SC Pressure Point">
  <meta property="og:description" content="{svc['description']}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="https://www.scpressurepoint.com/assets/images/og-image.jpg">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <link rel="stylesheet" href="../assets/css/main.css">
  <link rel="stylesheet" href="../assets/css/elderly-friendly.css">
{head_analytics()}
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "Service",
        "@id": "{url}#service",
        "name": "{svc['title']}",
        "description": "{svc['description']}",
        "provider": {{ "@id": "https://www.scpressurepoint.com/#business" }},
        "areaServed": "Columbia, SC and surrounding areas",
        "url": "{url}"
      }},
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.scpressurepoint.com/" }},
          {{ "@type": "ListItem", "position": 2, "name": "Services", "item": "https://www.scpressurepoint.com/pages/services.html" }},
          {{ "@type": "ListItem", "position": 3, "name": "{svc['short']}", "item": "{url}" }}
        ]
      }}
    ]
  }}
  </script>
</head>
<body>

{nav_html('services')}

<header class="page-header">
  <div class="container">
    <h1><i class="fa-solid {svc['icon']}" style="color:var(--yellow)"></i> {svc['title']}</h1>
    <p>Student-owned and operated in Columbia, SC. Text a photo for a fast quote — (803) 272-8118.</p>
  </div>
</header>

<nav class="breadcrumb container" aria-label="Breadcrumb" style="max-width:900px; margin:0 auto; padding:0 1.25rem 1rem;">
  <a href="/">Home</a> / <a href="../pages/services.html">Services</a> / <span aria-current="page">{svc['short']}</span>
</nav>

<main>
  <section class="section-pad-sm">
    <div class="container" style="max-width:900px;">
      <p style="margin-bottom:1.25rem;">{svc['intro']}</p>

      <h2 style="font-size:1.35rem; margin:1.5rem 0 0.75rem; color:var(--navy);">How we do it</h2>
      <ol class="service-process-list">
{process_html(svc['process'])}
      </ol>

      <p style="margin-top:1.5rem; padding:1rem 1.25rem; background:var(--blue-light); border-radius:var(--radius); border-left:4px solid var(--blue);">
        <strong>Pricing:</strong> {svc['pricing_note']}
        <a href="../pressure-washing-costs-columbia-sc.html" style="color:var(--blue); font-weight:700;"> See full pricing guide</a>.
      </p>

      <div class="cta-strip-btns" style="justify-content:flex-start; margin-top:1.5rem;">
        <a class="btn btn-primary btn-lg" href="../pages/estimate.html#form"><i class="fa-solid fa-file-invoice-dollar"></i> Request an Estimate</a>
        <a class="btn btn-blue btn-lg" href="sms:8032728118"><i class="fa-solid fa-comment-sms"></i> Text a Photo</a>
      </div>
    </div>
  </section>

  <section class="section-pad-sm" style="padding-top:0;">
    <div class="container" style="max-width:900px;">
      <h2 style="font-size:1.25rem; margin-bottom:0.65rem;">Related services</h2>
      <nav class="locale-links" aria-label="Related services">
        {related_links(slug)}
      </nav>
    </div>
  </section>

  <section class="section-pad-sm" style="padding-top:0;">
    <div class="container" style="max-width:900px;">
      <h2 style="font-size:1.25rem; margin-bottom:0.65rem;">Areas we serve</h2>
      <nav class="locale-links" aria-label="Local pressure washing pages">
{LOCALE_LINKS}
      </nav>
    </div>
  </section>
</main>

<footer class="footer">
  <div class="container">
    <div class="footer-bottom" style="border-top:none; padding-top:0;">
      <span>&copy; 2026 SC Pressure Point</span>
      <a href="/" style="color:rgba(255,255,255,0.5);">Back to Home</a>
    </div>
  </div>
</footer>

<script src="../assets/js/site-config.js"></script>
<script src="../assets/js/site-trust.js"></script>
<script src="../assets/js/main.js"></script>
</body>
</html>
"""


def services_hub_page() -> str:
    cards = []
    for svc in SERVICES:
        cards.append(f"""      <a href="../services/{svc['slug']}.html" class="service-card service-card--link fade-in">
        <div class="service-icon"><i class="fa-solid {svc['icon']}"></i></div>
        <h3>{svc['short']}</h3>
        <p>{svc['description'].split('.')[0]}.</p>
        <span class="service-card-more">Learn more <i class="fa-solid fa-arrow-right"></i></span>
      </a>""")
    cards_html = "\n".join(cards)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Pressure Washing Services | SC Pressure Point</title>
  <meta name="description" content="Pressure washing services in Columbia, SC: driveways, sidewalks, siding, patios, gutters, fences, and more. Student-owned. Free estimates.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://www.scpressurepoint.com/pages/services.html">

  <link rel="icon" href="../favicon.ico" sizes="any">
  <link rel="icon" href="../assets/images/Logo.png" type="image/png">
  <link rel="apple-touch-icon" href="../assets/images/apple-touch-icon.png">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <link rel="stylesheet" href="../assets/css/main.css">
  <link rel="stylesheet" href="../assets/css/elderly-friendly.css">
{head_analytics()}
</head>
<body>

{nav_html('pages')}

<header class="page-header">
  <div class="container">
    <span class="tag" style="background:rgba(255,255,255,0.15); color:#fff;">What We Clean</span>
    <h1>Our Services</h1>
    <p>Every service page explains our process, pricing approach, and where we work in the Columbia, SC area.</p>
  </div>
</header>

<nav class="breadcrumb container" aria-label="Breadcrumb" style="max-width:900px; margin:0 auto; padding:0 1.25rem 1rem;">
  <a href="/">Home</a> / <span aria-current="page">Services</span>
</nav>

<main>
  <section class="section-pad">
    <div class="container">
      <p class="section-sub" style="max-width:720px; margin-bottom:2rem;">
        Columbia humidity means algae, mold, and grime build up fast. Tap a service to see how we carry it out and get a quote.
        Serving <a href="../pressure-washing-columbia-sc.html">Columbia</a>,
        <a href="../pressure-washing-lexington-sc.html">Lexington</a>,
        <a href="../pressure-washing-irmo-sc.html">Irmo</a>, and nearby areas.
      </p>
      <div class="services-grid">
{cards_html}
      </div>
      <div class="pricing-cta" style="margin-top:2.5rem; text-align:center;">
        <a href="estimate.html#form" class="btn btn-primary btn-lg btn-wide">
          <i class="fa-solid fa-file-invoice-dollar"></i> Request an Estimate
        </a>
        <a href="../pressure-washing-costs-columbia-sc.html" class="btn btn-blue btn-lg" style="margin-left:0.5rem;">
          <i class="fa-solid fa-tags"></i> View Pricing Guide
        </a>
      </div>
    </div>
  </section>
</main>

<footer class="footer">
  <div class="container">
    <div class="footer-bottom" style="border-top:none; padding-top:0;">
      <span>&copy; 2026 SC Pressure Point</span>
      <a href="/" style="color:rgba(255,255,255,0.5);">Back to Home</a>
    </div>
  </div>
</footer>

<script src="../assets/js/site-config.js"></script>
<script src="../assets/js/site-trust.js"></script>
<script src="../assets/js/main.js"></script>
</body>
</html>
"""


def main():
    SERVICES_DIR.mkdir(exist_ok=True)
    for svc in SERVICES:
        path = SERVICES_DIR / f"{svc['slug']}.html"
        path.write_text(service_page(svc), encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")
    hub = PAGES_DIR / "services.html"
    hub.write_text(services_hub_page(), encoding="utf-8")
    print(f"Wrote {hub.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
