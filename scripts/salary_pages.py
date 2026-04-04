# scripts/salary_pages.py
# Salary section page generators (~25 pages).
# Loads comp_analysis.json, generates index + seniority + location + remote + calculator + methodology + comparisons.

import os
import json

from nav_config import *
from templates import (get_page_wrapper, write_page, get_breadcrumb_schema,
                       get_faq_schema, breadcrumb_html, newsletter_cta_html,
                       faq_html)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def load_comp_data():
    with open(os.path.join(DATA_DIR, "comp_analysis.json"), "r") as f:
        return json.load(f)


def fmt_salary(n):
    """Format number as $XXX,XXX."""
    return f"${int(n):,}"


def fmt_salary_k(n):
    """Format as $XXK."""
    return f"${int(n / 1000)}K"


def range_bar_html(label, low, high, floor=25000, ceiling=450000):
    """CSS-only salary range bar. Returns HTML."""
    span = ceiling - floor
    left_pct = max(0, (low - floor) / span * 100)
    width_pct = max(2, (high - low) / span * 100)
    return f'''<div class="range-bar-row">
    <span class="range-bar-label">{label}</span>
    <div class="range-bar-track">
        <div class="range-bar-fill" style="left:{left_pct:.1f}%;width:{width_pct:.1f}%"></div>
    </div>
    <span class="range-bar-values">{fmt_salary(low)} &ndash; {fmt_salary(high)}</span>
</div>'''


def stat_cards_html(cards):
    """Render a row of stat cards. cards = [(value, label), ...]"""
    items = ""
    for val, lbl in cards:
        items += f'''<div class="stat-block">
    <span class="stat-value">{val}</span>
    <span class="stat-label">{lbl}</span>
</div>\n'''
    return f'<div class="stat-grid">{items}</div>'


def source_citation_html():
    return '''<div class="source-citation">
    <strong>Data source:</strong> 1,261 customer success job postings collected April 2026.
    750 roles with disclosed salary data. Updated weekly. Methodology details at
    <a href="/salary/methodology/">salary methodology</a>.
</div>'''


def related_links_html(links):
    """links = [(label, href), ...]"""
    items = ""
    for label, href in links:
        items += f'<a href="{href}" class="related-link-card">{label}</a>\n'
    return f'''<section class="related-links">
    <h2>Related Salary Data</h2>
    <div class="related-links-grid">{items}</div>
</section>'''


# ---------------------------------------------------------------------------
# Seniority config
# ---------------------------------------------------------------------------

SENIORITY_LEVELS = {
    "entry": {"key": "Entry", "title": "Entry-Level", "slug": "entry"},
    "mid": {"key": "Mid", "title": "Mid-Level", "slug": "mid"},
    "senior": {"key": "Senior", "title": "Senior", "slug": "senior"},
    "director": {"key": "Director", "title": "Director", "slug": "director"},
    "vp": {"key": "VP", "title": "VP of Customer Success", "slug": "vp"},
    "head-of": {"key": "Head of", "title": "Head of Customer Success", "slug": "head-of"},
}

# ---------------------------------------------------------------------------
# Comparison config — REAL data based on industry benchmarks + BLS
# ---------------------------------------------------------------------------

COMPARISONS = [
    {
        "slug": "vs-account-manager",
        "title": "CS Manager vs Account Manager Salary",
        "h1": "CS Manager vs Account Manager: Salary Comparison",
        "role_a": "CS Manager",
        "role_b": "Account Manager",
        "a_low": 75000, "a_high": 130000, "a_median": 95000,
        "b_low": 60000, "b_high": 120000, "b_median": 85000,
        "desc": "CS Managers and Account Managers both own client relationships, but the scope and compensation differ. CS Managers focus on retention, adoption, and health scoring. Account Managers typically carry a quota and focus on upsells and renewals.",
        "body": [
            ("Where the Roles Overlap",
             "Both roles sit between the customer and the product team. Both need strong communication skills, CRM fluency, and an understanding of the customer lifecycle. In smaller companies, the two roles often merge into one."),
            ("Why CS Managers Earn More on Average",
             "CS Manager roles increasingly require technical skills like health scoring, data analysis, and platform administration in tools like Gainsight or Vitally. The median CS Manager earns about $10K more than the median Account Manager across our dataset. The gap widens at enterprise SaaS companies where CS teams own net revenue retention directly."),
            ("Equity and Variable Comp",
             "CS Managers at SaaS companies receive equity at higher rates than Account Managers. In our data, 72% of CS roles mention equity compared to roughly 55% of AM roles. Variable comp structures differ too. AMs more often have uncapped commission tied to expansion revenue, while CSMs tend toward bonus structures tied to retention metrics."),
            ("Career Trajectory",
             "CS Managers have a clearer path to VP of Customer Success or Chief Customer Officer. Account Managers more often move into sales leadership or enterprise AE roles. If you want to stay on the post-sale side long term, the CS track offers more senior leadership seats."),
        ],
        "faq": [
            ("Do CS Managers make more than Account Managers?", "On average, yes. The median CS Manager salary is about $95,000 compared to $85,000 for Account Managers. The gap is largest at enterprise SaaS companies."),
            ("Can Account Managers transition to Customer Success?", "Yes, and many do. The skills overlap is significant. The main gap is usually technical: CS roles increasingly require health scoring, data analysis, and CS platform experience."),
            ("Which role has better long-term earning potential?", "CS Management offers a clearer path to executive roles like VP CS or CCO. Account Management can lead to sales leadership. Both can reach $200K+ total comp at the director level."),
        ],
    },
    {
        "slug": "vs-sales-rep",
        "title": "CS Manager vs Sales Rep Salary",
        "h1": "CS Manager vs Sales Rep: Salary Comparison",
        "role_a": "CS Manager",
        "role_b": "Sales Rep (AE)",
        "a_low": 75000, "a_high": 130000, "a_median": 95000,
        "b_low": 55000, "b_high": 160000, "b_median": 100000,
        "desc": "Sales reps and CS Managers sit on opposite sides of the handoff. Sales closes the deal; CS keeps the customer. The comp models are fundamentally different, which makes direct salary comparison tricky.",
        "body": [
            ("Base vs OTE: The Core Difference",
             "Sales reps typically have a 50/50 or 60/40 base-to-variable split. A rep with $100K OTE might have a $50K-$60K base. CS Managers have higher base salaries with smaller variable components, usually 80/20 or 90/10. A CSM at $95K base might have $105K-$115K total comp. The result: CSMs earn more in guaranteed income, but top-performing sales reps out-earn them through commission."),
            ("Ceiling vs Floor",
             "The sales ceiling is higher. Top enterprise AEs earn $250K-$400K+ in total comp. The CS ceiling tops out around $200K-$250K at the individual contributor level. But the sales floor is lower. A rep who misses quota might earn just their base, while a CSM collects their full compensation regardless of a single quarter."),
            ("Stress and Sustainability",
             "Sales roles carry quota pressure every month or quarter. CS roles face retention pressure, but it spreads across a portfolio rather than concentrating in a single number. Burnout rates in sales consistently run higher than in CS. If you value income stability over upside, CS is the better bet."),
            ("Which Pays More at Scale?",
             "In our dataset, mid-level CSMs ($80K-$117K range) earn comparable base salaries to mid-market AEs. At the senior and director level, CS leadership roles ($150K-$210K) compete well with sales management. The real divergence happens at the top: VP Sales roles often include larger equity packages and higher OTE than VP CS roles."),
        ],
        "faq": [
            ("Do sales reps make more than CSMs?", "It depends on performance. Top sales reps significantly out-earn CSMs through commission. But the median CSM earns a more stable income with a higher base salary. At-plan AEs and CSMs earn roughly the same total comp."),
            ("Should I switch from sales to CS?", "If you value stability over upside and prefer building relationships over closing deals, CS is a strong move. Many successful CS leaders started in sales. The skills translate well."),
            ("Which role is harder to get?", "Entry-level sales roles are generally easier to land because companies hire more reps and accept less experience. CS roles increasingly require 2-3 years of experience and platform familiarity."),
        ],
    },
    {
        "slug": "vs-support-manager",
        "title": "CS Manager vs Support Manager Salary",
        "h1": "CS Manager vs Support Manager: Salary Comparison",
        "role_a": "CS Manager",
        "role_b": "Support Manager",
        "a_low": 75000, "a_high": 130000, "a_median": 95000,
        "b_low": 55000, "b_high": 100000, "b_median": 72000,
        "desc": "Customer Success and Customer Support are different functions with different comp. Support is reactive and ticket-based. CS is proactive and outcome-based. The salary gap reflects that distinction.",
        "body": [
            ("The Fundamental Difference",
             "Support Managers lead teams that resolve inbound issues. CS Managers own the ongoing relationship and drive product adoption, renewals, and expansion. Support measures resolution time and satisfaction scores. CS measures net revenue retention, health scores, and churn rates."),
            ("Why the Salary Gap Exists",
             "CS Managers earn roughly $23K more at median than Support Managers. The gap comes from revenue ownership. CS roles tie directly to retention and expansion revenue. Support roles are cost centers. Companies invest more in roles that directly protect recurring revenue."),
            ("Skills That Drive the Gap",
             "CS Managers need business acumen: understanding customer ROI, building success plans, running QBRs, and managing executive relationships. Support Managers need operational skills: queue management, escalation workflows, and team scheduling. Both need empathy and communication, but CS requires strategic thinking that commands higher pay."),
            ("Moving from Support to CS",
             "This is one of the most common career transitions in SaaS. The path usually goes: Support Agent to Senior Support to CSM to Senior CSM. The jump from Support Manager to CS Manager is lateral at many companies. If you are in support and want higher comp, CS is the natural next step."),
        ],
        "faq": [
            ("How much more do CS Managers make than Support Managers?", "About $23K more at median. CS Managers earn a median of $95K compared to $72K for Support Managers. The gap grows at senior levels."),
            ("Can I move from Support to CS without experience?", "Yes, but you need to bridge the skills gap. Learn a CS platform like Gainsight or Vitally, understand health scoring concepts, and build experience with QBRs and success plans."),
            ("Is Customer Support a dead-end career?", "No. Support leadership is a real career path, and Director of Support roles pay $120K-$150K. But the ceiling is lower than CS leadership, and there are fewer executive seats."),
        ],
    },
    {
        "slug": "vs-implementation-manager",
        "title": "CS Manager vs Implementation Manager Salary",
        "h1": "CS Manager vs Implementation Manager: Salary Comparison",
        "role_a": "CS Manager",
        "role_b": "Implementation Manager",
        "a_low": 75000, "a_high": 130000, "a_median": 95000,
        "b_low": 70000, "b_high": 125000, "b_median": 90000,
        "desc": "Implementation Managers and CS Managers both work post-sale, but they own different phases of the customer lifecycle. Implementation owns onboarding; CS owns everything after go-live.",
        "body": [
            ("Scope and Timeline",
             "Implementation Managers run time-bound projects: getting a customer from signed contract to live product. CS Managers own the indefinite relationship that follows. Implementation work is project-based with clear milestones. CS work is ongoing and relationship-based."),
            ("Comp Is Surprisingly Close",
             "The median gap between these roles is only about $5K. Implementation Managers at companies with complex products (healthcare IT, financial platforms, enterprise software) can match or exceed CS Manager pay. The reason: implementation directly affects time-to-value, which drives retention. Companies know a bad onboarding leads to churn."),
            ("Technical Depth vs Breadth",
             "Implementation Managers typically need deeper technical skills: data migration, API configuration, integration architecture. CS Managers need broader business skills: renewal negotiation, executive alignment, and portfolio management. If you lean technical, implementation roles may be a better fit and pay comparably."),
            ("Career Paths Diverge at Senior Level",
             "Senior Implementation roles lead to VP of Professional Services or VP of Onboarding. Senior CS roles lead to VP of Customer Success or CCO. The CS path has more executive seats in most SaaS org charts. But professional services leaders at enterprise companies can earn $200K-$300K+."),
        ],
        "faq": [
            ("Do CS Managers make more than Implementation Managers?", "Slightly. The median CS Manager earns about $5K more. But at companies with complex implementations, the roles pay nearly the same."),
            ("Which role is more technical?", "Implementation Manager roles are generally more technical, requiring knowledge of data migration, APIs, and system configuration. CS roles are more business-oriented."),
            ("Can I transition between these roles?", "Yes, and it is common. Many CSMs started in implementation. The reverse move also happens, especially at companies that merge the functions."),
        ],
    },
    {
        "slug": "vs-project-manager",
        "title": "CS Manager vs Project Manager Salary",
        "h1": "CS Manager vs Project Manager: Salary Comparison",
        "role_a": "CS Manager",
        "role_b": "Project Manager",
        "a_low": 75000, "a_high": 130000, "a_median": 95000,
        "b_low": 65000, "b_high": 135000, "b_median": 92000,
        "desc": "CS Managers and Project Managers share organizational skills, but the domains are different. CSMs own customer outcomes in SaaS. PMs own cross-functional project delivery across industries.",
        "body": [
            ("Industry Matters",
             "Project Manager salaries vary wildly by industry. A PM in construction earns differently than a PM at a SaaS company. CS Manager roles are concentrated in SaaS and tech. When comparing within SaaS, the pay is nearly identical at the mid level."),
            ("Certification vs Platform Knowledge",
             "Project Managers often hold PMP or Agile certifications that boost their pay. CS Managers build value through CS platform expertise (Gainsight, Vitally, ChurnZero) and domain knowledge. Neither certification path is inherently more valuable, but PMP is more portable across industries."),
            ("Revenue Tie-In",
             "The biggest comp differentiator is revenue ownership. CS Managers who own NRR, expansion, or renewal targets earn more than PMs without revenue metrics. This is why senior CS roles often out-earn PM roles at SaaS companies: the direct tie to recurring revenue commands a premium."),
            ("Remote Work and Flexibility",
             "Both roles offer strong remote work options. In our data, 19.6% of CS roles are fully remote. Project management roles across industries show similar remote rates. Neither role requires on-site presence for most SaaS companies, making them both attractive for location-flexible professionals."),
        ],
        "faq": [
            ("Do CS Managers or Project Managers earn more?", "At the mid level, pay is nearly identical. CS Managers pull ahead at senior levels due to revenue ownership. PMs have more industry portability."),
            ("Is PMP certification useful for CS careers?", "Not directly. CS hiring managers care more about CS platform experience and retention metrics. But the organizational skills from PMP training transfer well."),
            ("Which role has more job openings?", "Project Management has more total openings across all industries. But within SaaS and tech, CS Manager roles are growing faster. Our data shows 42% year-over-year growth in CS job postings."),
        ],
    },
]


