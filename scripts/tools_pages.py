# scripts/tools_pages.py
# Tool reviews section page generators (~40 pages).
# Loads market_intelligence.json, generates index + categories + individual reviews + comparisons + roundups.

import os
import json

from nav_config import *
from templates import (get_page_wrapper, write_page, get_breadcrumb_schema,
                       get_faq_schema, get_software_application_schema,
                       breadcrumb_html, newsletter_cta_html, faq_html)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def stat_cards_html(cards):
    """Render a row of stat cards. cards = [(value, label), ...]"""
    items = ""
    for val, lbl in cards:
        items += f'''<div class="stat-block">
    <span class="stat-value">{val}</span>
    <span class="stat-label">{lbl}</span>
</div>\n'''
    return f'<div class="stat-grid">{items}</div>'


def load_market_data():
    with open(os.path.join(DATA_DIR, "market_intelligence.json"), "r") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Tool database — REAL data + descriptions
# ---------------------------------------------------------------------------

CATEGORIES = {
    "cs-platforms": {
        "name": "CS Platforms",
        "description": "Dedicated customer success platforms that centralize health scoring, playbook automation, and customer lifecycle management.",
        "tools": ["Gainsight", "Vitally", "ChurnZero", "Totango", "Planhat", "Catalyst"],
    },
    "onboarding": {
        "name": "Onboarding Tools",
        "description": "Tools that structure and automate customer onboarding workflows, reducing time-to-value.",
        "tools": ["GuideCX", "Rocketlane", "OnRamp", "Arrows"],
    },
    "feedback": {
        "name": "Feedback & Survey",
        "description": "NPS, CSAT, and customer feedback collection platforms used by CS teams to measure sentiment.",
        "tools": ["Delighted", "AskNicely", "Pendo", "Medallia"],
    },
    "digital-adoption": {
        "name": "Digital Adoption Platforms",
        "description": "In-app guidance, onboarding tours, and feature adoption tools that CS teams use to drive product usage.",
        "tools": ["WalkMe", "Pendo", "Appcues", "Userpilot"],
    },
    "revenue-intelligence": {
        "name": "Revenue Intelligence",
        "description": "Conversation intelligence and revenue operations platforms that give CS teams visibility into customer engagement and pipeline.",
        "tools": ["Gong", "Clari", "People.ai"],
    },
    "crm": {
        "name": "CRM for Customer Success",
        "description": "CRM platforms that CS teams use as their system of record for customer data, workflows, and reporting.",
        "tools": ["Salesforce", "HubSpot"],
    },
}

