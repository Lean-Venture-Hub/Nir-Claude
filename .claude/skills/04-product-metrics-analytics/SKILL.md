---
name: product-metrics-analytics
description: Define product metrics frameworks, track KPIs, analyze data, interpret trends, set OKRs, and measure product success. Use when setting up analytics, defining success metrics, interpreting product data, tracking feature performance, setting objectives and key results, or analyzing user behavior and product health.
---

# Product Metrics & Analytics

Framework for defining, tracking, and analyzing product metrics to drive decisions.

## Metrics Framework

### 1. Product Metrics Hierarchy

**Strategic Metrics (Company Level)**
- North Star Metric
- Revenue (MRR, ARR)
- Growth Rate
- Market Share

**Product Metrics (Feature/Product Level)**
- Acquisition
- Activation
- Engagement
- Retention
- Revenue
- Referral

**Operational Metrics (Team Level)**
- Feature adoption rate
- Time-to-value
- Customer satisfaction (NPS, CSAT)
- Support tickets

### 2. Metrics by Category

#### Acquisition Metrics
```
Metric: New Users/Signups
Definition: Users who complete signup in period
Target: [Number]
Data Source: [Analytics platform]
Tracking: Daily/Weekly/Monthly

Related Metrics:
- Traffic sources breakdown
- Conversion rate by channel
- Cost per acquisition (CPA)
- Signup completion rate
```

#### Activation Metrics
```
Metric: Activation Rate
Definition: % of users who reach "aha moment" within [timeframe]
Aha Moment: [Specific action indicating value understanding]
Target: [Percentage]

Examples of Aha Moments:
- Slack: 2,000 messages sent by team
- Dropbox: File saved to one folder
- Twitter: Follow 30 accounts
```

#### Engagement Metrics
```
Core Engagement:
- DAU (Daily Active Users)
- WAU (Weekly Active Users)
- MAU (Monthly Active Users)
- DAU/MAU Ratio (stickiness)

Feature Engagement:
- Feature adoption rate
- Frequency of use
- Time spent in feature
- Power user threshold

Calculation:
DAU/MAU Ratio = (Daily Active / Monthly Active) × 100
Target: >20% for consumer, >40% for high-engagement products
```

#### Retention Metrics
```
Retention Cohorts:
- Day 1, Day 7, Day 30, Day 90 retention
- Weekly cohort retention
- Monthly cohort retention

Retention Curve:
- Plot retention % over time
- Identify where curve flattens (plateau indicates product-market fit)

Churn Metrics:
- User churn rate
- Revenue churn rate
- Churn reasons (categorized)

Retention Calculation:
N-Day Retention = (Users active on day N / Users who signed up N days ago) × 100
```

#### Revenue Metrics
```
SaaS Metrics:
- MRR (Monthly Recurring Revenue)
- ARR (Annual Recurring Revenue)
- ARPU (Average Revenue Per User)
- LTV (Lifetime Value)
- CAC (Customer Acquisition Cost)
- LTV:CAC Ratio (target >3:1)

Revenue Formula:
MRR = Number of Customers × Average MRR per Customer
ARR = MRR × 12
LTV = ARPU × (1 / Churn Rate)
```

### 3. OKR Framework

**OKR Structure:**
- **Objective**: Qualitative goal (inspiring, time-bound)
- **Key Results**: Quantitative measures (3-5 per objective)

**OKR Template:**
```
Objective: [Ambitious, qualitative goal]
Quarter: [Q1 2024]
Owner: [Team/Person]

Key Results:
1. [Measurable outcome] from [baseline] to [target]
   Status: [Current value] - [On track/At risk/Off track]
   
2. [Measurable outcome] from [baseline] to [target]
   Status: [Current value] - [On track/At risk/Off track]
   
3. [Measurable outcome] from [baseline] to [target]
   Status: [Current value] - [On track/At risk/Off track]

Initiatives (How we'll achieve KRs):
- [Initiative 1]
- [Initiative 2]

Progress Updates: [Weekly/Bi-weekly]
End of Quarter Score: [0.0-1.0, target: 0.7]
```

**Good OKR Examples:**
```
Objective: Make onboarding delightful and fast

Key Results:
1. Increase activation rate from 45% to 65%
2. Reduce time-to-first-value from 10 min to 3 min
3. Increase Day 7 retention from 30% to 45%

---

Objective: Become the go-to platform for small teams

Key Results:
1. Grow small team (<10 users) signups from 500/mo to 1,200/mo
2. Achieve 4.5+ rating in small team segment
3. Increase small team NPS from 35 to 50
```

### 4. Data Analysis Framework