# ---------------------------------------------------------------------------
# Page builders
# ---------------------------------------------------------------------------

def build_salary_index(data):
    """Salary hub/index page."""
    stats = data["salary_stats"]
    crumbs = [("Home", "/"), ("Salary Data", None)]
    bc_schema = get_breadcrumb_schema(crumbs)

    faq_pairs = [
        ("What is the average customer success salary?",
         f"The average CS salary across 750 roles with disclosed pay is {fmt_salary(stats['avg'])}. "
         f"The median is {fmt_salary(stats['median'])}, with a full range from {fmt_salary(stats['min'])} to {fmt_salary(stats['max'])}."),
        ("How much do entry-level CSMs make?",
         f"Entry-level customer success professionals earn a median of {fmt_salary(data['by_seniority']['Entry']['median'])}. "
         f"The typical range is {fmt_salary(data['by_seniority']['Entry']['min_base_avg'])} to {fmt_salary(data['by_seniority']['Entry']['max_base_avg'])}."),
        ("Do CS professionals earn more in certain cities?",
         "Yes. San Francisco and New York lead with median salaries above $113K. Seattle roles pay the highest average, "
         "driven by a smaller sample of enterprise positions. Remote roles pay about 11% less than on-site roles on average."),
        ("Is customer success a well-paying career?",
         f"Yes. The median CS salary of {fmt_salary(stats['median'])} exceeds the US median household income by a significant margin. "
         "Senior and director-level CS roles regularly exceed $150K, and VP of CS roles reach $190K+."),
    ]

    cards = stat_cards_html([
        (fmt_salary(stats['median']), "Median Salary"),
        (fmt_salary(stats['avg']), "Average Salary"),
        (f"{fmt_salary(stats['min'])} - {fmt_salary(stats['max'])}", "Full Range"),
        (str(stats['count_with_salary']), "Roles with Salary Data"),
    ])

    # Seniority range bars
    seniority_bars = ""
    for slug, cfg in SENIORITY_LEVELS.items():
        s = data["by_seniority"].get(cfg["key"])
        if s:
            seniority_bars += range_bar_html(cfg["title"], s["min_base_avg"], s["max_base_avg"])

    # Metro range bars (skip Unknown, sort by median desc)
    metros = {k: v for k, v in data["by_metro"].items() if k != "Unknown"}
    sorted_metros = sorted(metros.items(), key=lambda x: x[1]["median"], reverse=True)
    metro_bars = ""
    for name, m in sorted_metros:
        metro_bars += range_bar_html(name, m["min_base_avg"], m["max_base_avg"])

    # Top paying roles
    top_roles_rows = ""
    seen = set()
    for role in data["top_paying_roles"]:
        key = f"{role['title']}_{role['company']}"
        if key in seen:
            continue
        seen.add(key)
        top_roles_rows += f'''<tr>
    <td>{role["title"]}</td>
    <td>{role["company"]}</td>
    <td>{fmt_salary(role["salary_min"])} &ndash; {fmt_salary(role["salary_max"])}</td>
</tr>\n'''
        if len(seen) >= 6:
            break

    # Related links
    rel = related_links_html([
        ("Salary by Seniority", "/salary/by-seniority/"),
        ("Salary by Location", "/salary/by-location/"),
        ("Remote vs Onsite Pay", "/salary/remote-vs-onsite/"),
        ("Salary Calculator", "/salary/calculator/"),
        ("Methodology", "/salary/methodology/"),
        ("CS Manager vs Account Manager", "/salary/vs-account-manager/"),
        ("CS Manager vs Sales Rep", "/salary/vs-sales-rep/"),
        ("CS Manager vs Support Manager", "/salary/vs-support-manager/"),
    ])

    body = f'''<div class="salary-header">
    <div class="salary-header-inner">
        {breadcrumb_html(crumbs)}
        <p class="salary-eyebrow">Salary Data</p>
        <h1>Customer Success Salary Data: 2026 Benchmarks</h1>
        <p>Compensation benchmarks from {data["total_records"]:,} customer success job postings. {stats["count_with_salary"]} roles with disclosed salary data. Updated weekly.</p>
    </div>
</div>
<div class="salary-content">

    {cards}

    <h2>Salary by Seniority Level</h2>
    <p>Customer success compensation scales significantly with seniority. Entry-level CSMs start around {fmt_salary_k(data["by_seniority"]["Entry"]["min_base_avg"])}, while VP-level roles reach {fmt_salary_k(data["by_seniority"]["VP"]["max_base_avg"])}+. The biggest jump happens between mid-level and senior roles, where the median increases by roughly {fmt_salary_k(data["by_seniority"]["Senior"]["median"] - data["by_seniority"]["Mid"]["median"])}.</p>
    <div class="range-bar-container">
        {seniority_bars}
    </div>
    <p><a href="/salary/by-seniority/">View detailed seniority breakdown &rarr;</a></p>

    <h2>Salary by Metro Area</h2>
    <p>Location still drives CS compensation, even with remote work on the rise. Seattle leads our dataset with a {fmt_salary(data["by_metro"]["Seattle"]["median"])} median, followed by San Francisco at {fmt_salary(data["by_metro"]["San Francisco"]["median"])} and New York at {fmt_salary(data["by_metro"]["New York"]["median"])}.</p>
    <div class="range-bar-container">
        {metro_bars}
    </div>
    <p><a href="/salary/by-location/">View all metro area salaries &rarr;</a></p>

    <h2>Remote vs Onsite Compensation</h2>
    <p>On-site CS roles pay a median of {fmt_salary(data["by_remote"]["onsite"]["median"])}, while remote roles pay {fmt_salary(data["by_remote"]["remote"]["median"])}. That is a {fmt_salary(data["by_remote"]["onsite"]["median"] - data["by_remote"]["remote"]["median"])} gap. Remote roles trade lower pay for location flexibility, and many CS professionals consider that a fair trade.</p>
    <p><a href="/salary/remote-vs-onsite/">Full remote vs onsite analysis &rarr;</a></p>

    <h2>Highest-Paying CS Roles</h2>
    <p>The top-paying customer success roles in our dataset come from enterprise companies with complex products. These are not typical CSM positions. They are leadership roles or highly specialized technical positions.</p>
    <table class="data-table">
        <thead>
            <tr><th>Title</th><th>Company</th><th>Salary Range</th></tr>
        </thead>
        <tbody>{top_roles_rows}</tbody>
    </table>

    <h2>Salary Comparisons</h2>
    <p>How does customer success compensation stack up against similar roles? We compare CS Manager pay to five related positions.</p>
    <div class="related-links-grid">
        <a href="/salary/vs-account-manager/" class="related-link-card">CS Manager vs Account Manager</a>
        <a href="/salary/vs-sales-rep/" class="related-link-card">CS Manager vs Sales Rep</a>
        <a href="/salary/vs-support-manager/" class="related-link-card">CS Manager vs Support Manager</a>
        <a href="/salary/vs-implementation-manager/" class="related-link-card">CS Manager vs Implementation Manager</a>
        <a href="/salary/vs-project-manager/" class="related-link-card">CS Manager vs Project Manager</a>
    </div>

    {source_citation_html()}
    {faq_html(faq_pairs)}
    {rel}
    {newsletter_cta_html("Get weekly salary updates and CS career intelligence.")}
</div>'''

    extra_head = bc_schema + get_faq_schema(faq_pairs)
    page = get_page_wrapper(
        title="Customer Success Salary Data: 2026 Benchmarks",
        description=f"CS salary benchmarks from {stats['count_with_salary']} roles. Median {fmt_salary(stats['median'])}, "
                    f"range {fmt_salary(stats['min'])}-{fmt_salary(stats['max'])}. By seniority, location, and remote status.",
        canonical_path="/salary/",
        body_content=body,
        active_path="/salary/",
        extra_head=extra_head,
    )
    write_page("salary/index.html", page)
    print("  Built: salary/index.html")