# Tools with enough data for individual review pages
TOOL_PROFILES = {
    "Gainsight": {
        "slug": "gainsight",
        "mentions": 86,
        "category": "cs-platforms",
        "founded": "2013",
        "hq": "San Francisco, CA",
        "pricing": "Custom pricing, typically $2,500-$15,000/month depending on seats and modules",
        "best_for": "Enterprise CS teams with 10+ CSMs",
        "website": "https://www.gainsight.com",
        "rating": {"value": 4.4, "count": 1200},
        "description": "The dominant customer success platform. Health scoring, playbook automation, customer journey orchestration, and CS analytics in a single platform.",
        "pros": [
            "Most comprehensive feature set in the CS platform market",
            "Deep Salesforce integration with bidirectional sync",
            "Mature health scoring engine with configurable weights",
            "Robust playbook automation (CTAs, success plans, timeline)",
            "Strong analytics with Horizon Analytics module",
            "Large user community and ecosystem (Pulse conference)",
        ],
        "cons": [
            "Steep learning curve requiring dedicated admin resources",
            "Expensive for small teams (entry price often $30K+/year)",
            "Implementation typically takes 3-6 months",
            "UI can feel dated compared to newer competitors",
            "Some features require additional modules at extra cost",
        ],
        "body": """<h2>Why Gainsight Dominates the CS Platform Market</h2>
<p>Gainsight appears in {mentions} of the {total_jobs} CS job postings we track. That is more than ChurnZero, Totango, Vitally, Planhat, and Catalyst combined. When companies hire for CS roles, Gainsight experience is the most requested platform skill by a wide margin.</p>
<p>The dominance is not accidental. Gainsight was the first purpose-built CS platform, and it has had a decade to build depth. Health scores, playbooks, CTAs, success plans, customer journey orchestration, product usage analytics, and community management all live under one roof. No competitor matches the breadth.</p>

<h2>Who Should Use Gainsight</h2>
<p>Gainsight makes the most sense for CS teams with 10 or more CSMs managing mid-market to enterprise accounts. At that scale, the ROI on playbook automation and health scoring justifies the investment. A single CSM saved from reactive firefighting by an automated CTA is worth more than the monthly platform cost.</p>
<p>Smaller teams (under 5 CSMs) often find Gainsight overbuilt for their needs. The admin overhead of maintaining health score models, playbooks, and integrations requires at least a part-time Gainsight admin. If your team is small, look at Vitally or Planhat first.</p>

<h2>Gainsight Implementation Reality</h2>
<p>Expect 3-6 months for a full implementation. The first phase typically covers health scoring, basic playbooks, and Salesforce integration. Phase two adds advanced automation, product usage data, and executive dashboards. Companies that try to do everything at once usually stall.</p>
<p>The most common implementation mistake is over-engineering health scores from day one. Start with 3-5 simple health score components (product usage, support ticket volume, NPS, engagement recency) and iterate. You can always add complexity later. Starting complex means nobody trusts the scores.</p>

<h2>Gainsight Pricing</h2>
<p>Gainsight does not publish pricing. Based on market data, expect $2,500-$15,000/month depending on the number of users, modules, and customer volume. Enterprise deals with 50+ CSM seats can exceed $200K/year. Gainsight's pricing has historically been a barrier for smaller companies, which is exactly the gap that competitors like Vitally and Planhat target.</p>

<h2>Gainsight vs the Competition</h2>
<p>Every CS platform comparison starts with Gainsight as the benchmark. The question is never "Is Gainsight good?" It is "Is Gainsight worth the premium?" For enterprise teams with budget and admin resources, the answer is usually yes. For lean teams that need speed over depth, the answer is often no. Check our head-to-head comparisons for detailed analysis.</p>""",
    },
    "Vitally": {
        "slug": "vitally",
        "mentions": 10,
        "category": "cs-platforms",
        "founded": "2017",
        "hq": "New York, NY",
        "pricing": "Starting around $1,500/month for small teams",
        "best_for": "Growth-stage CS teams (5-30 CSMs) wanting modern UX",
        "website": "https://www.vitally.io",
        "rating": {"value": 4.6, "count": 280},
        "description": "Modern CS platform built for speed. Clean UI, flexible health scoring, and strong product analytics integration. The top Gainsight alternative for mid-market teams.",
        "pros": [
            "Clean, intuitive UI that CSMs actually enjoy using",
            "Fast implementation (weeks, not months)",
            "Strong product analytics with event-level tracking",
            "Flexible health scoring with custom models",
            "Good API and integration ecosystem",
            "More affordable than Gainsight at comparable scale",
        ],
        "cons": [
            "Less mature than Gainsight for complex enterprise workflows",
            "Smaller user community and ecosystem",
            "Fewer pre-built integrations than Gainsight",
            "Reporting depth lags behind Gainsight Horizon Analytics",
            "Less established brand for enterprise sales cycles",
        ],
        "body": """<h2>Why Vitally Is the Fastest-Growing CS Platform</h2>
<p>Vitally has earned a reputation as the modern alternative to Gainsight. The platform launched in 2017 and focused on two things legacy platforms got wrong: speed of implementation and user experience. While Gainsight implementations take 3-6 months, Vitally teams often go live in 2-4 weeks.</p>
<p>With {mentions} mentions in our job posting dataset, Vitally is gaining traction in hiring requirements. The mentions are concentrated at growth-stage SaaS companies (Series B-D) that need robust CS tooling without the overhead of an enterprise platform.</p>

<h2>Who Should Use Vitally</h2>
<p>Vitally fits best at companies with 5-30 CSMs managing a mix of mid-market and SMB accounts. The platform handles high account volumes well thanks to its automation engine, and the product analytics integration means you can build health scores from actual product usage data without a separate analytics tool.</p>
<p>If you are a CS leader evaluating platforms for the first time, Vitally should be on your shortlist. The implementation speed means you start getting value faster, and the lower price point reduces the risk of a platform bet.</p>

<h2>Vitally vs Gainsight: The Core Tradeoff</h2>
<p>Vitally trades depth for speed. Gainsight has more features, more integrations, and a larger ecosystem. Vitally has better UX, faster setup, and lower cost. For most mid-market CS teams, Vitally delivers 90% of the functionality at 60% of the cost and a third of the implementation time. That math works for a lot of companies.</p>
<p>The exception is complex enterprise environments with heavy Salesforce customization, multi-product portfolios, and 50+ CSM teams. At that scale, Gainsight's depth matters. Below that threshold, Vitally is the stronger choice for most teams.</p>

<h2>Product Analytics Edge</h2>
<p>Vitally's product analytics capabilities stand out. The platform ingests product events natively and lets CS teams build health scores, segments, and automations based on actual user behavior. Gainsight offers similar functionality through its PX module, but it is a separate product with separate pricing. Vitally includes it in the core platform.</p>""",
    },
    "ChurnZero": {
        "slug": "churnzero",
        "mentions": 17,
        "category": "cs-platforms",
        "founded": "2015",
        "hq": "Washington, DC",
        "pricing": "Starting around $1,200/month",
        "best_for": "Mid-market CS teams focused on real-time usage alerts",
        "website": "https://www.churnzero.net",
        "rating": {"value": 4.5, "count": 850},
        "description": "Real-time CS platform with strong usage tracking, journey-based automation, and in-app messaging. Particularly strong for SaaS companies with clear product usage patterns.",
        "pros": [
            "Real-time product usage tracking and alerts",
            "Strong journey-based automation engine",
            "In-app messaging and guided walkthroughs",
            "Good value for mid-market teams",
            "Solid Salesforce and HubSpot integrations",
            "Active product development with frequent releases",
        ],
        "cons": [
            "Health score configuration can be complex",
            "Reporting is functional but not as polished as Gainsight",
            "Smaller ecosystem than Gainsight",
            "UI has improved but still not as clean as Vitally",
            "Some features require technical setup that CSMs cannot do alone",
        ],
        "body": """<h2>ChurnZero's Position in the CS Platform Market</h2>
<p>ChurnZero sits in the sweet spot between Gainsight's enterprise depth and Vitally's modern simplicity. With {mentions} mentions in CS job postings, it has strong hiring signal, particularly among mid-market SaaS companies. The platform's strength is real-time product usage tracking. If your product generates clear usage events, ChurnZero turns those signals into health scores, alerts, and automated workflows faster than most competitors.</p>

<h2>Who Should Use ChurnZero</h2>
<p>ChurnZero works best for CS teams at SaaS companies where product usage patterns directly predict retention. If you can define "healthy" usage in measurable terms (daily active users, feature adoption rates, login frequency), ChurnZero turns that data into actionable CS workflows. The platform excels at catching at-risk customers before they churn by surfacing usage drops in real time.</p>
<p>Mid-market CS teams with 5-25 CSMs get the most value. The price point is lower than Gainsight, and the real-time alerting is more mature than what Vitally or Planhat offer. If real-time usage tracking is your top priority, ChurnZero should be your first demo.</p>

<h2>In-App Engagement</h2>
<p>ChurnZero includes in-app messaging that most CS platforms lack. You can create guided walkthroughs, announcement banners, and feature spotlights directly from the CS platform. This means CS teams can drive adoption without depending on the product team to build onboarding flows. It is a meaningful advantage for teams that want to own the adoption experience end-to-end.</p>

<h2>ChurnZero Implementation</h2>
<p>Implementation takes 4-8 weeks for a standard deployment. The real-time usage tracking requires a JavaScript snippet or backend integration, which adds technical complexity compared to platforms that work purely from CRM data. Plan for engineering support during setup. After that initial integration, CSMs can manage the platform day-to-day.</p>""",
    },
    "Totango": {
        "slug": "totango",
        "mentions": 20,
        "category": "cs-platforms",
        "founded": "2010",
        "hq": "Redwood City, CA",
        "pricing": "Free tier available; paid plans from $2,000/month",
        "best_for": "Teams wanting modular CS with a free entry point",
        "website": "https://www.totango.com",
        "rating": {"value": 4.2, "count": 700},
        "description": "One of the original CS platforms with a modular approach. Offers a free tier for small teams and scales to enterprise with SuccessBloc modules.",
        "pros": [
            "Free tier (Spark) for small teams",
            "Modular SuccessBloc approach lets teams start simple",
            "Strong segmentation and health scoring",
            "Good enterprise track record",
            "Flexible integration options",
        ],
        "cons": [
            "UI feels dated compared to Vitally and newer platforms",
            "Free tier is limited and pushes toward paid quickly",
            "Implementation can be complex for full deployment",
            "Community and ecosystem smaller than Gainsight",
            "Product development pace has slowed relative to competitors",
        ],
        "body": """<h2>Totango's Place in the CS Platform Landscape</h2>
<p>Totango is one of the oldest names in customer success software, founded in 2010. With {mentions} mentions in CS job postings, it maintains a meaningful market presence. The platform's differentiator is its modular "SuccessBloc" approach: pre-built customer success modules that teams can mix and match based on their needs. Onboarding, adoption, renewal, expansion, and advocacy each have dedicated SuccessBlocs.</p>

<h2>The Free Tier Advantage</h2>
<p>Totango offers a free tier called Spark that supports small teams. This is unique among major CS platforms. For a startup with 1-3 CSMs, Spark provides basic health scoring and customer tracking at zero cost. The strategy is clear: get teams using Totango early and upsell as they grow. It works. Many mid-market Totango customers started on Spark.</p>

<h2>Who Should Use Totango</h2>
<p>Totango works well for two profiles: early-stage teams that want a free starting point, and enterprise teams that value the modular approach. The SuccessBloc model lets large organizations deploy CS processes across different teams (onboarding team, renewal team, expansion team) with specialized tooling for each. This is different from Gainsight's monolithic approach and appeals to companies with highly specialized CS functions.</p>

<h2>Totango vs Modern Alternatives</h2>
<p>The honest assessment: Totango's UX and product velocity have not kept pace with Vitally, ChurnZero, or Planhat. The platform works, and existing customers generally stay, but new evaluations increasingly favor the newer players. If you are choosing a CS platform today and do not have a specific reason to pick Totango (like the free tier or the modular approach), the competition offers more modern experiences.</p>""",
    },
    "Planhat": {
        "slug": "planhat",
        "mentions": 12,
        "category": "cs-platforms",
        "founded": "2015",
        "hq": "Stockholm, Sweden",
        "pricing": "Starting around $1,000/month",
        "best_for": "European CS teams and companies wanting clean, flexible CS tooling",
        "website": "https://www.planhat.com",
        "rating": {"value": 4.5, "count": 350},
        "description": "European-origin CS platform with clean design, flexible data model, and strong revenue tracking. Growing rapidly in both European and US markets.",
        "pros": [
            "Clean, modern UI with strong visual design",
            "Flexible data model that adapts to your business",
            "Strong revenue tracking and forecasting",
            "Good for multi-product and multi-entity structures",
            "GDPR-compliant by design (European origin)",
            "Competitive pricing",
        ],
        "cons": [
            "Smaller US market presence than Gainsight or ChurnZero",
            "Fewer native integrations than US-based competitors",
            "Smaller talent pool of Planhat-experienced CSMs",
            "Less mature playbook automation than Gainsight",
            "Community and ecosystem still growing",
        ],
        "body": """<h2>Planhat's Growing Market Presence</h2>
<p>Planhat appears in {mentions} CS job postings in our dataset, reflecting its rapid growth from a European niche player to a global CS platform contender. The Stockholm-based company has won significant market share by offering clean design, flexible data modeling, and competitive pricing. CS leaders who have used both Gainsight and Planhat frequently describe Planhat as "what Gainsight would be if it were built today."</p>

<h2>Who Should Use Planhat</h2>
<p>Planhat fits well at companies with complex customer structures (multi-product, multi-entity, global accounts) and CS teams that value a clean, modern interface. The flexible data model means Planhat can represent your business the way it actually works, rather than forcing you into a rigid schema.</p>
<p>European companies should give Planhat strong consideration. GDPR compliance is native, and the company understands European business models. US companies evaluating Planhat should weigh the smaller ecosystem against the product's quality and price advantage.</p>

<h2>Revenue Intelligence</h2>
<p>Planhat's revenue tracking is arguably the best among dedicated CS platforms. The platform integrates financial data deeply, letting CS teams track ARR, expansion, contraction, and churn at the account and portfolio level. This revenue-first approach makes Planhat particularly attractive for CS teams that own NRR as a primary metric.</p>

<h2>The European Edge</h2>
<p>Being European-built gives Planhat structural advantages for companies operating in the EU. Data residency, GDPR compliance, and European business hour support are table stakes, not add-ons. As more SaaS companies expand into Europe, these capabilities become differentiators rather than nice-to-haves.</p>""",
    },
    "Catalyst": {
        "slug": "catalyst",
        "mentions": 18,
        "category": "cs-platforms",
        "founded": "2017",
        "hq": "New York, NY",
        "pricing": "Starting around $1,500/month",
        "best_for": "CS teams wanting CRM-like simplicity with CS-specific workflows",
        "website": "https://www.catalyst.io",
        "rating": {"value": 4.3, "count": 400},
        "description": "CS platform designed by former CS practitioners. Combines CRM-like usability with CS-specific health scoring, automation, and revenue tracking.",
        "pros": [
            "Built by CS practitioners, so workflows feel natural",
            "Strong CRM-like interface that CSMs adopt quickly",
            "Good health scoring with clear visualization",
            "Revenue and renewal tracking built-in",
            "Fast implementation (4-6 weeks typical)",
            "Growing integration ecosystem",
        ],
        "cons": [
            "Less mature than Gainsight for enterprise complexity",
            "Smaller market presence in hiring requirements",
            "Analytics depth is growing but not yet Gainsight-level",
            "Fewer pre-built playbook templates",
            "Brand awareness lower than top-3 competitors",
        ],
        "body": """<h2>Catalyst's Practitioner-First Approach</h2>
<p>Catalyst was built by former customer success managers, and it shows. The platform feels like a CRM that was purpose-built for CS workflows rather than a CS layer bolted onto generic software. With {mentions} mentions in CS job postings, Catalyst has meaningful market presence, particularly among growth-stage SaaS companies.</p>

<h2>Who Should Use Catalyst</h2>
<p>Catalyst works best for CS teams that want the structure of a dedicated CS platform without the complexity of Gainsight. If your team has been managing customer success in Salesforce or spreadsheets and wants a purpose-built tool, Catalyst bridges the gap between "no tool" and "enterprise platform" better than most alternatives.</p>
<p>The CRM-like interface means CSMs adopt it quickly. If your biggest challenge is getting your team to actually use the CS platform, Catalyst's usability is a real differentiator. It does not matter how powerful a platform is if nobody logs in.</p>

<h2>Catalyst Implementation</h2>
<p>Typical implementation takes 4-6 weeks. The CRM-like data model means less custom configuration than Gainsight, and the team provides hands-on onboarding support. This speed makes Catalyst a strong choice for CS leaders who need to show platform ROI quickly.</p>

<h2>Catalyst vs the Market</h2>
<p>Catalyst competes directly with Vitally for the "modern Gainsight alternative" position. Both offer cleaner UX and faster implementation. Catalyst leans more toward CRM-like workflows; Vitally leans more toward product analytics. Your choice depends on whether your CS model is more relationship-driven (Catalyst) or data-driven (Vitally).</p>""",
    },
    "Salesforce": {
        "slug": "salesforce",
        "mentions": 388,
        "category": "crm",
        "founded": "1999",
        "hq": "San Francisco, CA",
        "pricing": "Enterprise edition from $165/user/month; CS-specific add-ons extra",
        "best_for": "Enterprise CS teams already invested in the Salesforce ecosystem",
        "website": "https://www.salesforce.com",
        "rating": {"value": 4.3, "count": 15000},
        "description": "The dominant CRM platform. Most CS teams use Salesforce as their system of record, often paired with a dedicated CS platform like Gainsight or Vitally.",
        "pros": [
            "Industry standard CRM with massive ecosystem",
            "Deep customization and AppExchange marketplace",
            "Most CS platforms integrate with Salesforce first",
            "Strong reporting with native and add-on analytics",
            "Robust workflow automation (Flow, Process Builder)",
            "Enterprise-grade security and compliance",
        ],
        "cons": [
            "Not built for CS-specific workflows out of the box",
            "Expensive when adding CS-specific licenses and tools",
            "Steep admin learning curve for customization",
            "UI can feel heavy compared to modern CS platforms",
            "Requires dedicated admin for ongoing maintenance",
        ],
        "body": """<h2>Salesforce as the CS System of Record</h2>
<p>Salesforce appears in {mentions} of {total_jobs} CS job postings. That is by far the most mentioned tool in our dataset. But Salesforce is not a CS platform. It is a CRM that CS teams use as their data backbone. Most CS organizations run Salesforce as the system of record and layer a dedicated CS platform (Gainsight, Vitally, ChurnZero) on top for CS-specific workflows.</p>

<h2>When Salesforce Is Enough for CS</h2>
<p>Small CS teams (1-5 CSMs) can often manage in Salesforce without a separate CS platform. Custom objects for health scores, task-based playbooks, and dashboard reports cover the basics. If your team is small, your accounts are few, and your CS processes are straightforward, investing in Salesforce customization may be more cost-effective than adding a second platform.</p>
<p>The breaking point usually comes around 5-10 CSMs. At that scale, the lack of native health scoring, playbook automation, and CS analytics in Salesforce becomes a productivity bottleneck. That is when most teams add a dedicated CS platform.</p>

<h2>Salesforce + CS Platform Integration</h2>
<p>The most common CS tech stack is Salesforce + Gainsight. The second most common is Salesforce + a newer platform (Vitally, ChurnZero, Catalyst). The integration quality varies by platform, but all major CS tools prioritize Salesforce integration because it is where customer data lives.</p>
<p>Key integration points: account and contact sync, opportunity and renewal data, activity logging, and health score writeback. The best integrations are bidirectional, meaning changes in either system reflect in the other. Gainsight's Salesforce integration is the deepest in the market, which is one reason it dominates enterprise CS.</p>

<h2>Salesforce Certification for CS Professionals</h2>
<p>Salesforce Admin and Salesforce Advanced Admin certifications are valuable for CS professionals. They signal that you can configure and optimize the CRM, not just use it. In our data, Salesforce skills correlate with higher salaries across all seniority levels. If you want to maximize your CS career earnings, Salesforce fluency is a safe investment.</p>""",
    },
    "HubSpot": {
        "slug": "hubspot",
        "mentions": 65,
        "category": "crm",
        "founded": "2006",
        "hq": "Cambridge, MA",
        "pricing": "Free CRM; Service Hub from $45/month; Enterprise from $1,200/month",
        "best_for": "SMB and mid-market CS teams wanting an all-in-one platform",
        "website": "https://www.hubspot.com",
        "rating": {"value": 4.4, "count": 10000},
        "description": "All-in-one CRM with Service Hub for customer success workflows. Popular with SMB and mid-market CS teams that want CRM, ticketing, and CS in one platform.",
        "pros": [
            "Free CRM tier for getting started",
            "Service Hub adds CS-specific features natively",
            "Clean, intuitive interface",
            "Strong marketing and sales alignment tools",
            "Good knowledge base and customer portal",
            "Large ecosystem and marketplace",
        ],
        "cons": [
            "CS-specific features less mature than dedicated CS platforms",
            "Health scoring is basic compared to Gainsight or Vitally",
            "Enterprise features require expensive tier upgrades",
            "Not ideal for complex enterprise CS operations",
            "Automation depth lags behind dedicated CS platforms",
        ],
        "body": """<h2>HubSpot for Customer Success Teams</h2>
<p>HubSpot appears in {mentions} CS job postings. Its presence is strongest at SMB and mid-market companies that use HubSpot as their primary CRM. For these companies, adding HubSpot's Service Hub is a natural extension that avoids the cost and complexity of a separate CS platform.</p>

<h2>When HubSpot Is Enough</h2>
<p>HubSpot works well for CS at companies with simple customer journeys, SMB or mid-market accounts, and teams under 10 CSMs. The Service Hub provides ticketing, customer feedback surveys, knowledge bases, and basic automation. For companies already on HubSpot CRM, the marginal cost of adding CS capabilities is much lower than buying a separate platform.</p>
<p>The limitation hits when CS operations become complex. Health scoring in HubSpot is rudimentary compared to Gainsight or Vitally. Playbook automation is possible but requires workarounds. If your CS model involves sophisticated health models, multi-touch playbooks, or customer journey orchestration, you will outgrow HubSpot's CS capabilities.</p>

<h2>HubSpot vs Salesforce for CS</h2>
<p>This is one of the most common platform decisions for CS teams. HubSpot is easier to use and less expensive at the SMB level. Salesforce is more customizable and more powerful at the enterprise level. For CS specifically, neither is a CS platform. Both need supplementation with dedicated CS tools at scale. The difference is that HubSpot's Service Hub covers more CS use cases natively than Salesforce's out-of-box offerings.</p>

<h2>HubSpot CS Growing Pains</h2>
<p>CS teams that start on HubSpot often face a migration decision at the 50-100 customer mark. The platform handles onboarding and support well, but strategic CS workflows (health scoring, expansion playbooks, QBR management) require either heavy customization or a dedicated CS platform. Plan for this transition when building your CS tech stack roadmap.</p>""",
    },
    "Gong": {
        "slug": "gong",
        "mentions": 19,
        "category": "revenue-intelligence",
        "founded": "2015",
        "hq": "San Francisco, CA",
        "pricing": "Custom pricing, typically $100-$200/user/month",
        "best_for": "CS teams wanting conversation intelligence and deal visibility",
        "website": "https://www.gong.io",
        "rating": {"value": 4.7, "count": 5000},
        "description": "Conversation intelligence platform that records, transcribes, and analyzes customer calls. Used by CS teams to identify risk signals and coaching opportunities.",
        "pros": [
            "Best-in-class conversation intelligence and transcription",
            "Automatic risk and sentiment detection from calls",
            "Strong search across all recorded conversations",
            "Coaching features help CS managers develop their teams",
            "Integration with major CRM and CS platforms",
            "High user satisfaction scores",
        ],
        "cons": [
            "Not a CS platform (supplements, does not replace)",
            "Expensive per-user pricing",
            "Requires consistent call recording to be valuable",
            "Privacy concerns with call recording in some regions",
            "AI insights require volume to be accurate",
        ],
        "body": """<h2>Why CS Teams Use Gong</h2>
<p>Gong appears in {mentions} CS job postings, making it the most mentioned revenue intelligence tool for CS teams. The platform records and analyzes customer calls, giving CS managers visibility into what is actually happening in customer conversations. This is different from what CRM data shows, which is what CSMs say is happening.</p>

<h2>CS-Specific Use Cases</h2>
<p>CS teams use Gong differently than sales teams. Key CS use cases include:</p>
<ul>
    <li><strong>Risk detection.</strong> Gong's AI flags calls where customer sentiment drops, escalation language appears, or competitors are mentioned. These signals feed into health scoring and early warning systems.</li>
    <li><strong>QBR analysis.</strong> Recording and analyzing QBRs reveals patterns in what separates successful renewals from churned accounts.</li>
    <li><strong>Onboarding quality.</strong> Reviewing onboarding calls helps CS managers standardize the experience and identify where new customers get confused.</li>
    <li><strong>Coaching.</strong> CS managers use Gong to listen to calls and provide specific, actionable coaching to CSMs based on real interactions.</li>
</ul>

<h2>Gong + CS Platform Integration</h2>
<p>The highest-value setup pairs Gong with a CS platform like Gainsight or Vitally. Gong provides conversation-level signals; the CS platform provides account-level health scores and automation. Together, you get both quantitative data (product usage, support tickets) and qualitative data (call sentiment, customer language) feeding your CS operations.</p>

<h2>Is Gong Worth It for CS?</h2>
<p>If your CS team runs regular customer calls (weekly check-ins, QBRs, onboarding sessions), Gong pays for itself in reduced churn risk and improved coaching. If your CS model is mostly digital-touch with minimal live calls, the ROI is lower. The per-user pricing means you need to be selective about which CS team members need licenses.</p>""",
    },
    "Pendo": {
        "slug": "pendo",
        "mentions": 4,
        "category": "digital-adoption",
        "founded": "2013",
        "hq": "Raleigh, NC",
        "pricing": "Free tier for basic analytics; paid plans from $2,000/month",
        "best_for": "CS and product teams wanting combined analytics and in-app guidance",
        "website": "https://www.pendo.io",
        "rating": {"value": 4.4, "count": 1100},
        "description": "Product analytics and digital adoption platform. Combines usage tracking, in-app guides, and feedback collection. Used by both CS and product teams.",
        "pros": [
            "Combined analytics and in-app guidance in one platform",
            "Free tier for basic product analytics",
            "Strong feature adoption tracking",
            "NPS and in-app survey capabilities",
            "No-code guide creation",
            "Good integration with CS platforms",
        ],
        "cons": [
            "Not a CS platform (analytics and guidance only)",
            "Paid plans can be expensive for full features",
            "Guide creation has a learning curve",
            "Analytics depth varies by implementation quality",
            "Can overlap with other tools in the CS tech stack",
        ],
        "body": """<h2>How CS Teams Use Pendo</h2>
<p>Pendo sits at the intersection of product analytics and digital adoption. CS teams use it for two primary purposes: understanding how customers use the product, and driving adoption through in-app guidance. With {mentions} mentions in CS job postings (plus additional mentions as Pendo PLG), the tool has a steady presence in CS tech stacks.</p>

<h2>Product Analytics for CS</h2>
<p>CS teams use Pendo's analytics to answer critical questions: Which features are customers using? Where do users drop off? Which accounts have declining engagement? This data feeds directly into health scoring. A CS platform like Gainsight can ingest Pendo data and use it to calculate health scores that reflect actual product adoption, not just self-reported usage.</p>

<h2>In-App Guides for Adoption</h2>
<p>Pendo's guide builder lets CS teams create onboarding tours, feature announcements, and contextual help without writing code. This is powerful for CS teams that want to drive adoption at scale. Instead of scheduling a call to walk every customer through a new feature, you create a guide that appears in-app for the right users at the right time.</p>

<h2>Pendo in the CS Tech Stack</h2>
<p>Pendo complements CS platforms rather than replacing them. The typical stack is: CRM (Salesforce/HubSpot) + CS Platform (Gainsight/Vitally) + Product Analytics (Pendo). CS teams that skip dedicated product analytics often struggle to build data-driven health scores because they lack reliable usage data. Pendo fills that gap.</p>""",
    },
    "Userpilot": {
        "slug": "userpilot",
        "mentions": 2,
        "category": "digital-adoption",
        "founded": "2019",
        "hq": "Remote",
        "pricing": "From $249/month for Starter plan",
        "best_for": "Growth-stage SaaS companies wanting affordable digital adoption",
        "website": "https://www.userpilot.com",
        "rating": {"value": 4.5, "count": 200},
        "description": "Product adoption platform with in-app experiences, analytics, and user feedback. More affordable alternative to Pendo and WalkMe.",
        "pros": [
            "Affordable entry point compared to Pendo and WalkMe",
            "No-code experience builder",
            "Built-in NPS and micro-surveys",
            "Feature tagging for adoption analytics",
            "Good for self-serve onboarding flows",
        ],
        "cons": [
            "Less analytics depth than Pendo",
            "Smaller market presence and ecosystem",
            "Enterprise features still maturing",
            "Fewer integrations than established competitors",
            "Guide customization has limits compared to WalkMe",
        ],
        "body": """<h2>Userpilot as a CS Tool</h2>
<p>Userpilot is a newer entrant in the digital adoption space, and it is gaining traction among CS teams at growth-stage SaaS companies. With {mentions} mentions in CS job postings, it is still building market presence, but the product addresses real CS needs at a fraction of Pendo or WalkMe pricing.</p>

<h2>Why CS Teams Choose Userpilot</h2>
<p>Three reasons drive Userpilot adoption on CS teams. First, it is significantly cheaper than Pendo or WalkMe, starting at $249/month. Second, the no-code builder lets CSMs create onboarding flows without engineering help. Third, the built-in NPS surveys mean one less tool in the stack.</p>
<p>For early-stage CS teams that want in-app guidance and basic product analytics without a $2,000+/month commitment, Userpilot is a practical choice. You sacrifice some analytics depth, but you gain speed and affordability.</p>

<h2>Userpilot vs Pendo</h2>
<p>Pendo wins on analytics depth and enterprise features. Userpilot wins on price and simplicity. If your primary need is building onboarding flows and tracking feature adoption, Userpilot covers 80% of what Pendo does at 15-20% of the cost. If you need deep product analytics, cohort analysis, and enterprise-grade reporting, Pendo is the better investment.</p>""",
    },
    # --- Onboarding Tools ---
    "GuideCX": {
        "slug": "guidecx",
        "mentions": 3,
        "category": "onboarding",
        "founded": "2017",
        "hq": "Lehi, Utah",
        "pricing": "Custom pricing, typically $50-100/user/month",
        "best_for": "B2B companies with complex, multi-stakeholder onboarding processes",
        "website": "https://www.guidecx.com",
        "rating": {"value": 4.6, "count": 120},
        "description": "Project-based customer onboarding platform that gives both internal teams and customers visibility into implementation progress. Built around the idea that onboarding is a project, not a workflow.",
        "pros": [
            "Customer-facing project portal increases transparency",
            "Template library speeds up repeatable onboarding playbooks",
            "Built-in task assignment across internal and external stakeholders",
            "Time-to-value tracking tied to project milestones",
            "Strong Salesforce and HubSpot integrations for handoff data",
        ],
        "cons": [
            "Limited post-onboarding CS features, so you need another platform after go-live",
            "Reporting is functional but not deeply customizable",
            "Pricing is opaque and requires a sales conversation",
            "Smaller ecosystem and community than general CS platforms",
            "Mobile experience lags behind the desktop product",
        ],
        "body": """<h2>GuideCX as a CS Tool</h2>
<p>GuideCX appears in {mentions} of {total_jobs} CS job postings, which reflects its niche positioning. It is not a full CS platform. It is a purpose-built onboarding project management tool. CS teams that run complex implementations with multiple stakeholders, timelines, and dependencies are the core audience.</p>

<h2>What GuideCX Does Well</h2>
<p>The standout feature is the customer-facing project portal. Instead of sending spreadsheets or status update emails, you give the customer a login where they can see exactly where their onboarding stands, what tasks are pending on their side, and when the next milestone is expected. This alone reduces "where are we?" emails by 60-70% according to GuideCX case studies.</p>
<p>Template management is the second major advantage. If you onboard 50+ customers per quarter with a similar process, GuideCX lets you templatize the entire project plan and spin up new instances in minutes. Each template can have conditional logic, so enterprise customers get extra steps that SMB customers skip.</p>

<h2>Who Should Use GuideCX</h2>
<p>GuideCX fits B2B SaaS companies where onboarding takes 30+ days and involves 3+ stakeholders on the customer side. If your onboarding is a quick setup wizard, GuideCX is overkill. If your onboarding requires data migration, integrations, training sessions, and user provisioning across departments, GuideCX replaces the messy combination of spreadsheets, Asana boards, and email threads that most teams use.</p>

<h2>GuideCX Pricing</h2>
<p>GuideCX does not publish pricing. Based on market data, expect $50-100 per user per month depending on volume and feature tier. There is a free trial available. The ROI case is straightforward: if GuideCX saves your onboarding team 5 hours per customer and you onboard 20 customers per month, the math works quickly.</p>""",
    },
    "Rocketlane": {
        "slug": "rocketlane",
        "mentions": 2,
        "category": "onboarding",
        "founded": "2020",
        "hq": "San Francisco, California",
        "pricing": "Starts at $19/user/month, Professional tier at $49/user/month",
        "best_for": "Professional services and onboarding teams that need project management, document collaboration, and time tracking in one tool",
        "website": "https://www.rocketlane.com",
        "rating": {"value": 4.7, "count": 175},
        "description": "Customer onboarding and professional services automation platform that combines project management, document collaboration, and customer portals into a single workspace.",
        "pros": [
            "Combines project management, docs, and customer portal in one tool",
            "Published, transparent pricing starting at $19/user/month",
            "Built-in time tracking for services teams billing by hour",
            "Strong templatization with cross-project analytics",
            "Modern UI that customers actually enjoy using",
        ],
        "cons": [
            "Newer company with a smaller customer base than GuideCX",
            "Resource management features are still maturing",
            "Limited native integrations outside of CRM basics",
            "Reporting is improving but not yet enterprise-grade",
            "Some advanced features require the highest pricing tier",
        ],
        "body": """<h2>Rocketlane as a CS Tool</h2>
<p>Rocketlane shows up in {mentions} of {total_jobs} CS job postings. Founded in 2020, it is the newest entrant in the onboarding platform category, but it has gained traction fast. The product targets the overlap between professional services teams and CS onboarding teams, which is a gap that older tools miss.</p>

<h2>What Sets Rocketlane Apart</h2>
<p>Rocketlane's core differentiator is combining three tools into one: project management (like Asana), document collaboration (like Notion), and a customer portal (like GuideCX). For teams that previously juggled Asana for tasks, Google Docs for SOWs, and email for customer updates, Rocketlane consolidates everything.</p>
<p>The built-in time tracking is a specific advantage for services teams that bill hours. You can track time against project phases, generate utilization reports, and tie billable hours back to specific customers. No other onboarding platform does this natively.</p>

<h2>Who Should Use Rocketlane</h2>
<p>Rocketlane is ideal for SaaS companies where the onboarding team also functions as a professional services team. If you have implementation consultants who run onboarding projects, collaborate on configuration documents, and need to track time, Rocketlane replaces 3 tools at once. If your onboarding is purely CSM-led without a services component, GuideCX or even a standard project tool might be a simpler fit.</p>

<h2>Rocketlane Pricing</h2>
<p>Rocketlane publishes its pricing, which is refreshing in this space. The Essential plan starts at $19/user/month and covers basic project management and customer portals. The Professional plan at $49/user/month adds time tracking, resource management, and advanced automations. Enterprise pricing is custom. Compared to GuideCX, Rocketlane is generally 20-40% cheaper at similar feature levels.</p>""",
    },
    "OnRamp": {
        "slug": "onramp",
        "mentions": 1,
        "category": "onboarding",
        "founded": "2022",
        "hq": "New York, New York",
        "pricing": "Custom pricing, early-stage startup",
        "best_for": "B2B SaaS companies that want customers to self-serve through onboarding steps",
        "website": "https://www.onramp.us",
        "rating": {"value": 4.5, "count": 30},
        "description": "Self-serve customer onboarding portal that lets B2B SaaS companies build guided, step-by-step onboarding experiences customers complete on their own timeline.",
        "pros": [
            "Purpose-built for self-serve onboarding, not adapted from project management",
            "Customers complete onboarding steps independently, reducing CSM time",
            "Embeddable portal can live inside your product",
            "Dynamic flows that adapt based on customer inputs",
            "Clean, modern UX that feels native to SaaS products",
        ],
        "cons": [
            "Very early-stage company with a small customer base",
            "Feature set is narrower than GuideCX or Rocketlane",
            "Limited integrations and ecosystem",
            "Not suited for complex, multi-stakeholder implementations",
            "Pricing and long-term viability carry startup risk",
        ],
        "body": """<h2>OnRamp as a CS Tool</h2>
<p>OnRamp appears in {mentions} of {total_jobs} CS job postings, which is expected for a startup founded in 2022. It occupies a specific niche: self-serve onboarding portals for B2B SaaS. While GuideCX and Rocketlane treat onboarding as a managed project, OnRamp treats it as a guided experience the customer drives themselves.</p>

<h2>The Self-Serve Onboarding Bet</h2>
<p>OnRamp's thesis is that many B2B onboarding steps do not require a human. Connecting integrations, uploading data files, configuring settings, watching training videos, and completing setup checklists can all be done by the customer if you give them a clear, guided experience. OnRamp provides that experience as an embeddable portal.</p>
<p>For CS teams drowning in low-touch onboarding tasks, this is compelling. If 40% of your onboarding steps are administrative tasks you walk customers through on Zoom calls, OnRamp can automate those away and free your CSMs for higher-value conversations.</p>

<h2>Who Should Use OnRamp</h2>
<p>OnRamp fits product-led growth SaaS companies with a large volume of new customers and a relatively standardized onboarding process. If you onboard 100+ customers per month and most of them follow the same 10-15 setup steps, OnRamp scales that without adding headcount. If your onboarding requires heavy customization, consulting, or multi-stakeholder coordination, the managed project approach of GuideCX or Rocketlane is a better fit.</p>

<h2>OnRamp Pricing</h2>
<p>OnRamp does not publish pricing publicly. As an early-stage startup, expect flexibility in negotiations. The value proposition is headcount savings: if OnRamp reduces your onboarding team's per-customer time by 3 hours and you onboard 50 customers per month, that is 150 hours saved, roughly equivalent to a full-time employee.</p>""",
    },
    "Arrows": {
        "slug": "arrows",
        "mentions": 2,
        "category": "onboarding",
        "founded": "2020",
        "hq": "Remote (US-based)",
        "pricing": "Starts at $500/month, scales with HubSpot deal volume",
        "best_for": "HubSpot-native teams that want onboarding plans tied directly to CRM deals",
        "website": "https://www.arrows.to",
        "rating": {"value": 4.8, "count": 65},
        "description": "HubSpot-native onboarding and sales room tool that creates collaborative action plans synced bidirectionally with HubSpot deals, tickets, and contacts.",
        "pros": [
            "Deep, bidirectional HubSpot integration that competitors cannot match",
            "Onboarding task completion syncs directly to HubSpot deal properties",
            "Clean customer-facing plans that feel modern and collaborative",
            "Sales rooms for pre-close buyer enablement, not just post-sale",
            "Small team that ships fast and responds to customer feedback",
        ],
        "cons": [
            "Only works with HubSpot. Salesforce teams cannot use it.",
            "Smaller company with limited brand recognition",
            "Feature set is narrower than full onboarding platforms",
            "Reporting relies heavily on HubSpot's native reporting",
            "Pricing at $500/month starting point is steep for small teams",
        ],
        "body": """<h2>Arrows as a CS Tool</h2>
<p>Arrows appears in {mentions} of {total_jobs} CS job postings. Its market position is specific: it is the best onboarding tool for HubSpot-native teams. If your CRM is HubSpot and you want onboarding plans that sync directly to deals, Arrows is the only purpose-built option.</p>

<h2>The HubSpot Integration Advantage</h2>
<p>Arrows is not just "integrated with HubSpot." It is built on HubSpot. When a customer completes an onboarding task in Arrows, the corresponding HubSpot deal property updates in real time. When a deal moves stages in HubSpot, the Arrows plan can trigger new steps. This bidirectional sync means your CRM always reflects the true state of onboarding without manual data entry.</p>
<p>For CS leaders who spend hours reconciling onboarding status between a project tool and their CRM, this alone justifies the price. Your HubSpot dashboards and reports automatically include onboarding progress data.</p>

<h2>Who Should Use Arrows</h2>
<p>The decision tree is simple. Are you on HubSpot? If yes, Arrows deserves a look. If no, it is not an option. Among HubSpot teams, Arrows fits best when you want a lightweight, customer-facing onboarding plan without the complexity of a full project management tool. If you need Gantt charts, resource management, and time tracking, GuideCX or Rocketlane are better choices even for HubSpot teams.</p>

<h2>Arrows Pricing</h2>
<p>Arrows starts at $500/month and scales based on the number of active onboarding plans. There is no per-user pricing, which is a plus for larger teams. The pricing model means Arrows gets expensive if you run a high volume of concurrent onboarding projects. For teams onboarding 10-30 customers per month, the cost is manageable. At 100+ concurrent plans, negotiate a volume discount.</p>""",
    },
    # --- Feedback Tools ---
    "Delighted": {
        "slug": "delighted",
        "mentions": 4,
        "category": "feedback",
        "founded": "2013",
        "hq": "Menlo Park, California",
        "pricing": "Free tier available, Premium starts at $224/month",
        "best_for": "CS teams that need quick, clean NPS/CSAT surveys without a complex setup",
        "website": "https://www.delighted.com",
        "rating": {"value": 4.7, "count": 400},
        "description": "NPS, CSAT, CES, and star rating survey platform acquired by Qualtrics in 2018. Known for simplicity and high response rates across email, web, and SMS channels.",
        "pros": [
            "Extremely fast setup. First survey can go out in under 10 minutes.",
            "Free tier with 1,000 surveys/month covers many startup needs",
            "Multi-channel delivery: email, web intercept, SMS, and link",
            "Qualtrics backing provides stability and ongoing investment",
            "API is well-documented and integrations cover major CS platforms",
        ],
        "cons": [
            "Limited survey customization compared to full survey tools like Typeform",
            "Analytics are basic. Power users outgrow the built-in dashboards.",
            "The Qualtrics acquisition has slowed feature development",
            "No built-in closed-loop workflow for acting on survey responses",
            "Text analytics for open-ended responses are rudimentary",
        ],
        "body": """<h2>Delighted as a CS Tool</h2>
<p>Delighted appears in {mentions} of {total_jobs} CS job postings. It sits in the sweet spot between overly simple survey tools and enterprise-grade VoC platforms. CS teams use it primarily for relationship NPS, post-interaction CSAT, and onboarding CES surveys.</p>

<h2>Why CS Teams Choose Delighted</h2>
<p>Speed and response rates are the two reasons Delighted wins. The platform strips away complexity to focus on one thing: getting survey responses. The email surveys render inline (no click-through required), which pushes response rates to 20-30%, roughly double what most survey tools achieve. Setup takes minutes, not days.</p>
<p>The free tier is genuinely useful. At 1,000 surveys per month with NPS, CSAT, and CES support, many CS teams at startups and SMBs can run their entire feedback program without paying. That makes Delighted an easy recommendation for teams getting started with customer feedback.</p>

<h2>Delighted After the Qualtrics Acquisition</h2>
<p>Qualtrics acquired Delighted in 2018, and the impact has been mixed. On the positive side, Delighted has Qualtrics' resources and is not going anywhere. On the negative side, feature velocity has slowed. Some features that the community has requested for years (conditional logic, multi-question surveys, advanced text analytics) remain limited. If you need those capabilities, look at Qualtrics XM directly or a specialized tool like Medallia.</p>

<h2>Delighted Pricing</h2>
<p>The free plan includes 1,000 surveys/month, 1 user, and basic integrations. The Premium plan at $224/month adds unlimited surveys, multiple users, custom branding, and advanced integrations. Premium Plus at $449/month adds API access and priority support. Compared to Medallia or Qualtrics XM, Delighted is 80-90% cheaper for basic NPS/CSAT programs.</p>""",
    },
    "AskNicely": {
        "slug": "asknicely",
        "mentions": 2,
        "category": "feedback",
        "founded": "2014",
        "hq": "Portland, Oregon",
        "pricing": "Custom pricing, typically $200-500/month depending on volume",
        "best_for": "Service businesses with frontline teams where NPS needs to be operationalized at the branch/location level",
        "website": "https://www.asknicely.com",
        "rating": {"value": 4.5, "count": 180},
        "description": "NPS and customer feedback platform designed to push scores and comments to frontline managers and employees. Built around the idea that feedback only matters if it reaches the people who can act on it.",
        "pros": [
            "Frontline-focused design pushes feedback to individual employees and managers",
            "Mobile app for frontline staff to see their scores in real time",
            "Daily email digests with NPS trends per location/team/employee",
            "Coaching workflows tied to specific customer feedback",
            "Strong in multi-location and franchise business models",
        ],
        "cons": [
            "Less suited for pure SaaS CS teams without frontline roles",
            "Survey capabilities are basic compared to Delighted or Medallia",
            "Analytics and dashboards need improvement",
            "Limited integrations outside CRM and helpdesk basics",
            "Pricing is not published and requires a demo",
        ],
        "body": """<h2>AskNicely as a CS Tool</h2>
<p>AskNicely appears in {mentions} of {total_jobs} CS job postings. Its presence in CS roles is lower than NPS-focused competitors because AskNicely targets a specific use case: operationalizing NPS at the frontline. If your business has customer-facing employees at locations, branches, or service sites, AskNicely was built for you.</p>

<h2>The Frontline Feedback Model</h2>
<p>Most NPS tools collect feedback and put it in a dashboard that leadership reviews monthly. AskNicely flips this. When a customer submits an NPS score, AskNicely routes it immediately to the specific employee or manager associated with that interaction. A property manager sees their NPS in a mobile app. A regional director gets a daily email with scores across their 12 locations.</p>
<p>This model works well for healthcare practices, property management, professional services firms, and franchise operations. It works less well for SaaS companies where "frontline" means a CSM managing 50 accounts from a desk.</p>

<h2>Who Should Use AskNicely</h2>
<p>If your CS model involves frontline employees delivering service at physical locations, AskNicely is worth evaluating. The platform excels when you need to connect individual customer feedback to individual employees and give managers visibility into team performance. For SaaS CS teams that want NPS as a health score input, Delighted or even the NPS features built into Gainsight and ChurnZero are more practical choices.</p>

<h2>AskNicely Pricing</h2>
<p>AskNicely does not publish pricing. Based on market data, expect $200-500/month depending on survey volume and the number of frontline users. The mobile app for frontline staff may add per-user costs. For multi-location businesses with 50+ employees, plan to negotiate an annual contract for better rates.</p>""",
    },
    "Medallia": {
        "slug": "medallia",
        "mentions": 5,
        "category": "feedback",
        "founded": "2001",
        "hq": "San Francisco, California",
        "pricing": "Enterprise pricing only, typically $100K+/year",
        "best_for": "Large enterprises running multi-channel voice-of-customer programs across thousands of touchpoints",
        "website": "https://www.medallia.com",
        "rating": {"value": 4.4, "count": 650},
        "description": "Enterprise experience management platform that captures feedback signals across surveys, social media, call centers, chat, and IoT devices. Acquired by Thoma Bravo in 2021 for $6.4 billion.",
        "pros": [
            "Captures feedback from more channels than any competitor",
            "Text and speech analytics powered by AI process millions of signals",
            "Enterprise-grade permissions, SSO, and data governance",
            "Deep vertical expertise in hospitality, financial services, and healthcare",
            "Real-time alerting on critical customer feedback",
        ],
        "cons": [
            "Pricing starts at six figures annually. Not for SMBs.",
            "Implementation takes 3-6 months and requires dedicated resources",
            "The platform is complex and has a steep learning curve",
            "Overkill for teams that just need NPS and CSAT surveys",
            "Post-acquisition (Thoma Bravo) product direction has raised questions",
        ],
        "body": """<h2>Medallia as a CS Tool</h2>
<p>Medallia appears in {mentions} of {total_jobs} CS job postings. Most mentions come from enterprise CS roles at companies with 1,000+ employees. Medallia is not a tool you evaluate alongside Delighted or AskNicely. It is a platform you evaluate alongside Qualtrics XM when your feedback program spans call centers, retail locations, digital channels, and millions of customer interactions per year.</p>

<h2>What Medallia Does at Scale</h2>
<p>Medallia's strength is signal capture across every customer touchpoint. Surveys are just one input. The platform also ingests call center transcripts, chat logs, social media mentions, app store reviews, and IoT sensor data. Its AI processes these signals to identify themes, detect emerging issues, and predict churn risk at scale.</p>
<p>For a hotel chain with 500 properties, Medallia can track guest feedback from post-stay surveys, in-app reviews, social media, and call center interactions, then surface trends at the property, regional, and corporate level. No other platform matches this breadth.</p>

<h2>Who Should Use Medallia</h2>
<p>Medallia fits companies with 5,000+ employees, multiple customer touchpoints, and a dedicated CX or VoC team. If you have an analyst whose full-time job is managing customer feedback programs, Medallia gives them the most powerful toolset available. If you are a 50-person SaaS startup that wants to send NPS surveys, Medallia is the wrong answer by a factor of 100x.</p>

<h2>Medallia Pricing</h2>
<p>Medallia does not publish pricing. Enterprise contracts typically start at $100K/year and can exceed $500K/year for large deployments. Implementation costs add another $50-150K depending on scope. The total cost of ownership makes Medallia a strategic investment, not a tool purchase. Evaluate it alongside Qualtrics XM, not alongside Delighted.</p>""",
    },
    # --- Digital Adoption Tools ---
    "WalkMe": {
        "slug": "walkme",
        "mentions": 8,
        "category": "digital-adoption",
        "founded": "2011",
        "hq": "San Francisco, California",
        "pricing": "Enterprise pricing only, typically $10K-50K+/year",
        "best_for": "Large enterprises driving software adoption across internal tools and customer-facing applications",
        "website": "https://www.walkme.com",
        "rating": {"value": 4.3, "count": 750},
        "description": "Enterprise digital adoption platform that overlays any web application with guided walkthroughs, tooltips, and automations. Went public on NASDAQ in 2021. Acquired by SAP in 2024 for $1.5 billion.",
        "pros": [
            "Works on top of any web application, including third-party tools like Salesforce and Workday",
            "Enterprise-grade analytics showing where users struggle and drop off",
            "Automation features that complete repetitive tasks for users",
            "Largest DAP on the market with the most mature feature set",
            "SAP acquisition provides long-term stability and investment",
        ],
        "cons": [
            "Expensive. Enterprise pricing puts it out of reach for most SMBs.",
            "Implementation is complex and often requires a dedicated WalkMe admin",
            "The builder UI has a steep learning curve compared to Pendo or Appcues",
            "Performance overhead can slow down the host application",
            "Customer-facing use cases are secondary to internal IT adoption",
        ],
        "body": """<h2>WalkMe as a CS Tool</h2>
<p>WalkMe appears in {mentions} of {total_jobs} CS job postings. It is the most established digital adoption platform, but CS teams should understand that WalkMe's primary market is internal IT adoption (helping employees use Salesforce, Workday, ServiceNow), not customer-facing product adoption. CS use cases exist but are secondary.</p>

<h2>WalkMe for Customer Success</h2>
<p>When CS teams use WalkMe, it is typically for customer-facing onboarding walkthroughs and in-app guidance. WalkMe overlays your product with step-by-step guides that walk customers through complex workflows. The analytics show where customers get stuck, which steps they skip, and where they abandon processes.</p>
<p>The automation feature is underappreciated. WalkMe can auto-fill fields, navigate between pages, and complete repetitive steps for users. For products with complex data entry or multi-step configuration processes, this reduces customer frustration significantly.</p>

<h2>WalkMe vs Pendo for CS Teams</h2>
<p>Pendo and WalkMe overlap but serve different primary audiences. Pendo is product-analytics-first with adoption features. WalkMe is adoption-first with analytics as a supporting capability. For CS teams that want product usage data to build health scores and identify at-risk accounts, Pendo is the better choice. For CS teams that want to build complex, multi-step guided experiences across multiple applications, WalkMe has more power.</p>

<h2>WalkMe Pricing</h2>
<p>WalkMe does not publish pricing. Enterprise contracts typically start at $10,000/year for a single application and scale to $50,000+ for multi-application deployments. The SAP acquisition may shift pricing models over time. For CS teams specifically, evaluate whether Pendo at roughly half the cost covers your needs before committing to WalkMe's enterprise pricing.</p>""",
    },
    "Appcues": {
        "slug": "appcues",
        "mentions": 4,
        "category": "digital-adoption",
        "founded": "2013",
        "hq": "Boston, Massachusetts",
        "pricing": "Starts at $249/month, Growth plan at $879/month",
        "best_for": "Product and CS teams at SaaS companies that need no-code in-app experiences without enterprise complexity",
        "website": "https://www.appcues.com",
        "rating": {"value": 4.5, "count": 350},
        "description": "No-code product adoption platform for building in-app onboarding flows, feature announcements, and user surveys. Positioned between Userpilot (cheaper, simpler) and Pendo (more powerful, more expensive).",
        "pros": [
            "No-code builder that non-technical CSMs can use independently",
            "Clean UI with a shorter learning curve than Pendo or WalkMe",
            "Good template library for common onboarding patterns",
            "Solid event tracking and segmentation for targeting experiences",
            "Published pricing with a clear upgrade path",
        ],
        "cons": [
            "Analytics are less deep than Pendo. No retroactive data.",
            "Mobile support is limited compared to Pendo",
            "The $249/month Essentials plan caps at 2,500 monthly active users",
            "Advanced targeting requires the Growth plan at $879/month",
            "No native customer health scoring or CS-specific features",
        ],
        "body": """<h2>Appcues as a CS Tool</h2>
<p>Appcues appears in {mentions} of {total_jobs} CS job postings. It fills a specific gap in the CS tech stack: building in-app onboarding experiences and feature announcements without engineering help. Appcues is not a CS platform, but it is a tool CS teams use frequently to drive product adoption.</p>

<h2>Where Appcues Fits in the CS Stack</h2>
<p>CS teams typically use Appcues for three things. First, onboarding checklists and guided tours that help new users reach their first value milestone. Second, feature announcement modals and tooltips that drive adoption of new capabilities. Third, in-app NPS or micro-surveys triggered by specific user actions. Appcues handles all three without code.</p>
<p>The no-code builder is genuinely easy to use. A CSM can create a 5-step onboarding flow, target it to users who signed up in the last 7 days, and launch it within an hour. With Pendo or WalkMe, the same process typically requires training or admin help.</p>

<h2>Appcues vs Pendo vs Userpilot</h2>
<p>Think of these three as a pricing and power spectrum. Userpilot ($249/month) is the budget option with basic analytics. Appcues ($249-879/month) is the mid-range option with better experience building but limited analytics. Pendo ($2,000+/month) is the premium option with deep analytics, retroactive data, and enterprise features. CS teams with a tight budget start with Userpilot, upgrade to Appcues when they need better targeting and templates, and move to Pendo when product analytics become a strategic priority.</p>

<h2>Appcues Pricing</h2>
<p>Appcues publishes pricing clearly. The Essentials plan at $249/month supports up to 2,500 MAUs with basic flows and targeting. The Growth plan at $879/month adds advanced targeting, A/B testing, and unlimited MAUs. Enterprise is custom. The MAU cap on the Essentials plan is the key constraint. If your product has 10,000 monthly active users, you are immediately on the Growth plan.</p>""",
    },
    # --- Revenue Intelligence Tools ---
    "Clari": {
        "slug": "clari",
        "mentions": 7,
        "category": "revenue-intelligence",
        "founded": "2012",
        "hq": "Sunnyvale, California",
        "pricing": "Custom pricing, typically $50-100/user/month",
        "best_for": "Revenue teams that need forecasting accuracy and pipeline visibility across sales and CS",
        "website": "https://www.clari.com",
        "rating": {"value": 4.5, "count": 500},
        "description": "Revenue operations and forecasting platform that uses AI to analyze pipeline data, forecast revenue, and identify risk across the entire customer lifecycle from acquisition through renewal.",
        "pros": [
            "Forecasting accuracy that measurably outperforms spreadsheet-based methods",
            "Unified view of pipeline across new business, expansion, and renewals",
            "AI-driven risk scoring on deals and renewals",
            "Strong Salesforce integration that pulls data automatically",
            "Revenue cadence features replace manual forecast calls",
        ],
        "cons": [
            "Primarily a sales/revenue tool. CS-specific features are limited.",
            "Requires clean CRM data to function well. Garbage in, garbage out.",
            "Learning curve for CS teams unfamiliar with revenue operations concepts",
            "Pricing is not published and targets mid-market to enterprise",
            "Renewal-specific features lag behind new-business pipeline management",
        ],
        "body": """<h2>Clari as a CS Tool</h2>
<p>Clari appears in {mentions} of {total_jobs} CS job postings. Its presence in CS roles is growing as companies push CS teams to own renewal forecasting and net revenue retention. Clari is fundamentally a revenue operations platform, but CS teams increasingly use it to manage the renewal pipeline the same way sales teams use it to manage new business.</p>

<h2>How CS Teams Use Clari</h2>
<p>The primary CS use case is renewal forecasting. Clari pulls data from Salesforce (or HubSpot), overlays activity data from email and calendar, and uses AI to predict which renewals are on track and which are at risk. Instead of CSMs manually updating renewal probability in a spreadsheet, Clari auto-calculates a confidence score based on engagement patterns.</p>
<p>The second use case is expansion pipeline management. CS teams that own upsell and cross-sell revenue use Clari to track expansion opportunities through a pipeline view identical to what sales uses for new logos. This gives leadership a single platform for all revenue forecasting.</p>

<h2>Who Should Use Clari</h2>
<p>Clari fits CS organizations where the team owns a revenue number. If your CS team is responsible for renewal rates, expansion revenue, and net dollar retention, Clari gives you the forecasting tools to manage that number. If your CS team is focused on adoption and health scoring without direct revenue ownership, a CS platform like Gainsight or ChurnZero is a better investment.</p>

<h2>Clari Pricing</h2>
<p>Clari does not publish pricing. Based on market data, expect $50-100/user/month depending on modules and volume. Most deployments start with the sales team and expand to CS, which means the platform is often already purchased when CS starts using it. If your sales team already has Clari, the marginal cost to add CS users is typically lower than buying a standalone CS tool for renewal forecasting.</p>""",
    },
    "People.ai": {
        "slug": "people-ai",
        "mentions": 3,
        "category": "revenue-intelligence",
        "founded": "2016",
        "hq": "San Francisco, California",
        "pricing": "Custom pricing, enterprise-focused, typically $50-75/user/month",
        "best_for": "Revenue teams that need automatic activity capture and contact mapping without manual CRM entry",
        "website": "https://www.people.ai",
        "rating": {"value": 4.4, "count": 300},
        "description": "Activity intelligence platform that automatically captures email, calendar, and engagement data, maps it to CRM records, and provides AI-driven insights on account engagement and deal health.",
        "pros": [
            "Automatic activity capture eliminates manual CRM logging",
            "Contact and stakeholder mapping builds org charts from email/meeting data",
            "AI scoring identifies which accounts are getting enough attention and which are not",
            "Engagement benchmarks show what good CSM activity looks like across the book",
            "Strong Salesforce integration with native CRM data enrichment",
        ],
        "cons": [
            "Privacy concerns around email and calendar data capture require careful rollout",
            "Primarily designed for sales teams. CS features are an extension.",
            "Requires sufficient email/calendar volume to generate useful insights",
            "Pricing is not published and targets enterprise buyers",
            "Data accuracy depends on clean CRM contact records for matching",
        ],
        "body": """<h2>People.ai as a CS Tool</h2>
<p>People.ai appears in {mentions} of {total_jobs} CS job postings. It is an activity intelligence platform, which means it automatically captures and analyzes how your team engages with customers across email, meetings, and calls. For CS teams, the value proposition is twofold: eliminate manual CRM logging and surface which accounts are getting too little attention.</p>

<h2>Automatic Activity Capture for CS</h2>
<p>The biggest friction point in CS operations is getting CSMs to log activities in the CRM. Most do not, or they log selectively. People.ai eliminates this entirely by syncing email and calendar data to Salesforce automatically. Every email sent, every meeting held, every call made gets matched to the right account and contact record without the CSM doing anything.</p>
<p>This creates a complete activity history that CS leaders can use to answer questions like: How many touchpoints did this churned account receive in the 90 days before renewal? Are my CSMs spending time on the right accounts? Which accounts have gone dark with zero engagement in the last 30 days?</p>

<h2>Stakeholder Mapping</h2>
<p>People.ai builds stakeholder maps by analyzing email and meeting patterns. It identifies which contacts your team engages with, how frequently, and whether key decision-makers are in the loop. For CS teams managing renewals, knowing that your CSM only talks to the end user and has zero engagement with the economic buyer is a critical risk signal that most CS platforms miss.</p>

<h2>People.ai Pricing</h2>
<p>People.ai does not publish pricing. Enterprise contracts typically run $50-75/user/month. Like Clari, People.ai often enters an organization through the sales team first. If your sales team already uses People.ai, extending it to CS adds the activity capture and engagement analytics at marginal cost. Buying People.ai for CS alone is harder to justify unless your team is large enough (20+ CSMs) that the activity visibility creates measurable operational improvements.</p>""",
    },
}

