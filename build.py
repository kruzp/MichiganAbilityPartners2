#!/usr/bin/env python3
"""Builds the MAP site's HTML pages from one shared header/footer.

Run:  python3 tools/build.py      (writes *.html into the site root)
Edit the page bodies below, then re-run. The output is plain static HTML.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DONATE = "https://secure.qgiv.com/for/michiganabilitypartners/"
OLD = "https://www.mapagency.org"
FB = "https://www.facebook.com/Michigan-Ability-Partners-143128830800/"
IG = "https://www.instagram.com/michiganabilitypartners/"
LI = "https://www.linkedin.com/company/michigan-ability-partners-org/"
VET_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSdZfl0LH-_Tljt6bAVBvBFEwmQUhuw_79Rj9YCwtWRE-f9SfQ/viewform?usp=sf_link"
INKIND_PDF = "https://www.mapagency.org/_files/ugd/412849_132bef592c944ed2a35976db90d595f2.pdf"

# ---- Revenue features (fill these in from MAP's emails before launch) ----
LEGAL = "Michigan Ability Partners"          # full legal name on every giving / ticket / sponsor page
TAX_ID = "38-2595768"
BONFIRE = "https://www.bonfire.com/"         # TODO: MAP's Bonfire store / campaign URL
ROXANN_VIDEO = ""                            # TODO: Roxann's winter message (YouTube/Vimeo embed URL)
BOWLING_VENUE = "Venue to be confirmed"      # TODO: from MAP's event calendar PDF

# ---- MAP's existing photos (served from their current Wix media library) ----
IMG = {
    "logo":     ("412849_9ab34fd9edca444ca0d706979eb10a3b~mv2.png", 664, 306),
    "vets":     ("412849_2981395d7df74994bafe62869c278326~mv2.jpg", 2248, 1937),
    "vetface":  ("412849_554657dec3ba4b589114e98bc4725ae9~mv2.jpg", 305, 461),
    "key":      ("412849_8faede84a94b43c286afdb06afeaaaca~mv2.jpg", 2187, 1794),
    "budget":   ("412849_032d71d49287480989be290ffc4c3fde~mv2.jpg", 940, 788),
    "deck":     ("412849_1c9c87b8945240a0847cb4a8a97b69e2~mv2.jpeg", 4032, 3024),
    "crew":     ("412849_52166d6aac95470db6f742f205734d1e~mv2_d_2048_1536_s_2.jpg", 2048, 1536),
    "green":    ("412849_537e2c62247240efbfdcb552500f7c32~mv2_d_2048_1365_s_2.jpg", 2048, 1365),
    "truck":    ("412849_5d85101a328c457c8618d6901b558a07~mv2.jpg", 2048, 1152),
    "pantry":   ("412849_bcb5fb2feb5c4885952ab2c92c9a7451~mv2.jpg", 922, 925),
    "supplies": ("412849_ddc724c8110043068ccf61ed3fe0aa55~mv2.jpg", 895, 622),
    "ceo":      ("412849_e1d29dd0219c4816bb3f580c3f38d10a~mv2.jpg", 294, 290),
    "apt":      ("412849_5604bc58744e4f4cbbaf7e732f95f346~mv2.jpg", 1200, 696),
    "boxes":    ("412849_f55f9a47869a4aec9a26aaa04e239df4~mv2.jpg", 2333, 3500),
    "shake":    ("412849_a8615811ba2648a4a9de0d4e2aff3ca5~mv2.jpg", 6000, 4000),
}


def local(key):
    """Self-hosted copy made by tools/localize.py, if present."""
    mid = IMG[key][0]
    ext = "png" if mid.endswith(".png") else "jpg"
    f = ROOT / "img" / f"{key}.{ext}"
    return f"img/{key}.{ext}" if f.exists() else None


def wix(key, w, h, q=80):
    mid, ow, oh = IMG[key]
    ext = "png" if mid.endswith(".png") else "jpg"
    return f"https://static.wixstatic.com/media/{mid}/v1/fill/w_{w},h_{h},al_c,q_{q},enc_auto/map-{key}.{ext}"


def img(key, w, h, alt, cls="", eager=False, pos=None):
    """Responsive <img> at aspect w:h, never upscaled past the original."""
    mid, ow, oh = IMG[key]
    scale = min(1.0, ow / w, oh / h)
    w1, h1 = int(w * scale), int(h * scale)
    src = wix(key, w1, h1)
    srcset = f"{src} {w1}w"
    s2 = min(2.0, ow / w, oh / h)
    if s2 > 1.25:
        w2, h2 = int(w * s2), int(h * s2)
        srcset += f", {wix(key, w2, h2)} {w2}w"
    loc = local(key)
    if loc:
        src, srcset = loc, f"{loc} {min(ow, 2000)}w"
        w1, h1 = w, h
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    css = []
    if loc:
        css.append(f"aspect-ratio:{w}/{h};object-fit:cover")
    if pos:
        css.append(f"object-position:{pos}")
    style = f' style="{";".join(css)}"' if css else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{src}" srcset="{srcset}" sizes="(max-width: 900px) 100vw, 50vw" '
            f'width="{w1}" height="{h1}" alt="{alt}" {load} decoding="async"{style}>')


LOGO = local("logo") or f"https://static.wixstatic.com/media/{IMG['logo'][0]}/v1/fit/w_600,h_276,al_c/map-logo.png"

ARR = '<svg class="arr" width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15m-6-6 6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
EXT = '<svg width="14" height="14" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5h11v11M19 5 6 18" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>'

NAV = [
    ("index.html#lines", "Programs", "programs"),
    ("about.html", "About", "about"),
    ("events.html", "Events", "events"),
    ("stories.html", "Stories", "stories"),
    ("get-involved.html", "Get involved", "involved"),
    ("contact.html", "Contact", "contact"),
]

LINES = {
    "housing": dict(n="01", name="Housing", page="housing.html", c="var(--l-housing)",
                    short="Permanent supportive housing, rent help and one-on-one support to stay housed."),
    "payee": dict(n="02", name="Representative Payee", page="representative-payee.html", c="var(--l-payee)",
                  short="An SSA-approved payee who pays the essentials first and helps you budget."),
    "vets": dict(n="03", name="Veteran Services", page="veteran-services.html", c="var(--l-vets)",
                 short="Job training, placement and follow-up for Veterans facing homelessness."),
    "evict": dict(n="04", name="Eviction Prevention", page="eviction-prevention.html", c="var(--l-evict)",
                  short="Up to $3,000 for Washtenaw County renters with an eviction summons."),
}


def head(title, desc):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#16202A">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="{wix('vets', 1200, 630)}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://static.wixstatic.com">
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Mono:wght@400;500;600;700&family=Atkinson+Hyperlegible+Next:ital,wght@0,400;0,500;0,700;0,800;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/map.css">
<script>try{{var t=localStorage.getItem('map-text');if(t)document.documentElement.dataset.text=t}}catch(e){{}}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(active):
    cur = ' aria-current="page"'
    links = "".join(
        f'<a href="{h}"{cur if k == active else ""}>{t}</a>' for h, t, k in NAV)
    prog = "".join(f'<a href="{v["page"]}">{v["name"]}</a>' for v in LINES.values())
    return f"""<div class="band" role="region" aria-label="Quick contact and text size">
  <div class="wrap">
    <div class="band__l"><span>Michigan Ability Partners</span><span class="hide-s" aria-hidden="true">·</span><span class="hide-s">Since 1985</span></div>
    <div class="band__r">
      <div class="band__phones">
        <a href="tel:+17349756880"><span>Ann Arbor</span>734-975-6880</a>
        <a href="tel:+15178415780"><span>Jackson</span>517-841-5780</a>
      </div>
      <div class="textsize" role="group" aria-label="Text size">
        <button type="button" data-size="" aria-pressed="true" aria-label="Normal text">A</button>
        <button type="button" data-size="lg" aria-pressed="false" aria-label="Larger text">A</button>
        <button type="button" data-size="xl" aria-pressed="false" aria-label="Largest text">A</button>
      </div>
    </div>
  </div>
</div>
<header class="hdr">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="Michigan Ability Partners home"><img src="{LOGO}" width="600" height="276" alt="MAP — Michigan Ability Partners"></a>
    <nav class="nav" aria-label="Main">{links}</nav>
    <div class="hdr__cta">
      <a class="btn btn--ghost" href="{DONATE}">Donate</a>
      <a class="btn btn--teal" href="index.html#planner">Find help</a>
    </div>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="drawer"><i></i>Menu</button>
  </div>
</header>
<div class="drawer" id="drawer" aria-hidden="true">
  <div class="drawer__top">
    <img src="{LOGO}" width="600" height="276" alt="" style="height:40px;width:auto;filter:brightness(0) invert(1)">
    <button class="drawer__close" type="button">Close</button>
  </div>
  <nav aria-label="Mobile">
    <a href="index.html#planner">Find help</a>
    <small>Programs</small>
    <div class="sub">{prog}</div>
    <small>Organization</small>
    <a href="about.html">About</a>
    <a href="events.html">Events &amp; tickets</a>
    <a href="stories.html">Stories</a>
    <a href="sponsor.html">Sponsor MAP</a>
    <a href="get-involved.html">Get involved</a>
    <a href="contact.html">Contact</a>
  </nav>
  <div class="drawer__foot">
    <a class="btn btn--paper" href="{DONATE}">Donate to MAP {ARR}</a>
    <a class="btn btn--paper" href="tel:+17349756880" style="background:transparent;color:var(--paper)">Call Ann Arbor · 734-975-6880</a>
    <a class="btn btn--paper" href="tel:+15178415780" style="background:transparent;color:var(--paper)">Call Jackson · 517-841-5780</a>
  </div>
</div>
<main id="main">
"""


def footer():
    prog = "".join(f'<li><a href="{v["page"]}">{v["name"]}</a></li>' for v in LINES.values())
    return f"""</main>