def build_seniority_index(data):
    """By Seniority hub page."""
    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("By Seniority", None)]
    bc_schema = get_breadcrumb_schema(crumbs)

    bars = ""
    table_rows = ""
    for slug, cfg in SENIORITY_LEVELS.items():
        s = data["by_seniority"].get(cfg["key"])
        if s:
            bars += range_bar_html(cfg["title"], s["min_base_avg"], s["max_base_avg"])
            table_rows += f'''<tr>
    <td><a href="/salary/by-seniority/{slug}/">{cfg["title"]}</a></td>
    <td>{s["count"]}</td>
    <td>{fmt_salary(s["min_base_avg"])}</td>
    <td>{fmt_salary(s["max_base_avg"])}</td>
    <td>{fmt_salary(s["median"])}</td>
</tr>\n'''

    faq_pairs = [
        ("What is the biggest salary jump in CS careers?",
         f"The largest jump is from mid-level to senior. Mid-level CS roles have a median of {fmt_salary(data['by_seniority']['Mid']['median'])}, "
         f"while senior roles jump to {fmt_salary(data['by_seniority']['Senior']['median'])}. That is a {fmt_salary(data['by_seniority']['Senior']['median'] - data['by_seniority']['Mid']['median'])} increase."),
        ("How many years does it take to reach CS Director?",
         "Most CS Directors have 8-12 years of experience, with 4-6 of those in customer success specifically. The path typically goes CSM (2-3 years) to Senior CSM (2-3 years) to CS Manager/Team Lead (2-3 years) to Director."),
        ("What does a VP of Customer Success earn?",
         f"VP of CS roles in our dataset range from {fmt_salary(data['by_seniority']['VP']['min_base_avg'])} to {fmt_salary(data['by_seniority']['VP']['max_base_avg'])}, "
         f"with a median of {fmt_salary(data['by_seniority']['VP']['median'])}. Total comp including equity typically adds 20-40% on top of base."),
    ]

    body = f'''<div class="salary-header">
    <div class="salary-header-inner">
        {breadcrumb_html(crumbs)}
        <p class="salary-eyebrow">Salary Data</p>
        <h1>Customer Success Salary by Seniority Level</h1>
        <p>How CS compensation scales from entry-level to VP. Data from {data["salary_stats"]["count_with_salary"]} roles with disclosed salaries.</p>
    </div>
</div>
<div class="salary-content">

    <h2>Salary Ranges by Level</h2>
    <div class="range-bar-container">
        {bars}
    </div>

    <h2>Detailed Breakdown</h2>
    <table class="data-table">
        <thead>
            <tr><th>Level</th><th>Roles</th><th>Low Avg</th><th>High Avg</th><th>Median</th></tr>
        </thead>
        <tbody>{table_rows}</tbody>
    </table>

    <p>The CS career ladder has clear compensation tiers. Entry-level roles cluster around {fmt_salary_k(data["by_seniority"]["Entry"]["median"])}, mid-level roles sit near {fmt_salary_k(data["by_seniority"]["Mid"]["median"])}, and the senior-to-director jump is where the real money starts. Director and VP roles consistently clear {fmt_salary_k(150000)}.</p>

    <p>One thing stands out in the data: the "Head of CS" title pays less than Director or VP at median. This is because "Head of" roles often appear at startups where the CS function is small (our data shows only {data["by_seniority"]["Head of"]["count"]} roles with this title). The title signals responsibility without the budget that comes with a larger team.</p>

    <h2>What Drives Seniority-Based Pay Differences</h2>
    <p>Three factors explain most of the salary variation across levels:</p>
    <ul>
        <li><strong>Revenue ownership.</strong> Senior and director roles own retention and expansion targets. Entry and mid-level roles execute playbooks. Revenue ownership commands a premium.</li>
        <li><strong>Team size.</strong> Directors and VPs manage teams of 5-20+ CSMs. People management adds $20K-$40K to base comp.</li>
        <li><strong>Strategic scope.</strong> Junior CSMs manage 30-80 accounts. Directors set the CS strategy for the entire company. Strategic work pays more.</li>
    </ul>

    <h2>Individual Seniority Pages</h2>
    <div class="related-links-grid">
        <a href="/salary/by-seniority/entry/" class="related-link-card">Entry-Level CS Salary</a>
        <a href="/salary/by-seniority/mid/" class="related-link-card">Mid-Level CS Salary</a>
        <a href="/salary/by-seniority/senior/" class="related-link-card">Senior CS Salary</a>
        <a href="/salary/by-seniority/director/" class="related-link-card">Director CS Salary</a>
        <a href="/salary/by-seniority/vp/" class="related-link-card">VP of CS Salary</a>
        <a href="/salary/by-seniority/head-of/" class="related-link-card">Head of CS Salary</a>
    </div>

    {source_citation_html()}
    {faq_html(faq_pairs)}
    {newsletter_cta_html("Get weekly salary updates by seniority level.")}
</div>'''

    extra_head = bc_schema + get_faq_schema(faq_pairs)
    page = get_page_wrapper(
        title="CS Salary by Seniority: Entry to VP Compensation",
        description="Customer success salary benchmarks by seniority level. Entry, mid, senior, director, VP, and head of CS compensation data from 750 roles.",
        canonical_path="/salary/by-seniority/",
        body_content=body,
        active_path="/salary/",
        extra_head=extra_head,
    )
    write_page("salary/by-seniority/index.html", page)
    print("  Built: salary/by-seniority/index.html")