# ---------------------------------------------------------------------------
# Comparisons
# ---------------------------------------------------------------------------

TOOL_COMPARISONS = [
    {
        "slug": "gainsight-vs-churnzero",
        "tool_a": "Gainsight", "tool_b": "ChurnZero",
        "title": "Gainsight vs ChurnZero: CS Platform Comparison",
        "body": """<p>Gainsight and ChurnZero are the two most established dedicated CS platforms. Gainsight dominates enterprise; ChurnZero wins on mid-market value and real-time usage tracking.</p>
<h2>Feature Depth</h2>
<p>Gainsight has the deeper feature set. Health scoring, playbook automation, journey orchestration, community management, and analytics modules give Gainsight capabilities that ChurnZero simply does not match. ChurnZero counters with real-time product usage tracking and in-app messaging that Gainsight lacks natively.</p>
<h2>Implementation and Time to Value</h2>
<p>ChurnZero implements faster (4-8 weeks vs 3-6 months for Gainsight). If speed matters, ChurnZero gets you live sooner. If depth matters, Gainsight's longer implementation delivers more comprehensive tooling.</p>
<h2>Pricing</h2>
<p>ChurnZero is more affordable for teams under 20 CSMs. Gainsight's pricing starts higher and scales with modules. For mid-market teams on a budget, ChurnZero often delivers better ROI. For enterprise teams with budget, Gainsight's depth justifies the premium.</p>
<h2>The Verdict</h2>
<p>Choose Gainsight if you have 15+ CSMs, enterprise accounts, and admin resources to manage a complex platform. Choose ChurnZero if you have 5-15 CSMs, want real-time usage alerts, and need faster time to value at lower cost.</p>""",
        "faq": [
            ("Is Gainsight better than ChurnZero?", "For enterprise CS teams, yes. Gainsight has deeper features and a larger ecosystem. For mid-market teams, ChurnZero offers better value with faster implementation."),
            ("Which is cheaper, Gainsight or ChurnZero?", "ChurnZero is generally cheaper, starting around $1,200/month vs Gainsight's typical $2,500+/month entry point. The gap widens at enterprise scale."),
        ],
    },
    {
        "slug": "gainsight-vs-totango",
        "tool_a": "Gainsight", "tool_b": "Totango",
        "title": "Gainsight vs Totango: CS Platform Comparison",
        "body": """<p>Gainsight and Totango are both veteran CS platforms, but they have diverged significantly. Gainsight pushed upmarket into enterprise; Totango maintained a broader market approach with its free tier and modular design.</p>
<h2>Market Position</h2>
<p>Gainsight has {a_mentions} mentions in CS job postings vs Totango's {b_mentions}. Gainsight is the stronger hiring signal, which matters for your resume. Totango offers a free tier that Gainsight does not, making it accessible for early-stage teams.</p>
<h2>Product Approach</h2>
<p>Gainsight is monolithic: one platform with everything built-in. Totango is modular: SuccessBlocs let you deploy specific CS capabilities without buying the full platform. The modular approach sounds appealing, but in practice, most teams end up needing multiple modules, which narrows the cost advantage.</p>
<h2>User Experience</h2>
<p>Neither platform leads on UX. Both have mature but somewhat dated interfaces compared to Vitally and Planhat. Gainsight has invested more in UI updates recently, but neither feels as modern as the newer generation of CS platforms.</p>
<h2>The Verdict</h2>
<p>If budget is your primary constraint, start with Totango's free tier. If you are building an enterprise CS operation, Gainsight's depth and ecosystem make it the safer bet. If you are evaluating both and have budget flexibility, also look at Vitally and Planhat as modern alternatives to both.</p>""",
        "faq": [
            ("Is Gainsight or Totango better?", "Gainsight has deeper features and a stronger market position. Totango offers a free tier and modular approach. For enterprise CS, Gainsight wins. For budget-conscious teams, Totango is a valid starting point."),
            ("Does Totango have a free version?", "Yes. Totango's Spark tier is free for small teams with basic CS needs. It provides health scoring, customer tracking, and limited automation."),
        ],
    },
    {
        "slug": "gainsight-vs-vitally",
        "tool_a": "Gainsight", "tool_b": "Vitally",
        "title": "Gainsight vs Vitally: CS Platform Comparison",
        "body": """<p>This is the defining comparison in the CS platform market: the established leader vs the modern challenger. Gainsight has depth and ecosystem. Vitally has speed and UX. Your choice depends on your team size, budget, and tolerance for complexity.</p>
<h2>The 90/60 Rule</h2>
<p>Vitally delivers roughly 90% of Gainsight's core functionality at roughly 60% of the cost. For most mid-market CS teams, that math makes Vitally the better choice. The missing 10% is advanced enterprise features: complex multi-product journey orchestration, Horizon Analytics depth, and the breadth of the Gainsight ecosystem.</p>
<h2>Implementation Speed</h2>
<p>This is Vitally's biggest advantage. Where Gainsight takes 3-6 months, Vitally goes live in 2-4 weeks. For CS leaders who need to show platform ROI quickly, this speed difference is decisive.</p>
<h2>Product Analytics</h2>
<p>Vitally includes product analytics natively. Gainsight offers comparable functionality through its PX module, but PX is a separate product with separate pricing. If product usage data is critical to your health scoring model, Vitally's integrated approach is cleaner and more cost-effective.</p>
<h2>Ecosystem and Career Value</h2>
<p>Gainsight's ecosystem is larger. More consultants, more admin talent, more community resources. Gainsight experience on a resume carries more weight in the job market ({a_mentions} mentions vs {b_mentions} for Vitally). If career portability matters to you, Gainsight experience is more transferable.</p>
<h2>The Verdict</h2>
<p>Choose Vitally if you have 5-30 CSMs, want fast implementation, and prioritize product analytics and modern UX. Choose Gainsight if you have 20+ CSMs, complex enterprise requirements, and the admin resources to maximize a deep platform.</p>""",
        "faq": [
            ("Should I switch from Gainsight to Vitally?", "If your team underuses Gainsight's advanced features and struggles with admin overhead, switching to Vitally can reduce cost and complexity. If you fully leverage Gainsight's depth, switching loses more than it gains."),
            ("Is Vitally good for enterprise CS?", "Vitally is growing into enterprise, but Gainsight is still the stronger enterprise option. For companies with 30+ CSMs and complex requirements, Gainsight remains the safer choice."),
        ],
    },
    {
        "slug": "salesforce-vs-hubspot-cs",
        "tool_a": "Salesforce", "tool_b": "HubSpot",
        "title": "Salesforce vs HubSpot for Customer Success",
        "body": """<p>Salesforce and HubSpot are the two dominant CRM platforms, and CS teams must choose one as their system of record. The choice affects your CS tech stack, your integration options, and your team's daily workflows.</p>
<h2>Out-of-Box CS Capabilities</h2>
<p>HubSpot has better native CS capabilities through Service Hub. Ticketing, customer feedback, knowledge base, and basic automation work well for small CS teams. Salesforce requires more customization to serve CS needs, but its customization ceiling is much higher.</p>
<h2>CS Platform Integration</h2>
<p>Salesforce integrates more deeply with dedicated CS platforms. Gainsight's Salesforce integration is the gold standard in the industry. Most CS platforms prioritize Salesforce integration first, HubSpot second. If you plan to layer a CS platform on top, Salesforce gives you more integration options.</p>
<h2>Cost Structure</h2>
<p>HubSpot's free CRM tier makes it accessible for startups. Salesforce starts at $165/user/month for Enterprise edition. For a 5-person CS team, the annual CRM cost alone is $10K+ for Salesforce vs potentially $0 for HubSpot. Add CS-specific features, and HubSpot's Service Hub ($45-$1,200/month) is still cheaper than Salesforce customization.</p>
<h2>Scale and Complexity</h2>
<p>Salesforce wins at scale. Companies with 100+ employees, multiple product lines, complex workflows, and heavy reporting needs almost always outgrow HubSpot. HubSpot is excellent for companies under 100 employees with straightforward CS operations.</p>
<h2>The Verdict</h2>
<p>Choose HubSpot if you are under 100 employees, want simplicity, and plan to use Service Hub for CS. Choose Salesforce if you are building for enterprise scale, need deep CS platform integration, or have complex multi-product customer structures.</p>""",
        "faq": [
            ("Is HubSpot or Salesforce better for CS teams?", f"HubSpot is better for small CS teams (under 10 CSMs) wanting simplicity. Salesforce is better for enterprise CS operations that need deep customization and CS platform integration. Salesforce appears in {TOOL_PROFILES['Salesforce']['mentions']} CS job postings vs {TOOL_PROFILES['HubSpot']['mentions']} for HubSpot."),
            ("Can you do customer success in HubSpot?", "Yes, especially with Service Hub. HubSpot handles ticketing, customer feedback, knowledge base, and basic automation. For complex CS operations, you will eventually need a dedicated CS platform layered on top."),
        ],
    },
    {
        "slug": "gainsight-vs-planhat",
        "tool_a": "Gainsight", "tool_b": "Planhat",
        "title": "Gainsight vs Planhat: CS Platform Comparison",
        "body": """<p>Planhat is the European challenger to Gainsight's global dominance. The comparison matters for CS teams evaluating platforms, especially those with European operations or those seeking a modern alternative to Gainsight's complexity.</p>
<h2>Design Philosophy</h2>
<p>Gainsight was built to be comprehensive: every feature a CS team might need. Planhat was built to be flexible: a clean data model that adapts to your business. These are different design philosophies, and your preference depends on whether you want a platform that prescribes best practices (Gainsight) or one that lets you define your own (Planhat).</p>
<h2>Revenue Intelligence</h2>
<p>Planhat's revenue tracking is arguably best-in-class among CS platforms. ARR tracking, expansion forecasting, and financial reporting are deeply integrated. Gainsight offers revenue features but they are less central to the platform's identity. If NRR is your north star metric, Planhat's financial depth is compelling.</p>
<h2>European Advantage</h2>
<p>For companies with EU operations, Planhat's GDPR-native design and European support are meaningful advantages. Gainsight can serve European companies, but compliance is an add-on rather than a foundation. Data residency requirements increasingly favor European-built platforms.</p>
<h2>Market Presence</h2>
<p>Gainsight has {a_mentions} mentions in CS job postings vs {b_mentions} for Planhat. The career value of Gainsight experience is significantly higher in the US market. In Europe, Planhat experience is increasingly valued and the gap is narrowing.</p>
<h2>The Verdict</h2>
<p>Choose Planhat if you value clean design, flexible data modeling, strong revenue tracking, or have European operations. Choose Gainsight if you need maximum feature depth, the largest ecosystem, and the strongest career signal on your resume.</p>""",
        "faq": [
            ("Is Planhat as good as Gainsight?", "For many use cases, yes. Planhat matches Gainsight on core CS workflows and exceeds it in revenue intelligence and UX. Gainsight still leads on feature depth, ecosystem size, and enterprise complexity handling."),
            ("Is Planhat only for European companies?", "No. Planhat has a growing US presence and serves global companies. Its European origin gives it structural advantages for EU compliance, but the platform works well regardless of geography."),
        ],
    },
    {
        "slug": "churnzero-vs-vitally",
        "tool_a": "ChurnZero", "tool_b": "Vitally",
        "title": "ChurnZero vs Vitally: CS Platform Comparison",
        "body": """<p>ChurnZero and Vitally compete directly for mid-market CS teams. Both position as modern Gainsight alternatives with faster implementation and lower cost. The differences come down to real-time tracking vs product analytics.</p>
<h2>Real-Time vs Analytical</h2>
<p>ChurnZero's strength is real-time product usage tracking with instant alerts. When a key user stops logging in, ChurnZero flags it immediately. Vitally's strength is analytical product data with flexible health score models. Vitally gives you the full picture; ChurnZero gives you the urgent signal. Both are valuable, but they serve different CS workflows.</p>
<h2>In-App Capabilities</h2>
<p>ChurnZero includes in-app messaging and guided walkthroughs. Vitally does not. If your CS team wants to drive adoption through in-app experiences without adding a separate digital adoption tool, ChurnZero has the edge.</p>
<h2>Implementation</h2>
<p>Vitally is faster to implement (2-4 weeks vs 4-8 for ChurnZero). ChurnZero's real-time tracking requires a deeper technical integration that adds setup time. If implementation speed is your priority, Vitally wins.</p>
<h2>The Verdict</h2>
<p>Choose ChurnZero if real-time usage alerts and in-app engagement are your top priorities. Choose Vitally if you want the fastest implementation, best UX, and strong product analytics integration.</p>""",
        "faq": [
            ("Which is better, ChurnZero or Vitally?", "ChurnZero excels at real-time usage tracking and in-app engagement. Vitally excels at UX, implementation speed, and product analytics. Neither is universally better; it depends on your CS model."),
            ("Which is cheaper?", "Both are significantly cheaper than Gainsight. Pricing is comparable between ChurnZero and Vitally for similar team sizes. Get quotes from both."),
        ],
    },
    {
        "slug": "gainsight-vs-catalyst",
        "tool_a": "Gainsight", "tool_b": "Catalyst",
        "title": "Gainsight vs Catalyst: CS Platform Comparison",
        "body": """<p>Catalyst positions itself as the CS platform built by CS practitioners. The comparison with Gainsight comes down to usability vs comprehensiveness.</p>
<h2>Usability</h2>
<p>Catalyst's CRM-like interface means CSMs adopt it with minimal training. Gainsight's depth means more features but a steeper learning curve. If platform adoption is your biggest challenge (and it is for many CS teams), Catalyst's usability is a genuine advantage.</p>
<h2>Feature Depth</h2>
<p>Gainsight wins on feature depth in every category: health scoring, playbook automation, analytics, and journey orchestration. Catalyst covers the core CS workflows well but lacks the advanced capabilities that enterprise teams need.</p>
<h2>Revenue Tracking</h2>
<p>Catalyst has built strong revenue and renewal tracking. This is an area where Catalyst holds its own against Gainsight. If revenue visibility is your primary concern, Catalyst delivers good value.</p>
<h2>Implementation</h2>
<p>Catalyst implements in 4-6 weeks. Gainsight takes 3-6 months. The speed difference matters for CS leaders who need quick wins.</p>
<h2>The Verdict</h2>
<p>Choose Catalyst if usability, fast implementation, and revenue tracking are your priorities. Choose Gainsight if feature depth, ecosystem size, and enterprise complexity handling matter more. Catalyst is the pragmatic choice; Gainsight is the comprehensive choice.</p>""",
        "faq": [
            ("Is Catalyst a good Gainsight alternative?", "Yes, for mid-market teams. Catalyst delivers core CS functionality with better usability and faster implementation. Enterprise teams with complex requirements will find Gainsight more capable."),
            ("How does Catalyst pricing compare to Gainsight?", "Catalyst is more affordable, typically starting around $1,500/month vs Gainsight's $2,500+/month. The gap widens at enterprise scale."),
        ],
    },
    {
        "slug": "pendo-vs-walkme",
        "tool_a": "Pendo", "tool_b": "WalkMe",
        "title": "Pendo vs WalkMe for Customer Success",
        "body": """<p>Pendo and WalkMe are both used by CS teams for digital adoption, but they approach the problem differently. Pendo combines analytics with guidance; WalkMe focuses on guidance complexity.</p>
<h2>Analytics vs Guidance</h2>
<p>Pendo's strength is product analytics with guidance built on top. You see how users behave, then create guides to change that behavior. WalkMe's strength is complex, multi-step guidance for enterprise applications. The analytics are secondary to the walkthrough engine.</p>
<h2>CS Use Cases</h2>
<p>CS teams generally get more value from Pendo because the analytics feed health scoring and adoption tracking. WalkMe is more commonly used for employee-facing digital adoption (training users on internal tools like Salesforce) than customer-facing CS workflows.</p>
<h2>Pricing</h2>
<p>WalkMe is significantly more expensive than Pendo, especially for customer-facing deployments. Pendo's free tier makes it accessible for evaluation. WalkMe's enterprise pricing model can exceed $100K/year for large deployments.</p>
<h2>The Verdict</h2>
<p>For CS teams, Pendo is almost always the better choice. The analytics integration, lower cost, and CS-oriented feature set make it a natural fit. WalkMe is the better choice only for complex enterprise application adoption where multi-step walkthroughs across multiple applications are needed.</p>""",
        "faq": [
            ("Is Pendo or WalkMe better for CS?", "Pendo is better for most CS use cases. It combines product analytics with in-app guidance at a lower price point. WalkMe is better for complex enterprise application adoption."),
            ("What is the difference between Pendo and WalkMe?", "Pendo is analytics-first with guidance. WalkMe is guidance-first with basic analytics. Pendo is more CS-oriented; WalkMe is more IT/training-oriented."),
        ],
    },
]