<footer class="ftr">
  <div class="wrap">
    <div class="ftr__top">
      <div class="ftr__brand">
        <a class="logo-chip" href="index.html"><img src="{LOGO}" width="600" height="276" alt="MAP — Michigan Ability Partners" loading="lazy"></a>
        <p>Partnering with Veterans and people with disabilities on their own path to self-sufficiency — since 1985.</p>
        <a class="btn btn--paper" href="{DONATE}">Donate {ARR}</a>
        <div class="ftr__social">
          <a href="{FB}" aria-label="MAP on Facebook"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M14 8.5V6.8c0-.8.5-1 .9-1H17V2.1L14.1 2C10.9 2 10 4.4 10 6.4v2.1H8v3.8h2V22h4v-9.7h2.8l.4-3.8z"/></svg></a>
          <a href="{IG}" aria-label="MAP on Instagram"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.4" cy="6.6" r="1.2" fill="currentColor"/></svg></a>
          <a href="{LI}" aria-label="MAP on LinkedIn"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.5h4V21H3zM9.5 9.5h3.8v1.6h.1c.5-1 1.8-2 3.8-2 4 0 4.8 2.6 4.8 6V21h-4v-5.2c0-1.2 0-2.9-1.8-2.9s-2 1.4-2 2.8V21h-4z"/></svg></a>
        </div>
      </div>
      <div class="ftr__col"><h4>Programs</h4><ul>{prog}</ul></div>
      <div class="ftr__col"><h4>Organization</h4><ul>
        <li><a href="about.html">About MAP</a></li>
        <li><a href="about.html#history">Our history</a></li>
        <li><a href="events.html">Events &amp; tickets</a></li>
        <li><a href="sponsor.html">Sponsor MAP</a></li>
        <li><a href="stories.html">Success stories</a></li>
        <li><a href="get-involved.html#merch">Shop merch</a></li>
        <li><a href="get-involved.html#give">Ways to give</a></li>
        <li><a href="{OLD}/jobopportunities">Job opportunities</a></li>
        <li><a href="contact.html">Contact</a></li>
      </ul></div>
      <div class="ftr__col--wide">
        <h4>Offices</h4>
        <address><b>Ann Arbor</b>3810 Packard St., Suite 260<br>Ann Arbor, MI 48108<br><a href="tel:+17349756880">734-975-6880</a></address>
        <address><b>Jackson</b>216 E. Biddle St., Suite 200<br>Jackson, MI 49203<br><a href="tel:+15178415780">517-841-5780</a></address>
        <address><a href="mailto:info@mapagency.org">info@mapagency.org</a></address>
      </div>
    </div>
  </div>
  <div class="ftr__base">
    <div class="wrap">
      <span>Michigan Ability Partners is a 501(c)(3) nonprofit. Donations are tax deductible to the extent the law allows. Tax ID 38-2595768.</span>
      <span>© <span data-year>2026</span> Michigan Ability Partners</span>
    </div>
  </div>
</footer>
<script src="js/map.js" defer></script>
</body>
</html>
"""


def page(fname, title, desc, active, body):
    html = head(title, desc) + header(active) + body + footer()
    (ROOT / fname).write_text(html, encoding="utf-8")
    print("wrote", fname, f"{len(html)//1024} KB")


def line_card(key, stops):
    L = LINES[key]
    st = "".join(f'<li class="line__stop"><span>{s}</span></li>' for s in stops)
    return f"""<a class="line line--{key}" href="{L['page']}">
  <div class="line__track" aria-hidden="true"><div class="line__rail"></div><ol class="line__stops">{st}</ol><i class="line__train"></i></div>
  <div class="line__card">
    <span class="line__code"><i></i>Line {L['n']}</span>
    <h3>{L['name']}</h3>
    <p>{L['short']}</p>
    <u>Ride this line</u>
  </div>
</a>"""


def transfer(exclude):
    out = []
    for k, L in LINES.items():
        if k == exclude:
            continue
        out.append(f"""<a class="t-{k}" href="{L['page']}" style="--c:{L['c']}">
  <span class="line__code"><i style="background:{L['c']}"></i>Transfer · Line {L['n']}</span>
  <h3>{L['name']}</h3><p>{L['short']}</p></a>""")
    return "\n".join(out)


def ptitle(crumb, kicker, h1, lede, color="var(--teal)", chip=True):
    chip_html = f'<span class="ptitle__chip"><i></i>{kicker}</span>' if chip else kicker
    return f"""<section class="ptitle" style="--c:{color}">
  <div class="wrap">
    <div class="crumbs"><a href="index.html">Home</a> / {crumb}</div>
    <div class="kicker">{chip_html}</div>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
  </div>
  <div class="ptitle__line" aria-hidden="true"></div>
</section>
"""


# =====================================================================
# HOME
# =====================================================================
HERO_ROUTE = """<svg class="hero__route" viewBox="0 0 500 440" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">
    <g stroke="#F5F1E8" stroke-width="13">
      <path class="hr" d="M-20 386 H430 L484 440"/><path class="hr" d="M-20 395 H370 L415 440"/>
      <path class="hr" d="M-20 404 H310 L346 440"/><path class="hr" d="M-20 413 H250 L277 440"/>
    </g>
    <g stroke-width="7">
      <path class="hr" stroke="#0E6A7A" d="M-20 386 H430 L484 440"/><path class="hr" stroke="#5A4FBF" d="M-20 395 H370 L415 440"/>
      <path class="hr" stroke="#A8432E" d="M-20 404 H310 L346 440"/><path class="hr" stroke="#B87810" d="M-20 413 H250 L277 440"/>
    </g>
  </g>
  <g class="hr-pin">
    <rect x="34" y="330" width="96" height="24" rx="3" fill="#16202A"/>
    <text x="82" y="346.5" text-anchor="middle" fill="#F5F1E8" font-family="Atkinson Hyperlegible Mono, monospace" font-size="10.5" font-weight="600" letter-spacing=".8">YOU ARE HERE</text>
    <path d="M58 354 L64 362 L70 354" fill="#16202A"/>
    <circle cx="64" cy="399" r="15" fill="#F5F1E8" stroke="#16202A" stroke-width="5"/>
  </g>
</svg>"""

home = f"""
<section class="hero">
  <div class="wrap hero__grid">
    <div class="hero__copy">
      <div class="kicker rv"><span>Michigan Ability Partners</span><i class="dot"></i><span>Ann Arbor &amp; Jackson</span></div>
      <h1 class="h-xl rv rv-d1">Navigation for <em>real life.</em></h1>
      <p class="lede rv rv-d2">For 40 years, MAP has partnered with Veterans and people with disabilities on their own path to a stable home, steady income and a life they direct.</p>
      <div class="hero__ctas rv rv-d3">
        <a class="btn btn--teal" href="#planner">Find the right program {ARR}</a>
        <a class="btn btn--ghost" href="get-involved.html">Support MAP</a>
      </div>
    </div>
    <figure class="hero__fig atlas" style="margin-bottom:0">
      <div class="atlas__ticks" aria-hidden="true">
        <div class="t t--top"><span>A</span><span>B</span><span>C</span><span>D</span><span>E</span></div>
        <div class="t t--left"><span>1</span><span>2</span><span>3</span><span>4</span></div>
      </div>
      <div class="hero__photo">
        {img('vets', 1000, 880, 'Three Veterans in service caps smiling together at a MAP community event', eager=True, pos='50% 20%')}
        {HERO_ROUTE}
      </div>
      <figcaption class="hero__cap"><span>Fig. 1 — Veterans at a MAP community event</span><span>Four lines, one direction: home.</span></figcaption>
    </figure>
  </div>
</section>

<nav class="doors" aria-label="Start here">
  <a class="door" href="#planner"><span class="door__num">A</span><div><h3>I need help</h3><p>Answer two questions and we'll show you your route.</p></div><span class="door__arr">{ARR}</span></a>
  <a class="door" href="get-involved.html"><span class="door__num">B</span><div><h3>I want to help</h3><p>Give, volunteer, or bring MAP to your group.</p></div><span class="door__arr">{ARR}</span></a>
</nav>

<section class="next" aria-label="Next event">
  <div class="wrap next__in">
    <span class="next__lbl mono">Next departure</span>
    <div class="next__ev"><b>Impact Championship Bowling &amp; Billiards</b><span>Thu · April 8, 2027 · 5–9 PM</span></div>
    <div class="next__cd mono" data-countdown="2027-04-08T17:00:00-04:00"><b data-cd="d">--</b> days</div>
    <div class="next__acts"><a class="btn btn--paper" href="events.html#bowling">Get tickets {ARR}</a><a class="tlink tlink--ink" href="events.html">All events</a></div>
  </div>
</section>

<section class="sec" id="lines">
  <div class="wrap">
    <div class="sec-head">
      <div class="kicker rv">The system map</div>
      <h2 class="h-l rv">Four lines. One direction: a stable life you lead.</h2>
      <p class="lede rv" style="max-width:none">Every person who comes to MAP starts somewhere different. Our programs are built like a transit system — clear stops, real connections, and staff who ride alongside you.</p>
    </div>
    <div class="lines" data-lines>
      <div class="lines__junction" aria-hidden="true"><svg></svg><span class="lines__origin">You are here</span></div>
      <div class="lines__rows">
        {line_card('housing', ['HAWC referral', 'Find a home', 'Move-in help', 'Ongoing support', 'Stay housed'])}
        {line_card('payee', ['Apply', 'First meeting', 'Budget together', 'Bills paid first', 'Stability'])}
        {line_card('vets', ['Referral', 'Job readiness', 'Training', 'Placement', 'Steady work'])}
        {line_card('evict', ['Court summons', 'Inquiry form', 'Team review', 'Up to $3,000', 'Stay home'])}
      </div>
    </div>
  </div>
</section>

