"""Generate location landing pages from shared template + per-city data."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LOCALES = [
    {
        "slug": "columbia",
        "city": "Columbia",
        "map_query": "Columbia%2C%20SC",
        "intro_p1": (
            "Columbia weather makes outdoor surfaces grow algae and mildew fast. Driveways darken, "
            "sidewalks get slick, and patios lose their clean look. SC Pressure Point helps homeowners "
            "and small businesses keep exteriors looking sharp with a safe process and clear communication."
        ),
        "intro_p2": (
            "We clean concrete flatwork, steps, patios, and fences. We also offer all house sidings, "
            "soffit, and exterior gutter cleaning. If you are not sure what you need, text a photo and "
            "we will recommend the right approach and give you a fair estimate."
        ),
        "local_p1": (
            "Midlands humidity, oak pollen, and red clay runoff are tough on concrete and siding. In "
            "neighborhoods like Shandon, Forest Acres, Rosewood, and Lake Katherine, driveways often show "
            "dark algae lines and patios get slick under shade trees. Spring pollen and summer storms can "
            "leave siding and soffits green within a season."
        ),
        "local_p2": (
            "SC Pressure Point is student-owned and operated, but every job is run with owner oversight. "
            "clear quotes, on-time arrival, and results you can see before we leave. We regularly work near "
            "USC, Five Points, Devine Street, and the Harbison area. Typical Columbia jobs include two-car "
            "driveways, front walks with steps, back patios, and vinyl siding soft washes."
        ),
        "faq2_q": "Do you clean siding and gutters in Columbia, SC?",
        "faq2_a": "Yes. We offer all house sidings, soffit, and exterior gutter cleaning. We use a safe method based on the material.",
        "faq3_q": "Do I need to be home for pressure washing in Columbia, SC?",
        "faq3_a": "Not always. As long as we have access to the areas that need cleaning and a water source, you do not need to be home. We confirm details before we start.",
        "schema_faq2_q": "What surfaces do you clean in Columbia, SC?",
        "schema_faq2_a": "We clean driveways, sidewalks, steps, patios, fences, all house sidings, soffit, and exterior gutters. Text a photo if you want a quick recommendation.",
        "schema_faq3_q": "Do I need to be home for pressure washing service in Columbia, SC?",
        "schema_faq3_a": "As long as we have access to the areas that need cleaning and a water source, you do not need to be home. We confirm details before we start.",
        "reviews": ["rachel", "darla"],
    },
    {
        "slug": "lexington",
        "city": "Lexington",
        "map_query": "Lexington%2C%20SC",
        "intro_p1": (
            "Lexington homes deal with heat, humidity, and long growing seasons. That means algae, mildew, "
            "and grime can show up quickly on concrete and exterior surfaces. Regular cleaning keeps your "
            "property looking sharp and helps prevent slippery walkways."
        ),
        "intro_p2": (
            "SC Pressure Point focuses on clear communication and consistent results. We clean flatwork, "
            "steps, patios, fences, all house sidings, soffit, and exterior gutters. Text your address and "
            "a photo for a fair price before any work begins."
        ),
        "local_p1": (
            "Red clay, Lake Murray humidity, and heavy pollen hit Lexington driveways and patios hard. In "
            "areas like Red Bank, Whiteford, Old Mill, and neighborhoods off Sunset Boulevard, concrete often "
            "stays damp under tree cover and develops dark streaks. Newer subdivisions near Lake Murray see "
            "the same buildup on pool decks and back patios each summer."
        ),
        "local_p2": (
            "We are student-owned with owner oversight on every job: no vague quotes, no surprise add-ons. "
            "Common Lexington work includes two-car driveways, long suburban sidewalks, vinyl siding soft "
            "washes, and gutter brightening near the Town of Lexington and Gilbert corridor. We serve Lexington "
            "proper and nearby Lexington County communities."
        ),
        "faq2_q": "Do you offer soft washing for siding in Lexington, SC?",
        "faq2_a": "Yes. For siding and other delicate surfaces, we use a safe soft wash approach when needed to avoid damage while still removing grime and growth.",
        "faq3_q": "Do you clean soffit and exterior gutters in Lexington, SC?",
        "faq3_a": "Yes. We offer soffit and exterior gutter cleaning to remove streaks, mold, and grime along with driveways and patios.",
        "schema_faq2_q": "Do you offer soft washing in Lexington, SC?",
        "schema_faq2_a": "Yes. For delicate surfaces like siding, we use a safe soft wash approach when needed to avoid damage while still removing grime and growth.",
        "schema_faq3_q": "Do you clean soffit and exterior gutters in Lexington, SC?",
        "schema_faq3_a": "Yes. We offer soffit and exterior gutter cleaning to remove streaks, mold, and grime.",
        "reviews": ["jane", "loretta"],
    },
    {
        "slug": "irmo",
        "city": "Irmo",
        "map_query": "Irmo%2C%20SC",
        "intro_p1": (
            "Irmo sits in one of the fastest-growing parts of the Midlands. Humidity, pollen, and shaded "
            "lots mean driveways and patios can look dirty again within a single season if they are not cleaned."
        ),
        "intro_p2": (
            "SC Pressure Point provides driveways, sidewalks, steps, patios, fences, all house sidings, "
            "soffit, and exterior gutter cleaning with direct communication. Text a photo for a clear quote."
        ),
        "local_p1": (
            "Lake Murray moisture, mature trees, and red clay runoff are common in Seven Oaks, Oak Hall, "
            "and Dutch Fork areas. Shaded driveways near Harbison and Broad River Road often hold algae that "
            "makes concrete look years older than it is. Spring oak pollen can coat siding and soffits in weeks."
        ),
        "local_p2": (
            "Student-owned does not mean inconsistent. Parker oversees quality on every Irmo job. Typical "
            "work includes lake-community driveways, long front walks, back patios, and soft washes on vinyl "
            "and painted siding. We serve Irmo and nearby areas along the I-26 corridor toward Chapin."
        ),
        "faq2_q": "What do you clean for Irmo, SC homes?",
        "faq2_a": "We clean driveways, sidewalks, steps, patios, fences, all house sidings, soffit, and exterior gutters. Text a photo if you want a quick recommendation.",
        "faq3_q": "Do you offer weekend pressure washing in Irmo, SC?",
        "faq3_a": "Yes. We offer weekday and weekend availability depending on schedule. Text (803) 272-8118 to confirm a time that works.",
        "schema_faq2_q": "What do you clean in Irmo, SC?",
        "schema_faq2_a": "We clean driveways, sidewalks, steps, patios, fences, all house sidings, soffit, and exterior gutters. Text a photo if you want a quick recommendation.",
        "schema_faq3_q": "Do you work weekends for pressure washing in Irmo, SC?",
        "schema_faq3_a": "Yes. We offer weekday and weekend availability depending on schedule. Text us to confirm a time that works.",
        "reviews": ["jennifer", "jane"],
    },
    {
        "slug": "dentsville",
        "city": "Dentsville",
        "map_query": "Dentsville%2C%20SC",
        "intro_p1": (
            "Dentsville has humid summers and shaded areas that make algae and mildew build up fast. That "
            "buildup stains concrete and can make walkways slick. Our process restores curb appeal and helps "
            "keep surfaces cleaner longer."
        ),
        "intro_p2": (
            "We clean driveways, sidewalks, steps, patios, fences, all house sidings, soffit, and exterior "
            "gutters. You get direct communication and a fair price. If something falls short, we come back "
            "and make it right."
        ),
        "local_p1": (
            "As a busy Columbia-area community, Dentsville sees the same Midlands humidity and clay staining "
            "as the rest of the metro. Homes near Decker Boulevard, Sparkleberry Lane, and the Two Notch corridor "
            "often have driveways with tire marks, pollen film, and green algae in shaded strips along the house."
        ),
        "local_p2": (
            "SC Pressure Point serves Dentsville homeowners with owner-on-site standards: fast text replies, "
            "clear per-surface pricing, and satisfaction-backed work. Common jobs include suburban driveways, "
            "entry walks with steps, patios, and siding washes on split-level and ranch homes throughout the area."
        ),
        "faq2_q": "Do you clean siding and exterior gutters in Dentsville, SC?",
        "faq2_a": "Yes. We offer all house sidings, soffit, and exterior gutter cleaning. We use a safe method based on the material.",
        "faq3_q": "How do I get a fast pressure washing estimate in Dentsville, SC?",
        "faq3_a": "Text (803) 272-8118 with your address and a photo of what you want cleaned. We reply quickly with a clear quote.",
        "schema_faq2_q": "Do you clean siding and exterior gutters in Dentsville, SC?",
        "schema_faq2_a": "Yes. We offer all house sidings, soffit, and exterior gutter cleaning. We use a safe method based on the material.",
        "schema_faq3_q": "How do I get a fast estimate for pressure washing in Dentsville, SC?",
        "schema_faq3_a": "Text (803) 272-8118 with your address and a photo. We reply quickly with a clear quote.",
        "reviews": ["darla", "jane"],
    },
    {
        "slug": "west-columbia",
        "city": "West Columbia",
        "map_query": "West%20Columbia%2C%20SC",
        "intro_p1": (
            "West Columbia weather and river-area humidity can cause algae and mildew to show up quickly on "
            "concrete, siding, and exterior surfaces. Cleaning restores curb appeal and keeps walkways safer."
        ),
        "intro_p2": (
            "We clean driveways, sidewalks, steps, patios, fences, all house sidings, soffit, and exterior "
            "gutters. You get a clear quote and satisfaction-backed work from a student-owned team with owner oversight."
        ),
        "local_p1": (
            "Proximity to the Congaree and lower Midlands humidity means West Columbia driveways and patios "
            "stay wet longer. Neighborhoods near Meeting Street, Augusta Road, Triangle City, and Brookwood "
            "often see green growth on north-facing siding and dark patches on shaded concrete."
        ),
        "local_p2": (
            "We regularly work in West Columbia and nearby Cayce-accessible routes. Typical jobs include "
            "driveways, front steps, back patios, and gutter or soffit brightening on older brick and vinyl homes. "
            "Text a photo. We quote by surface and square footage, not vague job sizes."
        ),
        "faq2_q": "Do you clean exterior gutters and soffit in West Columbia, SC?",
        "faq2_a": "Yes. We offer soffit and exterior gutter cleaning along with concrete cleaning, fences, and siding.",
        "faq3_q": "What is the fastest way to get a pressure washing quote in West Columbia, SC?",
        "faq3_a": "Text (803) 272-8118 with your address and a photo. We reply quickly with a clear quote.",
        "schema_faq2_q": "Do you clean exterior gutters and soffit in West Columbia, SC?",
        "schema_faq2_a": "Yes. We offer soffit and exterior gutter cleaning along with concrete cleaning, fences, and siding.",
        "schema_faq3_q": "What is the fastest way to get a quote for pressure washing in West Columbia, SC?",
        "schema_faq3_a": "Text (803) 272-8118 with your address and a photo. We reply quickly with a clear quote.",
        "reviews": ["darla", "loretta"],
    },
    {
        "slug": "forest-acres",
        "city": "Forest Acres",
        "map_query": "Forest%20Acres%2C%20SC",
        "intro_p1": (
            "Forest Acres properties often have shaded driveways and sidewalks that hold moisture. That makes "
            "algae and mildew show up faster and can make concrete look permanently stained. A proper clean "
            "restores the bright look of concrete and improves curb appeal."
        ),
        "intro_p2": (
            "We clean driveways, sidewalks, steps, patios, fences, all house sidings, soffit, and exterior "
            "gutters. Text a photo and we will recommend the right approach and send a clear quote."
        ),
        "local_p1": (
            "Mature tree canopy around Forest Lake, Trenholm Road, and Gable Oaks means less sun on driveways "
            "and more organic growth on concrete and siding. Established brick and ranch homes often need soft "
            "washing on north elevations where mildew spreads along soffits and gutters."
        ),
        "local_p2": (
            "Forest Acres is one of our core Columbia-metro areas. We handle shaded concrete that stays dark, "
            "long front walks, pool patios, and detail work near Trenholm Plaza and Devine Street corridors. "
            "Owner oversight and honest per-sq-ft pricing apply on every visit."
        ),
        "faq2_q": "Do you clean exterior gutters and soffit in Forest Acres, SC?",
        "faq2_a": "Yes. We offer soffit and exterior gutter cleaning to remove streaks, mold, and grime.",
        "faq3_q": "Can you clean shaded concrete that stays dark in Forest Acres, SC?",
        "faq3_a": "Yes. Shaded areas can hold moisture and grow algae. We use the right mix and technique to lift buildup and leave a consistent finish.",
        "schema_faq2_q": "Do you clean exterior gutters and soffit in Forest Acres, SC?",
        "schema_faq2_a": "Yes. We offer soffit and exterior gutter cleaning to remove streaks, mold, and grime.",
        "schema_faq3_q": "Can you clean shaded concrete in Forest Acres, SC?",
        "schema_faq3_a": "Yes. Shaded areas can hold moisture and grow algae. We use the right technique to lift buildup and leave a consistent finish.",
        "reviews": ["rachel", "jennifer"],
    },
    {
        "slug": "blythewood",
        "city": "Blythewood",
        "map_query": "Blythewood%2C%20SC",
        "intro_p1": (
            "Blythewood properties deal with humidity, pollen, and growth that can stain concrete and dull "
            "exterior surfaces. A good clean makes a big difference for curb appeal before guests or listing photos."
        ),
        "intro_p2": (
            "We clean driveways, sidewalks, steps, patios, fences, all house sidings, soffit, and exterior "
            "gutters. Text a photo and we will send a clear quote with no surprise fees."
        ),
        "local_p1": (
            "Newer subdivisions near Lake Carolina, Cobblestone Park, and the I-77 corridor still see Midlands "
            "pollen, clay dust, and mildew on north-facing walls. Larger lots mean longer driveways and more "
            "concrete to maintain, especially after wet winters when algae shows up on flatwork."
        ),
        "local_p2": (
            "We serve Blythewood and growing Richland County pockets north of Columbia. Common work includes "
            "long suburban driveways, pool decks, back patios, and siding washes on newer vinyl and fiber-cement "
            "homes. Student-owned, but you get direct contact with the owner and fair per-surface pricing."
        ),
        "faq2_q": "Do you clean driveways and sidewalks in Blythewood, SC?",
        "faq2_a": "Yes. We clean concrete flatwork like driveways, sidewalks, steps, and patios. We also offer all house sidings, soffit, and exterior gutters.",
        "faq3_q": "How do I schedule pressure washing in Blythewood, SC?",
        "faq3_a": "Text (803) 272-8118 with your address and what you want cleaned. We will confirm availability and get you on the schedule.",
        "schema_faq2_q": "Do you clean driveways and sidewalks in Blythewood, SC?",
        "schema_faq2_a": "Yes. We clean driveways, sidewalks, steps, and patios. We also offer all house sidings, soffit, and exterior gutters.",
        "schema_faq3_q": "How do I schedule pressure washing in Blythewood, SC?",
        "schema_faq3_a": "Text (803) 272-8118 with your address and what you want cleaned. We confirm availability and schedule your job.",
        "reviews": ["jane", "loretta"],
    },
]

EL = "di" + "v"

REVIEW_CATALOG = {
    "darla": (
        "Darla H.",
        "Columbia area",
        "I had my front porch and sidewalk cleaned. He also washed down 16 windows and ledges on the back of the house - everything looks amazing.",
    ),
    "jane": (
        "Jane A.",
        "Lexington area",
        "Such dedication and professionalism in this young man. He showed up when he said. Worked in the rain, until I sent him home. Came back timely to wrap up. All looks great! It was long overdue! Thanks!!",
    ),
    "jennifer": (
        "Jennifer H.",
        "Columbia area",
        "Parker did an amazing job cleaning our front porch and windows. They haven't looked this good in years. I'd definitely recommend Parker to anyone needing detailed washing done.",
    ),
    "loretta": (
        "Loretta G.",
        "Columbia area",
        "Parker did a great job for us. Very respectful very thorough just overall a great person. I highly recommend his service.",
    ),
    "rachel": (
        "Rachel P.",
        "Columbia area",
        "Parker does an amazing job! He is timely and courteous. He communicates with you and ensures you are happy as a customer. He is always a delight to work with and an extremely hard worker who completes a very professional job.",
    ),
}

NAV_LINKS = [
    ("/#gallery", "Gallery"),
    ("/#services", "Services"),
    ("pressure-washing-costs-columbia-sc.html", "Pricing"),
    ("/#about", "About"),
    ("/#contact", "Contact"),
]

LOCALE_NAV = [
    ("columbia", "Columbia"),
    ("dentsville", "Dentsville"),
    ("irmo", "Irmo"),
    ("lexington", "Lexington"),
    ("west-columbia", "West Columbia"),
    ("forest-acres", "Forest Acres"),
    ("blythewood", "Blythewood"),
]

FAQ1_ANSWER_SCHEMA = (
    "Most driveways are $0.20 to $0.40 per square foot. A typical two-car driveway often falls "
    "between $125 and $275. See https://www.scpressurepoint.com/pressure-washing-costs-columbia-sc.html "
    "or text (803) 272-8118 for a free estimate."
)


def faq1_question(city: str) -> str:
    return f"How much does it cost to pressure wash a driveway in {city}, SC?"


def faq1_answer_html() -> str:
    return (
        '<p>Most driveways are $0.20 to $0.40 per square foot. A typical two-car driveway often falls '
        'between $125 and $275. <a href="pressure-washing-costs-columbia-sc.html" '
        'style="color:var(--blue); font-weight:700;">See full pricing</a> or text (803) 272-8118 '
        "for a free estimate.</p>"
    )


def locale_links(current_slug: str) -> str:
    parts = []
    for slug, label in LOCALE_NAV:
        href = f"pressure-washing-{slug}-sc.html"
        if slug == current_slug:
            parts.append(f'<a href="{href}" aria-current="page">{label}</a>')
        else:
            parts.append(f'<a href="{href}">{label}</a>')
    return "\n        ".join(parts)


def nav_items() -> str:
    return "\n      ".join(f'<li><a href="{href}">{label}</a></li>' for href, label in NAV_LINKS)


def drawer_items() -> str:
    items = [
        ("/#gallery", "Gallery"),
        ("/#services", "Services"),
        ("pressure-washing-costs-columbia-sc.html", "Pricing"),
        ("/#about", "About"),
        ("/#contact", "Contact"),
        ("pages/estimate.html", "Get a Free Estimate"),
    ]
    return "\n      ".join(f'<li><a href="{href}">{label}</a></li>' for href, label in items)


def render_review_card(key: str) -> str:
    name, area, text = REVIEW_CATALOG[key]
    stars = " ".join('<i class="fa-solid fa-star"></i>' for _ in range(5))
    return f"""      <{EL} class="review-card">
        <{EL} class="review-stars" aria-label="5 out of 5 stars">
          <span class="review-stars-icons" aria-hidden="true">{stars}</span>
        </{EL}>
        <p class="review-text">"{text}"</p>
        <{EL} class="review-author">
          <{EL} class="review-avatar" aria-hidden="true"><i class="fa-solid fa-user"></i></{EL}>
          <{EL}><strong>{name}</strong><span class="review-source">Customer · {area}</span></{EL}>
        </{EL}>
      </{EL}>"""


def render_reviews_section(city: str, keys: list) -> str:
    cards = "\n\n".join(render_review_card(k) for k in keys)
    return f"""  <section class="reviews section-pad locale-reviews" id="reviews">
    <{EL} class="container" style="max-width: 900px;">
      <span class="tag">What Customers Say</span>
      <h2 class="section-title">Real Feedback</h2>
      <p class="section-sub">Homeowners near {city}, SC and across the Midlands trust SC Pressure Point.</p>
      <{EL} class="reviews-grid locale-reviews-grid">
{cards}
      </{EL}>
      <p style="text-align:center; margin-top:1.5rem; color:var(--text-light); font-size:0.95rem;">
        Had a great experience?
        <a href="sms:8032728118" style="color:var(--blue); font-weight:700;">Text us your feedback</a>
      </p>
    </{EL}>
  </section>"""


def footer_area_item(slug: str, label: str, current_slug: str) -> str:
    href = f"pressure-washing-{slug}-sc.html"
    if slug == current_slug:
        return f'          <li><a href="{href}" aria-current="page">{label}</a></li>'
    return f'          <li><a href="{href}">{label}</a></li>'


def render_site_footer(current_slug: str) -> str:
    area_items = "\n".join(
        footer_area_item(slug, label, current_slug) for slug, label in LOCALE_NAV
    )
    return f"""<footer class="footer">
  <{EL} class="container">
    <{EL} class="footer-inner">

      <{EL} class="footer-brand">
        <img src="assets/images/Logo.png" alt="SC Pressure Point logo">
        <p>
          Student-owned pressure washing in Columbia, SC.
          Professional results, personal service, honest pricing.
        </p>
        <{EL} class="social-links">
          <a href="https://www.instagram.com/scpressurepoint" target="_blank" rel="noopener" aria-label="Instagram">
            <i class="fa-brands fa-instagram"></i>
          </a>
          <a href="sms:8032728118" aria-label="Text us">
            <i class="fa-solid fa-comment-sms"></i>
          </a>
          <a href="mailto:scpressurepoint@gmail.com" aria-label="Email">
            <i class="fa-solid fa-envelope"></i>
          </a>
        </{EL}>
      </{EL}>

      <{EL} class="footer-col">
        <h4>Quick Links</h4>
        <ul>
          <li><a href="/#gallery">Before &amp; After Gallery</a></li>
          <li><a href="pages/gallery.html">Full Gallery</a></li>
          <li><a href="/#services">Services</a></li>
          <li><a href="pressure-washing-costs-columbia-sc.html">Pricing Guide</a></li>
          <li><a href="/#about">About</a></li>
          <li><a href="pages/estimate.html">Get an Estimate</a></li>
          <li><a href="pages/careers.html">Careers</a></li>
        </ul>
      </{EL}>

      <{EL} class="footer-col">
        <h4>Service Areas</h4>
        <ul>
{area_items}
        </ul>
      </{EL}>

      <{EL} class="footer-col">
        <h4>Contact</h4>
        <{EL} class="footer-contact-item">
          <i class="fa-solid fa-phone"></i>
          <a href="tel:8032728118">(803) 272-8118</a>
        </{EL}>
        <{EL} class="footer-contact-item">
          <i class="fa-solid fa-comment-sms"></i>
          <a href="sms:8032728118">Text preferred</a>
        </{EL}>
        <{EL} class="footer-contact-item">
          <i class="fa-solid fa-envelope"></i>
          <a href="mailto:scpressurepoint@gmail.com">scpressurepoint@gmail.com</a>
        </{EL}>
        <{EL} class="footer-contact-item">
          <i class="fa-solid fa-location-dot"></i>
          <span>Columbia, SC &amp; surrounding areas</span>
        </{EL}>
        <{EL} class="footer-contact-item">
          <i class="fa-brands fa-instagram"></i>
          <a href="https://www.instagram.com/scpressurepoint" target="_blank" rel="noopener">@scpressurepoint</a>
        </{EL}>
      </{EL}>

    </{EL}>

    <{EL} class="footer-bottom">
      <span>&copy; 2026 SC Pressure Point, Columbia, SC</span>
      <span>Built by <a href="https://parkerbranham.com" target="_blank" rel="nofollow noopener">Parker Branham</a></span>
    </{EL}>
  </{EL}>
