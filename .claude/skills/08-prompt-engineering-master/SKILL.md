---
name: prompt-engineering-master
description: Master all core prompting techniques including clarity optimization, multi-shot prompting, chain-of-thought reasoning, prompt debugging, role-prompting, output formatting, and few/zero-shot learning. Use when crafting AI prompts, improving AI outputs, structuring complex requests, or debugging poor AI responses.
---

# Prompt Engineering Master

Core techniques for effective AI prompting and output optimization.

## 1. Core Principles

**Be Clear and Direct:**
- State exactly what you want
- Provide context upfront
- Specify format and constraints
- Use explicit instructions over hints

**Front-Load Information:**
- Most important info first
- Context before task
- Examples before instructions

## 2. Prompting Techniques

### Multi-Shot Prompting (Examples)
Provide 2-5 examples of desired output:

```
Task: Write product descriptions

Example 1:
Input: Wireless headphones
Output: "Experience crystal-clear audio with our Bluetooth 5.0 wireless headphones. 30-hour battery life, noise cancellation, and premium comfort for all-day listening."

Example 2:  
Input: Standing desk
Output: "Transform your workspace with our electric standing desk. One-touch height adjustment, sturdy steel frame, and spacious 60" surface for productive work sessions."

Now write for: [Your product]
```

### Chain-of-Thought (CoT) Prompting
For complex reasoning, ask AI to show its work:

```
Problem: [Complex question]

Let's approach this step-by-step:
1. First, identify...
2. Then, analyze...
3. Finally, conclude...

Please show your reasoning for each step.
```

### Zero-Shot Prompting
Clear instruction without examples:

```
Task: [What you want]
Format: [How to structure it]
Constraints: [What to avoid]
Tone: [How it should sound]

[Additional context]
```

### Few-Shot Learning
2-3 examples when full multi-shot isn't needed:

```
Convert casual to professional:

Casual: "Hey, got your email, will look into it"
Professional: "Thank you for your email. I will review this matter and respond shortly."

Casual: "Can't make the meeting, sorry"
Professional: "Unfortunately, I have a conflict and will be unable to attend the meeting."

Now convert: [Your text]
```

## 3. Output Formatting

### Using XML Tags
```
<task>Write a product launch email</task>

<context>
Product: AI writing assistant
Audience: Marketing professionals  
Goal: Drive trial signups
</context>

<constraints>
- Max 200 words
- Include clear CTA
- Professional but friendly tone
</constraints>

<format>
Subject: [engaging subject line]
Preview: [preview text]
Body: [email copy]
CTA: [call-to-action]
</format>
```

### JSON Output
```
Respond in valid JSON format:

{
  "summary": "brief overview",
  "key_points": ["point 1", "point 2", "point 3"],
  "recommendation": "your suggestion",
  "confidence": "high/medium/low"
}
```

### Structured Lists
```
Provide response as:
1. [Numbered list item]
2. [Numbered list item]

Or:
• [Bullet point]
• [Bullet point]

Or:
Heading 1:
- Detail
- Detail

Heading 2:
- Detail
- Detail
```

## 4. Role Prompting

**Effective Role Assignment:**
```
You are an expert [role] with [X years] experience in [domain].
Your expertise includes [specific skills].

Task: [What you need them to do]

Approach this from the perspective of [specific angle].
```

**Example:**
```
You are a senior product manager with 10 years at B2B SaaS companies.
Your expertise includes user research, roadmap planning, and stakeholder management.

Task: Review this PRD and identify gaps or unclear requirements.

Approach this as if you're preparing for a technical review with engineering.
```

## 5. Prompt Debugging

**When Output Is Wrong:**
1. Check if instructions are specific enough
2. Add examples of correct output
3. Specify what NOT to do
4. Break complex tasks into steps
5. Add constraints and format requirements

**Before:**
```
Write a blog post about project management.
```

**After:**
```
Write a 1,200-word blog post about project management for software teams.

Target audience: Engineering managers at startups
Tone: Practical and actionable, not theoretical
Structure:
- Introduction with hook (100 words)
- 3 main sections with examples
- Conclusion with actionable takeaways

Include:
- Specific frameworks (e.g., Agile, Scrum)
- Real-world scenarios
- Common pitfalls to avoid

Do NOT:
- Use jargon without explanation
- Make it too academic  
- Focus only on theory

Format: Use H2 headings, bullet points, and short paragraphs.
```

## 6. Context Management

**Provide Relevant Context:**
```
Context: [Background information]
Goal: [What success looks like]
Constraints: [Limitations]
Task: [Specific request]
```

**Example:**
```
Context: I'm a product manager at a B2B SaaS company (50 employees, Series A).
We're launching a new collaboration feature next month.

Goal: Create excitement among existing customers and drive adoption to 60% in Q1.

Constraints:
- Small marketing budget ($10K)
- No dedicated designer
- Must work with existing email tool (Mailchimp)

Task: Create a 3-email launch sequence with subject lines.
```

## 7. Iterative Refinement

**Self-Critique Pattern:**
```
[Initial request]

After providing your response, critique it and then provide an improved version.

Critique factors:
- Clarity
- Completeness  
- Actionability
- [Other relevant factors]
```

**Regeneration Pattern:**
```
Provide 3 different versions:
1. [Version optimized for X]
2. [Version optimized for Y]
3. [Version optimized for Z]

Then recommend which is best and why.
```

## 8. Constraints & Boundaries

**Define Boundaries:**
```
Must include: [Required elements]
Must NOT include: [Prohibited elements]
Word count: [Range]
Tone: [Specific tone]
Format: [Exact structure]
Focus on: [Specific aspects]
Ignore: [What not to address]
```

**Example:**
```
Write a LinkedIn post about our product launch.

Must include:
- Key benefit (saves time)
- Social proof (customer count)
- Clear CTA (try free)

Must NOT:
- Mention competitors by name
- Use technical jargon
- Include pricing

Word count: 150-200
Tone: Professional but conversational
Format: Hook + 3 bullet points + CTA
```

## 9. Quality Checklist

Before submitting a prompt, verify:
✓ Task is clearly stated
✓ Context provided where relevant
✓ Examples included (if complex)
✓ Format specified
✓ Constraints defined
✓ Tone indicated
✓ Success criteria clear

## 10. Common Patterns

**For Analysis:**
```
Analyze [X] and provide:
1. Summary (3 sentences)
2. Key insights (3-5 bullets)
3. Recommendations (prioritized)
4. Risks or considerations
```

**For Creation:**
```
Create [X] that:
- Achieves [goal]
- Targets [audience]
- Uses [format]
- Incorporates [elements]
```

**For Comparison:**
```
Compare [A] and [B] across:
- [Dimension 1]
- [Dimension 2]
- [Dimension 3]

Provide recommendation based on [criteria].
```