<section class="sec sec--ink" id="planner">
  <div class="wrap">
    <div class="sec-head">
      <div class="kicker rv">Trip planner</div>
      <h2 class="h-l rv">Where are you starting from?</h2>
      <p class="lede rv" style="max-width:none">Two questions. We'll point you to the program that fits, what to bring, and who to call first. Nothing you choose here is saved or sent.</p>
    </div>
    <div class="planner">
      <form class="planner__q" data-planner onsubmit="return false">
        <fieldset>
          <legend><span class="n">01</span>Which county do you live in?</legend>
          <div class="chips">
            <label class="chip"><input type="radio" name="county" value="Washtenaw"><span>Washtenaw</span></label>
            <label class="chip"><input type="radio" name="county" value="Jackson"><span>Jackson</span></label>
            <label class="chip"><input type="radio" name="county" value="Livingston"><span>Livingston</span></label>
            <label class="chip"><input type="radio" name="county" value="Oakland"><span>Oakland</span></label>
            <label class="chip"><input type="radio" name="county" value="Wayne"><span>Wayne</span></label>
            <label class="chip"><input type="radio" name="county" value="other"><span>Somewhere else</span></label>
          </div>
        </fieldset>
        <fieldset>
          <legend><span class="n">02</span>Which sounds most like you right now?</legend>
          <div class="opts">
            <label class="opt"><input type="radio" name="need" value="evict"><span><span><b>I got a court summons for eviction</b><small>Because of rent I haven't been able to pay.</small></span></span></label>
            <label class="opt"><input type="radio" name="need" value="housing"><span><span><b>I'm homeless or about to lose my home</b><small>And I live with a disability.</small></span></span></label>
            <label class="opt"><input type="radio" name="need" value="vets"><span><span><b>I'm a Veteran and I want to get back to work</b><small>Housing is unstable or I'm at risk of losing it.</small></span></span></label>
            <label class="opt"><input type="radio" name="need" value="payee"><span><span><b>I need help managing my benefits</b><small>Social Security, SSI or VA money — bills, budgeting, rent.</small></span></span></label>
            <label class="opt"><input type="radio" name="need" value="unsure"><span><span><b>I'm not sure — I just need to talk to someone</b><small>That's a good place to start, too.</small></span></span></label>
          </div>
        </fieldset>
      </form>
      <div class="planner__a" aria-live="polite">
        <div class="ticket" data-ticket>
          <div class="ticket__band"><span>Your route</span><span data-tk-county>—</span></div>
          <div class="ticket__empty">
            <svg width="64" height="64" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="26" r="10" fill="none" stroke="#5F6A74" stroke-width="4"/><path d="M32 36v20" stroke="#5F6A74" stroke-width="4" stroke-linecap="round"/><path d="M14 56h36" stroke="#CFC6B2" stroke-width="4" stroke-linecap="round" stroke-dasharray="2 8"/></svg>
            <p style="margin:0">Choose your county and situation.<br>Your route appears here.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec" id="impact">
  <div class="wrap">
    <div class="sec-head">
      <div class="kicker rv">Legend · Our impact</div>
      <h2 class="h-l rv">The route works.</h2>
      <p class="lede rv" style="max-width:none">More than 1,000 people find their footing with MAP every year. These are the numbers we hold ourselves to.</p>
    </div>
    <div class="legend-grid">
      <div class="stat rv"><div class="stat__n" data-count="99.4" data-dec="1">99.4<small>%</small></div><p>of Representative Payee participants kept their housing.</p><div class="scalebar" data-pct="99.4"><i></i><i></i><i></i><i></i><i></i><span class="scalebar__fill"></span></div><div class="scalebar__lbl"><span>0</span><span>50</span><span>100</span></div></div>
      <div class="stat rv rv-d1"><div class="stat__n" data-count="96">96<small>%</small></div><p>of housing program participants stayed in permanent housing.</p><div class="scalebar" data-pct="96"><i></i><i></i><i></i><i></i><i></i><span class="scalebar__fill"></span></div><div class="scalebar__lbl"><span>0</span><span>50</span><span>100</span></div></div>
      <div class="stat rv rv-d2"><div class="stat__n" data-count="100">100<small>%</small></div><p>of Veteran and housing participants kept or grew their income.</p><div class="scalebar" data-pct="100"><i></i><i></i><i></i><i></i><i></i><span class="scalebar__fill"></span></div><div class="scalebar__lbl"><span>0</span><span>50</span><span>100</span></div></div>
      <div class="stat rv"><div class="stat__n" data-count="63">63<small>%</small></div><p>of vocational clients held stable employment.</p></div>
      <div class="stat rv rv-d1"><div class="stat__n" data-count="36545">36,545</div><p>pounds of food distributed to the people we serve.</p></div>
      <div class="stat rv rv-d2"><div class="stat__n" data-count="1000" data-plus>1,000<small>+</small></div><p>people helped every year across five counties.</p></div>
      <div class="stat rv rv-d3"><div class="stat__n" data-count="38">38</div><p>affordable homes MAP owns and operates at six sites.</p></div>
    </div>
  </div>
</section>

<section class="sec sec--ink sec--tight">
  <div class="wrap quote">
    <div class="quote__mark" aria-hidden="true">&ldquo;</div>
    <blockquote class="rv">
      <p>Having a viable contact outside of my home reminding me that things would get better.</p>
      <cite>— M., MAP participant</cite>
    </blockquote>
  </div>
</section>

<section class="sec" id="where">
  <div class="wrap">
    <div class="sec-head">
      <div class="kicker rv">Service area · Southeast Michigan</div>
      <h2 class="h-l rv">Two offices. Five counties.</h2>
      <p class="lede rv" style="max-width:none">Our team works across Jackson, Livingston, Oakland, Wayne and Washtenaw counties. Walk in, call, or we'll come to you.</p>
    </div>
    <div class="where">
      <div class="where__map rv">
        <div class="tiles" role="img" aria-label="Schematic map of southeast Michigan counties. MAP serves Livingston, Oakland, Jackson, Washtenaw and Wayne, with offices in Jackson and Washtenaw.">
          <div class="tile tile--empty"></div>
          <div class="tile">Clinton</div><div class="tile">Shiawassee</div><div class="tile">Genesee</div><div class="tile">Lapeer</div>
          <div class="tile">Eaton</div><div class="tile">Ingham</div>
          <div class="tile tile--on">Livingston<small>Served</small></div>
          <div class="tile tile--on">Oakland<small>Served</small></div>
          <div class="tile">Macomb</div>
          <div class="tile">Calhoun</div>
          <div class="tile tile--on tile--hq">Jackson<small>Office</small><i class="tile__pin"></i></div>
          <div class="tile tile--on tile--hq">Washtenaw<small>Office · 38 homes</small><i class="tile__pin"></i></div>
          <div class="tile tile--on">Wayne<small>Served</small></div>
          <div class="tile lake" style="background:transparent">Lake St. Clair</div>
          <div class="tile">Branch</div><div class="tile">Hillsdale</div><div class="tile">Lenawee</div><div class="tile">Monroe</div>
          <div class="tile lake" style="background:transparent">Lake Erie</div>
        </div>
        <div class="tiles__key"><span><i style="background:var(--ink)"></i>MAP office</span><span><i style="background:var(--teal)"></i>Service area</span><span><i style="background:var(--paper-3)"></i>Neighboring county</span></div>
      </div>
      <div class="where__offices">
        <div class="office rv" data-office="aa">
          <h3>Ann Arbor</h3><span class="office__status" data-status>Hours</span>
          <address>3810 Packard St., Suite 260, Ann Arbor, MI 48108</address>
          <dl class="office__rows"><dt>Hours</dt><dd>Mon, Wed, Fri · 8:30–4:30<br><span class="muted">Closed 12–1 for lunch</span></dd><dt>Phone</dt><dd>734-975-6880</dd></dl>
          <div class="office__acts"><a class="btn" href="tel:+17349756880">Call 734-975-6880</a><a class="btn btn--ghost" href="https://maps.google.com/?q=3810+Packard+St+Suite+260+Ann+Arbor+MI+48108">Directions</a></div>
        </div>
        <div class="office rv rv-d1" data-office="jx">
          <h3>Jackson</h3><span class="office__status" data-status>Hours</span>
          <address>216 E. Biddle St., Suite 200, Jackson, MI 49203</address>
          <dl class="office__rows"><dt>Hours</dt><dd>Mon &amp; Fri · 10:00–3:00<br><span class="muted">Wednesday by appointment</span></dd><dt>Phone</dt><dd>517-841-5780</dd></dl>
          <div class="office__acts"><a class="btn" href="tel:+15178415780">Call 517-841-5780</a><a class="btn btn--ghost" href="https://maps.google.com/?q=216+E+Biddle+St+Suite+200+Jackson+MI+49203">Directions</a></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec sec--alt" id="involve">
  <div class="wrap">
    <div class="sec-head">
      <div class="kicker rv">Get involved</div>
      <h2 class="h-l rv">Built by neighbors.</h2>
      <p class="lede rv" style="max-width:none">Volunteer crews build decks and plant gardens at our homes. Local businesses move families in. Donors keep the lights on. There's a stop on this line for you.</p>
    </div>
    <div class="mosaic rv">
      <figure>{img('deck', 1100, 900, 'Volunteers standing on a newly built wooden deck at a MAP home')}<figcaption>Volunteer day · deck build</figcaption></figure>
      <figure>{img('green', 800, 520, 'A large group of volunteers in matching green shirts at a MAP property')}<figcaption>Washtenaw County volunteers</figcaption></figure>
      <figure>{img('truck', 800, 520, 'MAP staff with a Two Men and a Truck crew beside their moving truck')}<figcaption>Community partners</figcaption></figure>
    </div>
    <div class="acts3">
      <a class="act" href="{DONATE}"><span class="mono">Give</span><h3>Make a gift</h3><p>Tax-deductible support for housing, payee and Veteran programs.</p><u>Donate securely</u></a>
      <a class="act" href="get-involved.html#volunteer"><span class="mono">Volunteer</span><h3>Join a crew</h3><p>Office, food bank, landscaping, workshops, committees and events.</p><u>See roles</u></a>
      <a class="act" href="get-involved.html#give"><span class="mono">Organize</span><h3>Host a drive</h3><p>Rally your company or congregation around a supplies drive or day of service.</p><u>Ways to give</u></a>
    </div>
  </div>
</section>
"""
page("index.html", "Michigan Ability Partners — Navigation for Real Life",
     "MAP partners with Veterans and people with disabilities in southeast Michigan on housing, representative payee, employment and eviction prevention.",
     "home", home)


# =====================================================================
# PROGRAM PAGES
# =====================================================================
def program(key, crumb, h1, lede, photo, photo_alt, cap, intro, who_title, who, stops_title, stops, board, faq="", facts="", extra=""):
    L = LINES[key]
    who_li = "".join(f"<li>{w}</li>" for w in who)
    st = "".join(f"<li><div><h3>{a}</h3><p>{b}</p></div></li>" for a, b in stops)
    return ptitle(crumb, f"Line {L['n']} · {L['name']}", h1, lede, L['c']) + f"""
<section class="sec" style="--c:{L['c']}">
  <div class="wrap intro">
    <figure class="intro__fig rv">{photo}<figcaption>{cap}</figcaption></figure>
    <div class="intro__txt">
      {intro}
      <h2 class="h-s" style="margin-top:2.5rem">{who_title}</h2>
      <ul class="checks">{who_li}</ul>
    </div>
  </div>
</section>
{facts}
<section class="sec sec--alt" style="--c:{L['c']}">
  <div class="wrap split">
    <div><div class="kicker rv">Stops on this line</div><h2 class="h-l rv" style="margin-top:1rem">{stops_title}</h2></div>
    <ol class="stops" data-stops><span class="stops__rail" aria-hidden="true"></span>{st}</ol>
  </div>
</section>
{extra}
<section class="sec" id="apply" style="--c:{L['c']}">
  <div class="wrap">
    {board}
  </div>
</section>
{faq}
<section class="sec sec--alt sec--tight">
  <div class="wrap">
    <div class="kicker" style="margin-bottom:1.5rem">Other lines</div>
    <div class="transfer">{transfer(key)}</div>
  </div>
</section>
"""


housing = program(
    "housing", "Programs / Housing",
    "Homelessness should be rare, brief and one-time.",
    "Permanent supportive housing with subsidized rent, a case manager in your corner, and help with the everyday skills that keep a home.",
    img("key", 900, 1125, "A hand turning a key in the front door of a home"),
    "", "Fig. — Move-in day starts the route; staying housed is the destination.",
    """<p>A stable home is hard to keep when you're also facing a disability, a mental health condition, substance use or a past conviction. MAP helps you find the right place, secure the money to get started, and keep it.</p>
