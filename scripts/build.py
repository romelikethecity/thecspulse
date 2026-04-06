# scripts/build.py
# Main build pipeline: generates all pages, sitemap, robots, CNAME.
# Data + page generators live here. HTML shell lives in templates.py.
# Site constants live in nav_config.py.

import os
import sys
import re
import shutil
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nav_config import *
import templates
from templates import (get_page_wrapper, write_page, get_homepage_schema,
                       get_breadcrumb_schema, get_faq_schema,
                       get_article_schema,
                       breadcrumb_html, newsletter_cta_html, faq_html, ALL_PAGES)
from salary_pages import build_all_salary_pages
from tools_pages import build_all_tools_pages
from glossary_pages import build_all_glossary_pages

# OG image generation state
SKIP_OG = "--skip-og" in sys.argv


# ---------------------------------------------------------------------------
# Path constants
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
BUILD_DATE = datetime.now().strftime("%Y-%m-%d")

# Wire up templates module
templates.OUTPUT_DIR = OUTPUT_DIR
templates.SKIP_OG = SKIP_OG


# ---------------------------------------------------------------------------
# Homepage
# ---------------------------------------------------------------------------

def build_homepage():
    """Generate the homepage with Organization+WebSite schema."""
    title = "Customer Success Salary and Career Intelligence"
    description = (
        "Salary benchmarks, tool reviews, and career data for customer success professionals."
        " CS platform comparisons, health scoring intel, and job market trends. Updated weekly."
    )

    body = '''<section class="hero">
    <div class="hero-inner">
        <h1>Customer Success, Finally Mapped Out</h1>
        <p class="hero-subtitle">Salary data, tool reviews, career paths, and job listings. Everything CS professionals need to make smarter career moves.</p>
        <div class="stat-grid">
            <div class="stat-block">
                <span class="stat-value">12,000+</span>
                <span class="stat-label">Roles Tracked</span>
            </div>
            <div class="stat-block">
                <span class="stat-value">$55K&#8209;$220K+</span>
                <span class="stat-label">Salary Range</span>
            </div>
            <div class="stat-block">
                <span class="stat-value">42%</span>
                <span class="stat-label">YoY Growth</span>
            </div>
        </div>
        <form class="hero-signup" onsubmit="return false;">
            <input type="email" placeholder="Your email" aria-label="Email address" required>
            <button type="submit" class="btn btn--primary">Get the Weekly Pulse</button>
        </form>
        <p class="hero-signup-note">Free weekly newsletter. Salary shifts, tool intel, job data.</p>
    </div>
</section>

<section class="logo-bar">
    <p class="logo-bar-label">Tracking hiring data from companies like</p>
    <div class="logo-bar-row">
        <span class="logo-name">Gainsight</span>
        <span class="logo-name">Vitally</span>
        <span class="logo-name">ChurnZero</span>
        <span class="logo-name">Totango</span>
        <span class="logo-name">HubSpot</span>
        <span class="logo-name">Salesforce</span>
        <span class="logo-name">Planhat</span>
        <span class="logo-name">Catalyst</span>
        <span class="logo-name">ClientSuccess</span>
        <span class="logo-name">Custify</span>
    </div>
</section>

<section class="section-previews">
    <h2 class="section-previews-heading">Explore Customer Success Intelligence</h2>
    <div class="preview-grid">
        <a href="/salary/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128176;</span></div>
            <h3>Salary Data</h3>
            <p>Breakdowns by seniority, location, and company stage. CSM, CS Director, VP CS, and renewal manager comp data.</p>
            <span class="preview-link">Browse salary data &rarr;</span>
        </a>
        <a href="/tools/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128295;</span></div>
            <h3>Tool Reviews</h3>
            <p>Practitioner-tested reviews of Gainsight, Vitally, ChurnZero, and more. Honest scores, no pay-to-play.</p>
            <span class="preview-link">Browse tools &rarr;</span>
        </a>
        <a href="/careers/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128200;</span></div>
            <h3>Career Guides</h3>
            <p>How to break into CS leadership, negotiate comp, and navigate the CSM-to-VP path. Interview prep and skill maps.</p>
            <span class="preview-link">Browse guides &rarr;</span>
        </a>
        <a href="/jobs/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128188;</span></div>
            <h3>Job Board</h3>
            <p>Curated customer success roles from top SaaS companies. CSMs, CS leaders, renewal managers, and more.</p>
            <span class="preview-link">View all jobs &rarr;</span>
        </a>
        <a href="/glossary/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128218;</span></div>
            <h3>CS Glossary</h3>
            <p>Clear definitions for customer success terms. NRR, health scores, QBRs, expansion revenue, and more.</p>
            <span class="preview-link">Browse glossary &rarr;</span>
        </a>
        <a href="/newsletter/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128232;</span></div>
            <h3>Weekly Newsletter</h3>
            <p>Salary shifts, tool intel, and hiring trends delivered every Monday. Data from 12,000+ tracked job postings.</p>
            <span class="preview-link">Get the weekly pulse &rarr;</span>
        </a>
    </div>
</section>

'''
    body += newsletter_cta_html()

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/",
        body_content=body,
        active_path="/",
        extra_head=get_homepage_schema(),
        body_class="page-home",
    )
    write_page("index.html", page)
    print(f"  Built: index.html")