# ---------------------------------------------------------------------------
# Roundup definitions
# ---------------------------------------------------------------------------

ROUNDUPS = [
    {
        "slug": "best-cs-platforms",
        "title": "Best Customer Success Platforms (2026)",
        "h1": "Best Customer Success Platforms in 2026",
        "description": "Ranked comparison of the top CS platforms: Gainsight, Vitally, ChurnZero, Totango, Planhat, and Catalyst.",
        "tools": ["Gainsight", "Vitally", "ChurnZero", "Totango", "Planhat", "Catalyst"],
        "intro": "The CS platform market has matured significantly. Six platforms dominate the space, each with a distinct value proposition. This guide ranks them based on feature depth, implementation speed, pricing, and real-world CS team feedback.",
        "rankings": [
            ("Gainsight", "Best for Enterprise", "The most comprehensive CS platform. Unmatched feature depth, largest ecosystem, and deepest Salesforce integration. Best for teams with 15+ CSMs and enterprise accounts. Implementation takes 3-6 months. Most expensive option."),
            ("Vitally", "Best for Growth-Stage Teams", "Modern UX, fast implementation (2-4 weeks), and strong product analytics. Delivers 90% of Gainsight's functionality at 60% of the cost. Best for 5-30 CSMs wanting speed and simplicity."),
            ("ChurnZero", "Best for Real-Time Usage Tracking", "Leading real-time product usage alerts and in-app engagement. Strong mid-market value. Implementation in 4-8 weeks. Best for CS teams where product usage patterns directly predict retention."),
            ("Planhat", "Best for Revenue Intelligence", "Clean design, flexible data model, and the best revenue tracking among CS platforms. European origin with GDPR-native design. Growing US market presence. Best for revenue-focused CS teams."),
            ("Catalyst", "Best for Usability", "Built by CS practitioners with a CRM-like interface. Fastest adoption among CS teams. Strong revenue tracking. Best for teams where platform adoption is the primary concern."),
            ("Totango", "Best for Budget-Conscious Teams", "The only major CS platform with a free tier. Modular SuccessBloc approach. Established but UI and product velocity lag newer competitors. Best for early-stage teams with minimal budget."),
        ],
    },
    {
        "slug": "best-onboarding-tools",
        "title": "Best Customer Onboarding Tools (2026)",
        "h1": "Best Customer Onboarding Tools in 2026",
        "description": "Top onboarding platforms for CS teams: GuideCX, Rocketlane, OnRamp, and Arrows. Feature comparison and recommendations.",
        "tools": ["GuideCX", "Rocketlane", "OnRamp", "Arrows"],
        "intro": "Customer onboarding is where CS teams win or lose the relationship. A structured onboarding process reduces time-to-value, improves first-year retention, and sets the foundation for expansion. These four tools specialize in making onboarding repeatable and measurable.",
        "rankings": [
            ("GuideCX", "Best for Complex Implementations", "Purpose-built for project-based customer onboarding. Client-facing project views, task management, and milestone tracking. Best for companies with multi-week implementations that require customer collaboration."),
            ("Rocketlane", "Best for Professional Services Teams", "Combines project management, document collaboration, and client portals. Strong for PS teams that own onboarding. Revenue tracking built-in. Best for companies where onboarding is a billable service."),
            ("OnRamp", "Best for Self-Serve Onboarding", "Customer-facing onboarding portal with guided workflows. Customers complete onboarding steps at their own pace. Best for products with high-volume, self-serve onboarding needs."),
            ("Arrows", "Best for HubSpot Users", "Onboarding tool built specifically for the HubSpot ecosystem. Embeds onboarding plans directly in HubSpot. Best for CS teams already on HubSpot who want onboarding without adding another platform."),
        ],
    },
    {
        "slug": "best-digital-adoption-platforms",
        "title": "Best Digital Adoption Platforms for CS (2026)",
        "h1": "Best Digital Adoption Platforms for CS Teams in 2026",
        "description": "Comparison of DAPs for customer success: Pendo, WalkMe, Appcues, and Userpilot. In-app guidance and adoption tracking.",
        "tools": ["Pendo", "WalkMe", "Appcues", "Userpilot"],
        "intro": "Digital adoption platforms help CS teams drive product usage without scheduling more calls. In-app guides, feature announcements, and onboarding tours scale CS efforts beyond what any team could do manually. These four platforms lead the space for CS use cases.",
        "rankings": [
            ("Pendo", "Best Overall for CS", "Combines product analytics with in-app guidance. CS teams get usage tracking, health score data, and the ability to drive adoption through guides. Free tier available. The most CS-relevant DAP on the market."),
            ("Appcues", "Best for Speed", "No-code experience builder that non-technical CS teams can use immediately. Strong for onboarding flows and feature announcements. Less analytics depth than Pendo but faster to deploy."),
            ("Userpilot", "Best Value", "Most affordable option with solid feature coverage. Built-in NPS, feature tagging, and no-code guides. Best for growth-stage companies that need DAP functionality without Pendo-level pricing."),
            ("WalkMe", "Best for Complex Applications", "Enterprise-grade DAP with the most sophisticated walkthrough builder. Overkill for most CS use cases but unmatched for complex, multi-application workflows. Significantly more expensive than alternatives."),
        ],
    },
    {
        "slug": "best-revenue-intelligence-cs",
        "title": "Best Revenue Intelligence Tools for CS (2026)",
        "h1": "Best Revenue Intelligence Tools for CS Teams in 2026",
        "description": "Revenue intelligence platforms for customer success: Gong, Clari, and People.ai. Conversation intelligence and revenue visibility for CS.",
        "tools": ["Gong", "Clari", "People.ai"],
        "intro": "Revenue intelligence tools give CS teams visibility into what is actually happening in customer relationships. Call recordings, sentiment analysis, and revenue forecasting help CS leaders make data-driven decisions about renewals, expansions, and risk.",
        "rankings": [
            ("Gong", "Best for Conversation Intelligence", "The gold standard for call recording and analysis. CS teams use it for risk detection, QBR analysis, onboarding quality, and coaching. Highest user satisfaction scores in the category. Per-user pricing means selective licensing is key."),
            ("Clari", "Best for Revenue Forecasting", "Revenue operations platform with strong forecasting capabilities. CS teams use it for renewal forecasting and pipeline visibility. Less focused on conversation intelligence than Gong but better at the revenue operations layer."),
            ("People.ai", "Best for Activity Intelligence", "Automatically captures customer interactions across email, calendar, and calls. CS teams use it to understand engagement depth without manual logging. Strongest at quantifying the volume and quality of customer touchpoints."),
        ],
    },
]