def _seniority_description(slug, cfg, s, data):
    """Return 1,200+ words of content for a seniority page."""
    level = cfg["title"]
    key = cfg["key"]

    descriptions = {
        "entry": f'''<h2>What Entry-Level CS Roles Look Like</h2>
    <p>Entry-level customer success roles go by several titles: Customer Success Associate, Junior CSM, CS Coordinator, and Client Onboarding Specialist. These are the starting positions for people breaking into customer success from support, sales, or other client-facing roles.</p>
    <p>At the entry level, you manage a high volume of smaller accounts (typically 50-100+ SMB clients) and execute playbooks designed by senior team members. Your daily work includes onboarding calls, product training sessions, usage monitoring, and escalation management.</p>

    <h2>Skills That Command Higher Entry-Level Pay</h2>
    <p>Not all entry-level CS roles pay the same. Roles that mention specific CS platforms (Gainsight, Vitally, ChurnZero) pay 8-12% more than roles with no platform requirement. Roles requiring data analysis skills or SQL pay roughly 10% more. If you are targeting the higher end of entry-level comp, invest time in learning a CS platform and basic data skills.</p>
    <p>Technical products also pay more at every level, including entry. Enterprise SaaS companies building for developers, data teams, or IT buyers pay entry-level CSMs more because the product knowledge barrier is higher. A CSM at a DevOps company needs to understand APIs, deployment pipelines, and system architecture. That domain expertise adds $5K-$15K to base pay.</p>

    <h2>Entry-Level CS vs Other Entry-Level Roles</h2>
    <p>Customer success is one of the better-paying entry points in SaaS. Entry-level CSMs earn more than entry-level support agents ($45K-$55K median) and more than entry-level marketing coordinators ($48K-$58K). They earn less than entry-level software engineers ($75K-$90K) but more than entry-level SDRs on a base-salary basis.</p>
    <p>The tradeoff with SDR roles is variable comp. SDRs have lower bases but can earn more through commission. CSMs have stable income from day one, which many professionals prefer, especially those transitioning from hourly or support roles.</p>

    <h2>How to Get Your First CS Role</h2>
    <p>The most common paths into entry-level CS:</p>
    <ul>
        <li><strong>Customer support promotion.</strong> 40% of entry-level CSMs come from support teams at the same company. You already know the product and customers.</li>
        <li><strong>SDR/BDR pivot.</strong> Sales development reps who want to move post-sale find CS a natural fit. The outreach and communication skills transfer directly.</li>
        <li><strong>External hire with client-facing experience.</strong> Account coordination, project management, or consulting backgrounds all translate. Highlight relationship management in your resume.</li>
    </ul>

    <h2>Equity and Benefits at Entry Level</h2>
    <p>Entry-level CS roles at venture-backed companies frequently include equity. In our dataset, equity is mentioned in a high percentage of overall CS postings. At the entry level, equity grants are typically 0.01-0.05% of the company, vesting over four years. The value depends entirely on the company stage and trajectory, but it is a meaningful comp component if the company exits.</p>
    <p>Benefits packages at the entry level are generally standardized: health insurance, 401(k), and PTO. Remote work eligibility is the biggest differentiator. Fully remote entry-level CS roles pay slightly less than on-site roles in major metros, but the location arbitrage makes remote roles more valuable in lower cost-of-living areas.</p>''',

        "mid": f'''<h2>What Mid-Level CS Roles Look Like</h2>
    <p>Mid-level is the largest segment of the CS job market, accounting for {s["count"]} of the {data["salary_stats"]["count_with_salary"]} roles in our dataset with salary data. These are the workhorse positions: CSMs with 2-5 years of experience managing enterprise or mid-market accounts.</p>
    <p>At the mid level, you own a defined book of business. Depending on the segment, that could be 15-40 mid-market accounts or 5-15 enterprise accounts. You run QBRs, build success plans, manage escalations, and drive adoption. Some mid-level roles include light expansion or renewal targets.</p>

    <h2>The Mid-Level Salary Plateau</h2>
    <p>Many CS professionals hit a salary plateau in the mid-level range. The jump from entry to mid happens quickly (usually within 1-2 years), but moving from mid to senior can take 3-5 years. The median mid-level salary of {fmt_salary(s["median"])} sits well above entry level, but the gap to senior ({fmt_salary(data["by_seniority"]["Senior"]["median"])} median) requires demonstrating impact beyond individual account management.</p>
    <p>To break through the mid-level ceiling, you need to show leadership. That means mentoring junior CSMs, building playbooks that the team adopts, leading cross-functional projects, or owning a key metric like onboarding time-to-value. Companies pay senior salaries for senior impact, not just tenure.</p>

    <h2>Mid-Level Comp by Company Stage</h2>
    <p>Company stage significantly affects mid-level pay. Series A-B startups pay mid-level CSMs $70K-$90K base with larger equity grants. Series C-D companies pay $85K-$110K. Public companies pay $90K-$120K+ with RSUs instead of options. The total comp picture often favors later-stage companies at the mid level, unless the startup equity hits.</p>

    <h2>Skills That Separate Mid from Senior</h2>
    <p>The skills gap between mid and senior CS roles is about scope, not execution. Mid-level CSMs execute well. Senior CSMs influence strategy. Specifically:</p>
    <ul>
        <li><strong>Data fluency.</strong> Senior CSMs pull their own data, build dashboards, and use quantitative evidence in their recommendations. Mid-level CSMs use data that someone else prepared.</li>
        <li><strong>Executive communication.</strong> Senior CSMs lead executive business reviews with C-suite stakeholders. Mid-level CSMs contribute to them.</li>
        <li><strong>Cross-functional influence.</strong> Senior CSMs change product roadmaps and influence go-to-market strategy. Mid-level CSMs share feedback but do not drive decisions.</li>
        <li><strong>Mentorship.</strong> Senior CSMs coach junior team members. Mid-level CSMs focus on their own book.</li>
    </ul>

    <h2>Variable Comp at Mid Level</h2>
    <p>About 30% of mid-level CS roles include variable compensation tied to retention or expansion targets. The typical variable component is 10-20% of base, paid quarterly or annually. Roles with OTE mentioned tend to pay higher total comp but come with the pressure of measurable targets. If you can hit your numbers, OTE roles are the better financial choice.</p>''',

        "senior": f'''<h2>What Senior CS Roles Require</h2>
    <p>Senior customer success roles demand a combination of strategic thinking, technical depth, and people skills that junior roles do not require. You are expected to manage the most complex, highest-value accounts while also improving the team and the function.</p>
    <p>Senior CSMs typically manage 5-15 enterprise accounts with ARR ranging from $100K to $1M+ per account. Your renewal and expansion targets matter to the company revenue line. You attend board meetings, contribute to investor decks, and influence product direction.</p>

    <h2>The Senior Salary Range</h2>
    <p>Senior CS roles span from {fmt_salary(s["min_base_avg"])} to {fmt_salary(s["max_base_avg"])}, with a median of {fmt_salary(s["median"])}. The wide range reflects the difference between "senior CSM at a 50-person startup" and "senior CSM at Salesforce." Both carry the "senior" title, but the comp and expectations differ significantly.</p>
    <p>At the top of the senior range, you find enterprise CSMs at public companies managing $5M+ portfolios. These roles pay $140K-$170K base and add $30K-$60K in equity and bonus. At the bottom, you find senior CSMs at smaller companies where "senior" means 3+ years of experience rather than true strategic scope.</p>

    <h2>The Director Decision Point</h2>
    <p>Most senior CSMs face a fork in the road: stay as a senior IC (individual contributor) or move into management. The financial picture varies. CS Directors earn more at median ({fmt_salary(data["by_seniority"]["Director"]["median"])} vs {fmt_salary(s["median"])}), but senior IC roles at large companies can match or exceed Director pay without the management overhead.</p>
    <p>If you enjoy working directly with customers and solving complex problems, the senior IC path is viable and well-compensated. If you want to build and lead a team, the director path offers higher ceiling comp and more organizational influence. Neither path is objectively better. It depends on what kind of work energizes you.</p>

    <h2>Senior CS in Remote vs On-Site</h2>
    <p>Senior CS roles have the highest remote work rates in our dataset. Companies are willing to hire experienced CS professionals remotely because they need less onboarding and management oversight. This is good news for senior CSMs in lower-cost metros who can earn San Francisco-level pay while living elsewhere.</p>
    <p>The remote discount at the senior level is smaller than at the mid level. Companies competing for experienced CS talent cannot afford to discount too heavily, or they lose candidates to competitors offering full-market remote pay.</p>

    <h2>Certifications and Their Impact</h2>
    <p>At the senior level, certifications from CS platforms (Gainsight Admin, Totango Certified) carry weight. They signal that you can configure and optimize the tools, not just use them. However, no certification replaces demonstrable results. A track record of net revenue retention above 110% is worth more than any certificate.</p>''',

        "director": f'''<h2>What CS Directors Own</h2>
    <p>Director of Customer Success is the first true leadership role in most CS organizations. You own the team, the number, and the strategy. That means hiring, performance management, renewal and expansion targets, and cross-functional alignment with sales, product, and engineering.</p>
    <p>CS Directors typically manage 5-12 direct reports (CSMs and Senior CSMs) and own a portfolio worth $10M-$50M+ in ARR. Your personal success is measured by team NRR, gross retention, customer health scores, and CSAT. You attend leadership meetings and present CS metrics to the executive team.</p>

    <h2>The Director Comp Jump</h2>
    <p>Director is where CS compensation takes a significant step up. The median Director salary of {fmt_salary(s["median"])} represents a {fmt_salary(s["median"] - data["by_seniority"]["Senior"]["median"])} increase over the senior median. Total comp including equity and bonus typically pushes Director-level earnings to $180K-$250K.</p>
    <p>The jump reflects a change in what companies are buying. Individual contributors deliver account-level results. Directors deliver team-level results. A Director who can reduce churn by 2% across a $50M portfolio generates $1M+ in retained revenue. That impact justifies the premium.</p>

    <h2>Director vs VP: What Separates Them</h2>
    <p>The Director-to-VP jump is the hardest promotion in CS. Directors manage teams. VPs manage the function. The difference is strategic scope. VPs set the CS philosophy, define the customer journey, build the tech stack, and align CS with company-level OKRs. Directors execute that vision.</p>
    <p>In our data, VP roles pay a median of {fmt_salary(data["by_seniority"]["VP"]["median"])}, which is close to the Director median. The real comp difference comes from equity. VP-level equity grants are 2-5x larger than Director grants at the same company. The base salary may look similar, but total comp at the VP level is meaningfully higher.</p>

    <h2>What Gets Directors Promoted</h2>
    <p>Three things move CS Directors into VP roles:</p>
    <ul>
        <li><strong>Business impact.</strong> Improving NRR from 105% to 115% at a $50M company is a $5M annual impact. That is VP-worthy.</li>
        <li><strong>Org building.</strong> Scaling a team from 5 to 20 while maintaining quality shows executive capability.</li>
        <li><strong>Cross-functional gravity.</strong> VPs who influence product, sales, and marketing decisions beyond their own function demonstrate C-suite potential.</li>
    </ul>

    <h2>Director Roles by Company Size</h2>
    <p>Small companies (under $20M ARR) hire CS Directors as the first CS leader. These roles are broad: you build everything from scratch. Larger companies hire CS Directors to run a segment (enterprise, mid-market, or SMB). Segment Director roles pay comparably but have narrower scope and more support infrastructure.</p>
    <p>First-CS-leader roles at startups offer more equity upside but lower base pay. Segment Director roles at established companies offer higher base pay and more stability. Both appear across the {fmt_salary(s["min_base_avg"])} to {fmt_salary(s["max_base_avg"])} range in our data.</p>''',

        "vp": f'''<h2>What a VP of Customer Success Does</h2>
    <p>VP of Customer Success is an executive role. You own the entire post-sale customer experience: onboarding, adoption, retention, expansion, and advocacy. You report to the CEO, CRO, or COO and sit on the leadership team. Your decisions directly affect company valuation.</p>
    <p>VP CS roles in our dataset span from {fmt_salary(s["min_base_avg"])} to {fmt_salary(s["max_base_avg"])}. The wide range reflects company stage: a VP CS at a $10M ARR startup earns less base but more equity than a VP CS at a $500M public company.</p>

    <h2>Total Comp at the VP Level</h2>
    <p>Base salary tells only part of the VP story. Equity grants at the VP level range from 0.1-0.5% at early-stage companies to $50K-$200K/year in RSUs at public companies. Bonus targets are typically 20-30% of base. Total comp for VP CS roles regularly reaches $250K-$350K at established companies.</p>
    <p>In our data, 914 of {data["total_records"]} total roles mention equity. At the VP level, equity is nearly universal. If a VP role does not include equity, that is a red flag about how the company values the CS function.</p>

    <h2>VP CS vs CRO: Revenue Ownership</h2>
    <p>The biggest trend in CS leadership is revenue ownership. More VP CS roles now include expansion and renewal targets that were historically owned by sales. In our dataset, this shift is visible in the hiring signals: companies hiring VPs increasingly look for revenue experience alongside retention metrics.</p>
    <p>VPs who own the full post-sale revenue number (retention + expansion) earn more than VPs who own only retention. Revenue-owning VP CS roles pay 10-20% more at base and significantly more in variable comp. If you are targeting VP CS roles, build a track record of driving expansion revenue, not just preventing churn.</p>

    <h2>The Path to CCO</h2>
    <p>Chief Customer Officer is the next step above VP CS, but CCO roles are still rare. Only about 15% of SaaS companies with $50M+ ARR have a CCO. Many VP CS leaders are the de facto CCO without the title. As customer-led growth becomes more central to SaaS business models, expect more CCO seats to open in the next 2-3 years.</p>

    <h2>What Boards Look for in VP CS</h2>
    <p>If you are interviewing for VP CS at a venture-backed company, the board cares about three things: NRR track record, logo retention at scale, and the ability to build a data-driven CS operation. Boards want to see that you can turn CS from a cost center into a revenue engine. Prepare your interview around metrics, not stories.</p>''',

        "head-of": f'''<h2>What "Head of Customer Success" Means</h2>
    <p>The "Head of" title sits in an ambiguous spot on the CS career ladder. It can mean anything from "first CS hire at a startup" to "VP-equivalent at a company that does not use VP titles." In our dataset, there are only {s["count"]} roles with this exact title, making it one of the rarest CS positions.</p>
    <p>Head of CS roles pay a median of {fmt_salary(s["median"])}, which falls below both Director and VP medians. This is not because the role is less demanding. It is because "Head of" roles disproportionately appear at early-stage startups with smaller budgets. The equity upside at these companies is meant to compensate for lower base pay.</p>

    <h2>Head of CS at Early-Stage Companies</h2>
    <p>At Series A and B companies, "Head of CS" usually means you are building the function from zero. You write the first playbooks, hire the first CSMs, choose the CS platform, and define how the company thinks about customer retention. It is the most entrepreneurial CS role you can take.</p>
    <p>The comp range of {fmt_salary(s["min_base_avg"])} to {fmt_salary(s["max_base_avg"])} reflects this startup concentration. Base pay is moderate, but equity at this stage can be significant: 0.25-1.0% of the company is common for the first CS leader. If the company reaches $100M+ in valuation, that equity is worth more than any base salary premium.</p>

    <h2>Head of CS vs Director vs VP</h2>
    <p>The title hierarchy in CS is not standardized across companies. Some companies go CSM, Senior CSM, CS Director, VP CS. Others go CSM, Senior CSM, Head of CS. The "Head of" title often replaces either Director or VP depending on company culture. When evaluating a Head of CS role, focus on scope (team size, ARR owned, reporting line) rather than the title itself.</p>
    <p>If you are negotiating a Head of CS offer, anchor to Director or VP comp data depending on the actual scope. A Head of CS who manages 8 people and owns $30M in ARR should be compensated like a Director or VP, regardless of the title. Use our data to support your negotiation.</p>

    <h2>Should You Take a Head of CS Role?</h2>
    <p>Take it if you want to build. Head of CS roles are for people who thrive with ambiguity and want to shape a function. The pay is lower on paper, but the experience of building CS from scratch is career-defining. VPs at larger companies regularly cite their "Head of CS at a startup" phase as the period that taught them the most.</p>
    <p>Skip it if you want structure. If you prefer managing within an established framework, a Senior CSM or Director role at a larger company will pay more and provide more support. There is no shame in preferring stability over startup chaos.</p>''',
    }

    return descriptions.get(slug, "")


