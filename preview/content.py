"""Self-contained content for the public-site preview.

This module holds the redesigned public-facing copy *independently* of the CMS
so the preview can be rendered without touching any live CMS rows or templates.
Images are bundled under ``static/preview/`` so the preview deploys with the
code (no dependency on MEDIA_ROOT).

Links to other preview pages use the ``%%BASE%%`` sentinel, which the view
replaces with the preview root (``/preview/``). Links to real application pages
(contact, membership application, syllabus, ...) are absolute and point at the
live site.
"""

import re

# Static URLs must NOT be resolved at import time: production uses a manifest
# staticfiles storage (ManifestStaticFilesStorage), whose manifest is only
# populated by `collectstatic` — which runs *after* `migrate` during deploy
# (and `migrate` runs `manage.py check`, importing this module). Resolving too
# early raises "Missing staticfiles manifest entry". So embed tokens here and
# expand them to real URLs at request time via ``resolve_static``.
_STATIC_TOKEN = "@@STATIC:{}@@"


def resolve_static(text):
    """Expand ``@@STATIC:<path>@@`` tokens to (hashed) static URLs."""
    from django.templatetags.static import static

    return re.sub(r"@@STATIC:(.+?)@@", lambda m: static(m.group(1)), text)


_IMG_FILES = {
    "g_rainbow": "img-1538.jpg",
    "g_runway": "2-runway-before-extension.jpeg",
    "g_deck": "4-observation-deck.jpeg",
    "g_linecrew": "5-line-crew-in-golf-cart.jpeg",
    "g_grob": "6-grob-tied-down.jpg",
    "g_grobroll": "7-grob-rolling-out.jpg",
    "g_krey": "10-flight-line-at-krey.jpg",
    "g_img2522": "img-2522.jpeg",
    "g_img2509": "img-2509.jpeg",
    "g_img2512": "img-2512.jpeg",
    "g_towplane": "20220108-151425.jpg",
    "g_xc": "20210501-160445.jpg",
    "g_aidan": "aidan-tows.jpg",
    "g_grob2": "2189264.jpg",
    "g_wide1": "7802892.jpg",
    "g_wide2": "475753.jpg",
    "g_rear": "20210116-124704.jpg",
    "g_elmirage": "821634.jpg",
    "g_lookback": "7659521.jpg",
    "g_grob103": "1341602.jpg",
    "g_thunder": "245709.jpg",
    "h_hero": "hero-rainbow.jpg",
    "h_welcome": "welcome.jpg",
    "f_a1": "2433223.jpg",
    "f_a2": "763820.jpg",
    "f_a3": "4654579.jpg",
    "f_a4": "233-rainbow.jpg",
    "c_krey": "flight-line-krey.jpg",
    "c_flightline": "flight-line.jpg",
    "c_preparing": "preparing.jpg",
}

IMG = {k: _STATIC_TOKEN.format(f"preview/img/{name}") for k, name in _IMG_FILES.items()}

PDF = {
    "bylaws": _STATIC_TOKEN.format("preview/pdf/avsc-bylaws-2015.pdf"),
    "application": _STATIC_TOKEN.format(
        "preview/pdf/avsc-membership-application-2012.pdf"
    ),
    "dues": _STATIC_TOKEN.format("preview/pdf/avsc-dues-rates.pdf"),
}


def figure(key, caption="", cols="col-6 col-md-4"):
    url = IMG[key]
    cap = (
        f'<figcaption class="figure-caption">{caption}</figcaption>' if caption else ""
    )
    return (
        f'<figure class="figure {cols}">'
        f'<a href="{url}" target="_blank" rel="noopener">'
        f'<img src="{url}" class="figure-img img-fluid rounded" alt="{caption}">'
        f"</a>{cap}</figure>"
    )


