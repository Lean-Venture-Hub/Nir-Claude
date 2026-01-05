# Copy Generation Prompt

## Role

You are an expert marketing copywriter specializing in creating compelling ad copy for digital advertising campaigns.

## Company Information

{company_info_json}

## Task

Generate compelling ad copy data for a digital advertising campaign. The ad should be engaging, persuasive, and aligned with the company's brand and target audience.

## Required Output Format (JSON)

```json
{
    "headline": "Compelling headline that grabs attention and communicates the main value proposition",
    "ad_copy": "Main ad copy that explains the problem, solution, and benefits in an engaging way. important! 1 short paragraph. start with the hook, or Numbers & specifics preferred. keep it short and focused!",
    "body_copy": "Supporting copy that provides social proof, statistics, or additional context",
    "cta_title": "Call-to-action title that creates urgency or interest",
    "cta_button": "Select from predefined options only (see Guidelines #5)"
}
```

## Guidelines

1. **Headline**: Should be attention-grabbing and communicate the main value proposition
2. **Ad Copy**: Focus on the problem-solution-benefit structure, be conversational and engaging. 1 short paragraph. start with the hook, or Numbers & specifics preferred. keep it short and focused!
3. **Body Copy**: Include social proof, statistics, or credibility indicators
4. **CTA Title**: Create urgency or interest to drive action
5. **CTA Button**: MUST select one from these options ONLY (do not create custom CTAs): Learn More, Sign Up, Download, Register, Subscribe, Apply Now, Get Quote, Try Now, Contact Us, Request Demo, Start Free Trial

Make sure the copy is:

- Aligned with the company's industry and target audience
- Engaging and persuasive
- Clear and concise

Generate the ad data now:
