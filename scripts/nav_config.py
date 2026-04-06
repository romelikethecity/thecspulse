# scripts/nav_config.py
# Site constants, navigation, and footer configuration.
# Pure data — zero logic, zero imports.

SITE_NAME = "The CS Pulse"
SITE_URL = "https://thecspulse.com"
SITE_TAGLINE = "Career intelligence for customer success professionals"
COPYRIGHT_YEAR = "2026"
CURRENT_YEAR = 2026
CSS_VERSION = "1"

CTA_HREF = "/newsletter/"
CTA_LABEL = "Get the Weekly Pulse"

SIGNUP_WORKER_URL = "https://newsletter-subscribe.rome-workers.workers.dev/subscribe"

GA_MEASUREMENT_ID = "G-H8V6QYNJPC"
GOOGLE_SITE_VERIFICATION = ""  # Set to verification filename (e.g., "google1234abcd.html") to generate file
GOOGLE_SITE_VERIFICATION_META = ""  # Set to verification code for meta tag method (alternative to HTML file)

NAV_ITEMS = [
    {
        "href": "/salary/",
        "label": "Salary Data",
        "children": [
            {"href": "/salary/", "label": "Salary Index"},
            {"href": "/salary/by-seniority/", "label": "By Seniority"},
            {"href": "/salary/by-location/", "label": "By Location"},
            {"href": "/salary/remote-vs-onsite/", "label": "Remote vs Onsite"},
            {"href": "/salary/calculator/", "label": "Salary Calculator"},
            {"href": "/salary/methodology/", "label": "Methodology"},
        ],
    },
    {
        "href": "/tools/",
        "label": "Tools",
        "children": [
            {"href": "/tools/", "label": "Tools Index"},
            {"href": "/tools/category/cs-platforms/", "label": "CS Platforms"},
            {"href": "/tools/category/onboarding/", "label": "Onboarding"},
            {"href": "/tools/category/feedback/", "label": "Feedback & Survey"},
            {"href": "/tools/category/digital-adoption/", "label": "Digital Adoption"},
            {"href": "/tools/category/revenue-intelligence/", "label": "Revenue Intelligence"},
            {"href": "/tools/category/crm/", "label": "CRM"},
        ],
    },
    {
        "href": "/careers/",
        "label": "Careers",
        "children": [
            {"href": "/careers/", "label": "Career Guides"},
            {"href": "/careers/how-to-become-cs-leader/", "label": "How to Become a CS Leader"},
            {"href": "/careers/job-growth/", "label": "Job Market Growth"},
        ],
    },
    {"href": "/glossary/", "label": "Glossary"},
    {"href": "/insights/", "label": "Insights"},
]

FOOTER_COLUMNS = {
    "Salary Data": [
        {"href": "/salary/", "label": "Salary Index"},
        {"href": "/salary/by-seniority/", "label": "By Seniority"},
        {"href": "/salary/by-location/", "label": "By Location"},
        {"href": "/salary/remote-vs-onsite/", "label": "Remote vs Onsite"},
        {"href": "/salary/calculator/", "label": "Salary Calculator"},
        {"href": "/salary/methodology/", "label": "Methodology"},
    ],
    "CS Tools": [
        {"href": "/tools/", "label": "Tools Index"},
        {"href": "/tools/category/cs-platforms/", "label": "CS Platforms"},
        {"href": "/tools/category/onboarding/", "label": "Onboarding"},
        {"href": "/tools/category/feedback/", "label": "Feedback & Survey"},
        {"href": "/tools/gainsight/", "label": "Gainsight Review"},
        {"href": "/tools/roundup/best-cs-platforms/", "label": "Best CS Platforms"},
    ],
    "Resources": [
        {"href": "/careers/", "label": "Career Guides"},
        {"href": "/glossary/", "label": "Glossary"},
        {"href": "/insights/", "label": "Insights"},
        {"href": "/newsletter/", "label": "Newsletter"},
        {"href": "/about/", "label": "About"},
    ],
    "Site": [
        {"href": "/privacy/", "label": "Privacy Policy"},
        {"href": "/terms/", "label": "Terms of Service"},
    ],
    "CS Tools & Resources": [
        {"href": "https://gtmepulse.com", "label": "GTME Pulse", "external": True},
        {"href": "https://therevopsreport.com", "label": "RevOps Report", "external": True},
        {"href": "https://b2bsalestools.com", "label": "B2B Sales Tools", "external": True},
    ],
}
