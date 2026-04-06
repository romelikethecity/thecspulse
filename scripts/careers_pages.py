# scripts/careers_pages.py
# Career guides section: index + individual guide pages.

import os
import json

from nav_config import *
from templates import (get_page_wrapper, write_page, get_breadcrumb_schema,
                       get_faq_schema, breadcrumb_html, newsletter_cta_html,
                       faq_html)


# ---------------------------------------------------------------------------
# Careers Index Page
# ---------------------------------------------------------------------------

def build_careers_index():
    """Generate the /careers/ index page."""
    title = "Customer Success Career Guides"
    description = (
        "Career guides for customer success professionals. How to break into CS leadership,"
        " job market growth data, salary negotiation, and skill maps for CSMs through VP CS."
    )

    crumbs = [("Home", "/"), ("Career Guides", None)]
    body = f'''<div class="salary-content">
    {breadcrumb_html(crumbs)}
    <h1>Customer Success Career Guides</h1>

    <p>The customer success function has grown from a niche support role into one of the most critical departments in SaaS. CS teams now own retention, expansion revenue, and product adoption. That growth has created a clear career ladder and real demand for experienced practitioners.</p>

    <p>These guides break down the skills, certifications, and strategies that move CS professionals from individual contributor roles into leadership positions. Everything here is based on job posting data, compensation benchmarks, and practitioner interviews.</p>

    <h2>Career Path Overview</h2>

    <p>The most common customer success career progression follows this path:</p>

    <ul>
        <li><strong>Customer Success Associate / Onboarding Specialist</strong> - Entry-level. Handles onboarding workflows, basic account support, and product training. Typical comp: $45K-$65K.</li>
        <li><strong>Customer Success Manager (CSM)</strong> - Owns a book of business. Manages renewals, runs QBRs, and drives adoption. Typical comp: $65K-$95K base + variable.</li>
        <li><strong>Senior CSM / Strategic CSM</strong> - Manages enterprise accounts with higher ARR. Deeper product expertise and executive-level relationships. Typical comp: $90K-$130K.</li>
        <li><strong>CS Team Lead / Manager</strong> - First people-management role. Owns team metrics, coaches CSMs, and builds playbooks. Typical comp: $110K-$150K.</li>
        <li><strong>Director of Customer Success</strong> - Owns the CS function or a major segment. Sets strategy, manages managers, reports to VP or C-suite. Typical comp: $140K-$180K.</li>
        <li><strong>VP of Customer Success / CCO</strong> - Executive leadership. Owns NRR at the company level. Board-facing. Typical comp: $180K-$250K+ with equity.</li>
    </ul>

    <h2>Featured Guides</h2>

    <div class="preview-grid">
        <a href="/careers/how-to-become-cs-leader/" class="preview-card">
            <h3>How to Become a Customer Success Leader</h3>
            <p>The skills, certifications, and experience that separate CS managers from CS directors and VPs. A complete roadmap from CSM to executive.</p>
            <span class="preview-link">Read the guide &rarr;</span>
        </a>
        <a href="/careers/job-growth/" class="preview-card">
            <h3>Customer Success Job Market Growth</h3>
            <p>How fast is the CS job market growing? Data on open roles, new titles, salary trends, and which industries are hiring the most CS professionals.</p>
            <span class="preview-link">See the data &rarr;</span>
        </a>
    </div>

    <h2>Key Skills for Customer Success Professionals</h2>

    <p>Regardless of seniority level, the highest-performing CS professionals share a core skill set:</p>

    <ul>
        <li><strong>Data fluency</strong> - Ability to read dashboards, build health scores, and translate usage data into action plans. SQL and spreadsheet proficiency are table stakes at the senior level.</li>
        <li><strong>Business acumen</strong> - Understanding how your customers make money, what their KPIs are, and how your product fits into their P&amp;L. This separates strategic CSMs from reactive ones.</li>
        <li><strong>Communication</strong> - Running executive business reviews, writing renewal justifications, and navigating difficult conversations about churn risk. Written and verbal.</li>
        <li><strong>Technical aptitude</strong> - Not engineering-level depth, but enough to understand APIs, integrations, and product architecture. Critical for platform-focused CS roles.</li>
        <li><strong>Cross-functional collaboration</strong> - Working effectively with product, sales, marketing, and support. CS sits at the center of the post-sale org chart.</li>
    </ul>

    <h2>Certifications That Matter</h2>

    <p>The CS certification landscape is still maturing, but a few programs carry real weight with hiring managers:</p>

    <ul>
        <li><strong>Gainsight Admin Certification</strong> - Validates technical proficiency with the most widely adopted CS platform. Especially valuable for CS ops and team lead roles.</li>
        <li><strong>SuccessHACKING CSM Certification</strong> - Practitioner-focused program covering the full CSM workflow from onboarding to renewal.</li>
        <li><strong>Cisco Customer Success Manager (DTCSM)</strong> - Vendor-specific but respected in enterprise tech. Covers adoption frameworks and success planning.</li>
    </ul>

    <p>Certifications alone will not land a promotion. They are most useful as signals when combined with real account management experience and measurable business outcomes.</p>

'''
    body += newsletter_cta_html()
    body += '</div>'

    extra_head = get_breadcrumb_schema(crumbs)
    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/careers/",
        body_content=body,
        active_path="/careers/",
        extra_head=extra_head,
    )
    write_page("careers/index.html", page)
    print(f"  Built: careers/index.html")


