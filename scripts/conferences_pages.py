# scripts/conferences_pages.py
# Conference index page generator for The CS Pulse.

import os
import json

from nav_config import SITE_NAME, SITE_URL, CURRENT_YEAR
from templates import (get_page_wrapper, write_page, get_breadcrumb_schema,
                       breadcrumb_html, newsletter_cta_html)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data")


def load_conferences():
    with open(os.path.join(DATA_DIR, "conferences.json"), "r") as f:
        return json.load(f)


def build_conferences_index():
    """Build /conferences/ index page."""
    conferences = load_conferences()
    role = "Customer Success"
    title = f"Best {role} Conferences in {CURRENT_YEAR}"
    description = (
        f"Top {len(conferences)} conferences for customer success professionals in {CURRENT_YEAR}. "
        f"Events covering retention, NRR, CS platforms, churn reduction, and career growth."
    )

    crumbs = [("Home", "/"), ("Conferences", None)]
    bc_schema = get_breadcrumb_schema([("Home", "/"), (f"{role} Conferences", f"{SITE_URL}/conferences/")])
    bc_html = breadcrumb_html(crumbs)

    cards_html = ""
    for conf in conferences:
        tags_html = "".join(
            f'<span class="conference-tag">{tag}</span>' for tag in conf["relevance_tags"][:4]
        )
        attendees = f"{conf['typical_attendees']:,}" if conf['typical_attendees'] else "TBA"
        cards_html += f'''<div class="conference-card">
    <div class="conference-card-header">
        <h3><a href="{conf['website_url']}" target="_blank" rel="noopener">{conf['name']}</a></h3>
        <span class="conference-organizer">by {conf['organizer']}</span>
    </div>
    <p class="conference-description">{conf['description']}</p>
    <div class="conference-meta">
        <span class="conference-location">{conf['location']}</span>
        <span class="conference-attendees">{attendees} typical attendees</span>
    </div>
    <div class="conference-tags">{tags_html}</div>
    <a href="{conf['website_url']}" target="_blank" rel="noopener" class="conference-link">Visit website</a>
</div>
'''

    body = f'''{bc_html}
<section class="page-header">
    <h1>{title}</h1>
    <p class="page-subtitle">Where CS professionals learn retention strategies, discover tools, and build their peer network.</p>
</section>

<section class="content-section">
    <div class="content-body">
        <p>Customer success is still a relatively young profession, and the playbook is being written in real time. What worked for CS teams two years ago may not work today. Buyer expectations have shifted, boards are scrutinizing net revenue retention more closely, and the tools available to CS teams have expanded dramatically. Conferences are where you go to stay current.</p>

        <p>The CS conference circuit has matured significantly. You can now find events that focus specifically on customer success strategy, operations, and leadership rather than treating CS as a footnote in a broader SaaS conference. The best events attract practitioners who are willing to share what actually works, including the approaches that failed along the way.</p>

        <p>We selected the {len(conferences)} conferences below based on their relevance to customer success professionals, the quality of their content and speakers, and the networking opportunities they provide. Whether you are an individual contributor looking to sharpen your skills or a VP building a CS organization, there is an event on this list for you.</p>

        <h2>Choosing the Right CS Conference</h2>
        <p>CS conferences range from intimate leadership summits with 200 attendees to massive SaaS events with 12,000+ people. The right choice depends on what you need. If you want deep tactical knowledge about running a CS program, smaller dedicated events like Pulse, BIG RYG, or CS100 Summit are hard to beat. If you want broader business context for how CS fits into the revenue engine, events like SaaStr Annual provide that perspective.</p>

        <p>Platform-specific events from Gainsight, ChurnZero, Totango, and Catalyst are especially valuable if you use those tools. You will learn advanced workflows, connect with other users in your segment, and often get early access to features still in development.</p>

        <h2>Top {role} Conferences in {CURRENT_YEAR}</h2>
    </div>
</section>

<section class="conferences-grid">
    {cards_html}
</section>

<section class="content-section">
    <div class="content-body">
        <h2>Maximizing Your Conference Investment</h2>
        <p>CS conferences are a significant time and budget commitment. To get the most value, identify your top learning goals before you register. Review speaker lists and session descriptions early. Reach out to other registered attendees on LinkedIn to set up meetings in advance. The professionals who leave conferences with the most value are the ones who arrive with a clear plan.</p>

        <p>After the event, share your takeaways with your team. The best CS leaders treat conference attendance as a team investment, not a personal perk. Bring back specific ideas, frameworks, and contacts that can improve how your organization serves customers.</p>
    </div>
</section>

{newsletter_cta_html("Get conference recaps and CS insights delivered weekly.")}
'''

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/conferences/",
        body_content=body,
        active_path="/conferences/",
        extra_head=bc_schema,
    )
    write_page("/conferences/index.html", page)
    print(f"  Built: /conferences/ ({len(conferences)} conferences)")