GALLERY_GRID = (
    '<div class="row g-3">'
    + "".join(
        [
            figure(
                "g_rainbow",
                "We're located in a great spot for year-round soaring. Under a rainbow!",
            ),
            figure("g_runway", "Runway before the runway extension"),
            figure("g_deck", "View from the clubhouse deck"),
            figure("g_linecrew", "Line crew: Clark &amp; Tyler"),
            figure("g_grob", "Grob 103 trainer"),
            figure("g_grobroll"),
            figure("g_krey", "Getting ready for a flight."),
            figure("g_img2522"),
            figure("g_img2509", "The primary trainer &mdash; the 2-33."),
            figure(
                "g_img2512",
                "The 1-34 can be used for cross-country work for FAI badges.",
            ),
            figure("g_towplane", "Our towplane, after fueling."),
            figure(
                "g_xc",
                "The cross-country group learns to load a trailer with the 1-34.",
            ),
            figure("g_aidan", "Aidan, our newest tow pilot. 2021."),
            figure("g_grob2", "Our fibreglass trainer, the Grob 103"),
            figure("g_wide1"),
            figure("g_wide2"),
            figure(
                "g_rear", "Home, sweet home &mdash; view from the 2-33 rear window."
            ),
            figure("g_elmirage", "Glider on the nearby El Mirage dry lake bed."),
            figure("g_lookback", "A quick look back."),
            figure("g_grob103", "AVSC Grob 103"),
            figure("g_thunder", "The occasional summer thundershower. Seldom hail."),
        ]
    )
    + "</div>"
)

CLUB_ROW = (
    '<div class="row g-3 my-3">'
    + figure("c_krey", "The flight line back when we were at Krey Field.")
    + figure("c_flightline", "Our flight line.")
    + figure("c_preparing", "Preparing for flight.")
    + "</div>"
)

START_HERE = f"""
<div class="avsc-page-hero">
  <h2>Learn to Fly</h2>
  <p>Everything you need to know about learning to soar with the Antelope Valley Soaring Club.</p>
</div>

<h2>What is soaring?</h2>
<p>Gliders (sailplanes) are unpowered aircraft that stay aloft on rising air &mdash; thermals, ridge lift, and wave. A tow behind our tow plane gets you airborne; from there, it's pure flying.</p>

<div class="alert alert-info" role="alert">
  <strong>New to gliding?</strong> You don't need any flying experience to start. Most people begin with an introductory flight, then progress through instruction toward solo and beyond.
</div>

<h2 class="mt-4">How to get started</h2>
<div class="row g-4">
  <div class="col-md-6 col-lg-3">
    <div class="avsc-card h-100">
      <div class="avsc-feature__icon">1</div>
      <h3 class="h6">Come out and visit</h3>
      <p class="mb-0">We fly most Saturdays &mdash; see <a href="%%BASE%%location/">Visit Us</a> for directions and what to expect.</p>
    </div>
  </div>
  <div class="col-md-6 col-lg-3">
    <div class="avsc-card h-100">
      <div class="avsc-feature__icon">2</div>
      <h3 class="h6">Take an introductory flight</h3>
      <p class="mb-0">Fly with an FAA-certified instructor and get a feel for it.</p>
    </div>
  </div>
  <div class="col-md-6 col-lg-3">
    <div class="avsc-card h-100">
      <div class="avsc-feature__icon">3</div>
      <h3 class="h6">Join the club</h3>
      <p class="mb-0">Complete our <a href="/members/apply/">online membership application</a>.</p>
    </div>
  </div>
  <div class="col-md-6 col-lg-3">
    <div class="avsc-card h-100">
      <div class="avsc-feature__icon">4</div>
      <h3 class="h6">Learn to fly</h3>
      <p class="mb-0">Work through our structured <a href="/TRAINING/Syllabus/">training syllabus</a> at your own pace.</p>
    </div>
  </div>
</div>

<h2 class="mt-5">What it costs</h2>
<table class="table table-striped table-bordered align-middle">
  <thead class="table-light">
    <tr><th scope="col">Item</th><th scope="col">Cost</th><th scope="col">Notes</th></tr>
  </thead>
  <tbody>
    <tr><td>Initiation fee</td><td>$400.00</td><td>One-time, on joining</td></tr>
    <tr><td>Monthly dues</td><td>$35.00 / month</td><td>Standard membership</td></tr>
    <tr><td>Reduced monthly dues</td><td>$17.50 / month</td><td>Members who own a glider, subject to conditions</td></tr>
    <tr><td>SSA membership</td><td>$75.00 / year</td><td>Required for all members; includes a subscription to <em>Soaring</em> magazine</td></tr>
    <tr><td>Use of club aircraft &amp; equipment</td><td>No charge</td><td>Included with membership</td></tr>
  </tbody>
</table>
<p class="text-muted"><small>Rates shown are the club's published prices and may change. Contact a club officer for current rates.</small></p>

<h2>An all-volunteer club</h2>
<p>AVSC is a non-profit, all-volunteer organization. Members are expected to take part in club meetings, aircraft maintenance, and club projects &mdash; our low dues depend on it. In return you get a welcoming community and access to a well-maintained fleet.</p>

<h2>Instruction</h2>
<ul>
  <li>Three FAA-certified glider instructors.</li>
  <li>Flight reviews (BFRs) are provided <strong>free of charge</strong> to club members.</li>
  <li>Instruction is available on a case-by-case basis &mdash; just talk with us at the field.</li>
</ul>

<h2>When we fly</h2>
<p>Most Saturdays, year-round. Check the live <a href="/duty_roster/calendar/">duty roster calendar</a> for upcoming flying days, or <a href="/contact/">contact us</a> before your first visit.</p>

<h2 id="officers">Club Officers</h2>
<p>Interested in joining or visiting? Contact any club officer, or use our <a href="/contact/">contact form</a>. We fly most Saturdays from about 10am through the afternoon &mdash; prospective members are welcome to come out and see us.</p>
<table class="table table-striped table-bordered align-middle">
  <thead class="table-light">
    <tr><th scope="col">Officer</th><th scope="col">Role</th><th scope="col">Contact</th></tr>
  </thead>
  <tbody>
    <tr><td>Jack Gravance</td><td>President</td><td><a href="mailto:jackgravance@gmail.com">jackgravance@gmail.com</a></td></tr>
    <tr><td>Colin Driggs</td><td>Vice-President</td><td><a href="mailto:invrtd04@gmail.com">invrtd04@gmail.com</a><br><a href="tel:+17609879590">760-987-9590</a></td></tr>
    <tr><td>Raymond Swartz</td><td>Board Member</td><td><a href="mailto:rswartz@rocketmail.com">rswartz@rocketmail.com</a><br><a href="tel:+16266277772">626-627-7772</a></td></tr>
    <tr><td>Cindy Brickner</td><td>Secretary / Instructor</td><td><a href="mailto:writercindyb@gmail.com">writercindyb@gmail.com</a><br><a href="tel:+17603731019">760-373-1019</a></td></tr>
  </tbody>
</table>

<h2>Life at the field</h2>
{CLUB_ROW}
"""