# ---------------------------------------------------------------------------
# Page builders
# ---------------------------------------------------------------------------

def _tool_card_html(name, profile=None, mentions=0):
    """Card for a tool in a listing."""
    if profile:
        slug = profile["slug"]
        desc = profile["description"][:120] + "..."
        mention_str = f"{profile['mentions']} job mentions"
        return f'''<a href="/tools/{slug}/" class="related-link-card">
    <strong>{name}</strong><br>
    <span style="font-size:var(--cs-text-sm);color:var(--cs-text-secondary)">{mention_str}</span>
</a>'''
    return f'<span class="related-link-card">{name}</span>'


def build_tools_index(market_data):
    """Tools hub/index page."""
    crumbs = [("Home", "/"), ("Tools", None)]
    bc_schema = get_breadcrumb_schema(crumbs)

    total_jobs = market_data["total_jobs"]

    # Filter relevant tools
    cs_tools = {k: v for k, v in market_data["tools"].items()
                if k not in ["Rust", "Rag", "Aws", "Python", "Azure", "Gcp", "Docker",
                             "Kubernetes", "Javascript", "Bedrock", "Haystack", "Claude",
                             "Anthropic", "Openai", "Gemini", "Cohere", "Prompt Engineering"]}

    tool_rows = ""
    for name, count in sorted(cs_tools.items(), key=lambda x: x[1], reverse=True)[:20]:
        profile = TOOL_PROFILES.get(name) or TOOL_PROFILES.get(name.replace(" ", ""))
        link = f'<a href="/tools/{profile["slug"]}/">{name}</a>' if profile else name
        tool_rows += f'<tr><td>{link}</td><td>{count}</td><td>{count/total_jobs*100:.1f}%</td></tr>\n'

    cat_cards = ""
    for cat_slug, cat in CATEGORIES.items():
        tools_list = ", ".join(cat["tools"][:4])
        cat_cards += f'''<a href="/tools/category/{cat_slug}/" class="related-link-card">
    <strong>{cat["name"]}</strong><br>
    <span style="font-size:var(--cs-text-sm);color:var(--cs-text-secondary)">{tools_list}</span>
</a>\n'''

    faq_pairs = [
        ("What is the most popular CS tool?",
         f"Gainsight is the most mentioned dedicated CS platform in our data ({TOOL_PROFILES['Gainsight']['mentions']} mentions). Salesforce is the most mentioned overall tool ({TOOL_PROFILES['Salesforce']['mentions']} mentions), but it is a CRM, not a CS-specific platform."),
        ("What tools do CS teams use?",
         "Most CS teams use a CRM (Salesforce or HubSpot) as the system of record, a dedicated CS platform (Gainsight, Vitally, or ChurnZero) for health scoring and automation, and supplemental tools for conversation intelligence (Gong) and product analytics (Pendo)."),
        ("Do I need a dedicated CS platform?",
         "Teams under 5 CSMs can often manage in a CRM with manual processes. Once you reach 5-10 CSMs, the lack of automated health scoring and playbook execution becomes a bottleneck. That is when a dedicated CS platform pays for itself."),
    ]

    body = f'''<div class="salary-header">
    <div class="salary-header-inner">
        {breadcrumb_html(crumbs)}
        <p class="salary-eyebrow">Tool Reviews</p>
        <h1>Customer Success Tools and Platform Reviews</h1>
        <p>Practitioner-tested reviews of the tools CS teams use. Data from {total_jobs:,} job postings showing real adoption signals.</p>
    </div>
</div>
<div class="salary-content">

    <h2>Most Mentioned CS Tools in Job Postings</h2>
    <p>Tool mentions in job postings are one of the strongest signals of real adoption. When companies require specific tools in their hiring criteria, those tools are part of the daily workflow. Here are the most mentioned CS-relevant tools in our dataset.</p>
    <table class="data-table">
        <thead><tr><th>Tool</th><th>Mentions</th><th>% of Jobs</th></tr></thead>
        <tbody>{tool_rows}</tbody>
    </table>

    <h2>Browse by Category</h2>
    <div class="related-links-grid">
        {cat_cards}
    </div>

    <h2>Head-to-Head Comparisons</h2>
    <div class="related-links-grid">
        {"".join(f'<a href="/tools/compare/{c["slug"]}/" class="related-link-card">{c["tool_a"]} vs {c["tool_b"]}</a>' for c in TOOL_COMPARISONS)}
    </div>

    <h2>Roundup Guides</h2>
    <div class="related-links-grid">
        {"".join(f'<a href="/tools/roundup/{r["slug"]}/" class="related-link-card">{r["title"]}</a>' for r in ROUNDUPS)}
    </div>

    {source_citation_html()}
    {faq_html(faq_pairs)}
    {newsletter_cta_html("Get weekly CS tool intel and platform updates.")}
</div>'''

    extra_head = bc_schema + get_faq_schema(faq_pairs)
    page = get_page_wrapper(
        title="CS Tool Reviews and Platform Comparisons",
        description="Reviews of Gainsight, Vitally, ChurnZero, Salesforce, HubSpot, Gong, and more. Data-backed CS tool comparisons from 1,261 job postings.",
        canonical_path="/tools/",
        body_content=body,
        active_path="/tools/",
        extra_head=extra_head,
    )
    write_page("tools/index.html", page)
    print("  Built: tools/index.html")


