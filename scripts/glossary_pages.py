# scripts/glossary_pages.py
# Glossary section page generators (45 term pages + index).
# Each term page: 400-600 words, breadcrumb schema, FAQ schema, related terms, newsletter CTA.

import os
import re
import json

from nav_config import *
from templates import (get_page_wrapper, write_page, get_breadcrumb_schema,
                       get_faq_schema, breadcrumb_html, newsletter_cta_html,
                       faq_html)


def slugify(text):
    """Convert term name to URL slug."""
    text = text.lower()
    text = re.sub(r'\(.*?\)', '', text)  # strip parenthetical abbreviations
    text = text.strip()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')


# ---------------------------------------------------------------------------
# Term database
# ---------------------------------------------------------------------------

GLOSSARY_TERMS = [
    {
        "term": "Net Revenue Retention (NRR)",
        "slug": "net-revenue-retention",
        "abbr": "NRR",
        "definition": "Net Revenue Retention measures the percentage of recurring revenue retained from existing customers over a given period, including expansion, contraction, and churn. It is the single most important metric for measuring customer success at the portfolio level.",
        "body": """<p>NRR captures the full revenue picture for your existing customer base. It starts with your beginning-of-period recurring revenue, adds expansion (upsells, cross-sells, price increases), and subtracts contraction (downgrades) and churn (lost customers). An NRR above 100% means your existing customers are growing faster than they are shrinking.</p>

<p>The formula is straightforward: NRR = (Beginning MRR + Expansion - Contraction - Churn) / Beginning MRR x 100. A company with $100K in starting MRR, $15K in expansion, $3K in contraction, and $5K in churn would have an NRR of 107%.</p>

<p>Top-performing SaaS companies target NRR above 120%. For context, Snowflake reported 131% NRR at IPO. Companies below 90% NRR face serious headwinds because their existing base is shrinking, forcing them to acquire new logos just to stay flat.</p>

<h2>Why NRR Matters for CS Teams</h2>
<p>NRR is the metric that connects customer success directly to company valuation. Investors and boards use NRR as a proxy for product-market fit and customer satisfaction. CS leaders who can demonstrate NRR improvement have the strongest case for headcount and budget.</p>

<p>For individual CSMs, understanding NRR helps frame everyday work in business terms. Every successful onboarding, every risk mitigation, every expansion conversation moves NRR. It turns qualitative relationship work into quantifiable revenue impact.</p>

<h2>How to Improve NRR</h2>
<p>Reducing churn is the fastest lever. Even small improvements in retention have outsized effects on NRR because churn compounds. Beyond churn reduction, proactive expansion plays (identifying upsell timing through usage data, running structured QBRs, building multi-threaded relationships) drive the growth side of the equation.</p>

<p>Segmentation matters. High-touch enterprise accounts may have NRR above 130% while SMB segments sit at 85%. Breaking NRR down by segment, cohort, and CSM helps CS leaders allocate resources where they have the most impact.</p>""",
        "faq": [
            ("What is a good Net Revenue Retention rate?", "For B2B SaaS, an NRR above 110% is considered strong. Top-tier companies like Snowflake, Twilio, and Datadog have reported NRR above 120%. Below 90% signals a retention problem that new sales cannot outrun."),
            ("How is NRR different from GRR?", "GRR (Gross Revenue Retention) only measures revenue lost to churn and contraction. It cannot exceed 100%. NRR includes expansion revenue, so it can exceed 100% when upsells and cross-sells outpace losses."),
            ("How often should NRR be calculated?", "Most companies calculate NRR monthly or quarterly. Monthly gives faster signal for operational decisions. Quarterly smooths out noise and is more common for board-level reporting."),
        ],
        "related": ["gross-revenue-retention", "churn-rate", "revenue-churn", "expansion-revenue", "arr-annual-recurring-revenue"],
    },
    {
        "term": "Gross Revenue Retention (GRR)",
        "slug": "gross-revenue-retention",
        "abbr": "GRR",
        "definition": "Gross Revenue Retention measures the percentage of recurring revenue retained from existing customers, excluding any expansion revenue. It isolates your ability to keep the revenue you already have.",
        "body": """<p>GRR answers a simple question: how much of your existing revenue are you keeping? Unlike NRR, GRR strips out expansion. It can never exceed 100%. A GRR of 95% means you lost 5% of your starting revenue to downgrades and cancellations.</p>

<p>The formula: GRR = (Beginning MRR - Contraction - Churn) / Beginning MRR x 100. This isolation makes GRR a purer measure of retention health. A company with high NRR but low GRR is masking a retention problem with expansion, which is unsustainable long-term.</p>

<p>Benchmarks vary by segment. Enterprise SaaS companies typically target GRR above 90%. SMB-focused companies often see GRR in the 75-85% range because of higher logo churn rates in smaller accounts.</p>

<h2>Why GRR Matters for CS Teams</h2>
<p>GRR reveals the foundation beneath your revenue. If GRR is declining, your customer base is eroding regardless of how much expansion revenue you generate. CS leaders use GRR trends to justify investment in retention programs, onboarding improvements, and risk identification systems.</p>

<p>For board conversations, GRR is often more scrutinized than NRR because it is harder to manipulate. You cannot hide behind a few large expansions. GRR reflects the health of the entire book of business.</p>

<h2>Improving GRR</h2>
<p>The primary levers are reducing involuntary churn (failed payments, contract lapses), improving onboarding so customers reach value faster, and identifying at-risk accounts before they downgrade. Health scoring systems, automated alerts on usage drops, and proactive outreach during renewal windows all contribute to GRR improvement.</p>

<p>Tracking GRR by cohort (signup quarter, plan tier, industry) helps CS teams find patterns. If Q1 cohorts consistently have lower GRR than Q3 cohorts, there may be a seasonal onboarding issue worth investigating.</p>""",
        "faq": [
            ("What is a good GRR for SaaS?", "Enterprise SaaS companies target GRR above 90%. Mid-market companies typically see 85-92%. SMB-focused products often land in the 75-85% range. Anything below 70% suggests a fundamental product or market fit problem."),
            ("Can GRR exceed 100%?", "No. GRR excludes expansion revenue by definition. It can only measure how much of your starting revenue you kept. The maximum possible GRR is 100%, meaning zero churn and zero contraction."),
            ("How does GRR relate to customer success compensation?", "Many CS leaders have GRR targets in their compensation plans. CSMs at enterprise companies may have individual book-of-business GRR goals, typically 90%+ for variable compensation payouts."),
        ],
        "related": ["net-revenue-retention", "churn-rate", "revenue-churn", "renewal-rate", "customer-segmentation"],
    },
    {
        "term": "Churn Rate",
        "slug": "churn-rate",
        "definition": "Churn rate measures the percentage of customers or revenue lost during a specific period. It is the core metric that customer success teams exist to reduce.",
        "body": """<p>Churn rate comes in two flavors: logo churn (percentage of customers lost) and revenue churn (percentage of recurring revenue lost). Both matter, but they tell different stories. A company could lose 10% of its logos but only 2% of revenue if the churned accounts were small.</p>

<p>For logo churn: divide the number of customers lost in a period by the number of customers at the start of the period. For revenue churn: divide lost MRR by starting MRR. Monthly and annual calculations are both common, but be careful when annualizing monthly rates because churn compounds.</p>

<p>Benchmarks depend heavily on market segment. Enterprise SaaS companies with annual contracts often see 5-7% annual logo churn. SMB products with monthly billing can see 3-5% monthly churn, which annualizes to 30-45%.</p>

<h2>Types of Churn</h2>
<p>Voluntary churn happens when customers actively decide to leave. Involuntary churn happens due to expired credit cards, billing failures, or administrative oversights. The distinction matters because the solutions are different. Voluntary churn requires product improvement and better CS engagement. Involuntary churn requires dunning flows and payment recovery systems.</p>

<h2>Why CS Teams Own Churn</h2>
<p>Customer success was created specifically to reduce churn. Every activity a CSM performs, from onboarding to QBRs to health monitoring, ultimately ties back to keeping customers. CS leaders report churn metrics to the board more than any other number.</p>

<p>Reducing churn by even a few percentage points has massive impact. A SaaS company doing $10M ARR that reduces annual churn from 15% to 10% retains an extra $500K per year, compounding over time. This is why CS teams are a revenue function, not a cost center.</p>""",
        "faq": [
            ("What is an acceptable churn rate for SaaS?", "For enterprise SaaS, annual churn below 10% is considered healthy. For SMB SaaS, monthly churn below 3% is a common target. The acceptable rate depends on ACV, contract length, and market maturity."),
            ("What is the difference between gross churn and net churn?", "Gross churn counts all lost revenue without considering expansion. Net churn subtracts expansion revenue from losses. A company can have negative net churn (net revenue retention above 100%) while still having meaningful gross churn."),
            ("How do you calculate annual churn from monthly churn?", "Do not simply multiply monthly by 12. The correct formula is: Annual Churn = 1 - (1 - Monthly Churn Rate)^12. A 3% monthly churn rate annualizes to about 31%, not 36%."),
        ],
        "related": ["logo-churn", "revenue-churn", "net-revenue-retention", "gross-revenue-retention", "customer-health-score"],
    },
    {
        "term": "Logo Churn",
        "slug": "logo-churn",
        "definition": "Logo churn measures the percentage of customer accounts (logos) lost during a given period, regardless of the revenue those accounts represented.",
        "body": """<p>Logo churn counts customers, not dollars. If you start the quarter with 200 customers and lose 10, your quarterly logo churn is 5%. This metric matters because it reflects the breadth of your retention problem, even when revenue churn looks manageable.</p>

<p>A common trap is ignoring logo churn when NRR is healthy. A company might lose 20% of its logos annually but maintain 115% NRR because its remaining customers expand. This works until it does not. When expansion slows (and it always does eventually), the logo churn catches up.</p>

<h2>Why Logo Churn Deserves Its Own Metric</h2>
<p>Every lost customer is a lost reference, a lost case study, and a potential detractor. High logo churn also signals product or market fit issues that revenue churn can mask. If small customers churn at 25% annually while enterprise accounts stay, it might indicate a pricing or feature gap at the lower end.</p>

<p>CS teams should track logo churn by segment, plan tier, and cohort. Patterns in logo churn often reveal fixable problems. Maybe customers on monthly plans churn 4x faster than annual contracts. That is an actionable insight for sales and CS to drive annual commitments.</p>

<h2>Reducing Logo Churn</h2>
<p>Focus on the first 90 days. Most logo churn happens when customers fail to reach value during onboarding. Structured onboarding programs, milestone tracking, and early health monitoring catch at-risk accounts before they disengage.</p>

<p>For established accounts, multi-threading (building relationships with multiple stakeholders) reduces the risk of losing an account when a single champion leaves. Executive sponsors and regular business reviews reinforce the partnership beyond one person.</p>""",
        "faq": [
            ("What is the difference between logo churn and revenue churn?", "Logo churn counts the percentage of customer accounts lost. Revenue churn measures the percentage of recurring revenue lost. A company can have high logo churn but low revenue churn if the lost accounts were small."),
            ("What is a good logo churn rate?", "For enterprise SaaS, annual logo churn below 10% is strong. Mid-market companies typically see 10-15%. SMB products with self-serve onboarding often see 20-30% annual logo churn."),
            ("Why track logo churn separately from revenue churn?", "Logo churn reveals retention breadth. A company losing 30% of its logos annually has a systemic problem even if revenue churn is low. Every lost logo also reduces your reference base and market presence."),
        ],
        "related": ["churn-rate", "revenue-churn", "net-revenue-retention", "customer-health-score", "renewal-rate"],
    },
    {
        "term": "Revenue Churn",
        "slug": "revenue-churn",
        "definition": "Revenue churn measures the percentage of recurring revenue lost from existing customers due to cancellations and downgrades over a defined period.",
        "body": """<p>Revenue churn quantifies the dollar impact of lost and contracted accounts. It includes full cancellations and partial downgrades (seat reductions, plan tier decreases). The formula: Revenue Churn = (Lost MRR + Contraction MRR) / Beginning MRR x 100.</p>

<p>Gross revenue churn only counts losses. Net revenue churn factors in expansion, and can go negative when expansion exceeds losses. Both views are useful. Gross revenue churn shows your retention floor. Net revenue churn shows your actual growth trajectory from the existing base.</p>

<h2>Revenue Churn vs. Logo Churn</h2>
<p>These metrics diverge when customer size varies. Losing one $50K/year enterprise account has the same revenue churn impact as losing fifty $1K/year SMB accounts, but very different logo churn. CS teams need both metrics for a complete picture.</p>

<p>Revenue churn is often weighted more heavily in board reporting because it directly impacts ARR and valuation multiples. But logo churn provides earlier warning signals since small account departures often precede larger ones.</p>

<h2>Managing Revenue Churn</h2>
<p>Segment your revenue churn by contraction vs. full cancel. If most revenue churn comes from downgrades rather than cancellations, the root cause is likely over-selling or underutilization. Customers who contracted may be salvageable with better adoption support.</p>

<p>Cohort analysis is essential. Track revenue churn by signup quarter, industry, and initial deal size. If accounts sold during Q4 (when sales teams push hard to hit quotas) have 2x the revenue churn, that points to a sales process issue worth addressing with leadership.</p>

<p>Renewal timing is your biggest lever. Start renewal conversations 90-120 days before contract end. By the time a customer is in month 11 of 12, their decision is often already made. Early engagement gives CS teams time to address concerns and demonstrate value.</p>""",
        "faq": [
            ("How is revenue churn different from logo churn?", "Revenue churn measures dollars lost. Logo churn measures accounts lost. They can tell very different stories. A company might have low revenue churn but high logo churn if it is losing many small accounts while retaining large ones."),
            ("What causes revenue churn?", "The top causes are poor onboarding (customers never reach value), lack of engagement (usage drops over time), champion departure (key contact leaves), competitive displacement, and budget cuts. Each requires a different intervention strategy."),
            ("Can revenue churn be negative?", "Net revenue churn can be negative when expansion revenue from existing customers exceeds losses from churn and contraction. Negative net revenue churn is the gold standard. Gross revenue churn cannot be negative."),
        ],
        "related": ["churn-rate", "logo-churn", "gross-revenue-retention", "net-revenue-retention", "downsell"],
    },
    {
        "term": "Customer Lifetime Value (CLV)",
        "slug": "customer-lifetime-value",
        "abbr": "CLV",
        "definition": "Customer Lifetime Value estimates the total revenue a business can expect from a single customer account over the entire duration of the relationship.",
        "body": """<p>CLV helps CS and finance teams understand how much a customer is worth over time, not just at the point of sale. The simplest formula is: CLV = Average Revenue Per Account x Gross Margin x Average Customer Lifespan. More sophisticated models factor in expansion rates, discount rates, and segment-specific retention curves.</p>

<p>For a SaaS company with $24K ACV, 80% gross margin, and 4-year average lifespan, the CLV is roughly $76,800. That number shapes how much the company should invest in acquisition (CAC) and retention (CS headcount, tools, programs).</p>

<h2>CLV and Customer Success ROI</h2>
<p>CLV is the strongest argument for CS investment. If a CSM managing 30 accounts prevents just two from churning annually, and each account has a $76K CLV, that CSM preserves $152K in lifetime value. Against a $120K fully-loaded CSM cost, the ROI is clear.</p>

<p>CS leaders use CLV to justify expansion of their teams, investment in CS platforms, and development of scaled programs. The gap between current CLV and potential CLV (if churn were reduced or expansion increased) quantifies the opportunity for CS improvement.</p>

<h2>Improving CLV</h2>
<p>There are three levers: increase revenue per account (expansion), extend customer lifespan (reduce churn), and improve margins (reduce cost-to-serve). CS teams primarily influence the first two. Successful onboarding extends lifespan. Proactive QBRs surface expansion opportunities. Health scoring identifies at-risk accounts before they churn.</p>

<p>CLV should be tracked by segment. Enterprise CLV might be 10x SMB CLV, which justifies the higher cost-to-serve. If SMB CLV does not support the cost of even tech-touch engagement, it may signal a pricing or packaging problem.</p>""",
        "faq": [
            ("How do you calculate Customer Lifetime Value?", "The basic formula is CLV = Average Revenue Per Account x Gross Margin x Average Customer Lifespan. More advanced models use cohort retention curves and discount rates to account for the time value of money."),
            ("What is a good CLV to CAC ratio?", "A CLV:CAC ratio of 3:1 or higher is generally considered healthy for SaaS companies. Below 3:1, the business may be spending too much to acquire customers relative to their lifetime value."),
            ("How does customer success impact CLV?", "CS teams improve CLV by reducing churn (extending lifespan), driving expansion revenue (increasing revenue per account), and enabling efficient scaled engagement (improving margins on lower-tier segments)."),
        ],
        "related": ["churn-rate", "net-revenue-retention", "expansion-revenue", "customer-segmentation", "renewal-rate"],
    },
    {
        "term": "Customer Health Score",
        "slug": "customer-health-score",
        "definition": "A customer health score is a composite metric that aggregates multiple signals to predict the likelihood of a customer renewing, expanding, or churning.",
        "body": """<p>Health scores combine quantitative data (product usage, support tickets, payment history) with qualitative signals (relationship strength, executive engagement, NPS responses) into a single score or color-coded status. Most CS platforms support health scoring as a core feature.</p>

<p>A typical health score model weights inputs like: product login frequency (20%), feature adoption breadth (20%), support ticket volume and sentiment (15%), NPS/CSAT responses (15%), executive sponsor engagement (15%), and contract/payment health (15%). The weights vary by company and are calibrated over time based on actual churn outcomes.</p>

<h2>Building Effective Health Scores</h2>
<p>The biggest mistake in health scoring is relying on too few inputs. A login-only health score misses customers who log in daily but only use one feature. Conversely, a score with 30 inputs becomes impossible to interpret and act on.</p>

<p>Start simple: pick 4-6 inputs that your team believes correlate with retention. Run the model for two quarters and validate against actual renewals. Did red accounts actually churn? Did green accounts actually renew? Adjust weights based on what the data shows.</p>

<h2>Health Scores in Practice</h2>
<p>The value of health scores is not prediction accuracy alone. They create a shared language for the CS team. When everyone understands what "red" means and what playbook to run, the team responds to risk consistently rather than relying on individual judgment.</p>

<p>Health scores also enable resource allocation. CS leaders can ensure that high-touch attention goes to accounts that need it (red or declining yellow) rather than accounts where the CSM has the best personal relationship. Data-driven prioritization is one of the biggest operational wins from a well-built health scoring system.</p>

<p>Avoid the trap of gaming health scores. If CSMs can manually override scores without justification, the system loses its value as an early warning system. Overrides should be logged and reviewed.</p>""",
        "faq": [
            ("What inputs go into a customer health score?", "Common inputs include product usage frequency, feature adoption breadth, support ticket volume, NPS or CSAT scores, executive engagement, payment history, and contract renewal timeline. The specific inputs depend on your product and customer base."),
            ("How accurate are customer health scores?", "A well-calibrated health score predicts churn with 60-75% accuracy. Perfect accuracy is unrealistic because external factors (budget cuts, acquisitions, champion departures) are unpredictable. The goal is actionable signal, not perfect prediction."),
            ("Which CS platforms support health scoring?", "Gainsight, ChurnZero, Vitally, Totango, Planhat, and Catalyst all offer built-in health scoring features. Each has different approaches to weighting, automation, and visualization."),
        ],
        "related": ["churn-rate", "risk-score", "red-account", "net-promoter-score", "customer-segmentation"],
    },
    {
        "term": "Time to Value (TTV)",
        "slug": "time-to-value",
        "abbr": "TTV",
        "definition": "Time to Value measures how long it takes a new customer to realize the first meaningful outcome from your product after signing.",
        "body": """<p>TTV is the clock that starts ticking the moment a deal closes. The faster a customer reaches their "aha moment," the more likely they are to stick around. Research consistently shows that customers who achieve value within the first 30 days have significantly higher retention rates than those who take 90+ days.</p>

<p>Defining "value" is the hard part. It varies by product and customer. For a CS platform, value might mean "first automated playbook triggered." For an analytics tool, it might mean "first report shared with an executive." CS teams need to define these milestones explicitly and track them.</p>

<h2>Why TTV Predicts Retention</h2>
<p>Customers who take too long to see value lose internal momentum. The champion who bought your product faces pressure to justify the investment. If they cannot point to a concrete win within the first quarter, stakeholders start questioning the decision. That is the beginning of churn.</p>

<p>Reducing TTV is one of the highest-ROI activities for CS teams. A structured onboarding program that cuts TTV from 60 days to 30 days can meaningfully reduce first-year churn. It also accelerates expansion because customers who see value quickly are more receptive to adding seats, modules, or use cases.</p>

<h2>Measuring and Reducing TTV</h2>
<p>Track TTV as the number of days from contract start to first value milestone. Segment by customer size, industry, and onboarding model. If enterprise accounts take 3x longer than mid-market, investigate whether enterprise onboarding is appropriately resourced.</p>

<p>Common TTV reduction tactics include pre-built templates, guided setup wizards, integration acceleration, and dedicated onboarding specialists. Some companies offer a "quick win" package that gets the customer to one specific outcome within the first week, then expands from there.</p>""",
        "faq": [
            ("How do you measure Time to Value?", "Define a specific value milestone for your product (first report generated, first workflow automated, first integration live). Measure the number of days from contract signing to that milestone. Track by segment and onboarding model."),
            ("What is a good Time to Value benchmark?", "It depends on product complexity. Simple SaaS tools should target TTV under 7 days. Mid-market products with integrations typically aim for 30 days. Enterprise platforms with complex implementations may target 60-90 days."),
            ("How does TTV relate to churn?", "Customers with shorter TTV are significantly less likely to churn in the first year. The relationship is well-established across SaaS: the faster a customer sees value, the more likely they are to renew and expand."),
        ],
        "related": ["onboarding", "customer-onboarding", "implementation", "go-live", "adoption-rate"],
    },
    {
        "term": "Onboarding",
        "slug": "onboarding",
        "definition": "Onboarding is the structured process of guiding new customers from contract signing through initial setup, training, and first value realization.",
        "body": """<p>Onboarding is the most important phase of the customer lifecycle. It sets the tone for the entire relationship and has the largest impact on long-term retention. A customer who has a smooth, fast onboarding experience is fundamentally different from one who struggled for months to get started.</p>

<p>Effective onboarding programs include clear milestones, defined ownership, and measurable success criteria. The best CS teams break onboarding into phases: kickoff, technical setup, user training, first value milestone, and handoff to ongoing CSM. Each phase has a timeline, responsible party, and completion criteria.</p>

<h2>Onboarding Models</h2>
<p>High-touch onboarding uses a dedicated onboarding specialist or CSM to guide the customer through every step. This is standard for enterprise accounts with high ACV. Mid-market accounts often get a hybrid model: a few live calls plus self-serve resources. SMB and freemium products rely on product-led onboarding with in-app guidance, email sequences, and community resources.</p>

<p>The right model depends on ACV and complexity. Spending $5K to onboard a $500/year customer does not work. But under-investing in onboarding for a $100K/year enterprise account is equally wasteful when it leads to churn.</p>

<h2>Onboarding Metrics</h2>
<p>Track time to first value milestone, onboarding completion rate, and post-onboarding health score. If 40% of customers never complete onboarding, that is a leading indicator of future churn. Compare retention rates between customers who completed onboarding within target and those who did not. The data almost always justifies more investment in onboarding.</p>

<p>Modern onboarding tools like GuideCX, Rocketlane, and Arrows help CS teams manage onboarding projects at scale with task tracking, customer-facing portals, and automated reminders.</p>""",
        "faq": [
            ("What is customer onboarding in SaaS?", "Customer onboarding is the process of helping new customers set up your product, integrate it into their workflows, and achieve their first meaningful outcome. It typically includes kickoff calls, technical configuration, user training, and success milestone tracking."),
            ("How long should onboarding take?", "Onboarding duration depends on product complexity. Simple tools: 1-2 weeks. Mid-market products: 30-45 days. Enterprise platforms: 60-120 days. The goal is reaching first value as quickly as possible without rushing past critical setup steps."),
            ("What is the difference between onboarding and implementation?", "Onboarding covers the full experience from signing through first value. Implementation is the technical subset: data migration, integrations, configuration. Implementation is part of onboarding, but onboarding also includes training, change management, and success planning."),
        ],
        "related": ["customer-onboarding", "time-to-value", "implementation", "go-live", "digital-adoption"],
    },
    {
        "term": "Digital Adoption",
        "slug": "digital-adoption",
        "definition": "Digital adoption is the process of helping users fully utilize a software product's features through in-app guidance, walkthroughs, and contextual education.",
        "body": """<p>Digital adoption goes beyond basic onboarding. While onboarding gets users started, digital adoption ensures they continue discovering and using features over time. The goal is maximizing the percentage of purchased functionality that customers actually use, because feature adoption is one of the strongest predictors of retention.</p>

<p>Digital Adoption Platforms (DAPs) like WalkMe, Pendo, Appcues, and Userpilot sit on top of your product and deliver in-app experiences: guided tours, tooltips, checklists, and contextual help. These tools let CS teams drive adoption without requiring engineering resources for every new onboarding flow.</p>

<h2>Why Digital Adoption Matters for CS</h2>
<p>Customers who use only 20% of your product's features are at high churn risk. They are paying for value they are not receiving, and a simpler (cheaper) competitor can lure them away. Digital adoption programs close that gap by surfacing relevant features at the right moments in the user journey.</p>

<p>For CS teams managing hundreds or thousands of accounts, digital adoption is the primary tool for scaled engagement. Instead of a CSM manually walking each customer through features, in-app guidance does it automatically. This frees CSMs to focus on strategic conversations rather than product training.</p>

<h2>Measuring Digital Adoption</h2>
<p>Track feature adoption rate (percentage of users engaging with key features), DAU/MAU ratio (depth of daily engagement), and adoption by feature tier. If you sell three product modules but 60% of customers only use one, digital adoption programs should target the unused modules.</p>

<p>Connect adoption data to outcomes. Which features, when adopted, correlate with higher renewal rates? That analysis tells you exactly where to focus digital adoption efforts for the biggest retention impact.</p>""",
        "faq": [
            ("What is a Digital Adoption Platform?", "A Digital Adoption Platform (DAP) is software that layers on top of your product to deliver in-app guidance like walkthroughs, tooltips, checklists, and announcements. Popular DAPs include WalkMe, Pendo, Appcues, and Userpilot."),
            ("How does digital adoption relate to customer success?", "Digital adoption drives product usage, which is the strongest predictor of customer retention. CS teams use digital adoption tools to scale engagement, reduce support tickets, and increase feature utilization without requiring 1:1 CSM time."),
            ("What metrics track digital adoption?", "Key metrics include feature adoption rate, DAU/MAU ratio, time to feature discovery, onboarding completion rate, and support ticket volume. The goal is connecting adoption metrics to business outcomes like renewal and expansion."),
        ],
        "related": ["adoption-rate", "feature-adoption", "dau-mau-ratio", "product-led-growth", "onboarding"],
    },
    {
        "term": "Product-Led Growth (PLG)",
        "slug": "product-led-growth",
        "abbr": "PLG",
        "definition": "Product-Led Growth is a go-to-market strategy where the product itself drives acquisition, activation, expansion, and retention, reducing reliance on traditional sales and CS motions.",
        "body": """<p>PLG companies let users try before they buy. Free trials, freemium tiers, and self-serve upgrades replace (or supplement) traditional sales cycles. Companies like Slack, Zoom, Dropbox, and Atlassian built massive businesses this way. Users adopt the product, invite teammates, and eventually convert to paid plans.</p>

<p>For customer success, PLG changes the operating model. Instead of managing a defined book of business from day one, CS teams in PLG companies often engage after users have already adopted the product. The CS role shifts from onboarding and training (which the product handles) to strategic expansion, multi-department rollout, and executive alignment.</p>

<h2>CS in a PLG World</h2>
<p>PLG does not eliminate customer success. It changes what CS does. In PLG companies, CS teams focus on converting high-usage free accounts to paid, expanding paid accounts to enterprise, and ensuring that large accounts have executive sponsorship and governance.</p>

<p>Data becomes central. PLG CS teams rely heavily on product usage data to identify expansion opportunities, detect risk, and prioritize outreach. A user who has invited 50 teammates and uses the product daily is a very different conversation than one who signed up and never returned.</p>

<h2>PLG + CS Hybrid Models</h2>
<p>Most successful PLG companies eventually add CS for their largest accounts. Zoom is self-serve for small teams but has full CS coverage for enterprise deployments. This hybrid model uses PLG for efficient acquisition and CS for strategic retention and expansion.</p>

<p>The CS skills required in PLG are evolving. Data literacy, product analytics interpretation, and scaled engagement design are more important than traditional relationship management. CS professionals who can bridge product and revenue conversations are especially valuable in PLG organizations.</p>""",
        "faq": [
            ("What is Product-Led Growth?", "Product-Led Growth (PLG) is a strategy where the product itself drives user acquisition, activation, and expansion. Users can try the product for free and upgrade on their own, reducing dependence on traditional sales teams."),
            ("Does PLG replace customer success?", "No. PLG changes what CS does, but does not eliminate the need. PLG companies still need CS for enterprise accounts, strategic expansion, and complex deployments. CS in PLG focuses more on data-driven engagement than traditional high-touch relationship management."),
            ("What companies use Product-Led Growth?", "Prominent PLG companies include Slack, Zoom, Dropbox, Atlassian, Figma, Notion, and Canva. Many B2B SaaS companies use a hybrid model with PLG for acquisition and traditional sales/CS for enterprise expansion."),
        ],
        "related": ["digital-adoption", "adoption-rate", "feature-adoption", "tech-touch", "dau-mau-ratio"],
    },
    {
        "term": "Customer Journey",
        "slug": "customer-journey",
        "definition": "The customer journey maps every stage a customer goes through, from initial awareness and purchase through onboarding, adoption, renewal, and expansion.",
        "body": """<p>The customer journey is the complete lifecycle of a customer's relationship with your company. In SaaS, the typical stages are: awareness, evaluation, purchase, onboarding, adoption, value realization, renewal, and expansion. Customer success teams own the post-sale stages, though they increasingly influence pre-sale stages through advocacy and references.</p>

<p>Mapping the customer journey means identifying what happens at each stage, who is involved, what success looks like, and where friction exists. This map becomes the foundation for building CS programs, playbooks, and touchpoint cadences.</p>

<h2>Why Journey Mapping Matters</h2>
<p>Without a journey map, CS teams react to problems rather than preventing them. A mapped journey identifies critical moments (first login, first QBR, renewal window) where proactive engagement has the most impact. It also reveals gaps. If no one contacts the customer between onboarding completion and the first QBR, that is a 60-day gap where risk goes undetected.</p>

<p>Journey maps also align cross-functional teams. Sales, onboarding, CS, support, and product all touch the customer at different stages. A shared journey map ensures clean handoffs and consistent messaging rather than the customer repeating their goals to every new contact.</p>

<h2>Building a CS-Focused Journey Map</h2>
<p>Start with your actual data, not an idealized view. Look at when customers engage, when they disengage, when they submit support tickets, and when they churn. Overlay this with your current touchpoint cadence. The gaps between customer behavior and CS engagement are your biggest opportunities.</p>

<p>Segment your journey maps. Enterprise customers and SMB customers have very different journeys. A one-size-fits-all journey map misses the nuances that matter for each segment. Build separate maps for your top 2-3 segments and design engagement models around each.</p>""",
        "faq": [
            ("What are the stages of the customer journey in SaaS?", "The typical SaaS customer journey includes: awareness, evaluation, purchase, onboarding, adoption, value realization, renewal, and expansion. Some models add advocacy as a final stage where happy customers refer others."),
            ("Who owns the customer journey?", "No single team owns the entire journey. Marketing owns awareness and evaluation. Sales owns purchase. CS owns onboarding through expansion. But CS leaders increasingly take responsibility for the end-to-end journey, coordinating across teams."),
            ("How do you map a customer journey?", "Start with data: when do customers engage, drop off, escalate, and churn? Identify key milestones and decision points. Map current touchpoints against customer needs at each stage. Identify gaps where proactive engagement could prevent problems."),
        ],
        "related": ["touchpoint", "onboarding", "customer-segmentation", "success-plan", "playbook"],
    },
    {
        "term": "Touchpoint",
        "slug": "touchpoint",
        "definition": "A touchpoint is any planned interaction between a CS team and a customer, including emails, calls, QBRs, in-app messages, and automated communications.",
        "body": """<p>Touchpoints are the building blocks of customer engagement. They range from high-effort (in-person executive business reviews) to low-effort (automated usage summary emails). The right mix depends on account value, customer lifecycle stage, and engagement model (high-touch, low-touch, or tech-touch).</p>

<p>Effective CS teams plan touchpoints deliberately rather than relying on ad-hoc outreach. A touchpoint cadence defines what interactions happen, when they happen, and who initiates them. For an enterprise account, a typical cadence might include monthly check-ins, quarterly business reviews, and annual planning sessions, plus event-driven touchpoints triggered by usage changes or support escalations.</p>

<h2>Touchpoint Types</h2>
<p>Proactive touchpoints are initiated by the CS team: check-in calls, QBRs, training sessions, and success plan reviews. Reactive touchpoints respond to customer actions: support tickets, feature requests, or escalations. Automated touchpoints run without human involvement: onboarding emails, usage reports, renewal reminders, and health alerts.</p>

<p>The trend in CS is toward more automated and data-driven touchpoints. Instead of scheduling monthly calls for every account, modern CS teams trigger outreach when data signals warrant it. A usage drop triggers an automated check-in. A power user milestone triggers a congratulations message and expansion conversation.</p>

<h2>Measuring Touchpoint Effectiveness</h2>
<p>Not all touchpoints are equal. Track which touchpoints correlate with positive outcomes (renewal, expansion, improved health score) and which are just activity without impact. If monthly check-in calls show no correlation with retention, replace them with something more valuable.</p>

<p>Customer feedback on touchpoints matters too. If customers consistently reschedule or skip QBRs, the format or frequency may need adjustment. The goal is meaningful engagement, not checkbox activity.</p>""",
        "faq": [
            ("What is a touchpoint in customer success?", "A touchpoint is any planned interaction between your CS team and a customer. Examples include check-in calls, QBRs, onboarding sessions, automated emails, in-app messages, and training workshops."),
            ("How many touchpoints should a CSM have per account?", "It depends on the engagement model. High-touch enterprise accounts may have 4-6 touchpoints per month. Mid-market accounts might have 1-2. Tech-touch accounts rely primarily on automated touchpoints with occasional human outreach for specific triggers."),
            ("What makes a touchpoint effective?", "Effective touchpoints deliver value to the customer, not just activity for the CSM. They should be relevant to the customer's current stage, personalized to their goals, and connected to measurable outcomes like adoption, expansion, or risk reduction."),
        ],
        "related": ["customer-journey", "qbr-quarterly-business-review", "high-touch", "low-touch", "tech-touch"],
    },
    {
        "term": "QBR (Quarterly Business Review)",
        "slug": "qbr-quarterly-business-review",
        "abbr": "QBR",
        "definition": "A Quarterly Business Review is a structured meeting between a CS team and a customer to review outcomes achieved, align on goals, and plan for the next quarter.",
        "body": """<p>QBRs are the highest-value touchpoint in enterprise customer success. Done well, they demonstrate ROI, strengthen executive alignment, and surface expansion opportunities. Done poorly, they become status update meetings that customers skip.</p>

<p>A strong QBR agenda includes: review of outcomes vs. goals set last quarter, product usage and adoption highlights, ROI quantification, upcoming product roadmap relevant to the customer, goals and success criteria for next quarter, and open discussion on risks or opportunities.</p>

<h2>Making QBRs Valuable</h2>
<p>The biggest QBR mistake is making it about you instead of the customer. Presenting 30 slides about your product roadmap is not a QBR. Showing the customer how they saved $200K this quarter, which features drove that savings, and what the next $200K opportunity looks like is a QBR.</p>

<p>Executive attendance matters. A QBR with only the day-to-day admin on the customer side is a status meeting. Getting the VP or C-level sponsor in the room (even quarterly) reinforces the partnership at the decision-making level. It also protects the account when the day-to-day champion leaves.</p>

<h2>QBR Best Practices</h2>
<p>Send the agenda and key metrics 48 hours before the meeting so stakeholders can review and come prepared. Keep the presentation under 20 minutes and leave time for discussion. End with clear next steps and owners. Follow up within 24 hours with a written summary.</p>

<p>For mid-market accounts where full QBRs are not economically justified, consider a lighter-weight version: a quarterly email with usage highlights, ROI metrics, and a standing offer to meet if the customer wants to discuss. This scaled approach maintains the quarterly cadence without the overhead.</p>""",
        "faq": [
            ("What is a QBR in customer success?", "A QBR (Quarterly Business Review) is a structured meeting between a CS team and their customer to review outcomes, measure progress against goals, discuss challenges, and plan for the next quarter. It is the primary executive-level touchpoint in enterprise CS."),
            ("How do you prepare for a QBR?", "Preparation includes pulling usage and adoption data, calculating ROI metrics, reviewing support ticket history, identifying expansion opportunities, and building a concise presentation. Send the agenda to the customer at least 48 hours in advance."),
            ("How often should QBRs happen?", "Quarterly is standard for enterprise accounts. Some high-value accounts get monthly business reviews. Mid-market accounts may get semi-annual reviews or lightweight quarterly email summaries. The frequency should match the account value and complexity."),
        ],
        "related": ["ebr-executive-business-review", "touchpoint", "success-plan", "high-touch", "champion"],
    },
    {
        "term": "EBR (Executive Business Review)",
        "slug": "ebr-executive-business-review",
        "abbr": "EBR",
        "definition": "An Executive Business Review is a strategic meeting focused on executive stakeholders, covering business outcomes, partnership vision, and long-term alignment between vendor and customer.",
        "body": """<p>An EBR is a step above a QBR. While QBRs often involve operational managers and focus on quarter-over-quarter progress, EBRs are designed for VP and C-level stakeholders. They focus on strategic alignment: how is this partnership contributing to the customer's business objectives, and where is it going?</p>

<p>EBRs happen less frequently than QBRs, typically semi-annually or annually. They require more preparation, more senior participation from your side (CS leadership, product leaders, sometimes your own executives), and a more strategic agenda.</p>

<h2>EBR vs. QBR</h2>
<p>QBRs are operational: what did we accomplish, what are we doing next quarter. EBRs are strategic: how does this partnership fit into the customer's 12-month plan, what capabilities do they need that they do not have, and how can we grow together. The audience difference drives the content difference.</p>

<p>Not every account warrants EBRs. Reserve them for strategic accounts (top 10-20% by ARR or strategic importance). Trying to run EBRs for every account dilutes the effort and makes it impossible to deliver the executive-level preparation they require.</p>

<h2>Running an Effective EBR</h2>
<p>Start with the customer's business, not yours. Open with their strategic priorities and show how your partnership maps to those priorities. Use outcome data, not feature lists. Executives care about revenue impact, efficiency gains, and competitive advantage, not how many workflows you automated.</p>

<p>Include a "looking ahead" section that previews how your roadmap aligns with their stated direction. This is not a sales pitch. It is a genuine conversation about mutual investment and shared vision. Done right, EBRs turn customer relationships into partnerships where expansion happens naturally.</p>

<p>Bring your own executives. If you want a VP on the customer side to attend, you need a VP on your side. Executive matching signals that you take the relationship seriously at the highest level.</p>""",
        "faq": [
            ("What is the difference between an EBR and a QBR?", "QBRs are operational reviews (quarterly, with managers, focused on metrics and next-quarter plans). EBRs are strategic reviews (semi-annual or annual, with executives, focused on long-term partnership vision and business outcomes)."),
            ("Who should attend an EBR?", "On the customer side: VP or C-level sponsor, plus the operational champion. On your side: CSM, CS leader, and ideally a product or company executive. The seniority should be matched or slightly elevated on your side."),
            ("How often should EBRs happen?", "Semi-annually or annually for strategic accounts. EBRs require significant preparation and executive time, so they should be reserved for accounts where the investment is justified by ARR and strategic importance."),
        ],
        "related": ["qbr-quarterly-business-review", "champion", "economic-buyer", "stakeholder-mapping", "high-touch"],
    },
    {
        "term": "Expansion Revenue",
        "slug": "expansion-revenue",
        "definition": "Expansion revenue is additional recurring revenue generated from existing customers through upsells, cross-sells, seat additions, and plan upgrades.",
        "body": """<p>Expansion revenue is the growth engine within your existing customer base. It is cheaper to generate than new logo revenue (no acquisition cost) and contributes directly to NRR. For top-performing SaaS companies, expansion revenue can represent 30-40% of total new ARR.</p>

<p>Sources of expansion revenue include: adding seats or users, upgrading to a higher plan tier, purchasing additional modules or products, increasing usage-based billing, and price increases at renewal. Each source requires a different CS strategy.</p>

<h2>CS Role in Expansion</h2>
<p>Expansion is where customer success and sales intersect. In some organizations, CSMs own the entire expansion motion. In others, CSMs identify and qualify opportunities, then hand off to account executives or renewal managers for negotiation and close. The model depends on deal size, CS team maturity, and organizational philosophy.</p>

<p>Regardless of ownership, CSMs are best positioned to identify expansion signals. They see which customers are bumping against seat limits, which are asking about features on higher tiers, and which have new use cases that your product can address. Training CSMs to recognize and surface these signals is one of the highest-impact investments a CS leader can make.</p>

<h2>Driving Expansion Strategically</h2>
<p>Expansion should feel like a natural next step for the customer, not a sales pitch. The best expansion conversations start with demonstrated value: "You have saved $150K with module A. Module B addresses the same problem for your support team. Want to explore it?"</p>

<p>Timing matters. Expansion conversations land best after a clear value milestone, during QBR preparation, or when the customer proactively asks about additional capabilities. Pushing expansion on an account with open support escalations or declining usage is counterproductive.</p>""",
        "faq": [
            ("What counts as expansion revenue?", "Expansion revenue includes any additional recurring revenue from existing customers: seat additions, plan upgrades, new module purchases, usage-based overage, and price increases at renewal. One-time fees (services, setup) are typically excluded."),
            ("How much expansion revenue should come from existing customers?", "Top SaaS companies generate 30-40% of new ARR from expansion. The percentage varies by business model. PLG companies with usage-based pricing often see higher expansion ratios than companies with fixed-seat licensing."),
            ("Should CSMs own expansion revenue?", "It depends on deal size and organizational structure. Many CS teams own expansions under a certain threshold (e.g., under $50K ARR increase) while sales handles larger opportunities. The key is giving CSMs the tools and incentives to surface and qualify expansion opportunities."),
        ],
        "related": ["upsell", "cross-sell", "net-revenue-retention", "arr-annual-recurring-revenue", "renewal-rate"],
    },
    {
        "term": "Upsell",
        "slug": "upsell",
        "definition": "An upsell is a sale of a higher-tier plan, additional modules, or increased capacity to an existing customer, generating expansion revenue within the current account.",
        "body": """<p>Upselling means moving a customer to a more expensive version of what they already have. Upgrading from a Professional plan to Enterprise, adding premium support, or increasing their seat count are all upsells. The key distinction from cross-selling is that upsells deepen usage of the current product rather than adding a different product.</p>

<p>In SaaS, upsells are the most common form of expansion revenue. They have shorter sales cycles than new deals because the customer already knows your product, has an existing contract, and has internal advocates who can support the business case.</p>

<h2>Identifying Upsell Opportunities</h2>
<p>Usage data is the primary signal. Customers who consistently hit plan limits (seat caps, storage limits, API call ceilings) are natural upsell candidates. Feature requests for capabilities available on higher tiers are another strong signal.</p>

<p>Organizational growth is an external signal worth tracking. If a customer's company is hiring aggressively or expanding into new markets, their need for your product likely grows too. CS teams that monitor customer company news can time upsell conversations with these inflection points.</p>

<h2>Upsell Best Practices</h2>
<p>Lead with value, not price. Show the customer what they gain, not what it costs. Quantify the ROI of the upgrade using their own data whenever possible. "You are currently hitting your API limit twice a month, which delays your reporting by 2-3 hours. The Enterprise plan removes that limit for $X/month" is far more compelling than "Would you like to upgrade?"</p>

<p>Timing is critical. The best upsell conversations happen after a value milestone, during a QBR when outcomes are fresh, or when the customer proactively raises a limitation. Avoid upselling during support escalations or when health scores are declining.</p>""",
        "faq": [
            ("What is the difference between upsell and cross-sell?", "An upsell moves a customer to a higher tier or adds more of what they already use (more seats, higher plan). A cross-sell introduces a different product or module that complements their current purchase."),
            ("When is the best time to upsell?", "After a value milestone, during QBR preparation, when usage approaches plan limits, or when the customer proactively asks about additional capabilities. Avoid upselling during escalations or when customer health is declining."),
            ("Who should own upsells in CS?", "It varies by organization. Many CS teams own upsells below a certain ARR threshold. Larger upsells may involve sales or account management. CSMs should always be responsible for identifying and qualifying upsell opportunities, even if they do not close them."),
        ],
        "related": ["cross-sell", "expansion-revenue", "downsell", "renewal-rate", "qbr-quarterly-business-review"],
    },
    {
        "term": "Cross-Sell",
        "slug": "cross-sell",
        "definition": "A cross-sell is a sale of a different product, module, or service to an existing customer, expanding the relationship beyond the original purchase.",
        "body": """<p>Cross-selling introduces customers to products or modules they do not currently use. If a customer bought your CS platform and you sell them your separate survey product, that is a cross-sell. It broadens the relationship and increases switching costs, making the customer more sticky.</p>

<p>Cross-sells are more complex than upsells because the customer may not have evaluated the additional product. They require education, often a separate evaluation process, and sometimes different stakeholders on the customer side. But they are highly valuable because multi-product customers churn at significantly lower rates than single-product customers.</p>

<h2>Cross-Sell in Practice</h2>
<p>CSMs identify cross-sell opportunities by understanding the customer's broader pain points. During QBRs and check-ins, questions like "What other challenges is your team facing?" and "How are you handling X today?" can surface problems that your other products solve.</p>

<p>Product usage data also reveals opportunities. If a customer is exporting data from your platform to feed into a competitor's analytics tool, and you offer analytics, that is a clear cross-sell opportunity. The data integration pain alone can justify consolidation.</p>

<h2>Making Cross-Sells Successful</h2>
<p>Cross-sells require their own onboarding and success planning. Do not assume that a customer who is successful with Product A will automatically succeed with Product B. Treat each cross-sell as a new relationship that needs the same attention to time-to-value and adoption that the original purchase received.</p>

<p>Multi-product customers have higher CLV and lower churn, but only if they succeed with each product. A cross-sell that fails (customer buys Product B but never adopts it) can actually damage the relationship and put the original Product A renewal at risk.</p>""",
        "faq": [
            ("What is the difference between cross-sell and upsell?", "A cross-sell introduces a different product or module to an existing customer. An upsell increases the customer's investment in their current product through plan upgrades or additional seats."),
            ("Why do multi-product customers churn less?", "Multi-product customers have deeper integration into your ecosystem, more stakeholders involved, and higher switching costs. They also receive more value, which strengthens the business case for continued investment."),
            ("How do CSMs identify cross-sell opportunities?", "Through QBR discussions about broader challenges, observation of workaround behaviors (exporting data to other tools), customer requests for capabilities in your other products, and organizational changes that create new needs."),
        ],
        "related": ["upsell", "expansion-revenue", "customer-lifetime-value", "customer-journey", "stakeholder-mapping"],
    },
    {
        "term": "Downsell",
        "slug": "downsell",
        "definition": "A downsell is a reduction in a customer's contract value, typically through a plan downgrade, seat reduction, or module removal at renewal.",
        "body": """<p>Downsells are the middle ground between full retention and churn. A customer who downsells is not leaving, but they are spending less. From a GRR perspective, downsells count as contraction. From a relationship perspective, they may be a warning sign or a pragmatic adjustment.</p>

<p>Common causes of downsells include budget cuts, organizational downsizing, underutilization of purchased capacity, and shifting priorities. Not all downsells are bad. A customer reducing from 100 seats to 60 after a layoff is adjusting to reality. Forcing them to keep 100 seats increases the risk of full churn.</p>

<h2>Managing Downsell Conversations</h2>
<p>When a customer asks to downgrade, the first step is understanding why. Budget pressure requires a different response than underutilization. If the customer is not using features on their current tier, the conversation should be about driving adoption, not defending the price point.</p>

<p>If a downsell is inevitable, CS teams should negotiate strategically. Can you offer a discounted rate on the current tier instead of a full downgrade? Can you preserve certain features with a shorter commitment? The goal is minimizing revenue loss while maintaining a viable path to re-expansion.</p>

<h2>Preventing Downsells</h2>
<p>Most downsells are predictable if you track the right signals. Declining usage, missed QBRs, champion departure, and budget cycle timing are all leading indicators. CS teams that monitor these signals can intervene before the downsell request comes in.</p>

<p>Value documentation is the best prevention. If the customer can clearly see the ROI of their current investment, downsell requests are less likely. This is where regular QBRs with outcome data pay dividends. A customer who knows they saved $300K this year is unlikely to cut a $50K software contract.</p>""",
        "faq": [
            ("What causes downsells in SaaS?", "Common causes include budget cuts, organizational downsizing, underutilization of purchased features or seats, champion departure, and shifting strategic priorities. Some downsells reflect genuine business changes; others signal a retention problem."),
            ("Is a downsell better than churn?", "Yes. A downsell retains the customer relationship and keeps the door open for future expansion. Full churn eliminates the account entirely. However, frequent downsells across your portfolio indicate a systemic issue worth investigating."),
            ("How can CS teams prevent downsells?", "By demonstrating ongoing ROI, driving feature adoption (so customers use what they pay for), building multi-stakeholder relationships, and engaging proactively when usage or engagement signals decline."),
        ],
        "related": ["revenue-churn", "gross-revenue-retention", "renewal-rate", "upsell", "risk-score"],
    },
    {
        "term": "Renewal Rate",
        "slug": "renewal-rate",
        "definition": "Renewal rate measures the percentage of customers (or revenue) that renew their contracts when they come up for renewal during a given period.",
        "body": """<p>Renewal rate is the most direct measure of customer retention. It answers: when contracts come due, what percentage of customers choose to stay? The metric can be calculated by logo count or by revenue (dollar-weighted renewal rate).</p>

<p>Logo renewal rate = (Renewed Customers / Customers Up for Renewal) x 100. Dollar renewal rate = (Renewed ARR / ARR Up for Renewal) x 100. Dollar renewal rate is typically higher because larger customers renew at higher rates, pulling the weighted average up.</p>

<h2>Renewal Rate vs. Retention Rate</h2>
<p>These terms are often used interchangeably but have a subtle difference. Renewal rate measures only the cohort of customers whose contracts came up for renewal in a given period. Retention rate measures the entire customer base, including those not yet up for renewal. A company with annual contracts might have only 25% of customers renewing in any given quarter.</p>

<p>For CS teams, renewal rate is more actionable because it focuses on the accounts that are actually at decision points. A renewal playbook should activate 90-120 days before each renewal date, with escalating engagement as the date approaches.</p>

<h2>Improving Renewal Rates</h2>
<p>Start early. By the time a customer is 30 days from renewal, their decision is mostly made. The best renewal outcomes come from relationships built over the previous 11 months: strong onboarding, consistent value delivery, regular QBRs, and multi-threaded relationships.</p>

<p>Track renewal rate by segment, CSM, and cohort. If one CSM's renewal rate is 15 points below the team average, that is a coaching opportunity. If a specific customer segment renews at lower rates, the engagement model for that segment may need redesign.</p>

<p>Auto-renewal clauses help, but they are not a substitute for active renewal management. A customer on auto-renewal who is unhappy will cancel when they notice the charge or at the next cancellation window. Active engagement ensures they renew because they want to, not because they forgot to cancel.</p>""",
        "faq": [
            ("What is a good renewal rate for SaaS?", "Enterprise SaaS companies target dollar-weighted renewal rates above 90%, with best-in-class reaching 95%+. Logo renewal rates are typically 5-10 points lower because smaller accounts churn at higher rates."),
            ("How is renewal rate different from retention rate?", "Renewal rate measures only the cohort of customers whose contracts were up for renewal in a given period. Retention rate measures the full customer base. Renewal rate is more actionable for CS teams managing specific upcoming renewals."),
            ("When should renewal conversations start?", "Best practice is 90-120 days before the renewal date for enterprise accounts, and 60-90 days for mid-market. This gives enough time to address concerns, demonstrate value, and negotiate terms if needed."),
        ],
        "related": ["churn-rate", "gross-revenue-retention", "net-revenue-retention", "customer-lifetime-value", "upsell"],
    },
    {
        "term": "ARR (Annual Recurring Revenue)",
        "slug": "arr-annual-recurring-revenue",
        "abbr": "ARR",
        "definition": "Annual Recurring Revenue is the annualized value of all active subscription contracts, representing the predictable revenue a SaaS company expects to earn over the next 12 months.",
        "body": """<p>ARR is the primary revenue metric for subscription businesses. It normalizes all contracts to an annual basis, making it possible to track growth, retention, and expansion consistently. A customer on a $2,000/month plan contributes $24,000 to ARR. A customer on a $120,000/year contract contributes $120,000.</p>

<p>ARR changes in four ways: new business (new customers), expansion (existing customers spending more), contraction (existing customers spending less), and churn (customers leaving). Tracking each component separately reveals the health of different business functions: sales drives new business, CS drives expansion and retention.</p>

<h2>ARR and Customer Success</h2>
<p>CS teams are directly responsible for the expansion, contraction, and churn components of ARR. A CS organization that adds $2M in expansion and prevents $1M in churn is contributing $3M in net ARR impact. This framing is how CS leaders justify headcount and tooling investment.</p>

<p>Individual CSMs should understand their ARR book of business. A CSM managing $3M in ARR knows exactly what is at stake in every renewal conversation. This number also helps CS leaders balance workloads. Distributing ARR evenly across the team is more meaningful than distributing logo counts.</p>

<h2>ARR Benchmarks</h2>
<p>Growth benchmarks depend on company stage. Pre-Series A companies growing ARR 3x year-over-year are on track. Series B/C companies target 50-100% growth. At $50M+ ARR, 30-40% growth is considered strong. The "Rule of 40" (growth rate + profit margin > 40%) is a common benchmark for balancing growth and efficiency.</p>

<p>For CS teams, the most relevant ARR metric is net ARR retention (NRR expressed in dollars). If your CS team manages $50M in ARR and delivers 115% net retention, that is $7.5M in net new ARR from the existing base without a single new logo.</p>""",
        "faq": [
            ("What is the difference between ARR and MRR?", "ARR is the annualized value of recurring revenue. MRR is the monthly value. ARR = MRR x 12. ARR is more common for companies with annual contracts. MRR is more common for companies with monthly billing cycles."),
            ("Does ARR include one-time fees?", "No. ARR only includes recurring subscription revenue. One-time setup fees, professional services, and hardware sales are excluded. The goal is measuring predictable, repeating revenue."),
            ("How does customer success impact ARR?", "CS teams impact ARR through three levers: reducing churn (protecting existing ARR), driving expansion (growing ARR from existing customers), and minimizing contraction (preventing downgrades). Together, these determine net ARR retention."),
        ],
        "related": ["mrr-monthly-recurring-revenue", "net-revenue-retention", "expansion-revenue", "churn-rate", "renewal-rate"],
    },
    {
        "term": "MRR (Monthly Recurring Revenue)",
        "slug": "mrr-monthly-recurring-revenue",
        "abbr": "MRR",
        "definition": "Monthly Recurring Revenue is the total predictable revenue from all active subscriptions in a single month, normalized from contracts of varying lengths.",
        "body": """<p>MRR is ARR's monthly counterpart. It provides a more granular view of revenue trends, making it useful for tracking month-over-month changes in growth, churn, and expansion. A customer on an annual $24K contract contributes $2K to MRR.</p>

<p>MRR is typically broken into components: New MRR (from new customers), Expansion MRR (from upgrades), Contraction MRR (from downgrades), and Churned MRR (from cancellations). Net New MRR = New + Expansion - Contraction - Churned. This breakdown reveals the health of each revenue motion.</p>

<h2>When to Use MRR vs. ARR</h2>
<p>Companies with predominantly monthly billing use MRR as their primary metric. Companies with annual contracts typically use ARR. Both work. The key is consistency. Mixing MRR and ARR in the same analysis creates confusion.</p>

<p>For operational CS metrics, MRR is often more useful because it captures monthly fluctuations. A spike in churned MRR in March might not show up clearly in quarterly ARR reporting but is immediately visible in MRR analysis.</p>

<h2>MRR in CS Operations</h2>
<p>CS teams use MRR to prioritize accounts, allocate resources, and measure performance. A CSM's book of business is often defined by MRR under management. Renewal dashboards show upcoming MRR at risk. Expansion pipelines track potential MRR growth.</p>

<p>MRR forecasting is a key CS leadership skill. Predicting next month's MRR requires understanding the renewal calendar, expansion pipeline, and at-risk accounts. Accurate MRR forecasts demonstrate CS maturity and build credibility with finance and executive leadership.</p>

<p>When MRR trends downward, it is a leading indicator of deeper problems. Declining MRR from existing customers (negative net expansion) signals that churn and contraction are outpacing growth from the current base. CS leaders should treat MRR trends as a real-time health check on their programs.</p>""",
        "faq": [
            ("How do you calculate MRR?", "Sum the monthly subscription value of all active customers. For annual contracts, divide the annual value by 12. Exclude one-time fees, professional services, and variable usage charges that are not guaranteed."),
            ("What is the relationship between MRR and ARR?", "ARR = MRR x 12. MRR provides monthly granularity while ARR provides the annualized view. Companies with monthly contracts typically track MRR. Companies with annual contracts typically track ARR."),
            ("Why is MRR important for CS teams?", "MRR gives CS teams a monthly view of revenue health. It makes churn, contraction, and expansion visible in real time. CS leaders use MRR trends to forecast, allocate resources, and measure the impact of retention programs."),
        ],
        "related": ["arr-annual-recurring-revenue", "net-revenue-retention", "expansion-revenue", "churn-rate", "revenue-churn"],
    },
    {
        "term": "Customer Segmentation",
        "slug": "customer-segmentation",
        "definition": "Customer segmentation is the practice of dividing your customer base into groups based on shared characteristics to deliver the right level of engagement and resources to each group.",
        "body": """<p>Segmentation is the foundation of scalable customer success. Without it, CS teams either over-serve small accounts (unsustainable) or under-serve large accounts (risky). The goal is matching engagement intensity to customer value and needs.</p>

<p>Common segmentation dimensions include ARR (enterprise, mid-market, SMB), industry, product usage maturity, lifecycle stage, health score, and growth potential. Most CS organizations start with ARR-based segmentation and add dimensions as they mature.</p>

<h2>Segmentation Models</h2>
<p>The most common model is tiered by ARR: enterprise accounts get high-touch dedicated CSMs, mid-market gets pooled CSMs with defined touch cadences, and SMB gets tech-touch (automated engagement with human escalation triggers). The ARR thresholds vary by company, but a typical split might be: enterprise ($100K+ ARR), mid-market ($25K-$100K), SMB (under $25K).</p>

<p>More advanced segmentation layers in additional factors. A $50K ARR account in a fast-growing company with high product usage might warrant higher-touch engagement than a $75K account in a flat organization with declining usage. The best segmentation models are dynamic, not static.</p>

<h2>Operationalizing Segmentation</h2>
<p>Segmentation only works if it drives different engagement models. Define the touchpoint cadence, CSM ratio, and success metrics for each segment. Enterprise might get 1:15 CSM ratio with monthly calls and quarterly QBRs. Mid-market might get 1:50 with automated check-ins and quarterly emails. SMB might get 1:200+ with fully automated engagement.</p>

<p>Review segmentation quarterly. Customers move between segments as they grow, contract, or change engagement needs. A startup that was SMB a year ago might be mid-market today. CS operations teams should automate segment transitions based on defined triggers.</p>""",
        "faq": [
            ("How should CS teams segment customers?", "Start with ARR tiers (enterprise, mid-market, SMB) and layer in additional factors like industry, product maturity, health score, and growth potential. The segmentation should drive different engagement models with defined CSM ratios and touchpoint cadences."),
            ("What is the difference between segmentation and tiering?", "They are often used interchangeably. Tiering typically refers to ARR-based groupings that determine CS resource allocation. Segmentation is broader and can include any dimension (industry, geography, lifecycle stage) used to customize the customer experience."),
            ("How many segments should a CS organization have?", "Three to five segments is typical. More than five creates operational complexity without proportional benefit. Start with three (enterprise, mid-market, SMB) and add sub-segments only when data shows they need meaningfully different engagement."),
        ],
        "related": ["high-touch", "low-touch", "tech-touch", "customer-journey", "customer-health-score"],
    },
    {
        "term": "Tech Touch",
        "slug": "tech-touch",
        "definition": "Tech touch is a customer engagement model that uses automated, technology-driven interactions to manage a large volume of accounts without dedicated human CSMs.",
        "body": """<p>Tech touch serves the long tail of your customer base: accounts where the ARR does not justify dedicated CSM time, but engagement is still critical for retention. Automated email sequences, in-app messages, webinars, community forums, and self-serve knowledge bases form the backbone of tech-touch programs.</p>

<p>The goal is not zero human contact. Tech touch means human intervention is triggered by data signals rather than scheduled by default. A tech-touch account that shows declining usage might get a human outreach. One that is healthy and growing stays on the automated track.</p>

<h2>Building a Tech-Touch Program</h2>
<p>Effective tech touch requires investment in content, tooling, and data. You need a library of targeted content for each lifecycle stage: onboarding sequences, adoption tips, feature announcements, renewal reminders, and expansion prompts. Each piece should feel relevant and timely, not generic.</p>

<p>CS platforms (Gainsight, ChurnZero, Vitally) offer journey orchestration features that let you build automated playbooks triggered by customer behavior. A new customer completes onboarding and enters an adoption sequence. Usage drops below a threshold and a re-engagement campaign fires. Renewal approaches and an automated renewal flow starts.</p>

<h2>Measuring Tech Touch</h2>
<p>Track engagement rates (email opens, in-app interaction, webinar attendance), adoption metrics (feature usage after automated nudges), and retention metrics (renewal rate for tech-touch vs. other segments). If tech-touch renewal rates are within 10 points of low-touch rates at a fraction of the cost, the program is working.</p>

<p>The economics matter. A tech-touch program that manages 2,000 accounts with $5M in total ARR using one CS operations person and $50K in tooling delivers far better unit economics than assigning 10 CSMs to the same accounts.</p>""",
        "faq": [
            ("What is tech touch in customer success?", "Tech touch is an engagement model that uses automated communications (emails, in-app messages, webinars) to manage large volumes of accounts without dedicated CSMs. Human intervention is triggered by data signals rather than scheduled by default."),
            ("When should a company use tech touch?", "Tech touch is appropriate for accounts where the ARR does not justify dedicated CSM time, typically SMB accounts under $10K-$25K ARR. The exact threshold depends on CSM cost, product complexity, and retention economics."),
            ("What tools support tech-touch programs?", "CS platforms like Gainsight, ChurnZero, Vitally, and Totango offer journey orchestration for automated playbooks. Marketing automation tools (HubSpot, Intercom) and digital adoption platforms (Pendo, Appcues) also support tech-touch engagement."),
        ],
        "related": ["low-touch", "high-touch", "customer-segmentation", "digital-adoption", "playbook"],
    },
    {
        "term": "Low Touch",
        "slug": "low-touch",
        "definition": "Low touch is a customer engagement model that blends limited human interaction with automated communications to efficiently manage mid-tier accounts.",
        "body": """<p>Low touch sits between high touch and tech touch. It is designed for mid-market accounts that need some human interaction but not the full dedicated CSM experience. A typical low-touch model uses pooled CSMs who manage 50-100 accounts with a defined touchpoint cadence and automated support for routine interactions.</p>

<p>Low-touch engagement might include a quarterly check-in call, an annual business review, automated onboarding emails, and human outreach triggered by health score changes. The CSM is available but not proactive on a weekly basis. The customer has a human point of contact but understands that the relationship operates differently than enterprise-level engagement.</p>

<h2>Low-Touch Engagement Design</h2>
<p>The key to low touch is defining exactly which interactions are human and which are automated. Human interactions should be reserved for moments that require judgment, empathy, or strategic thinking: QBRs, escalation handling, expansion conversations, and renewal negotiations. Automated interactions handle the routine: onboarding task reminders, feature announcements, usage summaries, and satisfaction surveys.</p>

<p>Pooled CSM models work well for low touch. Instead of one CSM owning 80 accounts, a team of three CSMs shares a pool of 200 accounts. Any CSM on the team can handle incoming requests, and proactive outreach is assigned based on urgency and availability. This model provides coverage without bottlenecks.</p>

<h2>Low Touch Metrics</h2>
<p>Track the same outcomes as high touch (renewal rate, NRR, expansion) but also monitor efficiency metrics: CSM time per account, cost-to-serve ratio, and engagement conversion rates. If low-touch accounts renew at 85% vs. high-touch at 93%, the 8-point gap may be acceptable given the 4x difference in cost-to-serve.</p>

<p>Look for accounts that outgrow low touch. Rising ARR, increasing product complexity, or executive requests for more engagement are signals that an account should be promoted to high touch.</p>""",
        "faq": [
            ("What is low-touch customer success?", "Low touch is a CS engagement model for mid-tier accounts that blends limited human interaction (quarterly calls, annual reviews) with automated communications (onboarding emails, usage reports). It balances personalization with operational efficiency."),
            ("How many accounts can a low-touch CSM manage?", "Low-touch CSMs typically manage 50-100 accounts, compared to 15-25 for high-touch CSMs and 200+ for tech-touch programs. The exact ratio depends on product complexity, account needs, and automation maturity."),
            ("When should an account move from low touch to high touch?", "When ARR crosses the enterprise threshold, when product complexity increases significantly, when the customer requests more engagement, or when health score data shows the account needs more attention than the low-touch model provides."),
        ],
        "related": ["high-touch", "tech-touch", "customer-segmentation", "touchpoint", "playbook"],
    },
    {
        "term": "High Touch",
        "slug": "high-touch",
        "definition": "High touch is a customer engagement model where a dedicated CSM provides personalized, proactive service to a small number of high-value accounts.",
        "body": """<p>High touch is the premium engagement model reserved for your most valuable accounts. A dedicated CSM (sometimes a team including CSM, solutions architect, and executive sponsor) actively manages the relationship with regular meetings, customized success plans, executive alignment, and white-glove support.</p>

<p>Typical high-touch CSM ratios range from 1:10 to 1:25 accounts. The CSM knows each customer's business goals, key stakeholders, product usage patterns, and organizational dynamics. They are proactive, reaching out before problems arise and surfacing opportunities before the customer asks.</p>

<h2>What High-Touch Engagement Looks Like</h2>
<p>A high-touch cadence typically includes: weekly or biweekly check-ins with the operational champion, monthly strategic calls with leadership, quarterly business reviews (QBRs), semi-annual executive business reviews (EBRs), and ad-hoc engagement for escalations, product feedback, and expansion conversations.</p>

<p>Beyond scheduled meetings, high-touch CSMs monitor account health continuously. They review product usage weekly, track support ticket trends, monitor stakeholder changes, and stay informed about the customer's industry and competitive landscape. This depth of knowledge enables them to anticipate needs rather than react to problems.</p>

<h2>ROI of High Touch</h2>
<p>High touch is expensive. A fully-loaded CSM costs $100K-$150K annually. At a 1:15 ratio, that is $7K-$10K per account in CS cost. The investment is justified when the ARR at stake is 10-20x the cost: managing $1.5M-$3M in ARR per CSM is a common target.</p>

<p>The returns show up in renewal rates (95%+ for well-managed high-touch accounts), expansion rates (20-40% annual expansion), and NPS scores that generate referrals and case studies. High-touch accounts are also the primary source of product feedback that shapes roadmap decisions.</p>""",
        "faq": [
            ("What is high-touch customer success?", "High touch is a CS model where a dedicated CSM provides personalized, proactive management for a small number of high-value accounts. It includes regular meetings, customized success plans, executive alignment, and continuous health monitoring."),
            ("How many accounts should a high-touch CSM manage?", "High-touch CSMs typically manage 10-25 accounts depending on complexity, ACV, and the level of engagement required. Enterprise accounts with complex implementations may require ratios as low as 1:10."),
            ("Is high-touch CS worth the cost?", "Yes, when applied to the right accounts. High-touch CS typically achieves 95%+ renewal rates and 20-40% annual expansion. The ROI is positive when each CSM manages ARR that is 10-20x their fully-loaded cost."),
        ],
        "related": ["low-touch", "tech-touch", "customer-segmentation", "qbr-quarterly-business-review", "white-glove-service"],
    },
    {
        "term": "Customer Advocacy",
        "slug": "customer-advocacy",
        "definition": "Customer advocacy is a CS program that identifies and mobilizes satisfied customers to serve as references, case study participants, reviewers, and community ambassadors.",
        "body": """<p>Customer advocacy turns your happiest customers into a growth engine. Advocates participate in reference calls for prospects, co-present at conferences, write reviews on G2 and Capterra, contribute to case studies, and refer other potential customers. Their authentic voice is more credible than any marketing message.</p>

<p>Advocacy programs are a CS responsibility because CSMs have the closest relationships with customers and the best understanding of which accounts are genuinely satisfied. Advocacy should never be forced on unhappy customers. It works because advocates are genuinely enthusiastic about the product and willing to share their experience.</p>

<h2>Building an Advocacy Program</h2>
<p>Start by identifying potential advocates: high NPS scores, strong health scores, customers who have achieved documented ROI, and stakeholders who have already informally referred others. Build a tiered program with clear asks at each level: review site participation (easy ask), reference calls (medium ask), case study (bigger ask), speaking engagement (premium ask).</p>

<p>Incentives help but should not be the primary motivation. Early access to features, invitations to an advisory board, co-branding opportunities, and public recognition are more effective than gift cards. The best advocates do it because they believe in the product and enjoy the professional visibility.</p>

<h2>Measuring Advocacy Impact</h2>
<p>Track advocacy activities (references completed, reviews posted, case studies published) and connect them to business outcomes (deals influenced by references, pipeline generated from referrals). Some companies attribute 20-30% of closed-won deals to customer advocacy programs.</p>

<p>Protect your advocates. Do not over-ask. A customer who gets three reference call requests per month will burn out. Limit asks to a reasonable frequency and always follow up with gratitude and results. "Your reference call with Acme Corp helped close a $200K deal. Thank you." That feedback loop keeps advocates engaged.</p>""",
        "faq": [
            ("What is a customer advocacy program?", "A customer advocacy program identifies and mobilizes satisfied customers to participate in reference calls, case studies, product reviews, conference presentations, and referrals. It turns customer satisfaction into a measurable growth lever."),
            ("How do you identify customer advocates?", "Look for high NPS scores, strong health scores, documented ROI achievements, and customers who have already informally recommended your product. CSMs are the primary source for identifying potential advocates based on relationship quality."),
            ("What incentives work for customer advocates?", "Early feature access, advisory board membership, co-branding opportunities, and professional recognition are more effective than monetary rewards. The best advocates are motivated by genuine enthusiasm and professional visibility."),
        ],
        "related": ["net-promoter-score", "customer-satisfaction-score", "champion", "customer-journey", "high-touch"],
    },
    {
        "term": "NPS (Net Promoter Score)",
        "slug": "net-promoter-score",
        "abbr": "NPS",
        "definition": "Net Promoter Score measures customer loyalty by asking how likely a customer is to recommend your product on a 0-10 scale, then calculating the difference between promoters and detractors.",
        "body": """<p>NPS is the most widely used customer sentiment metric in SaaS. Customers are surveyed with a single question: "How likely are you to recommend [product] to a colleague?" Responses are grouped: 9-10 are Promoters, 7-8 are Passives, and 0-6 are Detractors. NPS = % Promoters - % Detractors, resulting in a score from -100 to +100.</p>

<p>A positive NPS means you have more promoters than detractors. B2B SaaS companies typically score between 30 and 60. Scores above 50 are considered excellent. But the number alone is less important than the trend and the follow-up actions it drives.</p>

<h2>Using NPS in Customer Success</h2>
<p>NPS responses should trigger CS workflows. Detractors (0-6) need immediate outreach to understand and address their concerns. Passives (7-8) are at risk of drifting toward detractor status and may benefit from a check-in. Promoters (9-10) are candidates for advocacy programs, references, and expansion conversations.</p>

<p>The qualitative feedback matters more than the score. The open-text "Why did you give that score?" field reveals specific pain points, competitive threats, and feature requests that CS teams can act on. A detractor who says "We love the product but support response times are terrible" gives you a clear fix.</p>

<h2>NPS Best Practices</h2>
<p>Survey frequency matters. Annual NPS misses too much. Quarterly or bi-annual surveys provide better trend data. Some companies use relationship NPS (periodic surveys to the whole base) and transactional NPS (triggered after specific interactions like support resolution).</p>

<p>Response rates are critical. If only 15% of customers respond, your NPS is based on a self-selected sample that may not represent the whole base. Aim for 30%+ response rates by keeping the survey short, sending from a recognized address, and closing the loop on previous feedback.</p>""",
        "faq": [
            ("What is a good NPS score for SaaS?", "B2B SaaS companies typically score between 30 and 60. Scores above 50 are considered excellent. Scores below 0 indicate more detractors than promoters and signal a serious customer satisfaction problem."),
            ("How often should you survey NPS?", "Quarterly or bi-annually is most common for relationship NPS. Some companies also use transactional NPS after specific interactions. Annual surveys miss too much. More frequent than quarterly risks survey fatigue."),
            ("What is the difference between NPS and CSAT?", "NPS measures overall loyalty and likelihood to recommend (strategic metric). CSAT measures satisfaction with a specific interaction or experience (tactical metric). NPS predicts long-term retention. CSAT measures immediate satisfaction."),
        ],
        "related": ["customer-satisfaction-score", "customer-effort-score", "voice-of-customer", "customer-advocacy", "customer-health-score"],
    },
    {
        "term": "CSAT (Customer Satisfaction Score)",
        "slug": "customer-satisfaction-score",
        "abbr": "CSAT",
        "definition": "Customer Satisfaction Score measures how satisfied a customer is with a specific interaction, feature, or experience, typically on a 1-5 scale.",
        "body": """<p>CSAT captures satisfaction at specific moments. Unlike NPS, which measures overall loyalty, CSAT is deployed after particular interactions: a support ticket resolution, an onboarding session, a product update, or a QBR. The question is usually "How satisfied were you with [interaction]?" on a 1-5 scale.</p>

<p>CSAT is calculated as the percentage of respondents who selected 4 (Satisfied) or 5 (Very Satisfied). A CSAT of 85% means 85% of respondents were satisfied or very satisfied. B2B SaaS support teams typically target CSAT above 90%.</p>

<h2>CSAT in CS Operations</h2>
<p>CSAT gives CS teams tactical feedback on specific touchpoints. If QBR CSAT scores are low, the format or content needs adjustment. If onboarding CSAT drops, something in the onboarding process changed. This specificity makes CSAT more actionable than NPS for improving individual programs.</p>

<p>CS teams should deploy CSAT surveys at key moments in the customer journey: post-onboarding, post-QBR, after major support interactions, and after product training sessions. Each survey provides a data point that helps optimize that specific touchpoint.</p>

<h2>Limitations of CSAT</h2>
<p>CSAT measures satisfaction, not loyalty. A customer can be satisfied with individual interactions but still churn because a competitor offers a better product. CSAT also suffers from recency bias and response bias. Customers who had extreme experiences (very good or very bad) are more likely to respond, skewing the results.</p>

<p>Use CSAT as one input alongside NPS, CES, and behavioral data. No single survey metric tells the full story. Together, they provide a more complete picture of customer sentiment and predict retention more accurately than any metric alone.</p>""",
        "faq": [
            ("How do you calculate CSAT?", "CSAT = (Number of respondents rating 4 or 5) / (Total respondents) x 100. It measures the percentage of satisfied customers after a specific interaction. Surveys use a 1-5 scale from Very Unsatisfied to Very Satisfied."),
            ("What is a good CSAT score?", "For B2B SaaS, CSAT above 85% is considered good. Support teams often target 90%+. Scores below 75% indicate a significant satisfaction problem with the measured interaction or experience."),
            ("When should you use CSAT vs. NPS?", "Use CSAT to measure satisfaction with specific interactions (support, onboarding, QBRs). Use NPS to measure overall loyalty and likelihood to recommend. CSAT is tactical and immediate. NPS is strategic and longitudinal."),
        ],
        "related": ["net-promoter-score", "customer-effort-score", "voice-of-customer", "customer-health-score", "touchpoint"],
    },
    {
        "term": "CES (Customer Effort Score)",
        "slug": "customer-effort-score",
        "abbr": "CES",
        "definition": "Customer Effort Score measures how easy or difficult it was for a customer to accomplish a task with your product or team, typically on a 1-7 scale.",
        "body": """<p>CES is built on a simple insight: customers are more loyal to companies that make things easy. The survey asks "How easy was it to [accomplish task]?" on a 1-7 scale, where 1 is Very Difficult and 7 is Very Easy. CES predicts retention better than CSAT in many studies because effort directly drives frustration and switching intent.</p>

<p>CES is typically deployed after specific interactions: resolving a support ticket, completing a setup step, finding information in documentation, or navigating a product workflow. It measures the friction in your customer experience rather than satisfaction or loyalty.</p>

<h2>Why Effort Matters</h2>
<p>High-effort experiences are the top driver of customer disloyalty. Research by CEB (now Gartner) found that reducing effort has 4x more impact on loyalty than delighting customers. Customers do not need to be wowed. They need things to work without friction.</p>

<p>For CS teams, CES reveals where your processes create unnecessary burden. If customers report high effort when submitting feature requests, maybe the process needs simplification. If onboarding CES is low (high effort), the setup workflow may have too many manual steps.</p>

<h2>Using CES to Improve CS Operations</h2>
<p>Deploy CES at friction-prone moments: after support interactions, after onboarding milestones, after self-serve actions (updating billing, managing users), and after product configuration changes. Look for patterns in low-CES responses. If 40% of low-CES scores come from integration setup, that is where investment in automation or documentation will have the most impact.</p>

<p>CES is especially useful for tech-touch and low-touch segments where customers must self-serve many tasks. High effort in self-serve workflows drives churn in segments where you do not have a CSM to smooth over the friction. Tracking and reducing effort for these segments directly improves retention.</p>""",
        "faq": [
            ("What does CES measure?", "CES measures how easy or difficult it was for a customer to accomplish a specific task. It captures the friction in your customer experience, which research shows is a strong predictor of loyalty and churn."),
            ("How is CES different from CSAT and NPS?", "CES measures effort (was this easy?). CSAT measures satisfaction (were you happy?). NPS measures loyalty (would you recommend us?). CES is the most tactical of the three, focused on specific process friction."),
            ("What is a good CES score?", "On a 1-7 scale, an average CES above 5.5 indicates low-effort experiences. Below 4.0 signals significant friction. The goal is for the vast majority of customers to rate their experience as easy (6-7)."),
        ],
        "related": ["customer-satisfaction-score", "net-promoter-score", "voice-of-customer", "customer-health-score", "digital-adoption"],
    },
    {
        "term": "Voice of Customer (VoC)",
        "slug": "voice-of-customer",
        "abbr": "VoC",
        "definition": "Voice of Customer is a systematic process of capturing, analyzing, and acting on customer feedback from surveys, conversations, support tickets, and usage data.",
        "body": """<p>VoC goes beyond any single survey metric. It is the discipline of collecting customer feedback from every channel, identifying themes, and feeding insights back into the organization. NPS, CSAT, and CES are inputs to VoC, but VoC also includes qualitative data from CSM conversations, support tickets, product reviews, community forums, and social media.</p>

<p>A VoC program centralizes this fragmented feedback into a single view. Without it, product teams hear one thing from support, CS hears another from QBRs, and sales hears something different from prospects. VoC connects these perspectives into actionable themes.</p>

<h2>Building a VoC Program</h2>
<p>Start with what you already collect. Most CS teams have NPS data, CSAT scores, support ticket themes, and CSM call notes. The first step is aggregating these sources and tagging feedback by theme (product quality, support experience, pricing, missing features, etc.).</p>

<p>Add structured collection where gaps exist. If you have survey data but no product usage feedback, add in-app micro-surveys. If you have support ticket data but no proactive outreach feedback, build a post-QBR survey. The goal is coverage across the full customer journey.</p>

<h2>VoC to Action</h2>
<p>The value of VoC is in the action loop, not the data collection. Every quarter, synthesize the top 5-10 themes from VoC data and present them to product, engineering, and leadership. Prioritize by frequency (how many customers mentioned it), revenue impact (are high-ARR accounts affected), and feasibility (can it be addressed this quarter).</p>

<p>Close the loop with customers. When you act on feedback, tell the customers who requested it. "You asked for X in your last QBR. We shipped it this month." That feedback loop increases NPS, strengthens the relationship, and encourages future feedback.</p>

<p>CS teams are the natural owners of VoC because they have the deepest customer relationships. The best CS leaders use VoC to influence product strategy, not just report on satisfaction.</p>""",
        "faq": [
            ("What is a Voice of Customer program?", "A VoC program systematically captures, aggregates, and acts on customer feedback from multiple sources: surveys, CSM conversations, support tickets, product usage data, and public reviews. The goal is turning fragmented feedback into actionable organizational insights."),
            ("Who should own VoC?", "CS teams are the natural VoC owners because they have the deepest customer relationships and widest feedback access. Some organizations create dedicated VoC roles within CS or product operations."),
            ("How is VoC different from NPS?", "NPS is a single metric within VoC. VoC is the broader program that includes NPS alongside CSAT, CES, qualitative feedback, usage data, support themes, and any other customer signal. VoC synthesizes all inputs into actionable insights."),
        ],
        "related": ["net-promoter-score", "customer-satisfaction-score", "customer-effort-score", "customer-health-score", "customer-advocacy"],
    },
    {
        "term": "Success Plan",
        "slug": "success-plan",
        "definition": "A success plan is a documented agreement between a CSM and customer that defines the customer's goals, success criteria, milestones, and the actions required to achieve them.",
        "body": """<p>A success plan translates a customer's business objectives into measurable goals with clear timelines and ownership. It is created during onboarding (or at the start of the CSM relationship) and updated regularly. A good success plan answers: What does success look like for this customer? How will we measure it? What do we need to do to get there?</p>

<p>A typical success plan includes: the customer's top 3-5 business objectives, success criteria for each (quantified when possible), a timeline with milestones, action items with owners (both vendor and customer), and risks or dependencies.</p>

<h2>Why Success Plans Work</h2>
<p>Success plans align expectations. Without one, the CSM and customer may have different definitions of success. The CSM focuses on product adoption while the customer cares about cost reduction. A success plan surfaces that gap early and ensures both parties are working toward the same outcomes.</p>

<p>Success plans also create accountability. When goals are documented with owners and timelines, both parties have a reference point. During QBRs, the success plan is the agenda. "You wanted to reduce support tickets by 30%. Here is where we are." That structured conversation is far more productive than an open-ended check-in.</p>

<h2>Building Effective Success Plans</h2>
<p>Start with the customer's words, not yours. Ask them what success looks like in their own language. Then translate that into measurable criteria. "We want to be more efficient" becomes "Reduce average case resolution time from 4 hours to 2 hours by Q3." Specific, measurable, and time-bound.</p>

<p>Keep success plans living documents. A plan created during onboarding and never updated is useless by month six. Review and revise the plan at every QBR. Add new goals as old ones are achieved. Remove goals that are no longer relevant. The plan should always reflect current reality.</p>

<p>Share the success plan with the customer. It should not be an internal CS document. When the customer has visibility into the plan, they take ownership of their action items and hold you accountable for yours. Shared accountability drives better outcomes.</p>""",
        "faq": [
            ("What is a success plan in customer success?", "A success plan is a documented agreement between a CSM and customer that defines business objectives, success criteria, milestones, and action items. It aligns both parties on what success looks like and how to achieve it."),
            ("When should a success plan be created?", "During onboarding or at the start of the CSM relationship. The initial plan should be based on objectives discussed during the sales process and refined with the customer's operational team. Update it quarterly."),
            ("What makes a success plan effective?", "Specificity (measurable goals, not vague aspirations), shared ownership (customer and vendor both have action items), and regular updates (reviewed and revised at every QBR). The plan should be a living document, not a one-time exercise."),
        ],
        "related": ["playbook", "customer-journey", "qbr-quarterly-business-review", "onboarding", "time-to-value"],
    },
    {
        "term": "Playbook",
        "slug": "playbook",
        "definition": "A CS playbook is a standardized set of actions, messaging, and workflows that CSMs follow in response to specific customer scenarios like onboarding, risk mitigation, or expansion.",
        "body": """<p>Playbooks are the operating system of a scalable CS organization. Instead of every CSM inventing their own approach to onboarding, risk response, or renewal, playbooks define the standard process. A risk playbook might specify: when health score drops to yellow, send check-in email (day 1), schedule call (day 3), escalate to CS manager if no response (day 7).</p>

<p>Common CS playbooks include: new customer onboarding, adoption acceleration, risk mitigation, renewal management, expansion identification, executive sponsor change, and re-engagement for dormant accounts. Each playbook defines triggers, steps, messaging templates, and escalation paths.</p>

<h2>Why Playbooks Matter</h2>
<p>Playbooks solve the consistency problem. Without them, customer experience varies dramatically based on which CSM they are assigned. One CSM might catch a risk signal and intervene early. Another might miss it. Playbooks ensure that every customer gets a consistent baseline of engagement regardless of their CSM.</p>

<p>Playbooks also accelerate onboarding of new CSMs. Instead of spending months learning through trial and error, a new CSM can follow established playbooks from day one. This is critical for fast-growing CS teams where the median CSM tenure may be under 18 months.</p>

<h2>Building and Maintaining Playbooks</h2>
<p>Start with your most common scenarios. If 80% of CSM time goes to onboarding, risk management, and renewals, build those three playbooks first. Document the current best practices (what your top CSMs already do), standardize them, and make them accessible in your CS platform.</p>

<p>Automate where possible. CS platforms like Gainsight and ChurnZero can trigger playbook actions automatically based on data signals. When a health score drops, the platform creates a task, sends an email, and notifies the CSM. This removes the gap between signal and action.</p>

<p>Review playbooks quarterly. Customer needs change, product evolves, and the team learns what works. A playbook that is never updated becomes stale and eventually ignored. Assign playbook ownership to specific CSMs or CS operations staff who are responsible for keeping them current.</p>""",
        "faq": [
            ("What is a CS playbook?", "A CS playbook is a standardized sequence of actions, messaging, and workflows that CSMs follow for specific scenarios. Examples include onboarding playbooks, risk response playbooks, and renewal management playbooks. They ensure consistent execution across the team."),
            ("How many playbooks should a CS team have?", "Start with 3-5 covering the most common scenarios: onboarding, risk mitigation, renewal, expansion, and re-engagement. Add more as the team matures. Too many playbooks (20+) create complexity and reduce adoption."),
            ("What is the difference between a playbook and a success plan?", "A playbook is a standardized process template applied across many accounts. A success plan is customized to a specific customer's goals. Playbooks define how the CS team operates. Success plans define what the CS team is working toward with each customer."),
        ],
        "related": ["success-plan", "customer-health-score", "risk-score", "tech-touch", "customer-journey"],
    },
    {
        "term": "Risk Score",
        "slug": "risk-score",
        "definition": "A risk score quantifies the likelihood that a customer will churn or downgrade, based on behavioral, engagement, and contractual signals.",
        "body": """<p>Risk scoring is the early warning system for customer success. While a health score provides a holistic view of account wellness, a risk score focuses specifically on negative signals that predict churn or contraction. The distinction matters because a customer can have moderate overall health but high risk due to a specific factor like an upcoming renewal with no executive sponsor.</p>

<p>Risk score inputs typically include: declining usage trends, increasing support tickets, missed QBRs, champion departure, negative NPS/CSAT, approaching renewal without confirmed budget, competitor mentions, and delayed payments.</p>

<h2>Risk Score Models</h2>
<p>Simple models use weighted rules: assign points for each risk factor and sum them. Usage declined 20%? Add 15 points. Champion left? Add 25 points. Renewal in 60 days with no engagement? Add 30 points. Thresholds define risk levels (0-30 low, 31-60 medium, 61+ high).</p>

<p>Advanced models use machine learning trained on historical churn data to identify which combinations of signals best predict churn. These models can surface non-obvious patterns, like "customers who stop using Feature X within 30 days of their champion changing roles churn at 3x the base rate."</p>

<h2>Acting on Risk Scores</h2>
<p>Risk scores without action are just dashboards. Every risk level should trigger a defined response (playbook). High risk triggers immediate CSM outreach plus CS leadership escalation. Medium risk triggers a CSM review and proactive check-in. Low risk is monitored but does not require immediate action.</p>

<p>Track risk score accuracy. After each renewal cycle, compare risk predictions against actual outcomes. Did high-risk accounts actually churn? Did low-risk accounts renew? Calibrate the model based on these results. A risk score that cries wolf too often loses the team's trust. One that misses real risk loses customers.</p>""",
        "faq": [
            ("What is a risk score in customer success?", "A risk score quantifies the likelihood that a customer will churn or downgrade based on behavioral signals like declining usage, missed meetings, champion departure, and negative survey responses. It focuses specifically on negative indicators."),
            ("How is a risk score different from a health score?", "A health score is a holistic view of account wellness across multiple dimensions. A risk score focuses specifically on churn and contraction indicators. A customer can have a moderate health score but a high risk score if a specific factor (like champion departure) is present."),
            ("What should trigger a risk score increase?", "Common triggers include declining product usage, increasing support escalations, champion or executive sponsor departure, negative NPS/CSAT responses, missed QBRs, delayed payments, and competitor mentions in conversations."),
        ],
        "related": ["customer-health-score", "red-account", "churn-rate", "playbook", "renewal-rate"],
    },
    {
        "term": "Red Account",
        "slug": "red-account",
        "definition": "A red account is a customer flagged as high-risk for churn based on health score, risk score, or CSM judgment, requiring immediate escalation and intervention.",
        "body": """<p>Red account status is the most urgent classification in customer success. It signals that an account is in danger of churning or significantly contracting without immediate intervention. Red accounts get priority attention, leadership involvement, and dedicated resources to attempt a save.</p>

<p>Red designation can be triggered by automated health/risk scoring (account drops below a threshold) or by CSM judgment (the CSM identifies a risk that data alone might miss, such as a key stakeholder expressing frustration in a call). Both triggers are valid. Over-reliance on automation misses nuanced signals. Over-reliance on CSM judgment introduces inconsistency.</p>

<h2>Red Account Management</h2>
<p>When an account goes red, a standard response protocol should activate. First, the CSM documents the specific risk factors and shares them with their manager. Second, a cross-functional team (CS leader, CSM, support lead, sometimes product) convenes to develop a save plan. Third, the save plan is executed with clear ownership, timelines, and check-in points.</p>

<p>Save plans should address the root cause, not just the symptoms. If the customer is frustrated with support response times, promising faster responses without actually fixing the underlying capacity issue will not work. If the customer's champion left and no successor is engaged, the save plan needs an executive re-engagement strategy.</p>

<h2>Red Account Metrics</h2>
<p>Track red account volume (what percentage of your book is red at any given time), save rate (percentage of red accounts that return to green/yellow within 90 days), and churn rate from red accounts. Healthy CS organizations have less than 10% of their book in red status at any time with save rates above 50%.</p>

<p>Post-mortem every churned red account. What signals were present before the account went red? Could earlier intervention have changed the outcome? These retrospectives improve future risk identification and response playbooks.</p>""",
        "faq": [
            ("What makes an account a red account?", "An account is flagged red when health or risk scores drop below critical thresholds, or when a CSM identifies imminent churn risk. Common triggers include sharp usage declines, escalations, champion departure, and explicit statements of intent to cancel."),
            ("What should happen when an account goes red?", "The CSM documents the risk factors, escalates to their manager, and a cross-functional team develops a save plan. The plan addresses root causes with clear owners, timelines, and check-ins. Leadership involvement is standard for red accounts."),
            ("What is a good red account save rate?", "A save rate above 50% is considered strong. This means more than half of accounts flagged as red are successfully brought back to healthy status. Save rates vary by industry, product, and how early risk is identified."),
        ],
        "related": ["risk-score", "customer-health-score", "churn-rate", "playbook", "champion"],
    },
    {
        "term": "Champion",
        "slug": "champion",
        "definition": "A champion is the internal advocate at the customer organization who actively supports and promotes your product, often serving as the primary point of contact for the CS team.",
        "body": """<p>Champions are the people inside your customer's organization who care about your product's success. They championed the original purchase, they promote adoption internally, and they defend the renewal when budget discussions happen. Losing a champion is one of the top predictors of churn.</p>

<p>Champions are not always the person who signed the contract. They are the people who use the product daily, see its value, and advocate for it to colleagues and leadership. In some accounts, the champion and the economic buyer are the same person. In others, they are different stakeholders with different motivations.</p>

<h2>Identifying and Nurturing Champions</h2>
<p>Look for engagement signals: frequent product usage, participation in training, attendance at user groups, responsiveness to CSM outreach, and proactive communication about feature requests or expansion needs. These behaviors indicate someone who is personally invested in the product's success.</p>

<p>Nurture champions by helping them look good internally. Share ROI data they can present to their leadership. Invite them to advisory boards and customer events. Give them early access to features. When your champion can demonstrate value to their organization, their advocacy strengthens and the account becomes more secure.</p>

<h2>Champion Risk Management</h2>
<p>Champion departure is one of the highest-risk events for any account. The person who loved your product leaves, and their replacement may prefer a different tool or have no context on why your product was chosen. Multi-threading (building relationships with multiple stakeholders) is the primary mitigation strategy.</p>

<p>When you learn a champion is leaving, activate immediately. Get an introduction to their successor before they depart. Ensure knowledge transfer happens. If possible, ask the departing champion to brief their replacement on the product's value and the relationship history. The transition window is narrow. Once they are gone, reconnecting is much harder.</p>

<p>Track champion status in your CS platform. Who is the champion for each account? When were they last engaged? Have they changed roles recently? Systematic champion tracking turns a relationship dependency into a manageable risk.</p>""",
        "faq": [
            ("What is a champion in customer success?", "A champion is the internal advocate at your customer's organization who actively supports, promotes, and defends your product. They are often the primary CSM contact and play a critical role in adoption, renewal, and expansion decisions."),
            ("What happens when a champion leaves?", "Champion departure is one of the highest churn risks. The successor may not value your product or may prefer alternatives. Mitigation strategies include multi-threading (building relationships with multiple stakeholders) and immediate outreach during the transition."),
            ("How do you build champions?", "Help them succeed internally. Share ROI data they can present to leadership, invite them to advisory boards, give them early feature access, and make them look good. Champions grow when they see personal and professional value in advocating for your product."),
        ],
        "related": ["economic-buyer", "stakeholder-mapping", "red-account", "customer-advocacy", "qbr-quarterly-business-review"],
    },
    {
        "term": "Economic Buyer",
        "slug": "economic-buyer",
        "definition": "The economic buyer is the person at the customer organization who has the authority and budget to approve, renew, or cancel the contract for your product.",
        "body": """<p>The economic buyer controls the money. They may not use your product daily (that is the champion), but they approve the purchase, sign the renewal, and make the call when budget cuts happen. Understanding who the economic buyer is and what they care about is essential for protecting and growing accounts.</p>

<p>In smaller companies, the economic buyer and champion may be the same person. In enterprise accounts, they are almost always different. The VP of Customer Success might be your champion, but the CFO or CRO is the economic buyer who approves the renewal.</p>

<h2>Engaging Economic Buyers</h2>
<p>Economic buyers care about business outcomes, not product features. They want to know: Is this investment delivering ROI? How does it compare to alternatives? Is it aligned with our strategic priorities? CSMs and CS leaders need to speak the economic buyer's language, which is about revenue, efficiency, risk, and competitive advantage.</p>

<p>Executive Business Reviews (EBRs) are the primary vehicle for economic buyer engagement. These meetings should present outcomes in business terms that resonate with the budget holder. "Your team processed 40% more renewals with 10% fewer FTEs" is more compelling to an economic buyer than "Your adoption rate increased from 65% to 82%."</p>

<h2>Protecting the Economic Buyer Relationship</h2>
<p>Do not rely on the champion to relay value to the economic buyer. Information gets filtered, diluted, or deprioritized. Build a direct (even if infrequent) relationship with the economic buyer. An annual EBR plus a brief mid-year email with ROI highlights keeps you visible at the decision-making level.</p>

<p>Economic buyer changes are high-risk events, similar to champion changes. A new CFO or VP may audit all vendor contracts. Being proactive with an introduction and value summary when a new economic buyer arrives positions you as a strategic partner rather than just another line item on the budget spreadsheet.</p>""",
        "faq": [
            ("What is an economic buyer?", "The economic buyer is the person with authority and budget to approve, renew, or cancel your contract. They control the financial decision even if they do not use the product daily. In enterprise accounts, this is typically a VP, SVP, or C-level executive."),
            ("How is the economic buyer different from the champion?", "The champion uses and advocates for the product daily. The economic buyer controls the budget. In small companies they may be the same person. In enterprise accounts they are usually different stakeholders with different motivations and concerns."),
            ("How should CSMs engage economic buyers?", "Through Executive Business Reviews, ROI summaries, and occasional direct communication. Speak in business outcomes (revenue, efficiency, cost savings) rather than product metrics. The goal is ensuring the economic buyer sees clear value for their investment."),
        ],
        "related": ["champion", "stakeholder-mapping", "ebr-executive-business-review", "renewal-rate", "qbr-quarterly-business-review"],
    },
    {
        "term": "Stakeholder Mapping",
        "slug": "stakeholder-mapping",
        "definition": "Stakeholder mapping is the process of identifying, categorizing, and tracking all relevant decision-makers, influencers, and users at a customer organization.",
        "body": """<p>Stakeholder mapping goes beyond knowing your primary contact. It documents everyone who influences the buying, renewal, and expansion decisions: the economic buyer, the champion, end users, IT gatekeepers, procurement, and executive sponsors. Understanding this web of relationships is critical for account protection and growth.</p>

<p>A typical stakeholder map includes each person's role, their relationship to your product (user, decision-maker, influencer, blocker), their sentiment (positive, neutral, negative), their level of engagement, and their connection to other stakeholders.</p>

<h2>Why Stakeholder Mapping Matters</h2>
<p>Single-threaded accounts (only one relationship) are fragile. If your only contact leaves, you have no relationship with the account. Multi-threaded accounts (relationships at multiple levels and functions) are resilient. Even if one person leaves, others maintain the connection and institutional knowledge.</p>

<p>Stakeholder mapping also reveals expansion paths. Maybe the VP of Sales has a similar problem to the one your product solves for the CS team. Maybe the IT team is consolidating vendors and would prefer to expand your contract rather than maintain a competitor alongside you. These opportunities only surface when you map the broader organization.</p>

<h2>Building Stakeholder Maps</h2>
<p>Start during onboarding. Ask your primary contact: "Who else should be involved in this rollout? Who will we need buy-in from?" LinkedIn and your CRM can fill in organizational structure. Build the initial map and update it at every QBR.</p>

<p>Actively work to expand your stakeholder footprint. Invite additional stakeholders to training sessions. Share relevant content with leaders your champion reports to. Offer executive-to-executive introductions. Each new relationship makes the account more secure and creates more surface area for expansion conversations.</p>

<p>Track stakeholder changes. Job changes, promotions, departures, and new hires all shift the stakeholder landscape. CS platforms can integrate with LinkedIn Sales Navigator to alert you when stakeholders change roles. These transitions are both risks (departures) and opportunities (new stakeholders may have different needs).</p>""",
        "faq": [
            ("What is stakeholder mapping in customer success?", "Stakeholder mapping identifies and tracks all relevant people at a customer organization: decision-makers, influencers, users, and blockers. It documents their roles, sentiment, engagement level, and relationships to each other."),
            ("Why is multi-threading important?", "Multi-threaded accounts (relationships with multiple stakeholders) are more resilient to champion departure, more likely to renew, and more likely to expand. Single-threaded accounts are fragile because the entire relationship depends on one person."),
            ("How often should stakeholder maps be updated?", "Review and update stakeholder maps at every QBR (quarterly at minimum). Additionally, update whenever you learn about role changes, departures, or new hires at the customer organization. Set alerts for LinkedIn changes."),
        ],
        "related": ["champion", "economic-buyer", "qbr-quarterly-business-review", "ebr-executive-business-review", "red-account"],
    },
    {
        "term": "Customer Onboarding",
        "slug": "customer-onboarding",
        "definition": "Customer onboarding is the structured post-sale process of configuring, training, and launching a customer on your product to achieve their first measurable outcome.",
        "body": """<p>Customer onboarding is where the promises made during the sales process become reality. It is the transition from "here is what our product can do" to "here is what our product is doing for you." Effective onboarding programs reduce time to value, improve first-year retention, and set the foundation for expansion.</p>

<p>A standard enterprise onboarding workflow includes: kickoff call (align on goals and timeline), technical setup (integrations, data migration, configuration), user training (admin and end-user sessions), go-live (first production use), and success milestone (first measurable outcome achieved). Each step has owners, deadlines, and completion criteria.</p>

<h2>Onboarding Success Factors</h2>
<p>Clean handoff from sales to CS is the first critical step. The customer should never have to repeat their goals, pain points, or requirements to the onboarding team. A structured handoff document (or CRM notes) that captures everything discussed during the sales process saves time and builds trust.</p>

<p>Set realistic timelines. Over-promising speed and under-delivering creates frustration. Under-promising creates a perception that your product is complex. Use historical data from similar customers to set accurate expectations. "Customers like you typically reach their first milestone in 3-4 weeks" is specific and credible.</p>

<h2>Measuring Onboarding Success</h2>
<p>Track onboarding completion rate (percentage of customers who complete all onboarding steps), time to first value, and post-onboarding health scores. If onboarding completion rates are below 80%, investigate where customers are dropping off and fix those steps.</p>

<p>Compare retention rates between customers who completed onboarding within target and those who did not. This data quantifies the ROI of onboarding investment and makes the case for additional resources when needed.</p>

<p>Collect CSAT after onboarding. Customer feedback on the onboarding experience reveals improvement opportunities and validates what is working well. A post-onboarding NPS survey also provides an early sentiment baseline.</p>""",
        "faq": [
            ("What is the difference between customer onboarding and implementation?", "Customer onboarding is the full post-sale experience from signing through first value. Implementation is the technical subset: configuration, data migration, integrations. Onboarding includes implementation plus training, change management, and success planning."),
            ("Who should own customer onboarding?", "It varies by organization. Some companies have dedicated onboarding specialists. Others assign onboarding to the CSM who will own the account long-term. Larger companies may have an implementation team for technical work and a CSM for relationship and training."),
            ("What makes onboarding successful?", "A clean sales-to-CS handoff, realistic timelines, clear milestones with owners, structured training, and a defined first-value milestone. Successful onboarding ends when the customer achieves a measurable outcome, not when setup is technically complete."),
        ],
        "related": ["onboarding", "implementation", "go-live", "time-to-value", "success-plan"],
    },
    {
        "term": "Implementation",
        "slug": "implementation",
        "definition": "Implementation is the technical phase of customer onboarding focused on product configuration, data migration, integrations, and environment setup.",
        "body": """<p>Implementation is the technical backbone of onboarding. It covers everything required to get the product working in the customer's environment: configuring settings, migrating data from previous systems, building integrations with existing tools, setting up user permissions, and creating custom workflows or reports.</p>

<p>Implementation complexity varies enormously by product. A self-serve SaaS tool might require 5 minutes of setup. An enterprise CS platform might need 4-8 weeks of implementation involving data engineers, solution architects, and multiple integration partners.</p>

<h2>Implementation Best Practices</h2>
<p>Define scope clearly at kickoff. Implementation scope creep is one of the top causes of delayed onboarding. Document exactly what will be configured, migrated, and integrated in phase one. Additional requirements go into a phase-two backlog, not the initial timeline.</p>

<p>Assign clear ownership for each implementation task. Some tasks require the customer's IT team (API access, SSO configuration, data exports). Some require your team (configuration, migration scripts). Ambiguous ownership causes delays when both sides assume the other is handling a task.</p>

<h2>Implementation and CS Alignment</h2>
<p>CSMs should be involved in implementation planning even if a separate team handles execution. The CSM understands the customer's business goals and can ensure that configuration decisions support those goals. A product configured for efficiency without considering the customer's specific workflow needs may technically work but fail to deliver the expected value.</p>

<p>Post-implementation handoff to the ongoing CSM should include documentation of configuration decisions, known limitations, workarounds implemented, and open items for future phases. This context prevents the CSM from re-discovering issues the implementation team already identified.</p>

<p>Track implementation metrics: days to completion, scope changes, customer satisfaction with the implementation experience, and time from implementation completion to first value milestone. These metrics identify bottlenecks and improvement opportunities in the implementation process.</p>""",
        "faq": [
            ("What is included in a SaaS implementation?", "SaaS implementation typically includes product configuration, data migration from existing systems, integration with other tools (CRM, email, data warehouses), user provisioning, SSO setup, and custom workflow or report creation."),
            ("How long does implementation take?", "It depends on product complexity. Simple tools: days. Mid-market products: 2-4 weeks. Enterprise platforms: 4-12 weeks or more. Factors include integration count, data migration volume, configuration complexity, and customer IT resource availability."),
            ("Who manages implementation?", "Some companies have dedicated implementation or solutions engineering teams. Others assign implementation to the CSM or a technical onboarding specialist. For complex enterprise products, a project manager often coordinates across vendor and customer teams."),
        ],
        "related": ["customer-onboarding", "go-live", "time-to-value", "onboarding", "success-plan"],
    },
    {
        "term": "Go-Live",
        "slug": "go-live",
        "definition": "Go-live is the milestone when a customer transitions from setup and testing to active production use of the product.",
        "body": """<p>Go-live marks the transition from implementation to real-world usage. It is when the product moves from a staging or test environment into production, and end users begin relying on it for their daily work. This milestone is a critical moment in the customer journey because it is where theoretical value becomes actual value.</p>

<p>A successful go-live requires preparation: final testing, user training completion, data validation, fallback procedures (in case something breaks), and communication to all affected users. Rushing go-live to meet a timeline without proper preparation creates a poor first impression that is difficult to recover from.</p>

<h2>Go-Live Planning</h2>
<p>Define go-live criteria: what conditions must be met before the product is ready for production use? Typical criteria include all integrations tested, key data migrated and validated, primary users trained, admin trained on configuration changes, and support escalation paths defined.</p>

<p>Plan for the go-live week. Have your team available for rapid support. Schedule daily check-ins during the first week of production use. Monitor usage closely for errors, confusion, and adoption patterns. The first week sets the tone. If users struggle and no one responds quickly, they disengage.</p>

<h2>Post-Go-Live Monitoring</h2>
<p>Go-live is not the finish line. It is the starting line for adoption. After go-live, monitor user activity: who is logging in, who is not, which features are being used, and where users are getting stuck. Use this data to provide targeted follow-up training and address friction points.</p>

<p>Schedule a go-live retrospective 2-4 weeks after launch. What went well? What should improve for the next implementation? Capture lessons learned and feed them back into the onboarding process. This continuous improvement loop is how CS teams make each implementation better than the last.</p>

<p>For the customer, go-live should feel like a celebration, not a stress test. Acknowledge the milestone. Share it with their leadership. "We are live and here is what we expect to accomplish in the first 30 days." That positive framing creates momentum for the adoption phase ahead.</p>""",
        "faq": [
            ("What does go-live mean in SaaS?", "Go-live is the milestone when a customer transitions from implementation and testing to active production use. End users begin using the product for their real work, and the product becomes part of their daily operations."),
            ("How do you prepare for a go-live?", "Preparation includes final testing, data validation, user training, defining fallback procedures, and communicating the launch to all affected users. Go-live criteria should be defined and verified before the transition."),
            ("What should happen after go-live?", "Monitor user activity closely during the first 1-2 weeks. Provide rapid support for issues. Schedule daily check-ins. Track adoption patterns. Conduct a retrospective 2-4 weeks later to capture lessons learned."),
        ],
        "related": ["implementation", "customer-onboarding", "time-to-value", "adoption-rate", "onboarding"],
    },
    {
        "term": "Adoption Rate",
        "slug": "adoption-rate",
        "definition": "Adoption rate measures the percentage of licensed or intended users who are actively using the product, reflecting how deeply the product has penetrated the customer organization.",
        "body": """<p>Adoption rate answers a fundamental question: of all the people who could be using your product, how many actually are? The formula is simple: Adoption Rate = (Active Users / Licensed Users) x 100. A customer with 100 seats and 65 monthly active users has a 65% adoption rate.</p>

<p>Low adoption is a leading indicator of churn. Customers who bought 100 seats but only 30 people use the product are paying for value they are not receiving. They will either downgrade (contraction) or leave entirely (churn) when the renewal comes.</p>

<h2>Tracking Adoption</h2>
<p>Measure adoption at multiple levels. Account-level adoption (how many users are active) is the starting point. Feature-level adoption (which features are being used) adds depth. Module-level adoption (which purchased modules are in use) reveals unused value. Each level provides different actionable insights.</p>

<p>Define "active" clearly. Daily active user? Weekly? Monthly? The right definition depends on your product's expected usage pattern. A daily workflow tool should measure daily or weekly active users. A quarterly reporting platform might measure monthly active users. Consistency matters more than the specific definition.</p>

<h2>Driving Adoption</h2>
<p>Start by understanding why adoption is low. Common causes include poor training (users do not know how to use the product), workflow misalignment (the product does not fit how users actually work), resistance to change (users prefer their old tools), and configuration issues (the product is not set up optimally for the customer's use case).</p>

<p>Each cause requires a different intervention. Training gaps need targeted education. Workflow misalignment needs configuration changes. Resistance to change needs executive sponsorship and change management. Configuration issues need technical support.</p>

<p>Digital adoption platforms (Pendo, WalkMe, Appcues) can drive adoption at scale by delivering in-app guidance to users at the moment they need it. These tools are especially effective for features that users do not discover organically.</p>""",
        "faq": [
            ("How do you calculate adoption rate?", "Adoption Rate = (Active Users / Licensed or Intended Users) x 100. Define 'active' based on your product's expected usage pattern (daily, weekly, or monthly). Measure at account, feature, and module levels for a complete picture."),
            ("Why does adoption rate matter?", "Low adoption is a leading indicator of churn. Customers who are not using the product are not receiving value and will eventually downgrade or cancel. High adoption signals value realization and correlates with higher renewal and expansion rates."),
            ("How can CS teams improve adoption?", "Diagnose the root cause (training gaps, workflow misalignment, change resistance, or configuration issues), then apply the appropriate intervention. Digital adoption platforms, targeted training, and CSM-led workshops all drive adoption depending on the cause."),
        ],
        "related": ["feature-adoption", "dau-mau-ratio", "digital-adoption", "time-to-value", "customer-health-score"],
    },
    {
        "term": "Feature Adoption",
        "slug": "feature-adoption",
        "definition": "Feature adoption measures the percentage of users engaging with specific product features, revealing which capabilities deliver value and which are underutilized.",
        "body": """<p>Feature adoption zooms in from overall product adoption to the feature level. It answers: which specific features are customers using, which are they ignoring, and which are they trying but abandoning? This granularity is essential for both CS and product teams.</p>

<p>The metric is typically: Feature Adoption Rate = (Users Who Used Feature X in Period) / (Total Active Users) x 100. If 200 users are active and 50 use the health scoring feature, health scoring has a 25% adoption rate.</p>

<h2>Feature Adoption and Retention</h2>
<p>Not all features correlate equally with retention. Some features are sticky: customers who use them churn at significantly lower rates. Identifying these "sticky features" and driving adoption of them is one of the highest-impact activities for CS teams.</p>

<p>Analyze which features are used by your longest-tenured, highest-NPS customers. If those customers all use features A, B, and C, but churned customers tended to only use A, then features B and C may be the key differentiators. Focus adoption efforts on those features.</p>

<h2>Driving Feature Adoption</h2>
<p>Awareness is the first barrier. Many users do not know a feature exists. In-app announcements, targeted email campaigns, webinars, and CSM-led workshops can increase awareness. Digital adoption platforms are particularly effective at contextually introducing features when a user is in a relevant workflow.</p>

<p>Complexity is the second barrier. If a feature requires 10 steps to configure and 30 minutes to learn, adoption will lag. Work with product to simplify feature onboarding. Pre-built templates, default configurations, and guided setup wizards all reduce the friction of trying a new feature.</p>

<p>Value demonstration is the third lever. Show users what the feature does for people like them. "Teams using health scores reduce churn by 15% on average" is more motivating than "Health scoring is now available." Connect features to outcomes that users care about.</p>""",
        "faq": [
            ("How do you measure feature adoption?", "Feature Adoption Rate = (Users Who Used Feature X) / (Total Active Users) x 100. Track over time to identify trends. Segment by customer tier, industry, and lifecycle stage for actionable insights."),
            ("Which features should CS teams focus on?", "Focus on features that correlate with retention and expansion. Analyze which features your longest-tenured, highest-NPS customers use. Those 'sticky features' should be the priority for adoption campaigns."),
            ("How do you increase feature adoption?", "Address three barriers: awareness (in-app announcements, webinars), complexity (templates, guided setup), and value perception (outcome-based messaging showing what the feature achieves for similar users)."),
        ],
        "related": ["adoption-rate", "dau-mau-ratio", "digital-adoption", "customer-health-score", "product-led-growth"],
    },
    {
        "term": "DAU/MAU Ratio",
        "slug": "dau-mau-ratio",
        "definition": "The DAU/MAU ratio measures user engagement by dividing daily active users by monthly active users, indicating how frequently users return to the product.",
        "body": """<p>DAU/MAU (Daily Active Users divided by Monthly Active Users) is a stickiness metric. A ratio of 0.5 (or 50%) means that on any given day, half of the monthly user base is active. Higher ratios indicate more habitual usage. Facebook famously targets a DAU/MAU ratio above 60%. For B2B SaaS, benchmarks are lower because not every product is designed for daily use.</p>

<p>The formula: DAU/MAU = Average Daily Active Users in a Month / Monthly Active Users. If 300 unique users are active in a month and the average daily count is 75, the DAU/MAU ratio is 25%.</p>

<h2>DAU/MAU for CS Teams</h2>
<p>This ratio tells CS teams how deeply embedded the product is in daily workflows. A product with a 50% DAU/MAU ratio is part of users' daily routines. A product with a 10% ratio is something users check occasionally. The implications for retention are significant: daily-use products have much higher switching costs than occasional-use products.</p>

<p>Track DAU/MAU at the account level. If one customer has a 40% ratio and another has 8%, the second is at much higher churn risk. The product is not embedded in their workflows, making it easy to drop without disruption.</p>

<h2>Using DAU/MAU Thoughtfully</h2>
<p>Not every product should target high DAU/MAU. A quarterly reporting tool that users open once a month during board prep is working as designed. Judging it by daily engagement misses the point. Match your expectations to your product's intended usage frequency.</p>

<p>For products that should have daily engagement, declining DAU/MAU is an early warning. If the ratio drops from 35% to 20% over two months, users are disengaging. That trend should trigger a CS investigation: is it a seasonal pattern, a product issue, a competitive threat, or a change in the customer's workflow?</p>

<p>DAU/MAU is most useful when combined with feature adoption data. Knowing that 30% of users are daily-active is helpful. Knowing that those users primarily use Feature A but not Feature B adds depth. The combination drives more targeted CS interventions.</p>""",
        "faq": [
            ("What is the DAU/MAU ratio?", "DAU/MAU divides daily active users by monthly active users to measure product stickiness. A higher ratio means users engage more frequently. It indicates how deeply the product is embedded in daily workflows."),
            ("What is a good DAU/MAU ratio for SaaS?", "It depends on the product type. Daily workflow tools (messaging, project management) should target 30-50%. Weekly-use products target 15-30%. Periodic-use tools (reporting, analytics) may naturally sit at 5-15%. Compare against similar products, not consumer apps."),
            ("How does DAU/MAU predict churn?", "Low or declining DAU/MAU indicates the product is not embedded in daily workflows, making it easier for customers to switch. Accounts with consistently low ratios are at higher churn risk because the product is not habitual."),
        ],
        "related": ["adoption-rate", "feature-adoption", "customer-health-score", "digital-adoption", "product-led-growth"],
    },
    {
        "term": "White Glove Service",
        "slug": "white-glove-service",
        "definition": "White glove service is the highest tier of customer engagement, providing premium, personalized, hands-on support and strategic guidance for top-tier accounts.",
        "body": """<p>White glove service goes beyond standard high-touch engagement. It is the premium experience reserved for your largest, most strategic accounts. These customers get dedicated team members (not shared), custom SLAs, priority escalation paths, on-site visits, executive-to-executive relationships, and bespoke success programs tailored to their specific needs.</p>

<p>The term comes from the luxury service industry where staff wear white gloves to handle precious items with extra care. In CS, it means treating the account with that same level of attention and customization.</p>

<h2>When White Glove Makes Sense</h2>
<p>White glove service is only sustainable for a small number of accounts. The investment is significant: a dedicated CSM (sometimes a dedicated team), custom integrations, priority support, and executive time. This level of service is justified for accounts where the ARR is large enough (typically $500K+) and the strategic importance (reference value, market positioning, expansion potential) warrants the cost.</p>

<p>Some companies offer white glove service as a paid tier, bundling premium support, dedicated resources, and guaranteed response times into a service package that customers purchase alongside the product. This model offsets the cost while giving willing customers access to premium engagement.</p>

<h2>Delivering White Glove Service</h2>
<p>Start with a dedicated team: a named CSM who is always available, a technical lead who knows the account's configuration intimately, and an executive sponsor who maintains the C-level relationship. This team meets internally weekly to review the account and externally on whatever cadence the customer prefers.</p>

<p>Customization is the differentiator. White glove accounts get custom reporting, bespoke training programs, early access to features, influence over the product roadmap, and flexibility in contract terms. The customer should feel like a partner, not just a subscriber.</p>

<p>Document everything. White glove service often relies on tribal knowledge held by the dedicated CSM. If that CSM leaves, the institutional knowledge and relationship depth should be captured in detailed account plans, meeting notes, and success documentation.</p>""",
        "faq": [
            ("What is white glove service in customer success?", "White glove service is the premium tier of CS engagement, providing dedicated team members, custom SLAs, priority support, executive relationships, and bespoke success programs for the highest-value accounts."),
            ("How is white glove different from high touch?", "High touch provides a dedicated CSM with regular engagement for valuable accounts. White glove goes further: dedicated teams (not just one CSM), custom SLAs, on-site visits, executive matching, and fully bespoke success programs."),
            ("Which accounts should get white glove service?", "Accounts with the highest ARR (typically $500K+), strong strategic value (reference, market positioning), and significant expansion potential. White glove is only sustainable for a small number of accounts due to cost."),
        ],
        "related": ["high-touch", "customer-segmentation", "ebr-executive-business-review", "champion", "stakeholder-mapping"],
    },
]