</footer>

<aside class="mobile-cta-bar" id="mobile-cta-bar" aria-label="Quick contact">
  <a href="tel:8032728118" class="mobile-cta-bar__call">
    <i class="fa-solid fa-phone" aria-hidden="true"></i>
    <span>Call</span>
  </a>
  <a href="pages/estimate.html" class="mobile-cta-bar__estimate btn btn-primary">
    <i class="fa-solid fa-file-invoice-dollar" aria-hidden="true"></i>
    Free Estimate
  </a>
</aside>"""


def render_site_nav() -> str:
    return f"""<nav class="nav">
  <{EL} class="nav-inner">
    <a href="/#hero" class="nav-logo">
      <img src="assets/images/Logo.png" alt="SC Pressure Point logo">
      <span class="nav-logo-text">
        <span class="brand-top">SC Pressure Point</span>
        <span class="brand-bottom">Pressure Washing</span>
      </span>
    </a>
    <ul class="nav-links">
      {nav_items()}
    </ul>
    <a href="tel:8032728118" class="nav-phone"><i class="fa-solid fa-phone"></i>(803) 272-8118</a>
    <button class="nav-hamburger" id="nav-hamburger" aria-label="Open menu"><span></span><span></span><span></span></button>
  </{EL}>
  <{EL} class="nav-drawer" id="nav-drawer">
    <ul>
      {drawer_items()}
    </ul>
    <{EL} class="drawer-phone">
      <a href="tel:8032728118" class="btn btn-primary btn-lg" style="width:100%; justify-content:center; margin-top:0.75rem;">
        <i class="fa-solid fa-phone"></i>&nbsp; (803) 272-8118
      </a>
    </{EL}>
  </{EL}>
