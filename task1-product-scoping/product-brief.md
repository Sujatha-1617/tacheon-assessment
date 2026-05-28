# Product Brief: Marketing Performance Intelligence Tool

## problem
The team constantly gets asked: "How is our marketing performing across 
channels right now, and where should we focus?" Today, answering it 
means manually digging through multiple tools, stitching numbers together. 
The answer is inconsistent, slow, and dependent on one person.

## Who Is This For (v1)
Primary user: Internal analysts and account managers.
Not clients — yet. Keeping v1 internal reduces scope, builds trust 
in the data before exposing it externally.

## What v1 Does
A single internal dashboard that:
- Shows key metrics per marketing channel (spend, clicks, 
  conversions, CPA) for the current week vs last week
- Flags channels that are up or down significantly (>10% change)
- Answers the core question in under 60 seconds without 
  opening any external tool

## What v1 Does NOT Do
- No client-facing view (added in v2 once data is trusted)
- No AI-generated recommendations
- No custom date range picker
- No multi-brand comparison view
- No alerting or notifications

These are deliberately excluded to keep v1 shippable and focused.

## Data Sources
Pulls from tools the team already uses (e.g. Google Ads, Meta Ads, 
GA4) via their existing APIs or scheduled exports.
Constraint respected: zero change to existing team workflows.

## How a User Interacts With It
1. Opens the tool (internal web page or Notion embed)
2. Selects a brand from a dropdown
3. Sees a summary table: channel | this week | last week | change %
4. Sees a highlight: "Paid Search CPA up 22% — worth investigating"
5. Done. No manual work needed.

## What Builds Trust
- Every metric shows its data source and "last refreshed" timestamp
- Numbers match what you'd see if you opened the source tool manually
- No black-box calculations — every derived number is explainable

## What I'd Revisit With More Time
- Validate data source API reliability and rate limits
- User interviews with 2-3 analysts before finalising the metric set
- Decide whether a Notion embed, internal web app, or Slack bot 
  is the right interface for how the team actually works