def _get_related_terms_html(current_slug, related_slugs):
    """Build related terms HTML section."""
    links = []
    for slug in related_slugs:
        for t in GLOSSARY_TERMS:
            if t["slug"] == slug:
                links.append(f'<a href="/glossary/{slug}/" class="related-link-card">{t["term"]}</a>')
                break
    if not links:
        return ""
    return f'''<section class="related-links">
    <h2>Related CS Terms</h2>
    <div class="related-links-grid">{"".join(links)}</div>
</section>'''


def _letter_groups():
    """Group terms by first letter for the index page."""
    groups = {}
    for t in GLOSSARY_TERMS:
        letter = t["term"][0].upper()
        if letter not in groups:
            groups[letter] = []
        groups[letter].append(t)
    return dict(sorted(groups.items()))


# ---------------------------------------------------------------------------
# Index page
# ---------------------------------------------------------------------------

def build_glossary_index():
    """Generate /glossary/ index page with all terms grouped alphabetically."""
    title = "Customer Success Glossary: 45 Key CS Terms Defined"
    description = (
        "A comprehensive glossary of customer success terms. Clear definitions for NRR, churn rate,"
        " health scores, QBRs, expansion revenue, and 40+ more CS metrics and concepts."
    )

    crumbs = [("Home", "/"), ("Glossary", None)]
    groups = _letter_groups()

    # Letter nav
    letter_nav = '<div class="glossary-letter-nav">'
    for letter in groups:
        letter_nav += f'<a href="#letter-{letter}">{letter}</a>'
    letter_nav += '</div>'

    # Term list by letter
    term_list = ''
    for letter, terms in groups.items():
        term_list += f'<div class="glossary-letter-group" id="letter-{letter}">'
        term_list += f'<h2 class="glossary-letter-heading">{letter}</h2>'
        term_list += '<div class="glossary-term-list">'
        for t in sorted(terms, key=lambda x: x["term"]):
            term_list += f'''<a href="/glossary/{t["slug"]}/" class="glossary-term-card">
    <h3>{t["term"]}</h3>
    <p>{t["definition"][:120]}{"..." if len(t["definition"]) > 120 else ""}</p>
</a>
'''
        term_list += '</div></div>'

    body = f'''<div class="salary-content">
    {breadcrumb_html(crumbs)}
    <h1>Customer Success Glossary</h1>
    <p class="lead">Clear, practical definitions for 45 customer success terms. Built for CS professionals who want substance, not buzzword soup.</p>
    {letter_nav}
    {term_list}
</div>
'''
    body += newsletter_cta_html("Stay sharp on CS terminology and trends.")

    schema = get_breadcrumb_schema(crumbs)
    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/glossary/",
        body_content=body,
        active_path="/glossary/",
        extra_head=schema,
    )
    write_page("glossary/index.html", page)
    print(f"  Built: glossary/index.html")