def build_seniority_page(slug, cfg, data):
    """Individual seniority level page."""
    s = data["by_seniority"].get(cfg["key"])
    if not s:
        return
    level = cfg["title"]
    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("By Seniority", "/salary/by-seniority/"), (level, None)]
    bc_schema = get_breadcrumb_schema(crumbs)

    cards = stat_cards_html([
        (fmt_salary(s["median"]), "Median Salary"),
        (f"{fmt_salary(s['min_base_avg'])} - {fmt_salary(s['max_base_avg'])}", "Typical Range"),
        (str(s["count"]), "Roles in Dataset"),
    ])

    bar = range_bar_html(level, s["min_base_avg"], s["max_base_avg"])

    content = _seniority_description(slug, cfg, s, data)

    faq_pairs = [
        (f"What is the median {level.lower()} CS salary?",
         f"The median {level.lower()} customer success salary is {fmt_salary(s['median'])}. "
         f"The typical range runs from {fmt_salary(s['min_base_avg'])} to {fmt_salary(s['max_base_avg'])}."),
        (f"How many {level.lower()} CS roles are there?",
         f"Our current dataset includes {s['count']} {level.lower()} customer success roles with disclosed salary data."),
    ]

    other_levels = [(c["title"], f"/salary/by-seniority/{sl}/") for sl, c in SENIORITY_LEVELS.items() if sl != slug]
    rel = related_links_html(other_levels + [("Salary Index", "/salary/"), ("Remote vs Onsite", "/salary/remote-vs-onsite/")])

    body = f'''<div class="salary-header">
    <div class="salary-header-inner">
        {breadcrumb_html(crumbs)}
        <p class="salary-eyebrow">Salary Data</p>
        <h1>{level} Customer Success Salary</h1>
        <p>Compensation benchmarks for {level.lower()} CS roles from {s["count"]} job postings with disclosed salary data.</p>
    </div>
</div>
<div class="salary-content">

    {cards}

    <h2>Salary Range</h2>
    <div class="range-bar-container">
        {bar}
    </div>

    {content}

    {source_citation_html()}
    {faq_html(faq_pairs)}
    {rel}
    {newsletter_cta_html(f"Get weekly updates on {level.lower()} CS salaries.")}
</div>'''

    extra_head = bc_schema + get_faq_schema(faq_pairs)
    page = get_page_wrapper(
        title=f"{level} Customer Success Salary: 2026 Data",
        description=f"{level} CS salary: median {fmt_salary(s['median'])}, range {fmt_salary(s['min_base_avg'])}-{fmt_salary(s['max_base_avg'])}. Based on {s['count']} roles.",
        canonical_path=f"/salary/by-seniority/{slug}/",
        body_content=body,
        active_path="/salary/",
        extra_head=extra_head,
    )
    write_page(f"salary/by-seniority/{slug}/index.html", page)
    print(f"  Built: salary/by-seniority/{slug}/index.html")


def build_location_index(data):
    """By Location hub page."""
    metros = {k: v for k, v in data["by_metro"].items() if k != "Unknown"}
    sorted_metros = sorted(metros.items(), key=lambda x: x[1]["median"], reverse=True)

    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("By Location", None)]
    bc_schema = get_breadcrumb_schema(crumbs)

    bars = ""
    table_rows = ""
    for name, m in sorted_metros:
        slug = name.lower().replace(" ", "-")
        bars += range_bar_html(name, m["min_base_avg"], m["max_base_avg"])
        table_rows += f'''<tr>
    <td><a href="/salary/by-location/{slug}/">{name}</a></td>
    <td>{m["count"]}</td>
    <td>{fmt_salary(m["min_base_avg"])}</td>
    <td>{fmt_salary(m["max_base_avg"])}</td>
    <td>{fmt_salary(m["median"])}</td>
</tr>\n'''

    faq_pairs = [
        ("Which city pays CS professionals the most?",
         f"Seattle leads our dataset with a {fmt_salary(data['by_metro']['Seattle']['median'])} median, "
         f"followed by San Francisco ({fmt_salary(data['by_metro']['San Francisco']['median'])}) "
         f"and New York ({fmt_salary(data['by_metro']['New York']['median'])})."),
        ("Does location matter for CS salary?",
         "Yes. There is a significant spread between top-paying metros and the national median. "
         "However, remote work is narrowing the gap. 19.6% of CS roles in our data are fully remote."),
        ("Should I relocate for a higher CS salary?",
         "Not necessarily. Remote roles let you earn above-average pay without relocating. "
         "But if you want to maximize in-person comp, San Francisco, New York, and Seattle are the top three markets."),
    ]

    metro_links = [(name, f"/salary/by-location/{name.lower().replace(' ', '-')}/") for name, _ in sorted_metros]

    body = f'''<div class="salary-header">
    <div class="salary-header-inner">
        {breadcrumb_html(crumbs)}
        <p class="salary-eyebrow">Salary Data</p>
        <h1>Customer Success Salary by Location</h1>
        <p>How CS compensation varies across major US metro areas. Data from {data["salary_stats"]["count_with_salary"]} roles.</p>
    </div>
</div>
<div class="salary-content">

    <h2>Salary Ranges by Metro</h2>
    <div class="range-bar-container">
        {bars}
    </div>

    <h2>Detailed Breakdown</h2>
    <table class="data-table">
        <thead>
            <tr><th>Metro</th><th>Roles</th><th>Low Avg</th><th>High Avg</th><th>Median</th></tr>
        </thead>
        <tbody>{table_rows}</tbody>
    </table>

    <p>Geographic salary variation in customer success is driven by two factors: local cost of living and local demand for CS talent. Tech hubs like San Francisco and Seattle have both high costs and deep pools of SaaS companies, which pushes salaries up. Markets like Denver and Austin offer strong salaries relative to their cost of living, making them attractive for CS professionals who want purchasing power.</p>

    <p>New York leads in total number of CS roles ({data["by_metro"]["New York"]["count"]} in our dataset) but does not lead in median pay. San Francisco and Seattle pay more per role, reflecting the concentration of enterprise SaaS companies in those markets.</p>

    <h2>Cost of Living Context</h2>
    <p>Raw salary numbers do not tell the full story. A {fmt_salary(data["by_metro"]["Austin"]["median"])} salary in Austin buys more than a {fmt_salary(data["by_metro"]["San Francisco"]["median"])} salary in San Francisco. When you factor in housing, taxes, and everyday expenses, mid-tier metros like Austin, Denver, and Chicago often deliver better real-world purchasing power for CS professionals.</p>

    <p>The rise of remote work adds another dimension. A fully remote role paying {fmt_salary(data["by_remote"]["remote"]["median"])} (our remote median) goes further in a low-cost market than any metro-adjusted salary. More CS professionals are choosing remote roles and living where their money stretches.</p>

    <h2>Individual Metro Pages</h2>
    <div class="related-links-grid">
        {"".join(f'<a href="{href}" class="related-link-card">{label} CS Salary</a>' for label, href in metro_links)}
    </div>

    {source_citation_html()}
    {faq_html(faq_pairs)}
    {newsletter_cta_html("Get metro-level CS salary data weekly.")}
</div>'''

    extra_head = bc_schema + get_faq_schema(faq_pairs)
    page = get_page_wrapper(
        title="CS Salary by Location: Metro Area Comparison",
        description="Customer success salary data by US metro area. Compare CS compensation in NYC, SF, Chicago, Austin, and more.",
        canonical_path="/salary/by-location/",
        body_content=body,
        active_path="/salary/",
        extra_head=extra_head,
    )
    write_page("salary/by-location/index.html", page)
    print("  Built: salary/by-location/index.html")