# ---------------------------------------------------------------------------
# How to Become a CS Leader
# ---------------------------------------------------------------------------

def build_cs_leader_guide():
    """Generate /careers/how-to-become-cs-leader/ page."""
    title = "How to Become a Customer Success Leader"
    description = (
        "A complete guide to advancing from CSM to CS Director or VP."
        " Skills, certifications, tools, salary expectations, and the career moves that matter most."
    )

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("How to Become a CS Leader", None)]
    body = f'''<div class="salary-content">
    {breadcrumb_html(crumbs)}
    <h1>How to Become a Customer Success Leader</h1>

    <p>The path from individual contributor to CS leadership is not random. It follows a pattern: build technical credibility, demonstrate revenue impact, and learn to manage people and process at the same time. This guide covers what that looks like at each stage.</p>

    <h2>The CSM-to-Leader Timeline</h2>

    <p>Most CS leaders reach their first director-level role within 5 to 8 years of entering customer success. The typical progression:</p>

    <ul>
        <li><strong>Years 1-2: CSM / Associate CSM</strong> - Learn the product inside out. Build a track record of strong NPS, on-time renewals, and adoption milestones. Focus on becoming the CSM that other CSMs ask for help.</li>
        <li><strong>Years 2-4: Senior CSM / Strategic CSM</strong> - Take on larger, more complex accounts. Start running executive business reviews. Develop a specialty (onboarding, enterprise, technical accounts). Begin mentoring junior CSMs informally.</li>
        <li><strong>Years 4-6: CS Team Lead / Manager</strong> - First official people-management role. Transition from carrying a book of business to coaching others on theirs. Build playbooks, define processes, own team-level KPIs.</li>
        <li><strong>Years 6-8: Director of Customer Success</strong> - Own the CS function or a major business segment. Set strategy, hire and develop managers, and present to the executive team. This is where CS leaders start owning NRR targets directly.</li>
        <li><strong>Years 8+: VP of Customer Success / CCO</strong> - Executive leadership with board-level visibility. Own the full post-sale revenue number. Influence product roadmap, pricing strategy, and company direction.</li>
    </ul>

    <p>These timelines compress at fast-growing startups and stretch at larger enterprises. The key accelerant is not tenure but demonstrable business impact.</p>

    <h2>Skills That Separate Leaders from ICs</h2>

    <p>Individual contributors are judged on account outcomes. Leaders are judged on team outcomes and strategic thinking. The skills that matter most at the leadership level:</p>

    <h3>Revenue Ownership</h3>
    <p>CS leaders own NRR, GRR, and expansion revenue. You need to be comfortable building forecasts, presenting revenue data to the board, and holding your team accountable to financial targets. If you have not managed a P&amp;L or revenue number before, find ways to get exposure before pursuing leadership roles.</p>

    <h3>People Management</h3>
    <p>Managing CSMs is fundamentally different from managing accounts. You need to develop coaching frameworks, run effective 1:1s, navigate performance conversations, and build a team culture that retains top performers. The best CS leaders spend 60%+ of their time on people development.</p>

    <h3>Process Design</h3>
    <p>Leaders build the playbooks that scale customer success beyond individual heroics. Onboarding workflows, health scoring models, risk escalation paths, QBR templates, and renewal processes all need to be documented, trained, and iterated. If your CS motion depends on any single person's tribal knowledge, it is not scalable.</p>

    <h3>Cross-Functional Influence</h3>
    <p>CS leaders sit at the intersection of product, sales, marketing, and support. You need to influence product roadmap decisions using customer data, align with sales on expansion motions, and partner with marketing on customer advocacy programs. The ability to drive outcomes through teams you do not manage is a defining leadership skill.</p>

    <h3>Data and Technology</h3>
    <p>Modern CS leadership requires fluency with CS platforms (Gainsight, Vitally, ChurnZero), CRMs (Salesforce, HubSpot), and data tools (Looker, Tableau, SQL). You do not need to be an admin, but you need to understand what is possible and make informed technology decisions for your team.</p>

    <h2>Certifications Worth Pursuing</h2>

    <p>Certifications are not a substitute for experience, but they signal commitment and can fill specific knowledge gaps:</p>

    <ul>
        <li><strong>Gainsight Admin Certification</strong> - The most recognized CS platform certification. Validates your ability to configure and optimize the tool that many enterprise CS teams run on. Especially valuable if you are moving into CS ops or leading a team that uses Gainsight.</li>
        <li><strong>SuccessHACKING Certified Customer Success Manager</strong> - Covers the full CSM lifecycle with a practitioner focus. Good for solidifying fundamentals if you are transitioning from support, sales, or another function.</li>
        <li><strong>Cisco DTCSM</strong> - Enterprise-oriented certification that covers adoption frameworks, success plans, and outcome-based engagement models. Carries weight in large tech environments.</li>
        <li><strong>PMP or equivalent</strong> - Not CS-specific, but project management skills are directly applicable to onboarding programs, CS ops buildouts, and cross-functional initiatives. Useful for rounding out a leadership profile.</li>
    </ul>

    <h2>Tools CS Leaders Should Know</h2>

    <p>You do not need to be an expert in every tool, but CS leaders should have working familiarity with the major categories:</p>

    <ul>
        <li><strong>CS Platforms</strong> - <a href="/tools/gainsight/">Gainsight</a>, <a href="/tools/vitally/">Vitally</a>, <a href="/tools/churnzero/">ChurnZero</a>, Totango, Planhat. Know the strengths and tradeoffs of each.</li>
        <li><strong>CRMs</strong> - Salesforce and HubSpot dominate. Understand how CS data flows into and out of the CRM.</li>
        <li><strong>Analytics</strong> - Looker, Tableau, Amplitude, Mixpanel. Usage and adoption data is the foundation of proactive CS.</li>
        <li><strong>Communication</strong> - Gong for call intelligence, Slack for internal collaboration, Loom for async updates. CS leaders who leverage these tools effectively scale their own output.</li>
    </ul>

    <h2>Salary Expectations by Level</h2>

    <p>Compensation data from our <a href="/salary/">salary benchmarks</a> shows clear jumps at each transition point:</p>

    <table class="data-table">
        <thead>
            <tr>
                <th>Role</th>
                <th>Base Salary Range</th>
                <th>Total Comp (with variable)</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>CSM</td><td>$65K - $95K</td><td>$75K - $115K</td></tr>
            <tr><td>Senior CSM</td><td>$90K - $130K</td><td>$105K - $155K</td></tr>
            <tr><td>CS Manager / Team Lead</td><td>$110K - $150K</td><td>$130K - $180K</td></tr>
            <tr><td>Director of CS</td><td>$140K - $180K</td><td>$170K - $220K</td></tr>
            <tr><td>VP of CS</td><td>$180K - $250K</td><td>$220K - $320K+</td></tr>
        </tbody>
    </table>

    <p>These ranges reflect US-based roles at mid-market to enterprise SaaS companies. Early-stage startups may offer lower base with equity upside. FAANG and late-stage companies typically pay at the top of these ranges or above.</p>

    <h2>Common Mistakes to Avoid</h2>

    <ul>
        <li><strong>Staying too long as an IC</strong> - If you want leadership, signal it early. Volunteer to lead projects, mentor new hires, and propose process improvements. Waiting to be tapped rarely works.</li>
        <li><strong>Neglecting the business side</strong> - CS leaders who only talk about relationships and NPS struggle to earn executive trust. Learn to speak in terms of revenue impact, retention rates, and pipeline influence.</li>
        <li><strong>Skipping the manager step</strong> - Jumping from Senior CSM directly to Director is rare and risky. The team lead or manager role builds critical people management skills you will need at every subsequent level.</li>
        <li><strong>Over-indexing on certifications</strong> - A certification without relevant experience is a line on a resume. Prioritize getting the right account experience, then supplement with credentials that fill genuine gaps.</li>
        <li><strong>Ignoring CS ops</strong> - Understanding how to instrument health scores, automate playbooks, and build dashboards is increasingly non-negotiable for CS leaders. If you cannot build it yourself, learn enough to spec it for someone who can.</li>
    </ul>

    <h2>Next Steps</h2>

    <p>Start by benchmarking your current compensation against our <a href="/salary/">salary data</a>. Review the <a href="/tools/">CS tools directory</a> to identify platform knowledge gaps. And if you are evaluating your next move, our <a href="/careers/job-growth/">job market growth data</a> shows where demand is heading.</p>

'''
    body += newsletter_cta_html()
    body += '</div>'

    faq_pairs = [
        ("How long does it take to become a CS Director?",
         "Most CS professionals reach Director level within 6 to 8 years of entering customer success. The timeline compresses at fast-growing startups where scope expands quickly and stretches at large enterprises with more structured promotion cycles."),
        ("What certifications do CS leaders need?",
         "Gainsight Admin Certification is the most widely recognized. SuccessHACKING and Cisco DTCSM also carry weight. However, certifications supplement experience rather than replace it. Hiring managers prioritize demonstrated business impact over credentials."),
        ("What is the salary range for VP of Customer Success?",
         "VP of Customer Success roles at US-based mid-market to enterprise SaaS companies typically pay $180K to $250K base salary, with total compensation (including variable and equity) ranging from $220K to $320K or higher at top-tier companies."),
    ]

    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)
    body_with_faq = body.replace('</div>', faq_html(faq_pairs) + '\n</div>')

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/careers/how-to-become-cs-leader/",
        body_content=body_with_faq,
        active_path="/careers/",
        extra_head=extra_head,
    )
    write_page("careers/how-to-become-cs-leader/index.html", page)
    print(f"  Built: careers/how-to-become-cs-leader/index.html")