# ---------------------------------------------------------------------------
# About Page
# ---------------------------------------------------------------------------

def build_about_page():
    """Generate the about page."""
    title = "About The CS Pulse: Independent CS Career Data"
    description = (
        "The CS Pulse offers vendor-neutral salary benchmarks, tool reviews,"
        " and career intelligence for customer success professionals. Built by Rome Thorndike."
    )

    crumbs = [("Home", "/"), ("About", None)]
    body = f'''<div class="salary-content">
    {breadcrumb_html(crumbs)}
    <h1>About The CS Pulse</h1>
    <p>The CS Pulse is an independent resource hub for customer success professionals. We publish salary benchmarks, tool reviews, career guides, and job market analysis.</p>
    <p>Our data comes from public job postings, industry surveys, and direct practitioner input. We are not affiliated with any CS platform vendor.</p>
    <h2>Who Builds This</h2>
    <p>The CS Pulse is built and maintained by <strong>Rome Thorndike</strong>.</p>
    <h2>Contact</h2>
    <p>Questions, corrections, or partnership inquiries: <a href="mailto:rome@getprovyx.com">rome@getprovyx.com</a></p>
</div>'''

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/about/",
        body_content=body,
        active_path="/about/",
        extra_head=get_breadcrumb_schema(crumbs),
    )
    write_page("about/index.html", page)
    print(f"  Built: about/index.html")


# ---------------------------------------------------------------------------
# Newsletter Page
# ---------------------------------------------------------------------------

def build_newsletter_page():
    """Generate the newsletter signup page."""
    title = "The CS Pulse Weekly Newsletter"
    description = (
        "Free weekly newsletter for customer success professionals."
        " Salary shifts, tool intel, CS platform updates, and job market data every Monday."
    )

    body = '''<div class="newsletter-page">
    <h1>Get the Weekly Pulse</h1>
    <p class="lead">Salary shifts, tool intel, and job market data for customer success professionals. Every Monday.</p>
    <ul class="newsletter-features">
        <li>CS salary benchmarks and week-over-week changes</li>
        <li>New CS platform features and tool comparisons</li>
        <li>Job market trends: who is hiring, what they pay</li>
        <li>Career moves and leadership transitions in CS</li>
    </ul>
    <form class="hero-signup" onsubmit="return false;">
        <input type="email" placeholder="Your email" aria-label="Email address" required>
        <button type="submit" class="btn btn--primary">Subscribe</button>
    </form>
    <p class="hero-signup-note">Free. No spam. Unsubscribe anytime.</p>
</div>'''

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/newsletter/",
        body_content=body,
        active_path="/newsletter/",
    )
    write_page("newsletter/index.html", page)
    print(f"  Built: newsletter/index.html")


# ---------------------------------------------------------------------------
# Privacy Policy
# ---------------------------------------------------------------------------

def build_privacy_page():
    title = "Privacy Policy"
    description = "Privacy policy for The CS Pulse. How we collect, use, and protect your data."

    body = f'''<div class="legal-content">
    <h1>Privacy Policy</h1>
    <p><em>Last updated: {BUILD_DATE}</em></p>
    <h2>Information We Collect</h2>
    <p>We collect your email address when you subscribe to our newsletter. We use Google Analytics to collect anonymous usage data including pages visited, time on site, and referral sources.</p>
    <h2>How We Use Your Information</h2>
    <p>Email addresses are used solely to send our weekly newsletter. Analytics data helps us understand which content is most useful and improve the site.</p>
    <h2>Third-Party Services</h2>
    <ul>
        <li><strong>Resend</strong> - email delivery and subscriber management</li>
        <li><strong>Google Analytics</strong> - anonymous site usage analytics</li>
        <li><strong>Cloudflare</strong> - CDN, DNS, and worker hosting</li>
        <li><strong>GitHub Pages</strong> - static site hosting</li>
    </ul>
    <h2>Data Retention</h2>
    <p>Email addresses are retained until you unsubscribe. Analytics data is retained per Google Analytics default settings.</p>
    <h2>Your Rights</h2>
    <p>You can unsubscribe from our newsletter at any time using the link in any email. To request data deletion, contact <a href="mailto:rome@getprovyx.com">rome@getprovyx.com</a>.</p>
    <h2>Contact</h2>
    <p>Questions about this policy: <a href="mailto:rome@getprovyx.com">rome@getprovyx.com</a></p>
</div>'''

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/privacy/",
        body_content=body,
    )
    write_page("privacy/index.html", page)
    print(f"  Built: privacy/index.html")