def source_citation_html():
    return '''<div class="source-citation">
    <strong>Data source:</strong> 1,261 customer success job postings analyzed April 2026.
    Tool mention counts reflect explicit requirements in job descriptions. Updated weekly.
</div>'''


def build_category_page(cat_slug, cat, market_data):
    """Build a tool category page."""
    crumbs = [("Home", "/"), ("Tools", "/tools/"), (cat["name"], None)]
    bc_schema = get_breadcrumb_schema(crumbs)

    tool_cards = ""
    for tool_name in cat["tools"]:
        profile = TOOL_PROFILES.get(tool_name)
        if profile:
            tool_cards += f'''<div class="card" style="margin-bottom:var(--cs-space-4)">
    <h3><a href="/tools/{profile["slug"]}/">{tool_name}</a></h3>
    <p>{profile["description"]}</p>
    <p style="font-size:var(--cs-text-sm);color:var(--cs-text-secondary)">{profile["mentions"]} job mentions &middot; {profile["best_for"]}</p>
</div>\n'''
        else:
            mentions = market_data["tools"].get(tool_name, 0) or market_data["tools"].get(tool_name.title(), 0)
            tool_cards += f'''<div class="card" style="margin-bottom:var(--cs-space-4)">
    <h3>{tool_name}</h3>
    <p style="font-size:var(--cs-text-sm);color:var(--cs-text-secondary)">{mentions} job mentions</p>
</div>\n'''

    # Find relevant comparisons
    comp_links = ""
    for comp in TOOL_COMPARISONS:
        if comp["tool_a"] in cat["tools"] or comp["tool_b"] in cat["tools"]:
            comp_links += f'<a href="/tools/compare/{comp["slug"]}/" class="related-link-card">{comp["tool_a"]} vs {comp["tool_b"]}</a>\n'

    faq_pairs = [
        (f"What are the best {cat['name'].lower()}?", f"The leading tools in {cat['name'].lower()} are: {', '.join(cat['tools'][:4])}. Rankings depend on team size, budget, and specific requirements."),
        (f"Do CS teams need {cat['name'].lower()}?", f"{cat['description']}"),
    ]

    body = f'''<div class="salary-header">
    <div class="salary-header-inner">
        {breadcrumb_html(crumbs)}
        <p class="salary-eyebrow">Tool Reviews</p>
        <h1>{cat["name"]}: CS Tool Reviews</h1>
        <p>{cat["description"]}</p>
    </div>
</div>
<div class="salary-content">

    <h2>Tools in This Category</h2>
    {tool_cards}

    {"<h2>Comparisons</h2>" + '<div class="related-links-grid">' + comp_links + "</div>" if comp_links else ""}

    {source_citation_html()}
    {faq_html(faq_pairs)}
    {newsletter_cta_html(f"Get weekly updates on {cat['name'].lower()}.")}
</div>'''

    extra_head = bc_schema + get_faq_schema(faq_pairs)
    page = get_page_wrapper(
        title=f"{cat['name']} Reviews for CS Teams",
        description=f"Reviews of the best {cat['name'].lower()} for customer success: {', '.join(cat['tools'][:4])}. Feature comparison and recommendations.",
        canonical_path=f"/tools/category/{cat_slug}/",
        body_content=body,
        active_path="/tools/",
        extra_head=extra_head,
    )
    write_page(f"tools/category/{cat_slug}/index.html", page)
    print(f"  Built: tools/category/{cat_slug}/index.html")