#### Trend Analysis
```
1. Establish Baseline
   - Current metric value
   - Historical average
   - Seasonality patterns

2. Identify Trend
   - Upward/Downward/Flat
   - Rate of change
   - Statistical significance

3. Find Drivers
   - Segment by user cohort
   - Segment by channel
   - Segment by feature usage
   - Correlate with product changes

4. Interpret Meaning
   - Is this good or bad?
   - What's causing it?
   - What should we do?
```

#### Cohort Analysis
```
Purpose: Compare behavior across user groups over time

Example Cohort Analysis:
| Cohort     | Week 0 | Week 1 | Week 2 | Week 3 | Week 4 |
|------------|--------|--------|--------|--------|--------|
| Jan 2024   | 100%   | 45%    | 38%    | 35%    | 33%    |
| Feb 2024   | 100%   | 52%    | 44%    | 41%    | 39%    |
| Mar 2024   | 100%   | 58%    | 50%    | 47%    | 45%    |

Insight: Retention improving month-over-month
Hypothesis: Onboarding improvements in Feb impacting retention
```

#### Funnel Analysis
```
Conversion Funnel Example:

Homepage Visit: 10,000 (100%)
    ↓ 35% conversion
Signup Page: 3,500 (35%)
    ↓ 60% conversion
Account Created: 2,100 (21%)
    ↓ 70% conversion
Aha Moment: 1,470 (14.7%)
    ↓ 80% conversion
Active User: 1,176 (11.8%)

Optimization Priority:
1. Homepage → Signup (35% - biggest drop)
2. Account → Aha (70% - high impact if improved)
```

#### Segment Analysis
```
Compare metrics across segments:

| Segment      | Users | Activation | Retention | ARPU  |
|--------------|-------|------------|-----------|-------|
| Enterprise   | 500   | 85%        | 92%       | $1200 |
| SMB          | 2,000 | 65%        | 78%       | $400  |
| Free         | 8,000 | 45%        | 45%       | $0    |

Insights:
- Enterprise has best metrics but smallest volume
- SMB is sweet spot (volume + quality)
- Free users need activation improvement
```

### 5. Metrics Dashboard Design

**Dashboard Principles:**
1. **Hierarchy**: Most important metric at top
2. **Actionability**: Include metrics you can influence
3. **Context**: Show trends, not just point-in-time
4. **Comparisons**: Previous period, targets, benchmarks
5. **Drill-down**: Enable exploration of underlying data

**Dashboard Template:**
```
# Product Health Dashboard

## North Star Metric
[Metric Name]: [Value] ↑/↓ [Change from last period]
Target: [Goal]
Status: 🟢 On Track / 🟡 At Risk / 🔴 Off Track

## Key Product Metrics

### Acquisition
- New Users: [Value] ([Change %])
- Conversion Rate: [Value] ([Change %])

### Activation
- Activation Rate: [Value] ([Change %])
- Time to Value: [Value] ([Change %])

### Engagement
- DAU/MAU: [Value] ([Change %])
- Sessions per User: [Value] ([Change %])

### Retention
- D7 Retention: [Value] ([Change %])
- D30 Retention: [Value] ([Change %])

### Revenue
- MRR: [Value] ([Change %])
- ARPU: [Value] ([Change %])

## Feature Performance
[Feature A]: [Adoption %] | [Engagement metric]
[Feature B]: [Adoption %] | [Engagement metric]

## Alerts & Anomalies
🔴 [Metric] dropped [%] - Investigate: [Hypothesis]
```

### 6. Metric Interpretation Guide

**When metrics go up:**
- Verify data accuracy (not a tracking bug)
- Identify what changed (feature launch, marketing campaign, etc.)
- Segment analysis (which users drove the increase?)
- Assess sustainability (one-time spike or sustained trend?)
- Document learnings

**When metrics go down:**
- Immediate: Check for tracking/technical issues
- Segment: Which user groups are affected?
- Timeline: When did it start?
- Correlate: What else changed around that time?
- Hypothesis: Form testable explanations
- Action: Decide on fix or experiment

**Statistical Significance:**
- Don't react to small changes (noise vs signal)
- Use statistical tests for A/B test results
- Consider sample size and confidence intervals
- Look for sustained trends over multiple periods

## Best Practices

1. **Define before building**: Agree on metrics before starting feature work
2. **Track leading indicators**: Don't wait for lagging metrics
3. **Ratio over absolute**: Percentages more meaningful than counts
4. **Trends over snapshots**: Track over time, not single points
5. **Segment everything**: Averages hide important patterns
6. **Counter-metrics**: Ensure you're not gaming the system
7. **Review cadence**: Weekly for tactical, monthly for strategic
8. **Act on insights**: Metrics without action are vanity

## Common Pitfalls

- **Vanity metrics**: Metrics that look good but don't drive decisions
- **Too many metrics**: Focus on vital few, not trivial many
- **Ignoring context**: Numbers need interpretation
- **Short-term thinking**: Optimizing metrics at expense of long-term health
- **Data without story**: Explain what the numbers mean