# ---------------------------------------------------------------------------
# Terms of Service
# ---------------------------------------------------------------------------

def build_terms_page():
    title = "Terms of Service"
    description = "Terms of service for The CS Pulse. Usage terms for our customer success career intelligence site."

    body = f'''<div class="legal-content">
    <h1>Terms of Service</h1>
    <p><em>Last updated: {BUILD_DATE}</em></p>
    <h2>Acceptance of Terms</h2>
    <p>By accessing The CS Pulse (thecspulse.com), you agree to these terms. If you do not agree, do not use the site.</p>
    <h2>Content</h2>
    <p>All content is provided for informational purposes only. Salary data, tool reviews, and career advice should not be considered financial or legal advice. We make reasonable efforts to ensure accuracy but cannot guarantee all information is current or error-free.</p>
    <h2>Intellectual Property</h2>
    <p>All original content, design, and code on this site is owned by The CS Pulse. You may not reproduce, distribute, or create derivative works without written permission.</p>
    <h2>Newsletter</h2>
    <p>By subscribing to our newsletter, you consent to receiving weekly emails. You can unsubscribe at any time.</p>
    <h2>Limitation of Liability</h2>
    <p>The CS Pulse is not liable for any decisions made based on information provided on this site. Use all data and recommendations at your own discretion.</p>
    <h2>Changes</h2>
    <p>We may update these terms at any time. Continued use of the site after changes constitutes acceptance.</p>
    <h2>Contact</h2>
    <p>Questions about these terms: <a href="mailto:rome@getprovyx.com">rome@getprovyx.com</a></p>
</div>'''

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/terms/",
        body_content=body,
    )
    write_page("terms/index.html", page)
    print(f"  Built: terms/index.html")


# ---------------------------------------------------------------------------
# 404 Page
# ---------------------------------------------------------------------------

def build_404_page():
    title = "Page Not Found"
    description = "The page you are looking for does not exist."

    body = '''<div class="error-page">
    <div class="error-code">404</div>
    <h1>Page Not Found</h1>
    <p>The page you are looking for does not exist or has been moved.</p>
    <a href="/" class="btn btn--primary">Back to Home</a>
</div>'''

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/404.html",
        body_content=body,
    )
    write_page("404.html", page)
    print(f"  Built: 404.html")


# ---------------------------------------------------------------------------
# Sitemap & Robots
# ---------------------------------------------------------------------------

def build_sitemap():
    urls = ""
    for page_path in ALL_PAGES:
        clean = page_path.replace("index.html", "")
        if not clean.startswith("/"):
            clean = "/" + clean
        if not clean.endswith("/"):
            clean += "/"
        if clean == "//":
            clean = "/"
        urls += f"  <url>\n    <loc>{SITE_URL}{clean}</loc>\n    <lastmod>{BUILD_DATE}</lastmod>\n  </url>\n"

    sitemap = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'
    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"  Built: sitemap.xml ({len(ALL_PAGES)} URLs)")


def build_robots():
    content = f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n"
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Built: robots.txt")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"=== The CS Pulse Build ({BUILD_DATE}) ===\n")

    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    print("  Cleaned output/")

    shutil.copytree(ASSETS_DIR, os.path.join(OUTPUT_DIR, "assets"))
    print("  Copied assets/")

    print("\n  Building core pages...")
    build_homepage()
    build_about_page()
    build_newsletter_page()
    build_privacy_page()
    build_terms_page()
    build_404_page()

    build_all_salary_pages()
    build_all_tools_pages()
    build_all_glossary_pages()

    print("\n  Building meta files...")
    build_sitemap()
    build_robots()

    with open(os.path.join(OUTPUT_DIR, "CNAME"), "w", encoding="utf-8") as f:
        f.write("thecspulse.com\n")
    print("  Built: CNAME")

    # Google Search Console verification file
    if GOOGLE_SITE_VERIFICATION:
        verification_path = os.path.join(OUTPUT_DIR, GOOGLE_SITE_VERIFICATION)
        with open(verification_path, "w", encoding="utf-8") as f:
            f.write(f"google-site-verification: {GOOGLE_SITE_VERIFICATION}")
        print(f"  Generated {GOOGLE_SITE_VERIFICATION}")

    print(f"\n=== Build complete: {len(ALL_PAGES)} pages ===")
    print(f"  Output: {OUTPUT_DIR}")
    print(f"  Preview: cd output && python3 -m http.server 8090")


if __name__ == "__main__":
    main()