</nav>"""


def render(loc: dict) -> str:
    slug = loc["slug"]
    city = loc["city"]
    filename = f"pressure-washing-{slug}-sc.html"
    url = f"https://www.scpressurepoint.com/{filename}"
    fq1 = faq1_question(city)
    site_nav = render_site_nav()
    site_footer = render_site_footer(slug)
    reviews_block = render_reviews_section(city, loc["reviews"])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Pressure Washing in {city}, SC | SC Pressure Point</title>
  <meta name="description" content="Pressure washing in {city}, SC from SC Pressure Point. Driveways, sidewalks, patios, siding, soffit, and exterior gutters. Owner oversight. Text (803) 272-8118 for a free estimate.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{url}">

  <link rel="icon" href="favicon.ico" sizes="any">
  <link rel="icon" href="assets/images/Logo.png" type="image/png">
  <link rel="apple-touch-icon" href="assets/images/apple-touch-icon.png">

  <meta property="og:type" content="website">
  <meta property="og:title" content="Pressure Washing in {city}, SC | SC Pressure Point">
  <meta property="og:description" content="Driveways, sidewalks, patios, siding, soffit, and exterior gutters. Free estimates. Text (803) 272-8118.">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="https://www.scpressurepoint.com/assets/images/og-image.jpg">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <link rel="stylesheet" href="assets/css/main.css">
  <link rel="stylesheet" href="assets/css/elderly-friendly.css">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "LocalBusiness",
        "@id": "https://www.scpressurepoint.com/#business",
        "name": "SC Pressure Point",
        "url": "https://www.scpressurepoint.com/",
        "telephone": "+18032728118",
        "areaServed": [
          {{ "@type": "City", "name": "{city}", "address": {{ "@type": "PostalAddress", "addressRegion": "SC", "addressCountry": "US" }} }}
        ],
        "sameAs": ["https://www.instagram.com/scpressurepoint"]
      }},
      {{
        "@type": "Service",
        "@id": "{url}#service",
        "serviceType": "Pressure Washing",
        "provider": {{ "@id": "https://www.scpressurepoint.com/#business" }},
        "areaServed": "{city}, SC"
      }},
      {{
        "@type": "FAQPage",
        "@id": "{url}#faqs",
        "mainEntity": [
          {{
            "@type": "Question",
            "name": {json_escape(fq1)},
            "acceptedAnswer": {{ "@type": "Answer", "text": {json_escape(FAQ1_ANSWER_SCHEMA)} }}
          }},
          {{
            "@type": "Question",
            "name": {json_escape(loc["schema_faq2_q"])},
            "acceptedAnswer": {{ "@type": "Answer", "text": {json_escape(loc["schema_faq2_a"])} }}
          }},
          {{
            "@type": "Question",
            "name": {json_escape(loc["schema_faq3_q"])},
            "acceptedAnswer": {{ "@type": "Answer", "text": {json_escape(loc["schema_faq3_a"])} }}
          }}
        ]
      }},
      {{
        "@type": "BreadcrumbList",
        "@id": "{url}#breadcrumb",
        "itemListElement": [
          {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.scpressurepoint.com/" }},
          {{ "@type": "ListItem", "position": 2, "name": "{city}, SC", "item": "{url}" }}
        ]
      }}
    ]
  }}
  </script>
</head>
<body>

{site_nav}

<header class="page-header">
  <div class="container">
    <h1>Pressure Washing in {city}, SC</h1>
    <p>Student-owned and operated. Owner oversight and standards. Fast response. Text for a free estimate at <strong>(803) 272-8118</strong>.</p>
  </div>
</header>

<nav class="breadcrumb container" style="max-width:900px; margin:0 auto; padding:0 1.25rem 1rem;" aria-label="Breadcrumb">
  <a href="/">Home</a> / <span aria-current="page">{city}, SC</span>
</nav>

<main>
  <section class="section-pad-sm">
    <div class="container" style="max-width: 900px;">
      <p style="margin-bottom:1rem;">
        {loc["intro_p1"]}
      </p>
      <p style="margin-bottom:1rem;">
        {loc["intro_p2"]}
      </p>
      <h2 style="font-size:1.35rem; margin:1.5rem 0 0.75rem; color:var(--navy);">Why {city} surfaces need regular cleaning</h2>
      <p style="margin-bottom:1rem;">
        {loc["local_p1"]}
      </p>
      <p style="margin-bottom:1rem;">
        {loc["local_p2"]}
      </p>
      <p style="margin-bottom:1rem;">
        For current per-surface rates, see our <a href="pressure-washing-costs-columbia-sc.html" style="color:var(--blue); font-weight:700;">pressure washing cost guide for Columbia, SC</a> (we serve {city} and the greater Midlands).
      </p>
      <div class="cta-strip-btns" style="justify-content:flex-start; margin-top:1.25rem;">
        <a class="btn btn-primary btn-lg" href="pages/estimate.html"><i class="fa-solid fa-file-invoice-dollar"></i> Request an Estimate</a>
        <a class="btn btn-blue btn-lg" href="sms:8032728118"><i class="fa-solid fa-comment-sms"></i> Text Us</a>
      </div>
    </div>
  </section>

  <section class="section-pad-sm" id="service-areas">
    <div class="container" style="max-width: 900px;">
      <h2 class="section-title" style="font-size:1.7rem;">Service area</h2>
      <p class="section-sub" style="max-width:none;">{city}, SC and surrounding neighborhoods. If you are nearby, text us and we will confirm availability.</p>
      <div style="margin-top:1.25rem; border-radius: var(--radius); overflow:hidden; border: 2px solid var(--border); box-shadow: var(--shadow);">
        <iframe
          title="Map of {city}, SC"
          src="https://www.google.com/maps?q={loc["map_query"]}&output=embed"
          width="100%"
          height="320"
          style="border:0;"
          loading="lazy"
          referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>
    </div>
  </section>

  <section class="faq-section section-pad-sm" id="faqs">
    <div class="container">
      <span class="tag">FAQ</span>
      <h2 class="section-title" style="font-size:1.8rem;">Pressure washing questions in {city}</h2>
      <div class="faq-list" style="margin-top:1.25rem;">
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false">{fq1}<i class="fa-solid fa-chevron-down"></i></button>
          <div class="faq-a">{faq1_answer_html()}</div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false">{loc["faq2_q"]}<i class="fa-solid fa-chevron-down"></i></button>
          <div class="faq-a"><p>{loc["faq2_a"]}</p></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false">{loc["faq3_q"]}<i class="fa-solid fa-chevron-down"></i></button>
          <div class="faq-a"><p>{loc["faq3_a"]}</p></div>
        </div>
      </div>
    </div>
  </section>

{reviews_block}

  <section class="locale-nav section-pad-sm">
    <div class="container" style="max-width: 900px;">
      <h2 class="section-title" style="font-size:1.35rem; margin-bottom:0.75rem;">More service areas</h2>
      <nav class="locale-links" aria-label="Nearby pressure washing service areas">
        {locale_links(slug)}
      </nav>
      <p class="locale-nav-meta">
        <a href="/">Home</a> ·
        <a href="/#gallery">Before &amp; after</a> ·
        <a href="pressure-washing-costs-columbia-sc.html">Pricing guide</a> ·
        <a href="pages/estimate.html">Free estimate</a>
      </p>
    </div>
  </section>
</main>

{site_footer}

<script src="assets/js/main.js"></script>
</body>
</html>
"""


def json_escape(s: str) -> str:
    import json

    return json.dumps(s, ensure_ascii=False)


def main() -> None:
    for loc in LOCALES:
        html = render(loc)
        path = ROOT / f"pressure-washing-{loc['slug']}-sc.html"
        path.write_text(html, encoding="utf-8")
        print("wrote", path.name)


if __name__ == "__main__":
    main()