def fleet_card(key, title, subtitle, specs, cols="col-md-6 col-lg-4"):
    rows = "".join(f"<li><span>{k}</span><span>{v}</span></li>" for k, v in specs)
    return (
        f'<div class="{cols}"><div class="avsc-card">'
        f'<img src="{IMG[key]}" class="img-fluid rounded-3 mb-3 w-100" alt="{title}">'
        f'<h3 class="h5 mb-1">{title}</h3>'
        f'<p class="text-muted mb-2">{subtitle}</p>'
        f'<ul class="avsc-spec">{rows}</ul>'
        f"</div></div>"
    )


OUR_FLEET = f"""
<div class="avsc-page-hero">
  <h2>Our Fleet</h2>
  <p>The club owns six aircraft &mdash; one tow plane and five gliders. Every member has access to the club fleet.</p>
</div>

<div class="row g-4">
  {fleet_card("g_towplane", "Piper PA-25 Pawnee", "Tow plane &mdash; the workhorse that gets us airborne", [("Role", "Aerotow"), ("Seats", "1"), ("Engine", "Lycoming O-540")])}
  {fleet_card("f_a4", "Schweizer SGS 2-33A", "Two-place primary trainer", [("Seats", "2"), ("L/D max", "22.25 @ 52 mph"), ("Min sink", "3.28 ft/s"), ("Wing span", "51 ft")])}
  {fleet_card("f_a1", "Schweizer SGS 1-26E", "Single-seat classic", [("Seats", "1"), ("L/D max", "23 @ 85 km/h"), ("Min sink", "2.9 ft/s"), ("Wing span", "40 ft")])}
  {fleet_card("f_a2", "Schweizer SGS 1-34", "Single-seat cross-country sailplane", [("Seats", "1"), ("L/D max", "34"), ("Min sink", "2.1 ft/s"), ("Wing span", "15 m")])}
  {fleet_card("f_a3", "Grob G-103 Twin II", "Two-place fibreglass trainer", [("Seats", "2"), ("L/D max", "35 @ 65 mph"), ("Min sink", "2.45 ft/s"), ("Wing span", "17.5 m")])}
  {fleet_card("g_elmirage", "Laister Nugget", "Vintage club sailplane", [("Seats", "1"), ("Type", "Vintage"), ("Structure", "Metal &amp; fabric")])}
</div>

<h2 class="mt-5">About the fleet</h2>
<div class="row g-4 mt-1">
  <div class="col-md-6"><h3 class="h5">Schweizer 2-33</h3><p>Our primary two-place trainer. Rugged, forgiving, and the aircraft most students solo in.</p></div>
  <div class="col-md-6"><h3 class="h5">Schweizer 1-26E</h3><p>A single-seat classic &mdash; light, simple, and a favourite for one-design and fun flying.</p></div>
  <div class="col-md-6"><h3 class="h5">Schweizer 1-34</h3><p>A single-seat metal sailplane well suited to cross-country work and FAI badge attempts.</p></div>
  <div class="col-md-6"><h3 class="h5">Grob G-103 Twin II</h3><p>Our fibreglass two-place trainer, used for instruction and higher-performance dual flights.</p></div>
</div>
"""