# ---------------------------------------------------------------------------
# Job Market Growth
# ---------------------------------------------------------------------------

def build_job_growth_page():
    """Generate /careers/job-growth/ page."""
    title = "Customer Success Job Market Growth"
    description = (
        "Data on customer success job market growth, open roles, emerging titles,"
        " and hiring trends. Which industries and company stages are adding CS headcount fastest."
    )

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Job Market Growth", None)]
    body = f'''<div class="salary-content">
    {breadcrumb_html(crumbs)}
    <h1>Customer Success Job Market Growth</h1>

    <p>Customer success is one of the fastest-growing functions in B2B SaaS. What started as a small team inside a few forward-thinking companies has become a standard department at nearly every subscription-based business. The data tells a clear story: demand for CS professionals continues to outpace supply, and the roles are getting more senior and more specialized.</p>

    <h2>Market Size and Growth Rate</h2>

    <p>LinkedIn data shows that "Customer Success Manager" is among the top 10 fastest-growing job titles over the past decade. The number of professionals listing customer success as their primary function has grown roughly 40% year over year since 2020.</p>

    <p>Several forces are driving this growth:</p>

    <ul>
        <li><strong>SaaS adoption continues expanding</strong> - Every new SaaS company needs a retention function. As the software market grows, so does the CS job market.</li>
        <li><strong>Revenue model alignment</strong> - Subscription businesses live and die by retention. CS is the primary function responsible for keeping customers renewing and expanding.</li>
        <li><strong>Board-level visibility</strong> - Investors now ask about NRR, GRR, and CS coverage ratios during due diligence. This executive attention drives headcount investment.</li>
        <li><strong>AI and automation</strong> - Rather than eliminating CS roles, AI tools are shifting CS work from administrative tasks to strategic account management, which requires more experienced (and more expensive) talent.</li>
    </ul>

    <h2>Emerging Titles and Specializations</h2>

    <p>The CS job market is not just growing in volume. It is growing in complexity. New titles reflect increasing specialization:</p>

    <table class="data-table">
        <thead>
            <tr>
                <th>Title</th>
                <th>Focus Area</th>
                <th>Growth Trend</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>Customer Success Operations Manager</td><td>CS tech stack, health scoring, automation</td><td>High - new function at most companies</td></tr>
            <tr><td>Digital Customer Success Manager</td><td>1-to-many engagement, tech-touch accounts</td><td>High - scaling CS without linear headcount</td></tr>
            <tr><td>Customer Success Enablement Manager</td><td>CSM training, playbook development, onboarding</td><td>Moderate - growing at companies with 10+ CSMs</td></tr>
            <tr><td>Renewal Manager</td><td>Dedicated renewal execution and forecasting</td><td>Moderate - splitting from CSM role at scale</td></tr>
            <tr><td>CS Data Analyst</td><td>Churn modeling, health score optimization, reporting</td><td>Emerging - data-mature CS orgs only</td></tr>
            <tr><td>Chief Customer Officer (CCO)</td><td>Executive ownership of entire post-sale experience</td><td>Moderate - mostly at companies above $50M ARR</td></tr>
        </tbody>
    </table>

    <h2>Hiring by Industry</h2>

    <p>CS hiring is concentrated in industries with high recurring revenue and complex products:</p>

    <ul>
        <li><strong>Enterprise SaaS</strong> - The largest employer of CS professionals. Complex implementations, long sales cycles, and high contract values mean dedicated CSM coverage is standard.</li>
        <li><strong>Fintech</strong> - Regulatory complexity and high switching costs make retention critical. Fintech companies are building CS teams earlier in their growth than most industries.</li>
        <li><strong>Healthcare IT / HealthTech</strong> - Long implementation cycles and compliance requirements create demand for experienced, patient CSMs who understand clinical workflows.</li>
        <li><strong>Cybersecurity</strong> - Rapid market growth and commoditized products make CS a competitive differentiator. Security vendors are investing heavily in post-sale experience.</li>
        <li><strong>HR Tech / People Platforms</strong> - High employee count = high user count = high need for adoption support. HR tech companies tend to have larger CS teams relative to revenue.</li>
    </ul>

    <h2>Company Stage and CS Headcount</h2>

    <p>When companies hire their first CSM and how fast they scale the team varies by stage:</p>

    <ul>
        <li><strong>Seed / Series A</strong> - Usually 0-2 CSMs. Often the founders or early employees handle customer success informally. First dedicated CS hire typically comes between $1M and $3M ARR.</li>
        <li><strong>Series B</strong> - CS team of 3-8. First CS manager hired. Beginning to segment accounts by tier. Playbooks are still ad hoc.</li>
        <li><strong>Series C+</strong> - CS team of 10-30+. Dedicated CS ops role. Formal health scoring. Specialized roles (onboarding, enterprise, renewals) begin splitting out.</li>
        <li><strong>Public / Late Stage</strong> - CS organizations of 50-200+. Multiple layers of management. Regional or segment-based team structures. CS is a named department in earnings calls.</li>
    </ul>

    <h2>Salary Trends</h2>

    <p>CS salaries have grown faster than the broader tech market, driven by demand outpacing supply. Key trends from our <a href="/salary/">salary data</a>:</p>

    <ul>
        <li>CSM base salaries have increased approximately 12% over the past two years.</li>
        <li>Director and VP roles have seen the largest absolute gains, with total comp packages at top companies exceeding $300K.</li>
        <li>Remote roles now pay 90-95% of on-site equivalents, up from roughly 80% in 2021. The gap is closing.</li>
        <li>Variable compensation (bonuses tied to NRR, renewal rate, or expansion) is becoming standard at the senior CSM level and above.</li>
    </ul>

    <h2>What This Means for CS Professionals</h2>

    <p>The market data points to a clear opportunity. CS is not a temporary trend driven by a single economic cycle. It is a structural shift in how software companies organize around retention and expansion revenue.</p>

    <p>For practitioners, this means:</p>

    <ul>
        <li>Demand for experienced CS professionals will remain strong through 2027 and beyond.</li>
        <li>Specialization (CS ops, digital CS, renewal management) creates new career paths beyond the traditional CSM-to-VP ladder.</li>
        <li>Compensation will continue rising, particularly for professionals who can demonstrate measurable revenue impact.</li>
        <li>AI proficiency will become a differentiator, not a replacement. CSMs who can leverage AI tools for account research, health scoring, and communication will command premium compensation.</li>
    </ul>

    <p>Explore our <a href="/careers/how-to-become-cs-leader/">CS leadership guide</a> for a detailed roadmap on advancing your career, or check the <a href="/salary/">salary benchmarks</a> to see where your compensation stands relative to the market.</p>

'''
    body += newsletter_cta_html()
    body += '</div>'

    faq_pairs = [
        ("How fast is the customer success job market growing?",
         "Customer success roles have grown roughly 40% year over year since 2020, making it one of the fastest-growing functions in B2B SaaS. Demand is driven by the continued shift to subscription revenue models and increasing board-level focus on retention metrics."),
        ("Which industries hire the most CS professionals?",
         "Enterprise SaaS is the largest employer, followed by fintech, healthcare IT, cybersecurity, and HR tech. Any industry with complex subscription products and high contract values tends to invest heavily in customer success."),
        ("Will AI replace customer success managers?",
         "AI is more likely to reshape CS roles than eliminate them. Administrative tasks like data entry, email drafting, and basic reporting are being automated. But strategic account management, executive relationships, and complex problem-solving remain human-driven. CSMs who adopt AI tools will outperform those who do not."),
    ]

    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)
    body_with_faq = body.replace('</div>', faq_html(faq_pairs) + '\n</div>')

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/careers/job-growth/",
        body_content=body_with_faq,
        active_path="/careers/",
        extra_head=extra_head,
    )
    write_page("careers/job-growth/index.html", page)
    print(f"  Built: careers/job-growth/index.html")


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def build_all_careers_pages():
    """Build all career guide pages."""
    print("\n  Building career guide pages...")
    build_careers_index()
    build_cs_leader_guide()
    build_job_growth_page()
