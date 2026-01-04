---
name: advanced-prompt-techniques
description: Advanced prompting including context engineering, prompt chaining, prompt evaluation, meta-prompting, and AI prompt library management. Use when building complex AI workflows, optimizing prompts for production, managing team prompt libraries, or creating prompts that generate prompts.
---

# Advanced Prompt Techniques

Advanced methods for complex AI workflows and prompt optimization.

## 1. Prompt Chaining

Break complex tasks into sequential prompts:

**Step 1:** Research and gather information
**Step 2:** Analyze and synthesize findings
**Step 3:** Create structured output
**Step 4:** Refine and optimize

Example chain:
```
Prompt 1: "Research the top 5 competitors in [market]. For each, list: positioning, key features, pricing, target audience."

Prompt 2: "Based on the competitive analysis, identify gaps and opportunities. What are customers asking for that competitors don't provide?"

Prompt 3: "Using the identified opportunities, create a differentiation strategy with 3 unique value propositions."

Prompt 4: "Convert the strategy into messaging: headline, subheadline, and 3 benefit statements."
```

## 2. Context Engineering

**Context Window Management:**
- Load only relevant information
- Use progressive disclosure
- Summarize when context grows large
- Remove outdated context

**Hierarchical Context:**
```
Layer 1: Core context (always present)
- Project goals
- Target audience
- Key constraints

Layer 2: Task context (loaded as needed)
- Specific requirements
- Examples
- Reference materials

Layer 3: Working context (dynamic)
- Previous iterations
- Feedback
- Current focus
```

## 3. Meta-Prompting

Prompts that create prompts:

```
Create a prompt template for [use case].

The template should:
- Include placeholders for [variables]
- Guide the AI to produce [output type]
- Enforce [constraints]
- Use [tone/style]

Provide:
1. The template with clear [PLACEHOLDERS]
2. An example with placeholders filled in
3. Usage instructions
```

## 4. Prompt Evaluation Framework

**Scoring Criteria:**
- Clarity: Are instructions unambiguous?
- Completeness: Is all necessary information included?
- Efficiency: Is it as concise as possible?
- Effectiveness: Does it reliably produce desired output?
- Robustness: Does it handle edge cases?

**A/B Testing Prompts:**
```
Version A: [Prompt variation 1]
Version B: [Prompt variation 2]

Test with 10 sample inputs
Compare outputs on:
- Quality
- Consistency
- Speed
- Error rate

Document winner and why
```

## 5. Prompt Library Management

**Template Structure:**
```
Name: [Template name]
Category: [Analysis/Creation/Optimization/etc.]
Use Case: [When to use this]

Variables:
- [VAR1]: Description
- [VAR2]: Description

Template:
[Prompt with [VARIABLES] marked]

Example:
[Filled-in example]

Performance Notes:
- Works best with: [Model/approach]
- Common issues: [Known problems]
- Last tested: [Date]
```

**Organization:**
- By use case (content/product/analysis)
- By complexity (simple/intermediate/advanced)
- By team (marketing/product/engineering)
- Version control for iterations

## 6. Self-Improvement Loops

**Pattern:**
```
1. Generate initial output
2. Critique output (identify weaknesses)
3. Generate improved version  
4. Validate improvement
5. Iterate if needed (max 2-3 times)
```

## 7. Ensemble Prompting

Multiple approaches to same problem:

```
Approach 1: Analytical (data-driven)
Approach 2: Creative (exploratory)
Approach 3: Practical (implementation-focused)

Compare results and synthesize best elements.
```

## 8. Context Compression

When hitting context limits:

**Summarization:**
```
Previous context summary:
- Key decisions: [list]
- Current state: [description]
- Open questions: [list]
```

**Reference System:**
```
Instead of full documents, use:
Document A: [Brief description] - Key points: [1,2,3]
Document B: [Brief description] - Key points: [1,2,3]

"Refer to Document A, point 2 for..."
```