LOCATION = """
<div class="avsc-page-hero">
  <h2>Visit Us</h2>
  <p>AVSC is based at a private airport north of Phelan, California, just a few miles from the historic El Mirage soaring site. Visitors are always welcome.</p>
</div>

<p><strong>GPS:</strong> approximately 34.56&nbsp;N, 117.60&nbsp;W &mdash;
<a href="https://www.google.com/maps/search/?api=1&amp;query=34.56,-117.60" target="_blank" rel="noopener">open in Google Maps</a></p>

<h2>Driving Directions</h2>

<h3>From Highway 18 / Palmdale Rd</h3>
<ol>
  <li>Turn north on Sheep Creek Road (about 9.5 miles east of the Hwy 138 intersection, and 10 miles west of Hwy 395).</li>
  <li>Proceed north about 2.5 miles. At the north end of the "S" turn, turn left (west) onto Rancho Road (a dirt road).</li>
  <li>Continue west about 1 mile to the wire fence corner on your right at Tanner Road. Our AVSC sign is on the fence.</li>
  <li>Turn right (north) about 1/4 mile to the gate on your left.</li>
</ol>

<h3>From El Mirage Rd</h3>
<ol>
  <li>Turn south on Sheep Creek Road and go 3 miles to Rancho Road (dirt) at the beginning of the "S" turn.</li>
  <li>Turn right (west) and follow the directions above.</li>
</ol>

<h2>Once You Arrive</h2>
<div class="alert alert-warning" role="alert">
  The gate is locked 24/7 for security. Please phone your host ahead of time so they can meet you at the gate &mdash; otherwise it is a long walk to the clubhouse for someone to let you in.
</div>
<p>After the gate is unlocked, drive in and <strong>stay to the right to avoid the runway</strong>. Proceed about 300 ft directly to our glider tie-down area. Parking is just beyond the clubhouse trailer.</p>

<div class="alert alert-danger" role="alert">
  <strong>Under no circumstances may you drive or park on the runway.</strong> This is a safety rule &mdash; please pass it on to every visitor.
</div>

<h2>Visiting Pilots</h2>
<p>Already a glider pilot and passing through the Antelope Valley? You're welcome to fly with us. Check in at the field and a club member will get you set up. <a href="/contact/">Contact us</a> in advance if you'd like to arrange a flight.</p>

<h2 id="weather">Weather &amp; Conditions</h2>
<p>The Antelope Valley offers excellent year-round soaring. When the marine air mass makes Los Angeles, Orange County, and the Inland Empire poor, the valley is usually clear and flyable. Depending on the season you'll find 14,000&nbsp;ft thermals, an active shear line, and occasional wave.</p>

<div class="row g-4 my-1">
  <div class="col-md-6 col-lg-3"><div class="avsc-card h-100"><h3 class="h6">Spring</h3><p class="mb-0">Thermals and shear lines. Lift of 1,000&nbsp;ft/min or more is possible, and multi-hour flights are frequent.</p></div></div>
  <div class="col-md-6 col-lg-3"><div class="avsc-card h-100"><h3 class="h6">Summer</h3><p class="mb-0">Excellent thermals all summer. On transition days the shear line makes for outstanding flying, and altitudes of 12,000&nbsp;ft and above are common.</p></div></div>
  <div class="col-md-6 col-lg-3"><div class="avsc-card h-100"><h3 class="h6">Fall</h3><p class="mb-0">Shear line, thermals, and occasional mild wave. The flying stays great well into late fall.</p></div></div>
  <div class="col-md-6 col-lg-3"><div class="avsc-card h-100"><h3 class="h6">Winter</h3><p class="mb-0">Shear line and decent thermals are still available. When it's raining in Los Angeles, we're usually flying.</p></div></div>
</div>

<h3 class="mt-4">Forecasts &amp; Weather</h3>
<ul>
  <li><a href="http://www.wrh.noaa.gov/sgx/data/aviation/soar.htm" target="_blank" rel="noopener">Soaring Forecast for Southern California (NOAA)</a></li>
  <li><a href="http://www.drjack.info/BLIP/NAM/CANV/index.html" target="_blank" rel="noopener">BLIPMAP soaring forecasts</a></li>
  <li><a href="https://forecast.weather.gov/MapClick.php?lat=34.557466483188996&amp;lon=-117.55096435546875&amp;site=sgx&amp;smap=1&amp;marine=0&amp;unit=0&amp;lg=en" target="_blank" rel="noopener">National Weather Service &mdash; local point forecast</a></li>
</ul>

<h3>Flight Planning</h3>
<ul>
  <li><a href="https://skyvector.com/" target="_blank" rel="noopener">SkyVector sectional charts</a></li>
  <li><a href="https://pilotweb.nas.faa.gov/PilotWeb/" target="_blank" rel="noopener">NOTAMs &mdash; FAA PilotWeb</a></li>
</ul>
"""

