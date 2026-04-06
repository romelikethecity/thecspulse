# scripts/insights_pages.py
# Insights hub page + /blog/ redirect.

import os

from nav_config import *
from templates import (get_page_wrapper, write_page, get_breadcrumb_schema,
                       breadcrumb_html, newsletter_cta_html)


# ---------------------------------------------------------------------------
# Insights Hub Page
# ---------------------------------------------------------------------------

def build_insights_index():
    """Generate the /insights/ hub page."""
    title = "Customer Success Insights and Analysis"
    description = (
        "Data-driven insights on customer success trends, compensation shifts,"
        " platform changes, and retention strategy. Original research for CS professionals."
    )

    crumbs = [("Home", "/"), ("Insights", None)]
    body = f'''<div class="salary-content">
    {breadcrumb_html(crumbs)}
    <h1>Customer Success Insights</h1>

    <p>Original research and analysis on the customer success industry. We dig into compensation data, platform adoption trends, retention benchmarks, and the operational changes reshaping how CS teams work.</p>

    <p>Every insight published here is grounded in data from job postings, public company filings, practitioner surveys, and our own benchmarking. No vendor-sponsored content. No pay-to-play rankings.</p>

    <h2>What We Cover</h2>

    <ul>
        <li><strong>Compensation analysis</strong> - How CS salaries are shifting by role, location, company stage, and industry. Quarterly deep dives with trend data.</li>
        <li><strong>Platform and tooling trends</strong> - Which CS platforms are gaining market share, which are losing it, and what that means for teams evaluating their tech stack.</li>
        <li><strong>Retention benchmarks</strong> - NRR, GRR, and churn data segmented by company size and vertical. How top-performing CS orgs structure their retention motions.</li>
        <li><strong>Operational playbooks</strong> - How leading CS teams are structuring onboarding, health scoring, renewal forecasting, and expansion plays.</li>
        <li><strong>Job market intelligence</strong> - Hiring velocity, emerging roles, and which skills are commanding premium compensation.</li>
    </ul>

    <h2>Coming Soon</h2>

    <p>We are building out our first wave of long-form research. Upcoming publications include:</p>

    <ul>
        <li>Q1 2026 CS Salary Benchmark Report</li>
        <li>CS Platform Market Share Analysis</li>
        <li>The State of Digital Customer Success</li>
        <li>NRR by Company Stage: What Good Looks Like</li>
    </ul>

    <p>Subscribe to our newsletter to get notified when new research drops.</p>

'''
    body += newsletter_cta_html()
    body += '</div>'

    extra_head = get_breadcrumb_schema(crumbs)
    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/insights/",
        body_content=body,
        active_path="/insights/",
        extra_head=extra_head,
    )
    write_page("insights/index.html", page)
    print(f"  Built: insights/index.html")


# ---------------------------------------------------------------------------
# Blog Redirect
# ---------------------------------------------------------------------------

def build_blog_redirect():
    """Generate /blog/ as a redirect to /insights/."""
    redirect_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0;url=/insights/">
    <link rel="canonical" href="https://thecspulse.com/insights/">
    <title>Redirecting to Insights</title>
</head>
<body>
    <p>Redirecting to <a href="/insights/">Insights</a>...</p>
</body>
</html>'''

    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
    blog_dir = os.path.join(out_dir, "blog")
    os.makedirs(blog_dir, exist_ok=True)
    with open(os.path.join(blog_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(redirect_html)
    print(f"  Built: blog/index.html (redirect to /insights/)")


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def build_all_insights_pages():
    """Build insights hub and blog redirect."""
    print("\n  Building insights pages...")
    build_insights_index()
    build_blog_redirect()