<p>Staff meet one-on-one with each participant on daily living skills — budgeting, cooking, cleaning, hygiene and keeping appointments — through regular check-ins that fit your goals.</p>""",
    "Permanent supportive housing is for people who are",
    ["Experiencing homelessness", "Low-income", "Living with a documented disability"],
    "From referral to a home you keep.",
    [("Connect with HAWC", "Housing Access for Washtenaw County is the front door. MAP receives its housing referrals from HAWC, so start there."),
     ("Find the right place", "Your MAP team helps you find housing that suits you — including the 38 affordable homes MAP owns and operates at six sites."),
     ("Get moved in", "We help secure the financial assistance to get started: deposits, first month, the basics."),
     ("Build daily routines", "One-on-one coaching on budgeting, cooking, cleaning, hygiene and managing appointments."),
     ("Stay housed", "Subsidized rent and long-term case management to break the cycle of chronic homelessness for good.")],
    f"""<div class="board" style="--c:var(--l-housing)">
  <div class="board__main">
    <div class="kicker">Board here</div>
    <h2 class="h-m">Start with HAWC.</h2>
    <p>MAP can only take housing referrals that come through Housing Access for Washtenaw County. Call HAWC first — they're also the number to call for anyone in a housing crisis.</p>
    <div class="board__acts"><a class="btn btn--paper" href="tel:+17349611999">Call HAWC · (734) 961-1999</a><a class="btn btn--paper" style="background:transparent;color:var(--paper)" href="https://housingaccess.net">housingaccess.net {EXT}</a></div>
  </div>
  <div class="board__side">
    <div><div class="lbl">Housing crisis line</div><a class="big" href="tel:+17349611999">(734) 961-1999</a></div>
    <div><div class="lbl">Questions for MAP</div><a class="big" style="font-size:1.6rem" href="tel:+17349756880">734-975-6880</a></div>
  </div>
</div>""",
    facts=f"""<section class="sec sec--tight"><div class="wrap"><div class="facts">
  <div class="fact rv"><b>96%</b><span>of housing participants stayed in permanent housing</span></div>
  <div class="fact rv rv-d1"><b>38</b><span>affordable homes MAP owns and operates</span></div>
  <div class="fact rv rv-d2"><b>6</b><span>sites across Washtenaw County, with more in development</span></div>
</div></div></section>""")
page("housing.html", "Housing — Michigan Ability Partners",
     "Permanent supportive housing, subsidized rent and one-on-one support for people with disabilities experiencing homelessness in Washtenaw County.",
     "programs", housing)

payee = program(
    "payee", "Programs / Representative Payee",
    "Your benefits, working for you.",
    "MAP is an SSA-approved representative payee. We receive your benefits, pay the essentials first, and help you build a budget that holds.",
    img("budget", 900, 760, "A monthly budget worksheet with a pen and calculator"),
    "", "Fig. — Rent, utilities and food come first. Always.",
    """<p>If budgeting or paying bills on time is a struggle — because of a disability, a mental health condition, or just a hard season — a representative payee can take the weight off. As your payee, MAP is required to act in your best interest at all times.</p>
<p>We started this program in 1989 and still offer the financial education and credit repair that came with it.</p>""",
    "This line is for",
    ["People with disabilities", "Senior citizens", "People receiving Social Security, SSI or Veterans Administration benefits",
     "Anyone at risk of losing housing, utilities or other essentials", "People referred by a doctor, caseworker or the SSA"],
    "How the program works.",
    [("You're matched with a payee", "One dedicated MAP representative payee who knows your situation."),
     ("Bring your bills to the first meeting", "Copies of your essential bills — rent, utilities, anything recurring."),
     ("Build a budget together", "We draft a preliminary budget with you, not for you."),
     ("Essentials paid first", "Your SSA or SSI check comes to MAP. Rent, utilities and food are paid, then you receive your personal spending money."),
     ("Adjust as life changes", "Regular meetings keep the budget current. Every dollar is recorded.")],
    f"""<div class="board" style="--c:var(--l-payee)">
  <div class="board__main">
    <div class="kicker">Board here · Accepting applications now</div>
    <h2 class="h-m">Apply any time.</h2>
    <p>Print the application, fill it out, and bring it to either office — or call and we'll walk you through it.</p>
    <div class="board__acts"><a class="btn btn--paper" href="{OLD}/representativepayee">Get the application {EXT}</a><a class="btn btn--paper" style="background:transparent;color:var(--paper)" href="tel:+17349756880">Call Ann Arbor</a></div>
  </div>
  <div class="board__side">
    <div><div class="lbl">Ann Arbor</div><a class="big" href="tel:+17349756880">734-975-6880</a></div>
    <div><div class="lbl">Jackson</div><a class="big" href="tel:+15178415780">517-841-5780</a></div>
  </div>
</div>""",
    facts=f"""<section class="sec sec--tight"><div class="wrap"><div class="facts">
  <div class="fact rv"><b>99.4%</b><span>of payee participants kept their housing</span></div>
  <div class="fact rv rv-d1"><b>1989</b><span>the year MAP launched this program</span></div>
  <div class="fact rv rv-d2"><b>1 : 1</b><span>a dedicated payee for every participant</span></div>
</div></div></section>""")
page("representative-payee.html", "Representative Payee — Michigan Ability Partners",
     "MAP is an SSA-approved representative payee helping people with disabilities, seniors and benefit recipients pay essentials first and budget for stability.",
     "programs", payee)

vets = program(
    "vets", "Programs / Veteran Services",
    "You served. Now let's get you working.",
    "The Homeless Veterans' Reintegration Program (HVRP) helps Veterans facing homelessness break down the barriers between them and a steady job.",
    img("vets", 900, 1125, "Three Veterans in service caps and uniforms smiling together", pos="40% 30%"),
    "", "Fig. — Funded by the U.S. Department of Labor, VETS.",
    """<p>HVRP is funded by the U.S. Department of Labor's Veterans' Employment and Training Service, and it's the only federal program focused entirely on employment for homeless Veterans. MAP has run it since 2015.</p>
<p>We match your strengths and interests to local openings, partner with employers who hire inclusively, and stay with you through the first weeks and months on the job.</p>""",
    "You may be eligible if you",
    ["Served in the U.S. military and did not receive a dishonorable discharge", "Are homeless or at risk of homelessness",
     "Are ready to re-enter the workforce", "Are working with HUD-VASH or SSVF, or live in transitional housing or a GPD program"],
    "From referral to steady work.",
    [("Refer in", "Fill out the referral form or call either office. We'll set up a first conversation."),
     ("Clear the barriers", "Career counseling and goal setting — and connections to housing and support services when you need them."),
     ("Get job-ready", "Résumé support, interview practice, job skills and workplace readiness."),
     ("Get placed", "We match you with employers who want Veterans on their team, and help you navigate hiring."),
     ("Keep it", "Follow-up coaching on time management, communication and fitting in at a new job.")],
    f"""<div class="board" style="--c:var(--l-vets)">
  <div class="board__main">
    <div class="kicker">Board here</div>
    <h2 class="h-m">Start your referral.</h2>
    <p>The online referral form takes a few minutes. Case managers and Veterans can both use it. Prefer to talk? Call either office.</p>
    <div class="board__acts"><a class="btn btn--paper" href="{VET_FORM}">Open the referral form {EXT}</a></div>
  </div>
  <div class="board__side">
    <div><div class="lbl">Ann Arbor</div><a class="big" href="tel:+17349756880">734-975-6880</a></div>
    <div><div class="lbl">Jackson</div><a class="big" href="tel:+15178415780">517-841-5780</a></div>
  </div>
</div>""",
    facts=f"""<section class="sec sec--tight"><div class="wrap"><div class="facts">
  <div class="fact rv"><b>100%</b><span>of Veteran and housing participants kept or grew their income</span></div>
  <div class="fact rv rv-d1"><b>192</b><span>Veterans enrolled in MAP's first year of HVRP</span></div>
  <div class="fact rv rv-d2"><b>$300K</b><span>from KeyBank's Key for Vets for Veteran housing</span></div>
</div></div></section>""")
page("veteran-services.html", "Veteran Services — Michigan Ability Partners",
     "HVRP job training, placement and follow-up support for Veterans experiencing or at risk of homelessness in southeast Michigan.",
     "programs", vets)

evict_form = f"""<section class="sec sec--alt" id="inquiry">
  <div class="wrap split">
    <div>
      <div class="kicker rv">Step 01 · Initial inquiry</div>
      <h2 class="h-l rv" style="margin:1rem 0 1.25rem">Check if you qualify.</h2>
      <p class="rv">This short inquiry tells our team the basics. A team member reviews it and contacts you about next steps.</p>
      <p class="muted rv" style="font-size:1rem">Have your court summons nearby. You may be asked for a copy.</p>
    </div>
    <form class="form" data-evict novalidate>
      <div class="field"><label for="e-name">Full name</label><input id="e-name" name="name" autocomplete="name" required></div>
      <div class="field"><label for="e-phone">Phone</label><input id="e-phone" name="phone" type="tel" autocomplete="tel" required></div>
      <div class="field full"><label for="e-email">Email <span class="muted">(optional)</span></label><input id="e-email" name="email" type="email" autocomplete="email"></div>
      <div class="field full"><label for="e-addr">Rental address</label><input id="e-addr" name="address" autocomplete="street-address" required><small>Must be in Washtenaw County.</small></div>
      <div class="field full"><span style="display:block;font-weight:700;margin-bottom:.4rem">Did you receive a court summons for eviction for nonpayment of rent?</span>
        <div class="radios"><label><input type="radio" name="summons" value="Yes"> Yes</label><label><input type="radio" name="summons" value="No"> No</label></div></div>
      <div class="field full"><label for="e-owed">Total amount owed</label><input id="e-owed" name="owed" inputmode="decimal" placeholder="$"><small>Assistance is up to $3,000.</small></div>
      <div class="form__msg" data-msg role="status"></div>
      <div class="full"><button class="btn btn--teal" type="submit">Send my inquiry {ARR}</button><p class="muted" style="font-size:.875rem;margin-top:.75rem">Opens your email app with your answers filled in, addressed to info@mapagency.org.</p></div>
    </form>
  </div>
</section>"""

evict = program(
    "evict", "Programs / Eviction Prevention",
    "Got a summons? You still have a stop before eviction.",
    "Emergency rent assistance — up to $3,000 — for qualified Washtenaw County residents facing eviction for nonpayment of rent.",
    img("apt", 900, 760, "A bright living room with keys hanging by the door"),
    "", "Fig. — The goal is simple: stay in your home.",
    """<p>When rent falls behind, an eviction summons can feel like the end of the line. It doesn't have to be. MAP's Eviction Prevention Assistance helps qualified households in Washtenaw County catch up and stay put.</p>