def build_tool_review(name, profile, market_data):
    """Build an individual tool review page."""
    slug = profile["slug"]
    crumbs = [("Home", "/"), ("Tools", "/tools/"), (name, None)]
    bc_schema = get_breadcrumb_schema(crumbs)

    total_jobs = market_data["total_jobs"]

    # Schema
    tool_schema_data = {
        "name": name,
        "description": profile["description"],
        "category": "BusinessApplication",
        "os": "Web",
        "url": profile.get("website", ""),
        "price_range": profile.get("pricing", "Contact for pricing"),
        "rating": profile.get("rating"),
    }
    tool_schema = get_software_application_schema(tool_schema_data)

    cards = stat_cards_html([
        (str(profile["mentions"]), "Job Mentions"),
        (f"{profile['mentions']/total_jobs*100:.1f}%", "% of CS Jobs"),
        (profile.get("founded", "N/A"), "Founded"),
        (str(profile.get("rating", {}).get("value", "N/A")), "Rating"),
    ])

    pros_html = "\n".join(f"<li>{p}</li>" for p in profile["pros"])
    cons_html = "\n".join(f"<li>{c}</li>" for c in profile["cons"])

    body_content = profile["body"].format(
        mentions=profile["mentions"],
        total_jobs=total_jobs,
    )

    # Related comparisons
    comp_links = ""
    for comp in TOOL_COMPARISONS:
        if name in [comp["tool_a"], comp["tool_b"]]:
            comp_links += f'<a href="/tools/compare/{comp["slug"]}/" class="related-link-card">{comp["tool_a"]} vs {comp["tool_b"]}</a>\n'

    # Related tools in same category
    cat_slug = profile.get("category", "")
    cat_tools = CATEGORIES.get(cat_slug, {}).get("tools", [])
    other_tools = [t for t in cat_tools if t != name and t in TOOL_PROFILES]
    tool_links = "".join(f'<a href="/tools/{TOOL_PROFILES[t]["slug"]}/" class="related-link-card">{t} Review</a>\n' for t in other_tools)

    faq_pairs = [
        (f"How much does {name} cost?", profile.get("pricing", "Contact the vendor for pricing details.")),
        (f"Who should use {name}?", profile.get("best_for", f"{name} is designed for customer success teams.")),
        (f"How many CS teams use {name}?", f"{name} appears in {profile['mentions']} of {total_jobs:,} CS job postings in our dataset, indicating {profile['mentions']/total_jobs*100:.1f}% market penetration in hiring requirements."),
    ]

    body = f'''<div class="salary-header">
    <div class="salary-header-inner">
        {breadcrumb_html(crumbs)}
        <p class="salary-eyebrow">Tool Review</p>
        <h1>{name} Review for Customer Success Teams</h1>
        <p>{profile["description"]}</p>
    </div>
</div>
<div class="salary-content">

    {cards}

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--cs-space-6);margin:var(--cs-space-8) 0">
        <div class="card">
            <h3 style="color:var(--cs-accent)">Pros</h3>
            <ul>{pros_html}</ul>
        </div>
        <div class="card">
            <h3 style="color:#ef4444">Cons</h3>
            <ul>{cons_html}</ul>
        </div>
    </div>

    {body_content}

    <h2>Quick Facts</h2>
    <table class="data-table">
        <tbody>
            <tr><td><strong>Founded</strong></td><td>{profile.get("founded", "N/A")}</td></tr>
            <tr><td><strong>Headquarters</strong></td><td>{profile.get("hq", "N/A")}</td></tr>
            <tr><td><strong>Pricing</strong></td><td>{profile.get("pricing", "Contact vendor")}</td></tr>
            <tr><td><strong>Best For</strong></td><td>{profile.get("best_for", "CS teams")}</td></tr>
            <tr><td><strong>Job Mentions</strong></td><td>{profile["mentions"]} of {total_jobs:,} CS job postings</td></tr>
        </tbody>
    </table>

    {"<h2>Comparisons</h2><div class='related-links-grid'>" + comp_links + "</div>" if comp_links else ""}

    {"<h2>Related Tools</h2><div class='related-links-grid'>" + tool_links + "</div>" if tool_links else ""}

    {source_citation_html()}
    {faq_html(faq_pairs)}
    {newsletter_cta_html(f"Get weekly updates on {name} and CS platform news.")}
</div>'''

    extra_head = bc_schema + tool_schema + get_faq_schema(faq_pairs)
    page = get_page_wrapper(
        title=f"{name} Review: CS Platform Analysis (2026)",
        description=f"{name} review for CS teams. {profile['mentions']} job mentions. {profile['description'][:100]}",
        canonical_path=f"/tools/{slug}/",
        body_content=body,
        active_path="/tools/",
        extra_head=extra_head,
    )
    write_page(f"tools/{slug}/index.html", page)
    print(f"  Built: tools/{slug}/index.html")