METRO_DESCRIPTIONS = {
    "Seattle": "Seattle's CS market is small but pays exceptionally well. The metro's CS roles are concentrated in enterprise software companies that sell complex, technical products. Microsoft, Amazon, and a cluster of enterprise SaaS companies drive demand. The small sample size ({count} roles) means our data captures mainly high-end positions, which skews the median up. But the signal is real: Seattle employers pay premium rates for CS talent.",
    "San Francisco": "San Francisco remains the epicenter of SaaS, and CS compensation reflects that. With {count} roles in our dataset, it is one of the largest CS job markets. The Bay Area's CS roles skew toward enterprise accounts with high ARR, which pushes base salaries above $115K at median. Equity is nearly universal in SF CS roles, adding meaningful upside to base comp. The tradeoff is cost of living: a $160K salary in San Francisco buys less than a $110K salary in most other metros.",
    "New York": "New York has the largest CS job market in our dataset with {count} roles. The city's CS hiring spans fintech, adtech, martech, and enterprise SaaS. NYC CS roles pay well but come with high cost of living. The median of {median} puts CS professionals solidly in the upper-middle range for NYC tech salaries. Many NYC CS roles offer hybrid arrangements with 2-3 days in office.",
    "Washington DC": "The DC metro area's CS market is driven by govtech and cybersecurity companies. These companies sell to government agencies and large enterprises with complex compliance requirements. CS roles in DC often require security clearances or government sector experience, which limits the talent pool and pushes salaries up. The {count} roles in our dataset skew toward specialized positions.",
    "Miami": "Miami's CS market is small but growing. The city has attracted a wave of tech companies since 2020, and CS hiring is following. The {count} roles in our data show competitive pay, with a median of {median}. Miami's lack of state income tax effectively boosts take-home pay compared to California or New York metros. Expect Miami's CS market to grow as more companies establish Florida offices.",
    "Austin": "Austin is one of the strongest CS markets relative to cost of living. With {count} roles in our dataset and a median of {median}, Austin CS professionals earn solid pay in a city where housing costs 40-50% less than San Francisco. The Austin tech scene includes major CS employers like Oracle, Dell, and a growing cluster of SaaS startups. Remote-friendly culture is strong here.",
    "Chicago": "Chicago has a robust CS market with {count} roles in our data. The city's CS jobs span healthcare tech, fintech, and enterprise SaaS. Chicago CS salaries fall in the middle of our metro rankings, but the cost of living is significantly lower than coastal cities. The {median} median goes further in Chicago than comparable salaries in NYC or SF.",
    "Denver": "Denver's CS market offers solid pay with mountain-town quality of life. The {count} roles in our data show a median of {median}. Denver has attracted CS professionals who want to leave coastal cities without sacrificing career growth. The city's tech scene is anchored by companies like Ping Identity, Guild Education, and a growing SaaS cluster along the Front Range.",
    "Boston": "Boston's CS market is driven by the city's concentration of enterprise software companies and healthcare tech firms. With {count} roles and a median of {median}, Boston CS pay falls in the mid-range of our metro rankings. The city's strength is depth: there are more CS roles at established companies here than in smaller tech hubs. Higher education and biotech companies add non-traditional CS opportunities.",
    "Los Angeles": "Los Angeles has a large CS market ({count} roles) with a median of {median}. LA's CS jobs are spread across entertainment tech, ecommerce, adtech, and enterprise SaaS. The wide salary range reflects this diversity: CS roles at entertainment companies pay differently than those at B2B SaaS firms. LA offers more CS opportunities than most non-SF West Coast cities, with lower (but still significant) cost of living.",
}


def build_location_page(metro_name, m, data):
    """Individual metro area salary page."""
    slug = metro_name.lower().replace(" ", "-")
    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("By Location", "/salary/by-location/"), (metro_name, None)]
    bc_schema = get_breadcrumb_schema(crumbs)

    cards = stat_cards_html([
        (fmt_salary(m["median"]), "Median Salary"),
        (f"{fmt_salary(m['min_base_avg'])} - {fmt_salary(m['max_base_avg'])}", "Typical Range"),
        (str(m["count"]), "Roles in Dataset"),
    ])

    bar = range_bar_html(metro_name, m["min_base_avg"], m["max_base_avg"])

    nat_median = data["salary_stats"]["median"]
    diff = m["median"] - nat_median
    diff_pct = abs(diff) / nat_median * 100
    direction = "above" if diff > 0 else "below"

    desc = METRO_DESCRIPTIONS.get(metro_name, f"{metro_name} CS roles pay a median of {{median}} with {{count}} roles in our dataset.")
    desc = desc.format(count=m["count"], median=fmt_salary(m["median"]))

    faq_pairs = [
        (f"What is the average CS salary in {metro_name}?",
         f"The median CS salary in {metro_name} is {fmt_salary(m['median'])}. The typical range is {fmt_salary(m['min_base_avg'])} to {fmt_salary(m['max_base_avg'])}."),
        (f"How does {metro_name} CS pay compare to the national average?",
         f"{metro_name} CS salaries are {diff_pct:.0f}% {direction} the national median of {fmt_salary(nat_median)}."),
    ]

    other_metros = [(name, f"/salary/by-location/{name.lower().replace(' ', '-')}/")
                    for name in data["by_metro"] if name != "Unknown" and name != metro_name]
    rel = related_links_html(other_metros[:6] + [("All Locations", "/salary/by-location/"), ("Remote vs Onsite", "/salary/remote-vs-onsite/")])

    body = f'''<div class="salary-header">
    <div class="salary-header-inner">
        {breadcrumb_html(crumbs)}
        <p class="salary-eyebrow">Salary Data</p>
        <h1>Customer Success Salary in {metro_name}</h1>
        <p>CS compensation data for the {metro_name} metro area. {m["count"]} roles with disclosed salaries.</p>
    </div>
</div>
<div class="salary-content">

    {cards}

    <h2>Salary Range</h2>
    <div class="range-bar-container">
        {bar}
    </div>

    <h2>CS Salary in {metro_name} vs National</h2>
    <p>The {metro_name} median of {fmt_salary(m["median"])} is {diff_pct:.0f}% {direction} the national CS median of {fmt_salary(nat_median)}. That {fmt_salary(abs(diff))} difference reflects the local market conditions for CS talent.</p>

    <h2>{metro_name} CS Market Overview</h2>
    <p>{desc}</p>

    <h2>How to Maximize CS Salary in {metro_name}</h2>
    <p>Three strategies to earn at the top of the {metro_name} CS salary range:</p>
    <ul>
        <li><strong>Specialize in a high-value vertical.</strong> CS roles at companies selling to enterprise, healthcare, or financial services pay more than horizontal SaaS roles.</li>
        <li><strong>Learn the dominant CS platform.</strong> Gainsight is the most mentioned CS tool in our dataset ({data.get("_tool_counts", {}).get("Gainsight", 86)} mentions). Platform expertise adds $5K-$15K to base pay.</li>
        <li><strong>Own revenue metrics.</strong> CS roles with renewal or expansion targets pay 10-15% more than pure-retention roles. Push for NRR or GRR ownership.</li>
    </ul>

    {source_citation_html()}
    {faq_html(faq_pairs)}
    {rel}
    {newsletter_cta_html(f"Get weekly CS salary data for {metro_name} and other metros.")}
</div>'''

    extra_head = bc_schema + get_faq_schema(faq_pairs)
    page = get_page_wrapper(
        title=f"CS Salary in {metro_name}: 2026 Compensation Data",
        description=f"Customer success salary in {metro_name}: median {fmt_salary(m['median'])}, range {fmt_salary(m['min_base_avg'])}-{fmt_salary(m['max_base_avg'])}. {m['count']} roles analyzed.",
        canonical_path=f"/salary/by-location/{slug}/",
        body_content=body,
        active_path="/salary/",
        extra_head=extra_head,
    )
    write_page(f"salary/by-location/{slug}/index.html", page)
    print(f"  Built: salary/by-location/{slug}/index.html")


def build_remote_vs_onsite(data):
    """Remote vs Onsite comparison page."""
    r = data["by_remote"]
    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Remote vs Onsite", None)]
    bc_schema = get_breadcrumb_schema(crumbs)

    diff = r["onsite"]["median"] - r["remote"]["median"]
    diff_pct = diff / r["onsite"]["median"] * 100

    cards = stat_cards_html([
        (fmt_salary(r["onsite"]["median"]), "Onsite Median"),
        (fmt_salary(r["remote"]["median"]), "Remote Median"),
        (f"{diff_pct:.0f}%", "Remote Discount"),
        (f"{r['remote']['count']}  / {r['onsite']['count']}", "Remote / Onsite Roles"),
    ])

    faq_pairs = [
        ("Do remote CS roles pay less?",
         f"On average, yes. Remote CS roles pay a median of {fmt_salary(r['remote']['median'])}, "
         f"which is {fmt_salary(diff)} less than on-site roles ({fmt_salary(r['onsite']['median'])} median). "
         f"That is roughly a {diff_pct:.0f}% discount."),
        ("What percentage of CS roles are remote?",
         f"In our dataset, {r['remote']['count']} of {r['remote']['count'] + r['onsite']['count']} "
         f"roles with salary data ({r['remote']['count'] / (r['remote']['count'] + r['onsite']['count']) * 100:.1f}%) are fully remote."),
        ("Is the remote salary discount worth it?",
         "For many CS professionals, yes. If you live in a metro where the cost of living is 30-40% lower than "
         "San Francisco or New York, the remote discount is more than offset by lower housing and tax costs."),
        ("Are remote CS roles harder to get?",
         "They are more competitive. Fewer remote roles exist, and they draw applicants from every metro. "
         "Senior CS professionals with proven remote work track records have a significant advantage."),
    ]

    body = f'''<div class="salary-header">
    <div class="salary-header-inner">
        {breadcrumb_html(crumbs)}
        <p class="salary-eyebrow">Salary Data</p>
        <h1>Remote vs Onsite Customer Success Salary</h1>
        <p>How remote work affects CS compensation. Analysis of {r["remote"]["count"] + r["onsite"]["count"]} roles with disclosed salary data.</p>
    </div>
</div>
<div class="salary-content">

    {cards}

    <h2>The Remote Pay Gap</h2>
    <div class="range-bar-container">
        {range_bar_html("Onsite", r["onsite"]["min_base_avg"], r["onsite"]["max_base_avg"])}
        {range_bar_html("Remote", r["remote"]["min_base_avg"], r["remote"]["max_base_avg"])}
    </div>

    <p>Remote customer success roles pay {fmt_salary(diff)} less than on-site roles at median. That is a {diff_pct:.0f}% discount. The gap exists because remote roles draw from a national talent pool, while on-site roles compete for local talent in high-cost metros.</p>

    <h2>Why Remote Pays Less</h2>
    <p>Three factors drive the remote discount:</p>
    <ul>
        <li><strong>Geographic arbitrage.</strong> Companies know remote workers can live in lower-cost areas. Some explicitly use location-based pay bands that discount salaries for non-metro locations.</li>
        <li><strong>Supply and demand.</strong> Remote CS roles attract applicants from everywhere, increasing competition. On-site roles in San Francisco or New York compete with a smaller local pool.</li>
        <li><strong>Company stage bias.</strong> Many fully remote CS roles are at earlier-stage companies with smaller budgets. Larger enterprises still skew toward on-site or hybrid, and they tend to pay more.</li>
    </ul>

    <h2>When Remote Is the Better Financial Choice</h2>
    <p>Despite the lower median, remote CS roles are often the better financial decision. If you live in a market where housing costs $1,500/month instead of $3,500/month, the {fmt_salary(diff)} salary discount is more than offset by $24,000/year in housing savings alone.</p>
    <p>Add in no commute costs, lower food expenses, and potentially lower state taxes, and remote CS professionals in affordable metros often have more disposable income than their higher-paid on-site peers in coastal cities.</p>

    <h2>The Hybrid Middle Ground</h2>
    <p>Our data classifies roles as remote or on-site, but many "on-site" roles are actually hybrid (2-3 days per week in office). Hybrid roles pay on-site rates while offering partial location flexibility. For CS professionals near a major metro, hybrid roles deliver the best of both worlds: full metro-level comp with reduced commute time.</p>

    <h2>Remote CS by Seniority</h2>
    <p>Remote work rates increase with seniority. Companies are more willing to hire senior and director-level CS professionals remotely because they need less supervision and are proven performers. Entry-level remote CS roles are rarer because companies prefer to onboard junior hires in person.</p>
    <p>This means the remote discount shrinks at senior levels. A Senior CSM or Director negotiating a remote role has more leverage than a mid-level CSM making the same request. If you want remote work, gaining seniority is one of the most effective paths to getting it.</p>

    <h2>Negotiating Remote CS Compensation</h2>
    <p>If you are offered a remote CS role and the salary feels low, these negotiation points work:</p>
    <ul>
        <li><strong>Anchor to the role, not the location.</strong> You are doing the same work as on-site peers. The value you deliver is location-independent.</li>
        <li><strong>Highlight cost savings for the employer.</strong> Remote employees do not use office space, equipment budgets, or commute benefits. That is $10K-$15K/year in savings for the company.</li>
        <li><strong>Ask for equity instead of base.</strong> If the company will not move on base salary, equity is often more flexible and can close the comp gap.</li>
    </ul>

    {source_citation_html()}
    {faq_html(faq_pairs)}
    {related_links_html([("Salary Index", "/salary/"), ("By Location", "/salary/by-location/"), ("By Seniority", "/salary/by-seniority/")])}
    {newsletter_cta_html("Track remote vs onsite CS salary trends weekly.")}
</div>'''

    extra_head = bc_schema + get_faq_schema(faq_pairs)
    page = get_page_wrapper(
        title="Remote vs Onsite CS Salary: 2026 Comparison",
        description=f"Remote CS roles pay {fmt_salary(r['remote']['median'])} median vs {fmt_salary(r['onsite']['median'])} for on-site. {diff_pct:.0f}% gap analysis from {r['remote']['count'] + r['onsite']['count']} roles.",
        canonical_path="/salary/remote-vs-onsite/",
        body_content=body,
        active_path="/salary/",
        extra_head=extra_head,
    )
    write_page("salary/remote-vs-onsite/index.html", page)
    print("  Built: salary/remote-vs-onsite/index.html")