<p>Assistance depends on eligibility and available funds, and processing times vary with how many applications we receive — so start as soon as you get your summons.</p>""",
    "To apply you must",
    ["Live in Washtenaw County", "Have received a court summons for eviction due to nonpayment of rent",
     "Owe $3,000 or less in total — larger balances can't be approved"],
    "What happens after you apply.",
    [("Fill out the inquiry", "The short form below helps us see whether you're likely eligible."),
     ("A team member reviews it", "We look at your information and contact you about next steps."),
     ("Share your summons", "You may be asked for a copy of the court summons during the application."),
     ("Assistance is decided", "Eligible households may receive up to $3,000, depending on available funds."),
     ("Stay in your home", "And if money management is the root of it, ask about our Representative Payee line.")],
    f"""<div class="board" style="--c:var(--l-evict)">
  <div class="board__main">
    <div class="kicker">Board here</div>
    <h2 class="h-m">Start the inquiry today.</h2>
    <p>Time matters with a court date. Fill out the inquiry, or call our Ann Arbor office and we'll help you through it.</p>
    <div class="board__acts"><a class="btn btn--paper" href="#inquiry">Go to the inquiry form</a></div>
  </div>
  <div class="board__side" data-dark>
    <div><div class="lbl">Ann Arbor office</div><a class="big" href="tel:+17349756880">734-975-6880</a></div>
    <div><div class="lbl">Up to</div><span class="big">$3,000</span></div>
  </div>
</div>""",
    faq="""<section class="sec sec--tight"><div class="wrap split">
  <div><div class="kicker">Questions</div><h2 class="h-m" style="margin-top:1rem">Before you apply.</h2></div>
  <div class="faq">
    <details><summary>I live outside Washtenaw County. Can I apply?</summary><p>This fund is for Washtenaw County residents only. Call our Ann Arbor or Jackson office and we'll help you find the right next call — or dial 2-1-1 for local emergency rental help.</p></details>
    <details><summary>I owe more than $3,000. Should I still apply?</summary><p>Applications with an outstanding balance over $3,000 are denied. Call us anyway — our staff may know of other options.</p></details>
    <details><summary>I'm behind on rent but haven't received a summons.</summary><p>This program requires a court summons for nonpayment of rent. If you receive Social Security, SSI or VA benefits, our Representative Payee program can help you get ahead of it.</p></details>
    <details><summary>How long does it take?</summary><p>Processing times vary with the number of applications and available funding. Apply as soon as you can.</p></details>
  </div>
</div></section>""",
    extra=evict_form,
    facts=f"""<section class="sec sec--tight"><div class="wrap"><div class="facts">
  <div class="fact rv"><b>$3,000</b><span>maximum assistance per eligible household</span></div>
  <div class="fact rv rv-d1"><b>1</b><span>county served: Washtenaw</span></div>
  <div class="fact rv rv-d2"><b>2</b><span>steps to start: inquiry, then review</span></div>
</div></div></section>""")
page("eviction-prevention.html", "Eviction Prevention — Michigan Ability Partners",
     "Up to $3,000 in eviction prevention assistance for qualified Washtenaw County residents with a court summons for nonpayment of rent.",
     "programs", evict)


# =====================================================================
# ABOUT
# =====================================================================
HIST = [
    ("1985", "The line opens", "MAP launches Michigan's first vocational program to close a segregated workshop, moving every participant into a community job.", True),
    ("1986", "Supported employment", "MAP joins the first Supported Employment Initiative and helps 100 people with severe disabilities find community jobs.", False),
    ("1988", "Downriver Ability Project", "A Wayne County program for formerly institutionalized people with severe disabilities.", False),
    ("1989", "Representative Payee begins", "Born from a national NIMH project on mental health and homelessness, with financial education and credit repair built in.", True),
    ("1995", "Housing joins the map", "Vocational programs reach 1,500+ students in three counties, and MAP becomes one of three local HUD-funded permanent supportive housing providers.", False),
    ("1996", "WISH Intensive Services", "Treatment, housing, employment training and financial management under one roof for people 17 and older.", False),
    ("1999", "Critical Intervention Project", "With the University of Michigan and the VA, MAP houses 12 chronically homeless men — results later replicated nationwide. Homezone opens for Veterans.", True),
    ("2002", "The ICAN Building System", "Homeless participants help build homes with a green prefabricated system, nominated for a HUD Best Practice Award.", False),
    ("2005", "REACH is founded", "With unemployment near 10%, MAP creates work crews, two social enterprises and REACH, its affordable-housing subsidiary.", False),
    ("2009", "Whispering Creek", "REACH's first rehab becomes the community's first LEED-certified affordable housing renovation.", False),
    ("2014", "Supportive Services for Veteran Families", "VA funding lets MAP house up to 94 Veterans a year.", True),
    ("2015", "HVRP and HireMIVet", "A Department of Labor grant enrolls 192 Veterans in employment services, and the HireMIVet job-matching event begins.", False),
    ("2018", "Key for Vets", "KeyBank invests $300,000 in MAP's Veteran housing programs.", False),
    ("2024", "Mapleview renewed", "A major renovation of Mapleview follows Whispering Creek's in 2020.", False),
    ("2025", "Forty years", "MAP marks 40 years of service, with property improvements continuing into 2026.", True),
]
hist_html = "".join(
    f'<div class="yr{" yr--major" if m else ""}"><div class="yr__y">{y}</div><span class="yr__dot" aria-hidden="true"></span><div class="yr__txt"><h3>{t}</h3><p>{d}</p></div></div>'
    for y, t, d, m in HIST)

about = ptitle("About", "About MAP · Est. 1985", "Forty years of walking alongside.",
               "MAP was founded to help Veterans and people with disabilities live more independent lives. That's still the whole job.", "var(--violet)", chip=False) + f"""
<section class="sec">
  <div class="wrap split">
    <div><div class="kicker rv">Mission</div></div>
    <div>
      <p class="rv" style="font-size:clamp(1.6rem,3vw,2.5rem);font-weight:700;letter-spacing:-0.025em;line-height:1.15">Michigan Ability Partners partners with Veterans and people with disabilities in support of their self-directed transformation to self-sufficiency.</p>
      <p class="rv measure" style="margin-top:2rem">Our vision is to equitably provide high-quality housing, vocational and representative payee programs and services that increase the self-sufficiency of the people we serve — and to be recognized across the region as a leading provider that works alongside other organizations to make every service better.</p>
    </div>
  </div>
</section>

<section class="sec sec--ink sec--tight">
  <div class="wrap leader">
    {img('ceo', 440, 440, 'Portrait of Jan Little, CEO of Michigan Ability Partners')}
    <blockquote class="rv"><p>&ldquo;MAP gives Veterans and others with disabilities hope for a better future!&rdquo;</p><cite class="kicker" style="color:rgba(245,241,232,.7)">Jan Little · Chief Executive Officer</cite></blockquote>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><div class="kicker">Core values</div><h2 class="h-l">How we ride.</h2></div>
    <ol class="values">
      <li><div><h3 class="h-s">Treat others as you'd want to be treated.</h3></div></li>
      <li><div><h3 class="h-s">Every path is personal.</h3><p class="muted" style="margin:.4rem 0 0">Each participant has unique goals, strengths and needs. We support their route to independence.</p></div></li>
      <li><div><h3 class="h-s">We serve the whole community.</h3><p class="muted" style="margin:.4rem 0 0">Sharing resources and aligning goals with partners across the region.</p></div></li>
      <li><div><h3 class="h-s">Our people are our strength.</h3><p class="muted" style="margin:.4rem 0 0">Employees and volunteers deserve training, support and fair compensation.</p></div></li>
      <li><div><h3 class="h-s">Every dollar is accounted for.</h3><p class="muted" style="margin:.4rem 0 0">We steward grants, donations and fees with transparency and accountability.</p></div></li>
      <li><div><h3 class="h-s">Lived experience shapes the work.</h3><p class="muted" style="margin:.4rem 0 0">We're committed to a diverse, equitable and inclusive environment for clients, staff and board.</p></div></li>
    </ol>
  </div>
</section>

<section class="sec sec--alt" id="history">
  <div class="wrap">
    <div class="sec-head"><div class="kicker">History · 1985 → today</div><h2 class="h-l">The route so far.</h2><p class="lede" style="max-width:none">Four decades of firsts — many of them later copied across the country.</p></div>
    <div class="history" data-history><span class="history__rail" aria-hidden="true"></span><span class="history__fill" aria-hidden="true"></span>{hist_html}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><div class="kicker">Library</div><h2 class="h-m">People, partners and reports.</h2></div>
    <div class="library">
      <a href="{OLD}/staff"><span class="mono">Directory</span><b>Staff</b></a>
      <a href="{OLD}/boardofdirectors"><span class="mono">Governance</span><b>Board of Directors</b></a>
      <a href="{OLD}/communitypartners"><span class="mono">Thank you</span><b>Partners &amp; supporters</b></a>
      <a href="{OLD}/newsletters-1"><span class="mono">Archive</span><b>Newsletters</b></a>
      <a href="{OLD}/financials"><span class="mono">Form 990</span><b>Financials</b></a>
    </div>
  </div>
</section>
"""
page("about.html", "About — Michigan Ability Partners",
     "Since 1985, Michigan Ability Partners has partnered with Veterans and people with disabilities on housing, employment and financial stability.",
     "about", about)


# =====================================================================
# GET INVOLVED
# =====================================================================
# Each row on the departure board. status: tickets | sponsor | soon | save
EVENTS = [
    dict(when="Apr 2, 2027", day="Fri", time="Morning", name="Match My Mocha", sub="Coffee outreach · morning 1 of 3",
         c="var(--l-vets)", status="sponsor", href="sponsor.html#cat-events", act="Sponsor a morning"),
    dict(when="Apr 8, 2027", day="Thu", time="5–9 PM", name="Impact Championship Bowling & Billiards", sub="Fundraiser · tickets from $100",
         c="var(--l-payee)", status="tickets", href="#bowling", act="Get tickets"),
    dict(when="Spring 2027", day="TBA", time="Mornings", name="Match My Mocha", sub="Coffee outreach · mornings 2 & 3",
         c="var(--l-vets)", status="sponsor", href="sponsor.html#cat-events", act="Sponsor a morning"),
    dict(when="2027", day="TBA", time="All day", name="Community Impact Days", sub="Two volunteer days at MAP homes",
         c="var(--l-housing)", status="sponsor", href="sponsor.html#cat-events", act="Sponsor a day"),
    dict(when="Sep 11, 2027", day="Sat", time="Check-in 5 PM", name="Toss for the Cause Cornhole", sub="Fundraiser · $20 per player",
         c="var(--l-evict)", status="soon", href="#cornhole", act="Details"),
    dict(when="2028", day="—", time="Save the date", name="PickleFest 2028", sub="Pickleball tournament fundraiser",
         c="var(--teal-lt)", status="save", href="#picklefest", act="Get notified"),
]
STATUS = {"tickets": "Tickets on sale", "sponsor": "Sponsors wanted", "soon": "Registration this summer", "save": "Save the date"}


def board_rows():
    out = []
    for e in EVENTS:
        out.append(f"""<a class="dep dep--{e['status']}" href="{e['href']}" style="--c:{e['c']}">
  <span class="dep__when"><b>{e['when']}</b><small>{e['day']} · {e['time']}</small></span>
  <span class="dep__name"><i aria-hidden="true"></i><b>{e['name']}</b><small>{e['sub']}</small></span>
  <span class="dep__status">{STATUS[e['status']]}</span>
  <span class="dep__act">{e['act']} {ARR}</span>