def build_comparison_page(comp, market_data):
    """Build a tool comparison page."""
    slug = comp["slug"]
    crumbs = [("Home", "/"), ("Tools", "/tools/"), (f"{comp['tool_a']} vs {comp['tool_b']}", None)]
    bc_schema = get_breadcrumb_schema(crumbs)

    a_profile = TOOL_PROFILES.get(comp["tool_a"], {})
    b_profile = TOOL_PROFILES.get(comp["tool_b"], {})

    a_mentions = a_profile.get("mentions", 0)
    b_mentions = b_profile.get("mentions", 0)

    cards = stat_cards_html([
        (str(a_mentions), f"{comp['tool_a']} Mentions"),
        (str(b_mentions), f"{comp['tool_b']} Mentions"),
    ])

    body_content = comp["body"].format(
        a_mentions=a_mentions,
        b_mentions=b_mentions,
        total_jobs=market_data["total_jobs"],
    ) if "{a_mentions}" in comp["body"] else comp["body"]

    # Quick comparison table
    comparison_table = "<h2>Quick Comparison</h2>\n<table class='data-table'>\n<thead><tr><th></th>"
    comparison_table += f"<th>{comp['tool_a']}</th><th>{comp['tool_b']}</th></tr></thead>\n<tbody>\n"

    if a_profile and b_profile:
        comparison_table += f"<tr><td><strong>Job Mentions</strong></td><td>{a_mentions}</td><td>{b_mentions}</td></tr>\n"
        comparison_table += f"<tr><td><strong>Founded</strong></td><td>{a_profile.get('founded', 'N/A')}</td><td>{b_profile.get('founded', 'N/A')}</td></tr>\n"
        comparison_table += f"<tr><td><strong>Best For</strong></td><td>{a_profile.get('best_for', 'N/A')}</td><td>{b_profile.get('best_for', 'N/A')}</td></tr>\n"
        comparison_table += f"<tr><td><strong>Rating</strong></td><td>{a_profile.get('rating', {}).get('value', 'N/A')}/5</td><td>{b_profile.get('rating', {}).get('value', 'N/A')}/5</td></tr>\n"
        comparison_table += f"<tr><td><strong>Pricing</strong></td><td>{a_profile.get('pricing', 'N/A')}</td><td>{b_profile.get('pricing', 'N/A')}</td></tr>\n"

    comparison_table += "</tbody></table>\n"

    # Links to individual reviews
    review_links = ""
    for tool_name in [comp["tool_a"], comp["tool_b"]]:
        p = TOOL_PROFILES.get(tool_name)
        if p:
            review_links += f'<a href="/tools/{p["slug"]}/" class="related-link-card">{tool_name} Full Review</a>\n'

    body = f'''<div class="salary-header">
    <div class="salary-header-inner">
        {breadcrumb_html(crumbs)}
        <p class="salary-eyebrow">Tool Comparison</p>
        <h1>{comp["title"]}</h1>
    </div>
</div>
<div class="salary-content">

    {cards}
    {comparison_table}
    {body_content}

    <h2>Full Reviews</h2>
    <div class="related-links-grid">{review_links}</div>

    {source_citation_html()}
    {faq_html(comp["faq"])}
    {newsletter_cta_html("Get weekly CS tool comparisons and platform updates.")}
</div>'''

    extra_head = bc_schema + get_faq_schema(comp["faq"])
    page = get_page_wrapper(
        title=comp["title"],
        description=f"{comp['tool_a']} vs {comp['tool_b']} for customer success. Feature comparison, pricing, and recommendations based on {market_data['total_jobs']} job postings.",
        canonical_path=f"/tools/compare/{slug}/",
        body_content=body,
        active_path="/tools/",
        extra_head=extra_head,
    )
    write_page(f"tools/compare/{slug}/index.html", page)
    print(f"  Built: tools/compare/{slug}/index.html")


def build_roundup_page(roundup, market_data):
    """Build a roundup/best-of page."""
    slug = roundup["slug"]
    crumbs = [("Home", "/"), ("Tools", "/tools/"), (roundup["h1"], None)]
    bc_schema = get_breadcrumb_schema(crumbs)

    rankings_html = ""
    for i, (name, badge, desc) in enumerate(roundup["rankings"], 1):
        profile = TOOL_PROFILES.get(name, {})
        link = f'<a href="/tools/{profile["slug"]}/">{name}</a>' if profile else name
        mentions = profile.get("mentions", 0)
        rankings_html += f'''<div class="card" style="margin-bottom:var(--cs-space-4)">
    <div style="display:flex;align-items:center;gap:var(--cs-space-3);margin-bottom:var(--cs-space-2)">
        <span style="font-family:var(--cs-font-heading);font-size:var(--cs-text-2xl);font-weight:var(--cs-weight-bold);color:var(--cs-accent)">#{i}</span>
        <div>
            <h3 style="margin-bottom:0">{link}</h3>
            <span style="font-size:var(--cs-text-sm);color:var(--cs-accent);font-weight:var(--cs-weight-semibold)">{badge}</span>
        </div>
    </div>
    <p>{desc}</p>
    {"<p style='font-size:var(--cs-text-sm);color:var(--cs-text-secondary)'>" + str(mentions) + " mentions in CS job postings</p>" if mentions else ""}
</div>\n'''

    faq_pairs = [
        (f"What is the best tool in this category?", f"Based on our analysis, {roundup['rankings'][0][0]} ranks first for {roundup['rankings'][0][1].lower()}. But the best choice depends on your team size, budget, and specific requirements."),
        ("How do you rank these tools?", "Rankings are based on feature depth, implementation speed, pricing, job posting mentions (indicating real-world adoption), and practitioner feedback."),
    ]

    body = f'''<div class="salary-header">
    <div class="salary-header-inner">
        {breadcrumb_html(crumbs)}
        <p class="salary-eyebrow">Roundup</p>
        <h1>{roundup["h1"]}</h1>
        <p>{roundup["description"]}</p>
    </div>
</div>
<div class="salary-content">

    <p>{roundup["intro"]}</p>

    <h2>Rankings</h2>
    {rankings_html}

    <h2>How to Choose</h2>
    <p>The right tool depends on three factors: your team size (determines complexity tolerance), your budget (determines tier), and your primary use case (determines which features matter most). Start with a free trial or demo of the top two options for your profile, and run a 2-week evaluation with your actual workflows before committing.</p>

    {source_citation_html()}
    {faq_html(faq_pairs)}
    {newsletter_cta_html("Get weekly CS tool roundups and platform updates.")}
</div>'''

    extra_head = bc_schema + get_faq_schema(faq_pairs)
    page = get_page_wrapper(
        title=roundup["title"],
        description=roundup["description"],
        canonical_path=f"/tools/roundup/{slug}/",
        body_content=body,
        active_path="/tools/",
        extra_head=extra_head,
    )
    write_page(f"tools/roundup/{slug}/index.html", page)
    print(f"  Built: tools/roundup/{slug}/index.html")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def build_all_tools_pages():
    """Build all tool review pages. Called from build.py."""
    market_data = load_market_data()

    print("\n  Building tool review pages...")
    build_tools_index(market_data)

    for cat_slug, cat in CATEGORIES.items():
        build_category_page(cat_slug, cat, market_data)

    for name, profile in TOOL_PROFILES.items():
        build_tool_review(name, profile, market_data)

    for comp in TOOL_COMPARISONS:
        build_comparison_page(comp, market_data)

    for roundup in ROUNDUPS:
        build_roundup_page(roundup, market_data)

    print(f"  Tools section complete.")