# ---------------------------------------------------------------------------
# Individual term pages
# ---------------------------------------------------------------------------

def build_glossary_term(t):
    """Generate a single glossary term page."""
    term = t["term"]
    slug = t["slug"]
    definition = t["definition"]
    body_content = t["body"]
    faq_pairs = t["faq"]
    related = t.get("related", [])

    title = f"What Is {term}? Definition and Guide"
    description = definition[:155].rstrip('.') + '.' if len(definition) > 155 else definition

    crumbs = [("Home", "/"), ("Glossary", "/glossary/"), (term, None)]

    # Build body
    body = f'''<div class="salary-content">
    {breadcrumb_html(crumbs)}
    <h1>What Is {term}?</h1>
    <p class="lead">{definition}</p>
    {body_content}
    {faq_html(faq_pairs)}
    {_get_related_terms_html(slug, related)}
</div>
'''
    body += newsletter_cta_html(f"Get weekly CS intelligence on {term.split('(')[0].strip().lower()} and more.")

    # Schema: breadcrumb + FAQ
    schema = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path=f"/glossary/{slug}/",
        body_content=body,
        active_path="/glossary/",
        extra_head=schema,
    )
    write_page(f"glossary/{slug}/index.html", page)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def build_all_glossary_pages():
    """Build glossary index + all term pages."""
    print(f"\n  Building glossary pages ({len(GLOSSARY_TERMS)} terms)...")
    build_glossary_index()
    for t in GLOSSARY_TERMS:
        build_glossary_term(t)
    print(f"  Built: {len(GLOSSARY_TERMS)} glossary term pages")