</a>""")
    return "\n".join(out)


TEE = """<svg viewBox="0 0 200 200" aria-hidden="true"><path d="M70 30 L40 42 L18 76 L42 88 L52 74 L52 176 L148 176 L148 74 L158 88 L182 76 L160 42 L130 30 Q100 48 70 30Z" fill="var(--t)" stroke="rgba(22,32,42,.25)" stroke-width="1.5"/><g fill="var(--f)" style="color:var(--f)" font-family="Atkinson Hyperlegible Next, sans-serif">{art}</g></svg>"""

ROLES = [("Board member", "Help steer MAP's direction", "Leadership"), ("Committee member", "Lend expertise to a standing committee", "Leadership"),
         ("Office assistant", "Front-desk and admin support", "Weekday"), ("Food bank assistant", "Sort, stock and distribute food", "Weekday"),
         ("Workshop presenter", "Music, art, yoga, meditation, financial literacy", "Residences"), ("Landscaping crew", "Gardens and grounds at MAP homes", "Seasonal"),
         ("Fundraising & events committee", "Plan the events that fund the work", "Events"), ("Event participant", "Show up, play, and bring a friend", "Events")]
roles_html = "".join(f'<div class="role"><div><b>{a}</b><span>{b}</span></div><span class="mono">{c}</span></div>' for a, b, c in ROLES)

involved = ptitle("Get involved", "Get involved", "There's a stop on this line for you.",
                  "Give, volunteer, organize, or simply tell people about MAP. Every bit keeps the route open.", "var(--teal)", chip=False) + f"""
<section class="sec" id="give">
  <div class="wrap">
    <div class="sec-head"><div class="kicker">Ways to give</div><h2 class="h-l">Fuel for the route.</h2><p class="lede" style="max-width:none">MAP is a 501(c)(3) nonprofit. Gifts are tax deductible to the extent the law allows — Tax ID 38-2595768.</p></div>
    <div class="give">
      <div class="give__card give__card--feature"><span class="mono">Fastest</span><h3 style="font-size:2rem">Give online</h3><p>A secure gift through our donation partner goes straight to housing, payee and Veteran programs.</p><a class="btn btn--paper" href="{DONATE}">Donate now {ARR}</a></div>
      <div class="give__card"><span class="mono">By mail</span><h3>Send a check</h3><p>Payable to Michigan Ability Partners<br>3810 Packard St., Suite 260<br>Ann Arbor, MI 48108</p></div>
      <div class="give__card"><span class="mono">In kind</span><h3>Donate new items</h3><p>See the current list of household and personal items our participants need.</p><a class="tlink" href="{INKIND_PDF}">Needed items (PDF)</a></div>
      <div class="give__card"><span class="mono">Organize</span><h3>Host a drive</h3><p>Rally friends or coworkers around a fundraiser or supplies drive.</p><a class="tlink" href="mailto:info@mapagency.org?subject=Host%20an%20event%20with%20MAP">info@mapagency.org</a></div>
      <div class="give__card"><span class="mono">Speak up</span><h3>Advocate</h3><p>Use your voice for housing and disability policy that works.</p><a class="tlink" href="{OLD}/advocate">How to advocate</a></div>
    </div>
  </div>
</section>

<section class="sec sec--alt" id="volunteer">
  <div class="wrap">
    <div class="mosaic rv" style="margin-bottom:clamp(48px,6vw,88px)">
      <figure>{img('crew', 1100, 900, 'A volunteer crew posing together outside a MAP home')}<figcaption>Volunteer day</figcaption></figure>
      <figure>{img('pantry', 800, 520, 'Shelves stocked with food in the MAP pantry')}<figcaption>Food pantry</figcaption></figure>
      <figure>{img('supplies', 800, 520, 'Tables of donated household supplies ready to be sorted')}<figcaption>Supplies drive</figcaption></figure>
    </div>
    <div class="split">
      <div><div class="kicker">Volunteer</div><h2 class="h-l" style="margin:1rem 0 1.25rem">Pick your role.</h2>
        <p>Individuals, companies, congregations and neighborhood groups all have a place. Invite MAP to speak, arrange a day of service, or schedule a beautification day at one of our properties.</p>
        <div style="display:flex;gap:.6rem;flex-wrap:wrap;margin-top:1.5rem"><a class="btn" href="mailto:info@mapagency.org?subject=Volunteering%20with%20MAP">Email to volunteer</a><a class="btn btn--ghost" href="tel:+17349756880">734-975-6880</a></div>
      </div>
      <div class="roles">{roles_html}</div>
    </div>
  </div>
</section>

<section class="sec" id="events">
  <div class="wrap">
    <div class="sec-head"><div class="kicker">Events &amp; sponsorship</div><h2 class="h-l">Come out and play.</h2><p class="lede"><a class="tlink" href="events.html">See the full 2027 timetable</a> or <a class="tlink" href="sponsor.html">browse sponsorships</a>.</p></div>
    <div class="deps" role="list">{board_rows().replace('href="#', 'href="events.html#')}</div>
  </div>
</section>

<section class="sec sec--alt" id="merch">
  <div class="wrap">
    <div class="sec-head"><div class="kicker">Merch campaigns · Bonfire</div><h2 class="h-l">Wear the route.</h2><p class="lede">Limited-run shirts printed and shipped by Bonfire. Part of every purchase goes to {LEGAL}.</p></div>
    <div class="merch">
      <a class="tee" href="{BONFIRE}" style="--t:var(--ink);--f:var(--paper)"><div class="tee__art">{TEE.format(art='<text x="100" y="92" text-anchor="middle" font-size="15" font-weight="800">Navigation</text><text x="100" y="110" text-anchor="middle" font-size="15" font-weight="800">for real life.</text>')}</div><div class="tee__info"><b>Navigation for Real Life</b><span>Unisex tee · Ink</span><u>Shop on Bonfire</u></div></a>
      <a class="tee" href="{BONFIRE}" style="--t:var(--paper);--f:var(--ink)"><div class="tee__art">{TEE.format(art='<g stroke-width="5" fill="none" stroke-linecap="round"><path d="M62 84h76" stroke="#0E6A7A"/><path d="M62 94h76" stroke="#5A4FBF"/><path d="M62 104h76" stroke="#A8432E"/><path d="M62 114h76" stroke="#B87810"/></g><text x="100" y="134" text-anchor="middle" font-size="8" font-weight="700" letter-spacing="1.5">FOUR LINES · ONE DIRECTION</text>')}</div><div class="tee__info"><b>Four Lines</b><span>Unisex tee · Natural</span><u>Shop on Bonfire</u></div></a>
      <a class="tee" href="{BONFIRE}" style="--t:#B87810;--f:var(--paper)"><div class="tee__art">{TEE.format(art='<rect x="80" y="78" width="40" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="3"/><circle cx="100" cy="90" r="6" fill="currentColor"/><text x="100" y="134" text-anchor="middle" font-size="9" font-weight="800" letter-spacing="1">TOSS FOR THE CAUSE</text>')}</div><div class="tee__info"><b>Toss for the Cause 2027</b><span>Event tee · Ochre</span><u>Shop on Bonfire</u></div></a>
    </div>
  </div>
</section>

<section class="sec sec--tight" style="border-top:2px solid var(--ink)">
  <div class="wrap" style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:1.5rem">
    <div><div class="kicker" style="margin-bottom:.75rem">Careers</div><h2 class="h-m">Work at MAP.</h2></div>
    <a class="btn" href="{OLD}/jobopportunities">See job openings {EXT}</a>
  </div>
</section>
"""
page("get-involved.html", "Get Involved — Michigan Ability Partners",
     "Donate, volunteer, host a drive or advocate with Michigan Ability Partners in Ann Arbor and Jackson.",
     "involved", involved)


# =====================================================================
# CONTACT
# =====================================================================
CLOSURES = [("2026-01-01", "Thu, Jan 1", "New Year's Day"), ("2026-01-19", "Mon, Jan 19", "Martin Luther King Jr. Day"),
            ("2026-05-25", "Mon, May 25", "Memorial Day"), ("2026-06-19", "Fri, Jun 19", "Juneteenth"),
            ("2026-07-03", "Fri, Jul 3", "Independence Day"), ("2026-09-07", "Mon, Sep 7", "Labor Day"),
            ("2026-11-26", "Thu, Nov 26", "Thanksgiving"), ("2026-11-27", "Fri, Nov 27", "Day after Thanksgiving"),
            ("2026-12-25", "Fri, Dec 25", "Christmas Day")]
cl_html = "".join(f'<li data-date="{d}"><span class="mono">{a}</span><span>{b}</span></li>' for d, a, b in CLOSURES)

contact = ptitle("Contact", "Contact", "Call, stop by, or write.",
                 "A real person answers. If you're not sure which program you need, that's exactly why we're here.", "var(--teal)", chip=False) + f"""
<section class="sec">
  <div class="wrap">
    <div class="offices2">
      <div class="office" data-office="aa">
        <h3>Ann Arbor</h3><span class="office__status" data-status>Hours</span>
        <address>3810 Packard St., Suite 260<br>Ann Arbor, MI 48108</address>
        <dl class="office__rows"><dt>Hours</dt><dd>Mon, Wed, Fri · 8:30–4:30<br><span class="muted">Closed 12–1 for lunch. Also open the 1st and 3rd of each month unless they fall on a weekend.</span></dd>
          <dt>Phone</dt><dd>734-975-6880</dd><dt>Fax</dt><dd>734-975-2956</dd><dt>Email</dt><dd>info@mapagency.org</dd></dl>
        <div class="office__acts"><a class="btn" href="tel:+17349756880">Call</a><a class="btn btn--ghost" href="mailto:info@mapagency.org">Email</a><a class="btn btn--ghost" href="https://maps.google.com/?q=3810+Packard+St+Suite+260+Ann+Arbor+MI+48108">Directions</a></div>
      </div>
      <div class="office" data-office="jx">
        <h3>Jackson</h3><span class="office__status" data-status>Hours</span>
        <address>216 E. Biddle St., Suite 200<br>Jackson, MI 49203</address>
        <dl class="office__rows"><dt>Hours</dt><dd>Mon &amp; Fri · 10:00–3:00<br><span class="muted">Wednesday by appointment. Also open the 1st and 3rd of each month unless they fall on a weekend.</span></dd>
          <dt>Phone</dt><dd>517-841-5780</dd><dt>Fax</dt><dd>517-795-1400</dd></dl>
        <div class="office__acts"><a class="btn" href="tel:+15178415780">Call</a><a class="btn btn--ghost" href="https://maps.google.com/?q=216+E+Biddle+St+Suite+200+Jackson+MI+49203">Directions</a></div>
      </div>
    </div>
  </div>