GALLERY = f"""
<p class="lead">A look at life at the Antelope Valley Soaring Club &mdash; the flight line, our aircraft, and the view from the air.</p>

<div class="ratio ratio-16x9 my-3">
  <iframe src="https://www.youtube.com/embed/19Pzl6u63Dc" title="AVSC member cross-country camp" allowfullscreen></iframe>
</div>
<p class="text-muted"><small>One of our members at a cross-country camp. More on our <a href="https://www.youtube.com/@antelopevalleysoaringclub457" target="_blank" rel="noopener">YouTube channel</a>.</small></p>

{GALLERY_GRID}
<p class="mt-3"><small class="text-muted">Watching these videos is not flight instruction. Contact an FAA-certified instructor to learn to fly gliders &mdash; we have several in the AVSC.</small></p>
"""

DOCUMENTS = f"""
<p class="lead">Club documents &mdash; bylaws, membership information, and dues &mdash; appear below. Click a document to open it.</p>

<h2>Membership &amp; Governing Documents</h2>
<ul>
  <li><a href="{PDF['bylaws']}" target="_blank" rel="noopener">AVSC Bylaws (June 2015)</a> &mdash; the club's governing rules.</li>
  <li><a href="{PDF['application']}" target="_blank" rel="noopener">Membership Application (June 2012)</a> &mdash; prefer to apply online? Use our <a href="/members/apply/">online application form</a>.</li>
  <li><a href="{PDF['dues']}" target="_blank" rel="noopener">Dues Rates</a> &mdash; current membership cost schedule. See also <a href="%%BASE%%start-here/">Learn to Fly</a>.</li>
</ul>

<h2>Tow &amp; Launch Rates</h2>
<table class="table table-striped table-bordered align-middle">
  <thead class="table-light">
    <tr><th scope="col">Tow Altitude</th><th scope="col">Price</th></tr>
  </thead>
  <tbody>
    <tr><td>1,500 ft AGL</td><td>$50</td></tr>
    <tr><td>2,000 ft AGL</td><td>$60</td></tr>
    <tr><td>2,500 ft AGL</td><td>$70</td></tr>
    <tr><td>3,000 ft AGL</td><td>$80</td></tr>
    <tr><td>Above 3,000 ft AGL</td><td>$80 + $2 per additional 100 ft</td></tr>
    <tr><td>Simulated rope break / pattern tow (below 1,000 ft AGL)</td><td>$25</td></tr>
  </tbody>
</table>
<p class="text-muted"><small>Rates shown are the club's published prices and may change. Contact a club officer for current pricing.</small></p>
"""