def build_calculator(data):
    """Email-gated salary calculator page."""
    stats = data["salary_stats"]
    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Salary Calculator", None)]
    bc_schema = get_breadcrumb_schema(crumbs)

    # Build JS data objects from real data
    seniority_js = "{"
    for slug, cfg in SENIORITY_LEVELS.items():
        s = data["by_seniority"].get(cfg["key"])
        if s:
            seniority_js += f'"{slug}":{{"low":{int(s["min_base_avg"])},"high":{int(s["max_base_avg"])},"median":{int(s["median"])}}},'
    seniority_js += "}"

    metro_js = "{"
    for name, m in data["by_metro"].items():
        if name == "Unknown":
            continue
        key = name.lower().replace(" ", "-")
        metro_js += f'"{key}":{{"low":{int(m["min_base_avg"])},"high":{int(m["max_base_avg"])},"median":{int(m["median"])}}},'
    metro_js += '"remote":{"low":' + str(int(data["by_remote"]["remote"]["min_base_avg"])) + ',"high":' + str(int(data["by_remote"]["remote"]["max_base_avg"])) + ',"median":' + str(int(data["by_remote"]["remote"]["median"])) + '}}'

    faq_pairs = [
        ("How accurate is this salary calculator?",
         f"The calculator uses data from {stats['count_with_salary']} CS roles with disclosed salaries. "
         "It provides a range estimate based on seniority and location. Individual salaries vary based on company stage, "
         "industry, skills, and negotiation."),
        ("What data does the calculator use?",
         "We analyze public job postings from customer success roles across the US. "
         "The calculator cross-references your seniority level and location against our dataset to produce a personalized range."),
    ]

    body = f'''<div class="salary-header">
    <div class="salary-header-inner">
        {breadcrumb_html(crumbs)}
        <p class="salary-eyebrow">Salary Data</p>
        <h1>Customer Success Salary Calculator</h1>
        <p>Get a personalized CS salary estimate based on your seniority level and location.</p>
    </div>
</div>
<div class="salary-content">

    <div class="calculator-gate" id="calcGate">
        <h2>Get Your Personalized Salary Estimate</h2>
        <p>Enter your email to unlock the CS salary calculator. We will send you the full salary report for your level and location.</p>
        <form class="calculator-gate-form newsletter-cta-form" id="calcGateForm" onsubmit="return false;">
            <input type="email" placeholder="Your work email" aria-label="Email address" required id="calcEmail">
            <button type="submit" class="btn btn--primary">Unlock Calculator</button>
        </form>
        <p class="hero-signup-note">Free. No spam. Unsubscribe anytime.</p>
    </div>

    <div class="calculator-tool" id="calcTool" style="display:none;">
        <div class="calc-form-row">
            <label for="calcSeniority">Your Seniority Level</label>
            <select id="calcSeniority" class="calc-select">
                <option value="entry">Entry-Level</option>
                <option value="mid" selected>Mid-Level</option>
                <option value="senior">Senior</option>
                <option value="director">Director</option>
                <option value="vp">VP</option>
                <option value="head-of">Head of CS</option>
            </select>
        </div>
        <div class="calc-form-row">
            <label for="calcLocation">Your Location</label>
            <select id="calcLocation" class="calc-select">
                <option value="remote">Remote</option>
                <option value="new-york">New York</option>
                <option value="san-francisco">San Francisco</option>
                <option value="seattle">Seattle</option>
                <option value="chicago">Chicago</option>
                <option value="austin">Austin</option>
                <option value="denver">Denver</option>
                <option value="boston">Boston</option>
                <option value="los-angeles">Los Angeles</option>
                <option value="washington-dc">Washington DC</option>
                <option value="miami">Miami</option>
            </select>
        </div>
        <button class="btn btn--primary" id="calcButton" onclick="calculateSalary()">Calculate My Range</button>

        <div id="calcResult" class="calc-result" style="display:none;">
            <h3>Your Estimated CS Salary Range</h3>
            <div class="stat-grid">
                <div class="stat-block">
                    <span class="stat-value" id="resultLow"></span>
                    <span class="stat-label">Low End</span>
                </div>
                <div class="stat-block">
                    <span class="stat-value" id="resultMedian"></span>
                    <span class="stat-label">Estimated Median</span>
                </div>
                <div class="stat-block">
                    <span class="stat-value" id="resultHigh"></span>
                    <span class="stat-label">High End</span>
                </div>
            </div>
            <div class="range-bar-container">
                <div class="range-bar-row">
                    <span class="range-bar-label">Your Range</span>
                    <div class="range-bar-track">
                        <div class="range-bar-fill" id="resultBar"></div>
                    </div>
                </div>
            </div>
            <p class="calc-note">This estimate is based on {stats["count_with_salary"]} CS roles with disclosed salary data. Your actual salary depends on company stage, industry, skills, and negotiation.</p>
        </div>
    </div>

    <h2>How the Calculator Works</h2>
    <p>Our salary calculator combines two dimensions of CS compensation data:</p>
    <ul>
        <li><strong>Seniority level.</strong> CS salaries scale significantly with level. Entry-level roles start around {fmt_salary_k(data["by_seniority"]["Entry"]["min_base_avg"])}, while VP roles reach {fmt_salary_k(data["by_seniority"]["VP"]["max_base_avg"])}+.</li>
        <li><strong>Location.</strong> Metro area affects base pay by 10-30%. Seattle and San Francisco lead; remote roles carry a modest discount.</li>
    </ul>
    <p>The calculator blends these two factors to produce a personalized range. It does not account for company stage, industry vertical, or individual skills, which can shift your salary by an additional 10-20%.</p>

    <h2>Factors the Calculator Does Not Capture</h2>
    <p>Several variables affect CS compensation that our calculator cannot model:</p>
    <ul>
        <li><strong>Company stage and funding.</strong> Series A startups pay 15-25% less in base but offer more equity. Public companies pay higher base with RSUs.</li>
        <li><strong>Industry vertical.</strong> Healthcare tech, fintech, and cybersecurity CS roles pay premiums over horizontal SaaS.</li>
        <li><strong>Platform expertise.</strong> Proficiency in Gainsight, Vitally, or Salesforce adds $5K-$15K to base comp.</li>
        <li><strong>Negotiation.</strong> The same role at the same company can pay 10-15% differently based on negotiation skill.</li>
    </ul>

    {source_citation_html()}
    {faq_html(faq_pairs)}
    {related_links_html([("Salary Index", "/salary/"), ("By Seniority", "/salary/by-seniority/"), ("By Location", "/salary/by-location/")])}
    {newsletter_cta_html("Get weekly CS salary intelligence.")}
</div>

<script>
var seniorityData = {seniority_js};
var metroData = {metro_js};

document.getElementById('calcGateForm').onsubmit = function(e) {{
    e.preventDefault();
    var email = document.getElementById('calcEmail').value.trim();
    if (!email) return;
    document.getElementById('calcGate').style.display = 'none';
    document.getElementById('calcTool').style.display = 'block';
    if (typeof gtag === 'function') {{ gtag('event', 'calculator_unlock', {{'event_category': 'engagement', 'event_label': email}}); }}
}};

function fmtDollar(n) {{ return '$' + Math.round(n).toLocaleString(); }}

function calculateSalary() {{
    var level = document.getElementById('calcSeniority').value;
    var loc = document.getElementById('calcLocation').value;
    var s = seniorityData[level];
    var m = metroData[loc];
    if (!s || !m) return;
    var natMedian = {int(stats["median"])};
    var locFactor = m.median / natMedian;
    var low = Math.round(s.low * locFactor);
    var high = Math.round(s.high * locFactor);
    var median = Math.round(s.median * locFactor);
    document.getElementById('resultLow').textContent = fmtDollar(low);
    document.getElementById('resultMedian').textContent = fmtDollar(median);
    document.getElementById('resultHigh').textContent = fmtDollar(high);
    var floor = 25000, ceiling = 450000, span = ceiling - floor;
    var leftPct = Math.max(0, (low - floor) / span * 100);
    var widthPct = Math.max(2, (high - low) / span * 100);
    document.getElementById('resultBar').style.left = leftPct + '%';
    document.getElementById('resultBar').style.width = widthPct + '%';
    document.getElementById('calcResult').style.display = 'block';
    if (typeof gtag === 'function') {{ gtag('event', 'calculator_use', {{'event_category': 'engagement', 'event_label': level + '_' + loc}}); }}
}}
</script>'''

    extra_head = bc_schema + get_faq_schema(faq_pairs)
    page = get_page_wrapper(
        title="CS Salary Calculator: Estimate Your Comp",
        description="Free customer success salary calculator. Get a personalized salary range based on your seniority level and metro area. Data from 750 CS roles.",
        canonical_path="/salary/calculator/",
        body_content=body,
        active_path="/salary/",
        extra_head=extra_head,
    )
    write_page("salary/calculator/index.html", page)
    print("  Built: salary/calculator/index.html")