</section>

<section class="sec sec--alt">
  <div class="wrap split">
    <div>
      <div class="kicker">Write to us</div>
      <h2 class="h-l" style="margin:1rem 0 1.25rem">Send a message.</h2>
      <p>For general questions, partnerships or media. If you need help with housing, rent or benefits, the <a class="tlink" href="index.html#planner">trip planner</a> or a phone call is the fastest route.</p>
      <div class="quick" style="margin-top:2rem">
        <a href="{OLD}/maintenancerequests"><div>Maintenance request<span>For residents of MAP properties</span></div>{EXT}</a>
        <a href="{OLD}/resources"><div>Community resources<span>Other help in the region</span></div>{EXT}</a>
        <a href="{OLD}/staff"><div>Staff directory<span>Reach a team member directly</span></div>{EXT}</a>
        <a href="mailto:info@mapagency.org?subject=Please%20add%20me%20to%20your%20newsletter%20mailing%20list"><div>Join the newsletter<span>News from MAP, a few times a year</span></div>{ARR}</a>
      </div>
    </div>
    <form class="form" data-contact novalidate>
      <div class="field"><label for="c-name">Name</label><input id="c-name" name="name" autocomplete="name" required></div>
      <div class="field"><label for="c-email">Email or phone</label><input id="c-email" name="reply" required></div>
      <div class="field full"><label for="c-topic">What's this about?</label>
        <select id="c-topic" name="topic"><option>General question</option><option>Housing</option><option>Representative Payee</option><option>Veteran Services</option><option>Eviction Prevention</option><option>Volunteering or giving</option><option>Partnership or media</option></select></div>
      <div class="field full"><label for="c-msg">Message</label><textarea id="c-msg" name="message" required></textarea></div>
      <div class="form__msg" data-msg role="status"></div>
      <div class="full"><button class="btn btn--teal" type="submit">Send message {ARR}</button><p class="muted" style="font-size:.875rem;margin-top:.75rem">Opens your email app, addressed to info@mapagency.org.</p></div>
    </form>
  </div>
</section>

<section class="sec">
  <div class="wrap split">
    <div><div class="kicker">2026 schedule</div><h2 class="h-m" style="margin-top:1rem">Office closures.</h2><p class="muted" style="margin-top:1rem">Both offices are closed on these days.</p></div>
    <ul class="closures" data-closures>{cl_html}</ul>
  </div>
</section>
"""
page("contact.html", "Contact — Michigan Ability Partners",
     "Contact Michigan Ability Partners in Ann Arbor (734-975-6880) and Jackson (517-841-5780). Hours, directions and 2026 office closures.",
     "contact", contact)


# =====================================================================
# EVENTS & TICKETS
# =====================================================================
RECEIPT = f"""
<div class="modal" data-receipt hidden>
  <div class="modal__box receipt" role="dialog" aria-modal="true" aria-labelledby="rc-title">
    <button class="modal__x" type="button" data-close aria-label="Close">×</button>
    <div class="receipt__head">
      <img src="{LOGO}" width="600" height="276" alt="" style="height:38px;width:auto">
      <span class="mono">Confirmation</span>
    </div>
    <div class="receipt__rail" aria-hidden="true"><i style="background:var(--l-housing)"></i><i style="background:var(--l-payee)"></i><i style="background:var(--l-vets)"></i><i style="background:var(--l-evict)"></i></div>
    <h2 id="rc-title" data-rc-title>Thank you.</h2>
    <p class="receipt__sub" data-rc-sub></p>
    <ul class="receipt__lines" data-rc-lines></ul>
    <div class="receipt__total"><span>Total</span><b data-rc-total></b></div>
    <div class="receipt__foot">
      <div class="qr" data-qr aria-label="Check-in code"></div>
      <div><b>{LEGAL}</b><br>501(c)(3) · Tax ID {TAX_ID}<br>3810 Packard St., Suite 260, Ann Arbor, MI 48108<br><span class="mono" data-rc-no></span></div>
    </div>
    <p class="receipt__note">Preview of the branded receipt. On the live site, payment is processed securely by Qgiv and this confirmation is emailed automatically.</p>
  </div>
</div>
"""

TICKETS = [("single", "Single", "One player", 100), ("couple", "Couple", "Two players", 180), ("lane", "Lane of 6", "Your own lane for six", 500)]


tix_rows = "".join(f"""<div class="tix__row" data-tix="{k}" data-price="{p}">
  <div><b>{n}</b><small>{d}</small></div>
  <span class="tix__price">${p}</span>
  <div class="step" role="group" aria-label="{n} tickets">
    <button type="button" data-d="-1" aria-label="Fewer {n} tickets">−</button><output aria-live="polite">0</output><button type="button" data-d="1" aria-label="More {n} tickets">+</button>
  </div>
</div>""" for k, n, d, p in TICKETS)

events = ptitle("Events &amp; tickets", "2027 season", "Every event moves someone closer to home.",
                f"Bowling, billiards, coffee, cornhole and pickleball. Every ticket and sponsorship goes straight to {LEGAL}.",
                "var(--l-payee)") + f"""
<section class="sec sec--tight">
  <div class="wrap">
    <div class="sec-head"><div class="kicker">Departures · 2027</div><h2 class="h-l">The event timetable.</h2><p class="lede">Pick an event to buy tickets, sponsor it or save the date. Dates marked TBA are added as soon as they're set.</p></div>
    <div class="deps" role="list">
      <div class="deps__head" aria-hidden="true"><span>Date</span><span>Event</span><span>Status</span><span></span></div>
      {board_rows()}
    </div>
  </div>
</section>

<section class="sec sec--ink" id="bowling">
  <div class="wrap bowl">
    <div class="bowl__info">
      <div class="kicker"><span class="ptitle__chip" style="--c:var(--l-payee)"><i></i>Fundraiser · Tickets on sale</span></div>
      <h2 class="h-l" style="margin:1.25rem 0 1.5rem">Impact Championship Bowling &amp; Billiards</h2>
      <dl class="bowl__facts">
        <div><dt>Date</dt><dd>Thursday, April 8, 2027</dd></div>
        <div><dt>Time</dt><dd>5:00–9:00 PM</dd></div>
        <div><dt>Where</dt><dd>{BOWLING_VENUE}</dd></div>
        <div><dt>Benefits</dt><dd>{LEGAL}</dd></div>
      </dl>
      <div class="count" data-countdown="2027-04-08T17:00:00-04:00" aria-label="Countdown to the event">
        <div><b data-cd="d">--</b><span>days</span></div><div><b data-cd="h">--</b><span>hours</span></div><div><b data-cd="m">--</b><span>min</span></div>
      </div>
      <p class="muted-ink">Bring a team, a date or your whole office. Every dollar funds housing, payee and Veteran programs across five counties.</p>
    </div>
    <form class="tix" data-tickets novalidate>
      <div class="tix__top"><span class="mono">Buy tickets</span><span class="mono">Secure checkout · Qgiv</span></div>
      {tix_rows}
      <div class="tix__total"><span>Total</span><b data-total>$0</b></div>
      <div class="form" style="padding:0 1.5rem">
        <div class="field full"><label for="tb-name">Name on the order</label><input id="tb-name" name="name" autocomplete="name"></div>
        <div class="field full"><label for="tb-email">Email for your receipt</label><input id="tb-email" name="email" type="email" autocomplete="email"></div>
        <div class="form__msg" data-msg role="status"></div>
      </div>
      <div class="tix__go"><button class="btn btn--teal" type="submit">Continue to checkout {ARR}</button><small>Payment goes directly to {LEGAL}. Tax ID {TAX_ID}.</small></div>
    </form>
  </div>
</section>

<section class="sec sec--alt" id="cornhole">
  <div class="wrap split">
    <div><div class="kicker">Sep 11, 2027 · Fundraiser</div><h2 class="h-l" style="margin:1rem 0 1.25rem">Toss for the Cause Cornhole</h2>
      <p>Check in at 5 PM. Registration is $20 per player, with food and drinks for a suggested $60 donation per person. Registration opens this summer, and you can prepay online or pay at the event.</p>
      <div style="display:flex;gap:.6rem;flex-wrap:wrap;margin-top:1.5rem"><a class="btn" href="sponsor.html#cat-events">Sponsor a board {ARR}</a><a class="btn btn--ghost" href="mailto:info@mapagency.org?subject=Toss%20for%20the%20Cause%20%E2%80%94%20remind%20me">Remind me</a></div>
    </div>
    <div id="picklefest"><div class="kicker">2028 · Save the date</div><h2 class="h-l" style="margin:1rem 0 1.25rem">PickleFest 2028</h2>
      <p>MAP's pickleball tournament returns in 2028. Leave your email and you'll be first to hear when courts and sponsorships open.</p>
      <form class="notify" data-notify novalidate><label class="vh" for="pf-email">Email</label><input id="pf-email" type="email" name="email" placeholder="you@email.com" autocomplete="email"><button class="btn" type="submit">Notify me</button><div class="form__msg" data-msg role="status"></div></form>
    </div>
  </div>
</section>

<section class="sec sec--tight">
  <div class="wrap" style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:1.5rem">
    <div><div class="kicker" style="margin-bottom:.75rem">For businesses</div><h2 class="h-m">Put your name on a lane, a morning or a home.</h2></div>
    <a class="btn btn--teal" href="sponsor.html">See all sponsorships {ARR}</a>
  </div>