HOME = f"""
<section class="avsc-hero" style="background-image:url('{IMG['h_hero']}');">
  <div class="container avsc-hero__inner">
    <p class="avsc-hero__eyebrow">Est. 1955 &middot; El Mirage, California</p>
    <h1 class="avsc-hero__title">Welcome to the Antelope Valley Soaring Club</h1>
    <p class="avsc-hero__lead mt-3">A volunteer-run glider club flying the high desert north of Los Angeles. No engine, no noise &mdash; just you and the sky.</p>
    <p class="mt-4">
      <a class="btn btn-primary btn-lg me-2 mb-2" href="%%BASE%%start-here/">Learn to Fly</a>
      <a class="btn btn-outline-light btn-lg mb-2" href="/members/apply/">Apply for Membership</a>
    </p>
  </div>
</section>

<section class="avsc-stats">
  <div class="container">
    <div class="row g-0">
      <div class="col-6 col-md-3"><div class="avsc-stat"><div class="avsc-stat__num">1955</div><div class="avsc-stat__label">Founded</div></div></div>
      <div class="col-6 col-md-3"><div class="avsc-stat"><div class="avsc-stat__num">6</div><div class="avsc-stat__label">Aircraft</div></div></div>
      <div class="col-6 col-md-3"><div class="avsc-stat"><div class="avsc-stat__num">14,000<span style="font-size:0.6em;"> ft</span></div><div class="avsc-stat__label">Summer thermals</div></div></div>
      <div class="col-6 col-md-3"><div class="avsc-stat"><div class="avsc-stat__num">90<span style="font-size:0.6em;"> min</span></div><div class="avsc-stat__label">From Los Angeles</div></div></div>
    </div>
  </div>
</section>

<section class="avsc-section">
  <div class="container">
    <div class="row align-items-center g-5">
      <div class="col-lg-6">
        <h2 class="avsc-section__title">A soaring tradition since 1955</h2>
        <p>The Antelope Valley Soaring Club (AVSC) was established in <strong>1955</strong> at the world-famous El Mirage soaring site. The club flew there for many years, until it closed in the late 1980s; we are now based just four miles away, on a private field beside the El Mirage lake bed.</p>
        <p>AVSC is a chapter member of the <a href="https://www.ssa.org/" target="_blank" rel="noopener">Soaring Society of America</a> and a non-profit organization. Our mission is to promote and encourage the art of motorless flight in the Antelope Valley, in Southern California.</p>
        <p>We are about a 90-minute drive from most of Los Angeles and the Inland Empire. If you are looking for a well-established, quality soaring club with excellent flying conditions &mdash; and "plane" good times at a reasonable cost &mdash; come join us.</p>
        <a class="btn btn-outline-primary" href="%%BASE%%start-here/">About the club &rarr;</a>
      </div>
      <div class="col-lg-6">
        <img src="{IMG['h_welcome']}" class="img-fluid rounded-4 shadow-sm w-100" alt="A glider on the AVSC flight line">
      </div>
    </div>
  </div>
</section>

<section class="avsc-section avsc-section--tint">
  <div class="container">
    <h2 class="avsc-section__title text-center mb-5">Why fly with AVSC?</h2>
    <div class="row g-4">
      <div class="col-md-4">
        <div class="avsc-feature">
          <div class="avsc-feature__icon"><i class="fas fa-graduation-cap"></i></div>
          <h3>Learn to fly</h3>
          <p>No experience needed. Start with an introductory flight and progress toward solo with our FAA-certified instructors.</p>
          <a href="%%BASE%%start-here/">Start here &rarr;</a>
        </div>
      </div>
      <div class="col-md-4">
        <div class="avsc-feature">
          <div class="avsc-feature__icon"><i class="fas fa-plane-departure"></i></div>
          <h3>A fleet you can fly</h3>
          <p>Five gliders and our own tow plane, maintained and shared by the members who fly them.</p>
          <a href="%%BASE%%our-fleet/">Our fleet &rarr;</a>
        </div>
      </div>
      <div class="col-md-4">
        <div class="avsc-feature">
          <div class="avsc-feature__icon"><i class="fas fa-sun"></i></div>
          <h3>World-class conditions</h3>
          <p>Strong thermals, an active shear line, and year-round flying in the high desert.</p>
          <a href="%%BASE%%location/#weather">Weather &amp; conditions &rarr;</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="avsc-section">
  <div class="container">
    <div class="d-flex justify-content-between align-items-end mb-4 flex-wrap gap-2">
      <h2 class="avsc-section__title mb-0">Life at the field</h2>
      <a href="%%BASE%%gallery/">See the full gallery &rarr;</a>
    </div>
    <div class="avsc-gallery-strip">
      {''.join(f'<a href="{IMG[k]}" target="_blank" rel="noopener"><img src="{IMG[k]}" alt="" loading="lazy"></a>' for k in ['g_deck','g_linecrew','g_grob','g_xc','g_towplane','g_elmirage','g_rear','g_wide1'])}
    </div>
  </div>
</section>

<section class="avsc-section avsc-section--tint">
  <div class="container">
    <div class="avsc-cta text-center">
      <h2>Open to new members</h2>
      <p class="lead mb-4">Students, pilots, and visitors of all types are welcome &mdash; tow pilots and instructors especially. We fly most Saturdays, so come by for a visit.</p>
      <a class="btn btn-primary btn-lg me-2 mb-2" href="/members/apply/">Apply for Membership</a>
      <a class="btn btn-outline-light btn-lg mb-2" href="/contact/">Contact Us</a>
    </div>
  </div>
</section>

<section class="avsc-section">
  <div class="container">
    <h2 class="avsc-section__title mb-4">Latest News</h2>
    <div class="avsc-news__item">
      <div class="avsc-news__date">2024-07-19 &middot; Summer flying</div>
      <p class="mb-2">The heat is hot, the altitude is great, the flights are long.</p>
      <ul class="mb-0">
        <li>Still looking for more <strong>tow pilots</strong>.</li>
        <li>We're on Instagram now: <a href="https://www.instagram.com/antelope_valley_soaring/" target="_blank" rel="noopener">@Antelope_valley_soaring</a>.</li>
        <li>Come by for a visit &mdash; we fly most Saturdays.</li>
        <li>One of our members attended a cross-country camp! <a href="https://www.youtube.com/watch?v=19Pzl6u63Dc" target="_blank" rel="noopener">Watch the video</a>.</li>
      </ul>
    </div>
    <div class="avsc-news__item">
      <div class="avsc-news__date">2024-01-01</div>
      <ul class="mb-0">
        <li>We are looking for <strong>tow pilots</strong>.</li>
        <li>We have a <a href="https://www.youtube.com/@antelopevalleysoaringclub457" target="_blank" rel="noopener">YouTube channel</a>.</li>
      </ul>
    </div>
  </div>
</section>
"""

# Ordered page registry. ``home`` is special: its content already manages its own
# full-bleed sections, so the base template does not wrap it in a container.
PAGES = [
    ("home", "Home", HOME),
    ("start-here", "Learn to Fly", START_HERE),
    ("our-fleet", "Our Fleet", OUR_FLEET),
    ("location", "Visit Us", LOCATION),
    ("gallery", "Gallery", GALLERY),
    ("documents", "Club Files", DOCUMENTS),
]

PAGE_MAP = {slug: (title, html) for slug, title, html in PAGES}
