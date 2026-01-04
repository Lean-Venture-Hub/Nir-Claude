# Skills Quick Reference Card

## When to Use Each Skill

### Product Management

| Skill | Use When... |
|-------|------------|
| **product-documentation** | Writing PRDs, user stories, roadmaps, status updates, backlog items |
| **product-strategy-framework** | Prioritizing features, evaluating opportunities, planning GTM, competitive analysis |
| **user-research-insights** | Analyzing research, creating personas, mapping journeys, applying JTBD |
| **product-metrics-analytics** | Defining metrics, tracking KPIs, analyzing data, setting OKRs |

### Content & Communication

| Skill | Use When... |
|-------|------------|
| **content-creation-suite** | Writing any content: blogs, social, emails, docs, microcopy |
| **brand-voice-messaging** | Establishing brand voice, storytelling, persuasive copywriting |
| **seo-content-strategy** | Optimizing for search, keyword research, content planning |

### Prompt Engineering

| Skill | Use When... |
|-------|------------|
| **prompt-engineering-master** | Crafting any AI prompt, improving outputs, basic techniques |
| **advanced-prompt-techniques** | Complex workflows, chaining prompts, managing context, meta-prompting |

### Design & UX

| Skill | Use When... |
|-------|------------|
| **design-thinking-facilitator** | Running workshops, ideation sessions, design sprints, facilitation |
| **user-experience-research** | Journey mapping, usability testing, UX research, IA planning |
| **visual-interaction-design** | Designing interfaces, visual assets, interactions, layouts |
| **design-system-standards** | Building design systems, accessibility, critiques, dev handoffs |

### Cross-Functional

| Skill | Use When... |
|-------|------------|
| **prototyping-testing-suite** | Building prototypes, testing ideas, beta programs, gathering feedback |
| **collaboration-integration** | Cross-team work, handoffs, alignment, collaboration patterns |

---

## Quick Command Examples

### Product Work
```
"Use product-documentation to create a PRD for [feature]"
"Apply product-strategy-framework to prioritize these 10 features using RICE"
"With user-research-insights, create 3 personas from this interview data"
"Using product-metrics-analytics, set up OKRs for Q2"
```

### Content Work
```
"Use content-creation-suite to write a blog post about [topic]"
"Apply brand-voice-messaging to create our brand voice guidelines"
"With seo-content-strategy, plan a 12-week content calendar for [topic]"
```

### Prompting Work
```
"Use prompt-engineering-master to improve this prompt: [prompt]"
"Apply advanced-prompt-techniques to chain these 3 complex tasks"
```

### Design Work
```
"Use design-thinking-facilitator to plan a 5-day design sprint"
"Apply user-experience-research to create a journey map for [user]"
"With visual-interaction-design, design a distinctive dashboard UI"
"Using design-system-standards, create component documentation"
```

### Testing & Collaboration
```
"Use prototyping-testing-suite to plan a usability test for [feature]"
"Apply collaboration-integration to create PM-to-Design handoff checklist"
```

---

## Skill Stacking Examples

**Complete Product Launch:**
```
Use product-documentation for PRD + 
product-strategy-framework for GTM + 
content-creation-suite for launch content +
prototyping-testing-suite for beta program
```

**Content Marketing Campaign:**
```
Use brand-voice-messaging for guidelines +
content-creation-suite for content creation +
seo-content-strategy for optimization
```

**Design Project:**
```
Use design-thinking-facilitator for process +
user-experience-research for research +
visual-interaction-design for execution +
prototyping-testing-suite for testing
```

**AI Product Development:**
```
Use prompt-engineering-master for core prompts +
advanced-prompt-techniques for optimization +
product-documentation for specs +
prototyping-testing-suite for testing
```

---

## Installation Commands

### Claude.ai
Upload each folder as a .skill file through Settings → Skills

### Claude Code
```bash
# Install all skills
cd nir-skills-library
for dir in */; do claude plugins install "${dir}"; done

# Or install individually
claude plugins install ./01-product-documentation
```

### API
```python
# Load specific skills for a task
skills=["product-documentation", "product-strategy-framework"]
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Skill not activating | Reference it by name explicitly |
| Too slow | Start with 4-5 skills, add more as needed |
| Wrong skill activates | Be specific: "Using [skill-name]..." |
| Need custom workflow | Edit SKILL.md and add your templates |

---

## Most Common Combinations

1. **PM Daily Work:** product-documentation + product-strategy-framework
2. **Content Marketing:** content-creation-suite + seo-content-strategy  
3. **UX Research:** user-research-insights + user-experience-research
4. **AI Development:** prompt-engineering-master + advanced-prompt-techniques
5. **Design Projects:** design-thinking-facilitator + visual-interaction-design

---

Print this card for quick reference!