</section>
""" + RECEIPT
page("events.html", f"Events & Tickets — {LEGAL}",
     "Buy tickets for Impact Championship Bowling & Billiards and see every Michigan Ability Partners event for 2027.",
     "events", events)


# =====================================================================
# SPONSORSHIP STORE
# =====================================================================
# PREVIEW DATA: names/prices/slots are stand-ins until MAP's 2027 sponsor booklet is loaded.
# Real anchors from MAP: tiers run from $250 (Helping Hand) to $100,000 (Willow Pond).
SPONSORS = [
    # cat, id, name, price, slots_total, slots_left, line color, perks
    ("events", "bb-present", "Bowling & Billiards — Presenting", 5000, 1, 1, "var(--l-payee)", ["Name on all event signage and tickets", "Two lanes for your team", "Logo on the event page"]),
    ("events", "bb-lane", "Bowling & Billiards — Lane", 500, 16, 11, "var(--l-payee)", ["Your logo at one lane", "Recognition from the stage"]),
    ("events", "bb-table", "Bowling & Billiards — Billiards table", 350, 8, 5, "var(--l-payee)", ["Your name on one table", "Listed on the event page"]),
    ("events", "mocha", "Match My Mocha — Morning", 1000, 3, 2, "var(--l-vets)", ["Host one coffee morning", "Your logo on cups and signage"]),
    ("events", "impact", "Community Impact Day", 1500, 2, 2, "var(--l-housing)", ["Your team leads a volunteer day", "Supplies covered for one MAP home"]),
    ("events", "corn-present", "Toss for the Cause — Presenting", 2500, 1, 1, "var(--l-evict)", ["Name on the tournament bracket", "Two teams entered free"]),
    ("events", "corn-board", "Toss for the Cause — Board", 250, 20, 14, "var(--l-evict)", ["Your logo on one set of boards"]),
    ("events", "pickle", "PickleFest 2028 — Court", 750, 6, 6, "var(--teal-lt)", ["Your name on one court", "Early sponsor recognition"]),
    ("programs", "helping-hand", "Helping Hand", 250, 0, 0, "var(--l-housing)", ["Supports any MAP program", "Listed on our sponsor wall"]),
    ("programs", "move-in", "Move-In Kit", 500, 0, 0, "var(--l-housing)", ["Furnishes a new home on move-in day"]),
    ("programs", "vet-ready", "Veteran Job-Ready", 1000, 0, 0, "var(--l-vets)", ["Training and work gear for one Veteran"]),
    ("programs", "payee", "Payee Partner", 2500, 0, 0, "var(--l-payee)", ["A year of payee support for participants"]),
    ("programs", "evict", "Keep a Family Home", 3000, 10, 7, "var(--l-evict)", ["Covers one full Eviction Prevention award"]),
    ("programs", "housing-champion", "Housing Champion", 10000, 4, 3, "var(--l-housing)", ["Annual housing program sponsor", "Recognition in MAP's annual report"]),
    ("buildings", "garden", "Gardens & Grounds", 5000, 6, 4, "var(--l-housing)", ["Landscaping for one MAP property for a year"]),
    ("buildings", "home", "Sponsor a Home", 25000, 6, 5, "var(--l-housing)", ["Your name at one MAP home", "A plaque at the entry"]),
    ("buildings", "willow-pond", "Willow Pond", 100000, 1, 1, "var(--teal)", ["Naming recognition for Willow Pond", "Personal partnership with MAP's leadership"]),
]
CATS = [("events", "Events"), ("programs", "Programs"), ("buildings", "Buildings")]


def sponsor_cards():
    out = []
    for cat, sid, name, price, tot, left, c, perks in SPONSORS:
        big = price >= 10000
        slots = (f'<div class="pk__slots"><span><b>{left}</b> of {tot} left</span><i style="--p:{left/tot*100:.0f}%"></i></div>'
                 if tot else '<div class="pk__slots pk__slots--open"><span>Open to everyone</span></div>')
        btn = (f'<button class="btn btn--ghost" type="button" data-talk="{sid}">Talk with us</button>' if big
               else f'<button class="btn" type="button" data-add="{sid}">Add {ARR}</button>')
        li = "".join(f"<li>{p}</li>" for p in perks)
        out.append(f"""<article class="pk" data-cat="{cat}" data-id="{sid}" data-name="{name}" data-price="{price}" style="--c:{c}">
  <span class="pk__cat mono"><i></i>{dict(CATS)[cat]}</span>
  <h3>{name}</h3>
  <div class="pk__price">${price:,}</div>
  <ul>{li}</ul>
  {slots}
  {btn}
</article>""")
    return "\n".join(out)


sponsor = ptitle("Sponsor MAP", "2027 sponsorships", "Put your name on the route home.",
                 f"Choose a package, pay online or request an invoice. No paper forms and no card numbers on paper. Every sponsorship is made to {LEGAL}.",
                 "var(--teal)") + f"""
<section class="sec sec--tight">
  <div class="wrap">
    <div class="store">
      <div class="store__main">
        <div class="store__bar">
          <div class="chips" role="group" aria-label="Filter packages">
            <button type="button" data-filter="all" aria-pressed="true">All</button>
            {''.join(f'<button type="button" data-filter="{k}" aria-pressed="false" id="cat-{k}">{v}</button>' for k, v in CATS)}
          </div>
          <span class="mono store__note">From $250 Helping Hand to $100,000 Willow Pond</span>
        </div>
        <div class="pks">{sponsor_cards()}</div>
      </div>
      <aside class="cart" data-cart aria-label="Your sponsorship">
        <div class="cart__top"><span class="mono">Your sponsorship</span><span class="mono" data-count>0 items</span></div>
        <ul class="cart__list" data-list><li class="cart__empty">Add a package to get started.</li></ul>
        <div class="cart__total"><span>Total</span><b data-total>$0</b></div>
        <form class="cart__form" data-checkout novalidate>
          <div class="field"><label for="sp-org">Business or name</label><input id="sp-org" name="org" autocomplete="organization"></div>
          <div class="field"><label for="sp-email">Email</label><input id="sp-email" name="email" type="email" autocomplete="email"></div>
          <fieldset class="pay"><legend class="vh">How would you like to pay?</legend>
            <label><input type="radio" name="pay" value="online" checked><span>Pay online now</span></label>
            <label><input type="radio" name="pay" value="invoice"><span>Send me an invoice</span></label>
          </fieldset>
          <div class="form__msg" data-msg role="status"></div>
          <button class="btn btn--teal" type="submit">Continue {ARR}</button>
          <small>Paid directly to {LEGAL} · Tax ID {TAX_ID}</small>
        </form>
      </aside>
    </div>
  </div>
</section>

<section class="sec sec--ink sec--tight" id="talk">
  <div class="wrap split">
    <div><div class="kicker">Gifts of $10,000 and more</div><h2 class="h-l" style="margin:1rem 0 1.25rem">Let's talk first.</h2>
      <p class="lede">Naming gifts and annual partnerships are shaped together. Tell us a little and MAP's development team will reach out personally.</p></div>
    <form class="form" data-talkform novalidate>
      <div class="field"><label for="tk-name">Your name</label><input id="tk-name" name="name" autocomplete="name"></div>
      <div class="field"><label for="tk-org">Business</label><input id="tk-org" name="org" autocomplete="organization"></div>
      <div class="field"><label for="tk-email">Email or phone</label><input id="tk-email" name="reply"></div>
      <div class="field"><label for="tk-pkg">Interested in</label><select id="tk-pkg" name="pkg">{''.join(f'<option>{n} (${p:,})</option>' for _, _, n, p, *_ in SPONSORS if p >= 10000)}<option>Something else</option></select></div>
      <div class="form__msg" data-msg role="status"></div>
      <div class="full"><button class="btn btn--paper" type="submit">Request a conversation {ARR}</button></div>
    </form>
  </div>
</section>
""" + RECEIPT
page("sponsor.html", f"Sponsor — {LEGAL}",
     "Sponsor Michigan Ability Partners events, programs and buildings for 2027. Pay online or request an invoice.",
     "involved", sponsor)


# =====================================================================
# MEDIA & SUCCESS STORIES
# =====================================================================
STORIES = [
    ("housing", "key", "Keys in hand", "96%", "of housing participants stayed in permanent housing."),
    ("payee", "budget", "Bills paid first", "99.4%", "of Representative Payee participants kept their housing."),
    ("vets", "vets", "Back to work", "100%", "of Veteran participants kept or grew their income."),
    ("evict", "apt", "Still home", "$3,000", "can stop an eviction for a Washtenaw County family."),
]


def story_cards():
    out = []
    for key, photo, title, n, txt in STORIES:
        L = LINES[key]
        out.append(f"""<article class="story" style="--c:{L['c']}">
  <a class="story__media" href="{L['page']}">{img(photo, 720, 480, '')}<span class="line__code story__tag"><i></i>Line {L['n']} · {L['name']}</span></a>
  <div class="story__body">
    <h3>{title}</h3>
    <p><b>{n}</b> {txt}</p>
    <div class="story__acts"><a class="tlink" href="{L['page']}">The {L['name']} line</a><a class="btn btn--teal" href="{DONATE}">Give to {L['name']} {ARR}</a></div>
  </div>
</article>""")
    return "\n".join(out)


stories = ptitle("Stories", "Media &amp; success stories", "Real people. Real routes home.",
                 "Videos and stories from the people MAP serves, each tied to the program behind it and a way to help.",
                 "var(--l-vets)") + f"""
<section class="sec sec--tight">
  <div class="wrap feature">
    <button class="feature__video" type="button" data-video="{ROXANN_VIDEO}" aria-label="Play Roxann's winter message">
      {img('green', 1200, 680, 'MAP volunteers in green shirts gathered at a MAP property')}
      <span class="play" aria-hidden="true"><svg width="34" height="34" viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="currentColor"/></svg></span>
      <span class="feature__cap mono">Video · Winter message</span>
    </button>
    <div class="feature__txt">
      <div class="kicker">Featured</div>
      <h2 class="h-l" style="margin:1rem 0 1.25rem">A winter message from Roxann.</h2>
      <p>A message from Roxann this winter, on what MAP's support means and why a stable home is where every other step begins.</p>
      <div style="display:flex;gap:.6rem;flex-wrap:wrap;margin-top:1.5rem"><a class="btn btn--teal" href="{DONATE}">Give this winter {ARR}</a><a class="btn btn--ghost" href="#more">More stories</a></div>
    </div>
  </div>
</section>

<section class="sec sec--ink sec--tight">
  <div class="wrap quote">
    <div class="quote__mark" aria-hidden="true">&ldquo;</div>
    <blockquote><p>Having a viable contact outside of my home reminding me that things would get better.</p><cite>— M., MAP participant</cite></blockquote>
  </div>
</section>

<section class="sec" id="more">
  <div class="wrap">
    <div class="sec-head"><div class="kicker">By line</div><h2 class="h-l">Every story rides a line.</h2><p class="lede">Each program has its own results. Pick the one that moves you and give to it directly.</p></div>
    <div class="stories">{story_cards()}</div>
  </div>
</section>

<div class="modal" data-modal hidden>
  <div class="modal__box" role="dialog" aria-modal="true" aria-label="Video">
    <button class="modal__x" type="button" data-close aria-label="Close">×</button>
    <div class="modal__video" data-video-slot></div>
  </div>
</div>
"""
page("stories.html", f"Stories — {LEGAL}",
     "Videos and success stories from Michigan Ability Partners, each tied to the program behind it.",
     "stories", stories)