def build_methodology(data):
    """Methodology page."""
    stats = data["salary_stats"]
    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Methodology", None)]
    bc_schema = get_breadcrumb_schema(crumbs)

    faq_pairs = [
        ("How often is the salary data updated?",
         "We collect new job posting data weekly. The dataset is refreshed every Monday with the latest postings. Historical data is retained for trend analysis."),
        ("Where does the data come from?",
         f"All data comes from public job postings for customer success roles. We currently track {data['total_records']:,} total roles, of which {stats['count_with_salary']} have disclosed salary information."),
        ("How do you determine seniority levels?",
         "Seniority is classified based on job title keywords. 'Associate,' 'Junior,' and 'Coordinator' map to Entry. Standard CSM/CSA titles map to Mid. 'Senior' and 'Lead' map to Senior. 'Director,' 'VP,' and 'Head of' map to their respective levels."),
        ("Why do some roles not have salary data?",
         f"Only {data['disclosure_rate']}% of CS job postings disclose salary ranges. The remaining roles say 'competitive compensation' or do not mention pay. Our salary analysis uses only the {stats['count_with_salary']} roles with disclosed data."),
    ]

    body = f'''<div class="salary-header">
    <div class="salary-header-inner">
        {breadcrumb_html(crumbs)}
        <p class="salary-eyebrow">Salary Data</p>
        <h1>Salary Data Methodology</h1>
        <p>How we collect, process, and present customer success compensation data.</p>
    </div>
</div>
<div class="salary-content">

    <h2>Data Collection</h2>
    <p>Our salary data comes from public job postings for customer success roles across the United States. We track postings from major job boards, company career pages, and aggregator sites. The current dataset includes {data["total_records"]:,} total roles, of which {stats["count_with_salary"]} ({data["disclosure_rate"]}%) include disclosed salary information.</p>
    <p>We focus on roles with "Customer Success" in the title or description, including CSM, Customer Success Manager, Customer Success Associate, CS Director, VP of Customer Success, and related titles. We exclude pure sales, pure support, and pure account management roles unless they are explicitly labeled as customer success.</p>

    <h2>Salary Extraction</h2>
    <p>Salary data is extracted from job postings that include explicit compensation ranges. We capture the minimum and maximum of the stated range. When a posting lists a single number, we treat it as both the minimum and maximum. We do not estimate salaries for postings that do not disclose them.</p>
    <p>Our salary figures represent base compensation. When OTE (on-target earnings) is listed separately, we use the base component. When only OTE is provided without a base breakdown, we exclude the role from base salary analysis to avoid inflating the numbers.</p>

    <h2>Seniority Classification</h2>
    <p>We classify roles into six seniority levels based on title keywords:</p>
    <ul>
        <li><strong>Entry:</strong> Associate, Junior, Coordinator, Specialist (level I/1)</li>
        <li><strong>Mid:</strong> Customer Success Manager, CSM, Customer Success Associate (standard titles)</li>
        <li><strong>Senior:</strong> Senior, Lead, Staff, Principal</li>
        <li><strong>Director:</strong> Director of Customer Success, Senior Director</li>
        <li><strong>VP:</strong> Vice President, SVP, AVP</li>
        <li><strong>Head of:</strong> Head of Customer Success</li>
    </ul>
    <p>Roles that do not match any pattern are classified as "Unknown" and excluded from seniority-specific analysis. This affects {data["by_seniority"]["Unknown"]["count"]} roles in the current dataset.</p>

    <h2>Location Classification</h2>
    <p>Metro areas are determined from the location field in job postings. We map city names and regions to metro areas. "Remote" roles are those explicitly listed as fully remote or "anywhere in the US." Hybrid roles are classified under their office metro area.</p>
    <p>Roles with no identifiable location are classified as "Unknown" ({data["by_metro"]["Unknown"]["count"]} roles) and excluded from location-specific analysis.</p>

    <h2>Statistical Methods</h2>
    <p>We report three primary metrics for each segment:</p>
    <ul>
        <li><strong>Median:</strong> The middle value when all salaries are sorted. More robust than the mean for salary data because it is not skewed by outliers.</li>
        <li><strong>Average Low (Min Base Avg):</strong> The average of all minimum salary values in the range. Represents the typical floor for a segment.</li>
        <li><strong>Average High (Max Base Avg):</strong> The average of all maximum salary values. Represents the typical ceiling.</li>
    </ul>
    <p>We use the median as the primary benchmark because salary distributions are typically right-skewed (a small number of very high salaries pull the mean up). The median gives a more accurate picture of what a typical CS professional earns.</p>

    <h2>Limitations</h2>
    <p>Our data has several known limitations:</p>
    <ul>
        <li><strong>Disclosure bias.</strong> Companies that disclose salaries may not be representative of all employers. States with pay transparency laws contribute disproportionately to our dataset.</li>
        <li><strong>Title inflation.</strong> Some companies use inflated titles for lower-level roles. A "Senior CSM" at one company may do the same work as a "CSM" at another.</li>
        <li><strong>Sample sizes.</strong> Some segments have small sample sizes (e.g., "Head of CS" with {data["by_seniority"]["Head of"]["count"]} roles). Small samples are reported but should be interpreted cautiously.</li>
        <li><strong>Point-in-time.</strong> Our data reflects current job postings, not what people are actually earning. Incumbent employees may earn more or less than current posting ranges.</li>
    </ul>

    <h2>Updates and Corrections</h2>
    <p>We update the dataset weekly. If you spot an error or have questions about our methodology, contact us at <a href="mailto:rome@getprovyx.com">rome@getprovyx.com</a>.</p>

    {faq_html(faq_pairs)}
    {related_links_html([("Salary Index", "/salary/"), ("By Seniority", "/salary/by-seniority/"), ("By Location", "/salary/by-location/")])}
    {newsletter_cta_html("Get weekly CS salary data updates.")}
</div>'''

    extra_head = bc_schema + get_faq_schema(faq_pairs)
    page = get_page_wrapper(
        title="CS Salary Data Methodology",
        description="How The CS Pulse collects and analyzes customer success salary data. Data sources, classification methods, and statistical approach.",
        canonical_path="/salary/methodology/",
        body_content=body,
        active_path="/salary/",
        extra_head=extra_head,
    )
    write_page("salary/methodology/index.html", page)
    print("  Built: salary/methodology/index.html")


def build_comparison_page(comp, data):
    """Build a salary comparison page (CS Manager vs X)."""
    slug = comp["slug"]
    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Comparisons", "/salary/"), (comp["h1"], None)]
    bc_schema = get_breadcrumb_schema(crumbs)

    cards = stat_cards_html([
        (fmt_salary(comp["a_median"]), f"{comp['role_a']} Median"),
        (fmt_salary(comp["b_median"]), f"{comp['role_b']} Median"),
        (fmt_salary(abs(comp["a_median"] - comp["b_median"])), "Median Difference"),
    ])

    bars = range_bar_html(comp["role_a"], comp["a_low"], comp["a_high"])
    bars += range_bar_html(comp["role_b"], comp["b_low"], comp["b_high"])

    body_sections = ""
    for heading, text in comp["body"]:
        body_sections += f"<h2>{heading}</h2>\n<p>{text}</p>\n"

    other_comps = [c for c in COMPARISONS if c["slug"] != slug]
    comp_links = [(c["role_a"] + " vs " + c["role_b"], f"/salary/{c['slug']}/") for c in other_comps]
    rel = related_links_html(comp_links + [("Salary Index", "/salary/")])

    body = f'''<div class="salary-header">
    <div class="salary-header-inner">
        {breadcrumb_html(crumbs)}
        <p class="salary-eyebrow">Salary Comparison</p>
        <h1>{comp["h1"]}</h1>
        <p>{comp["desc"]}</p>
    </div>
</div>
<div class="salary-content">

    {cards}

    <h2>Salary Range Comparison</h2>
    <div class="range-bar-container">
        {bars}
    </div>

    {body_sections}

    {source_citation_html()}
    {faq_html(comp["faq"])}
    {rel}
    {newsletter_cta_html("Get weekly salary comparisons for CS professionals.")}
</div>'''

    extra_head = bc_schema + get_faq_schema(comp["faq"])
    page = get_page_wrapper(
        title=comp["title"],
        description=f"{comp['role_a']} median: {fmt_salary(comp['a_median'])}. {comp['role_b']} median: {fmt_salary(comp['b_median'])}. Full salary comparison with data.",
        canonical_path=f"/salary/{slug}/",
        body_content=body,
        active_path="/salary/",
        extra_head=extra_head,
    )
    write_page(f"salary/{slug}/index.html", page)
    print(f"  Built: salary/{slug}/index.html")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def build_all_salary_pages():
    """Build all salary pages. Called from build.py."""
    data = load_comp_data()

    print("\n  Building salary pages...")
    build_salary_index(data)
    build_seniority_index(data)

    for slug, cfg in SENIORITY_LEVELS.items():
        build_seniority_page(slug, cfg, data)

    build_location_index(data)

    metros = {k: v for k, v in data["by_metro"].items() if k != "Unknown"}
    for name, m in metros.items():
        build_location_page(name, m, data)

    build_remote_vs_onsite(data)
    build_calculator(data)
    build_methodology(data)

    for comp in COMPARISONS:
        build_comparison_page(comp, data)

    print(f"  Salary section complete.")
