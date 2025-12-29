# Video Ad Analysis Prompt

**TL;DR**: Analyze video ad for foundation elements (UVP, audience, style, funnel) + video-specific elements (hook, transcription, scenes, audio, motion, narrative). Return comprehensive JSON.

## Input

1. Video file
2. Ad details JSON:
```json
{
  "call_to_action_title": "string",
  "call_to_action_Description": "string",
  "call_to_action_button": "string",
  "video_url": "string",
  "ad_copy": "string",
  "about_ad": {"text-sm": "string", "about-ad__paying-entity": "string"},
  "ad_impressions": "string",
  "ad_targeting": "string",
  "video_num": "string",
  "ad_link": "string"
}
```

## Analysis Framework

### A. FOUNDATION (Same as Image Ads)

**1. Target Audience**
Infer from title, copy, about_ad, video content, voiceover style, visuals. Use ad_targeting if available.

**2. UVP/USP**
Core benefit communicated through narrative arc.

**3. Style**
- Creative style/tone (minimalist, energetic, corporate, documentary)
- Color palette evolution
- Typography for on-screen text
- Production quality & visual aesthetic
- Brand-audience alignment

**4. Funnel & Archetype**
- Stage: Top / Middle / Bottom
- Archetype: Testimonial, Thought Leadership, Product Demo, Data-Backed Insight, Limited-Time Offer, Case Study, Event Invitation, Lead Magnet, Competitive Comparison, Founder Story, Trend-Jacking, Employee Spotlight, Checklist/How-To, Poll/Survey, Pain-Point→Solution, Explainer Video, Brand Story

**5. Compositional Elements** (select all)
Title, logo, CTA, supporting text, textual/minimal, user-focused, VS/split, minimal/elegant, product screens/UI, full-frame imagery, illustration/animation, big number/stat, point-out, talking head, screen recording, motion graphics, live action, mixed media

---

### B. VIDEO-SPECIFIC

**6. Fundamentals**
- Duration (seconds)
- Pacing: Fast-cut / Medium / Slow-burn
- Optimal length: Yes/No + why
- Aspect ratio: 16:9 / 1:1 / 9:16 / 4:5
- Production quality: Professional / Semi-professional / UGC-style / Low-budget
- Video type: Live-action / Animation / Screen recording / Mixed / Stop-motion / AI-generated

**7. Opening Hook (First 3 Seconds) - CRITICAL**
- Type: Visual shock, Question, Bold claim, Problem, Curiosity gap, Direct benefit, Story, Other
- Attention score: 1-10
- Establishes relevance: Y/N
- Aligns with pain points: Y/N
- Full description of first 3 seconds

**8. Transcription**

*8a. Spoken Content*
Word-for-word with timing:
```
[00:00-00:03] "Opening statement"
[00:03-00:08] "Next segment"
```

*8b. On-Screen Text*
All text with timing + styling:
```
[00:02] "HEADLINE" - Large, bold, centered
[00:05] "Supporting text" - Smaller, animated left
```

**9. Scene Breakdown**
```
Scene 1 [00:00-00:05]:
- Visual: <What's shown>
- Text: <On-screen text>
- Voiceover: <What's said>
- Message: <Key communication>
- Transition: <To next scene>
```

**10. Audio**

*10a. Music/Sound*
- Type: Upbeat / Corporate / Inspirational / Dramatic / None / Ambient
- Volume vs voiceover: Background / Equal / No music
- Effectiveness: Enhancement or distraction?
- Sound effects: List notable SFX

*10b. Voiceover*
- Present: Yes / No / Partial
- Gender: Male / Female / AI / Multiple
- Tone: Professional / Conversational / Energetic / Calm / Authoritative / Friendly
- Accent/dialect: If notable
- Pacing: Fast / Medium / Slow
- Effectiveness: Voice-brand-message fit?

**11. Motion & Animation**

*11a. Motion Style*
- Primary: Static / Subtle / Dynamic / Fast-paced / Smooth
- Camera: Fixed / Pan / Zoom / Tracking / Handheld / None
- Animation: Kinetic type / Object / Character / Transitions only

*11b. Transitions*
- Type: Cut / Fade / Wipe / Zoom / Slide / Custom
- Frequency: Every X seconds
- Effectiveness: Smooth / Jarring / Creative / Standard

*11c. Visual Effects*
- Effects: Overlays, filters, split screens, PIP, etc.
- Purpose: Emphasis / Branding / Style / Functional

**12. Narrative Flow**

*12a. Story Arc*
- Structure: Problem→Solution / Before→After / Step-by-step / Testimonial / Feature showcase / Other
- Progression: How narrative builds

*12b. Emotional Journey*
- Opening emotion
- Mid-video emotion
- Closing emotion
- Alignment: Match funnel stage & archetype?

*12c. Message Clarity*
- Primary message (one sentence)
- Reinforcement count
- Value prop timestamp

**13. CTA Strategy**

*13a. Timing*
- First CTA: Timestamp
- Final CTA: Timestamp
- Frequency: Count

*13b. Presentation*
- Visual CTA: How appears on screen
- Verbal CTA: What's said
- Clarity score: 1-10
- Creates urgency: Y/N + how

*13c. End Screen*
- Present: Y/N
- Duration: X seconds
- Elements: Logo, CTA, contact, social, etc.
- Effectiveness: Clear next steps?

**14. Visual Inventory**

*14a. Key Elements*
For each: description, flexibility (replaceable/not), duration/appearances

- Product screens
- Brand logo
- People shown
- B-roll footage

*14b. Company-Specific Assets*
Elements that MUST be real/company-provided (can't be invented):
```json
{
  "element": "product_interface_demo",
  "asset_type": "Screen recording",
  "reason": "Requires actual product",
  "timestamps": "[00:05-00:18]"
}
```

**15. Color**
- Brand colors (list)
- Main brand color + rationale
- Accent/highlighting colors
- Color psychology
- Color evolution throughout video
- Brand consistency
- Contrast/accessibility

---

### C. EFFECTIVENESS

**16. What's Working**
- Video strengths (overall effectiveness)
- Hook effectiveness
- Visual appeal (production quality, aesthetics)
- Messaging effectiveness (clarity, persuasiveness)
- Messaging framework (PAS, AIDA, StoryBrand, etc.)
- Audio effectiveness (voiceover, music, sound)
- Pacing & retention
- Audience appeal

**17. What Needs Improvement**
- Video production issues
- Hook weaknesses
- Messaging problems
- Pacing issues
- Audio issues
- Visual confusion
- Audience alignment issues
- CTA weaknesses

---

## Output JSON

```json
{
  "video_num": "Number assigned to the ad's video",
  "ad_link": "URL linking to the ad",

  "_SECTION_A_FOUNDATION": "======================",

  "CTA_title": "The headline or title of the ad",
  "CTA_area": "title only / title and button / title and description",
  "uvp_usp": "Core benefit or promise",
  "target_audience": "Description of intended audience",

  "style": {
    "tags": ["Style labels"],
    "style_description": "Full paragraph on creative style, tone, palette, typography",
    "brand_alignment": "Paragraph on style-brand-audience fit"
  },

  "funnel_stage": "Top / Middle / Bottom",
  "ad_archetype": "Primary archetype",
  "compositional_elements": "Comma-separated list of all relevant elements",

  "_SECTION_B_VIDEO_SPECIFIC": "======================",

  "video_fundamentals": {
    "duration_seconds": 0,
    "pacing": "Fast-cut / Medium / Slow-burn",
    "optimal_length": "Yes/No + brief explanation",
    "aspect_ratio": "16:9 / 1:1 / 9:16 / 4:5 / other",
    "production_quality": "Professional / Semi-professional / UGC-style / Low-budget",
    "video_type": "Live-action / Animation / Screen recording / Mixed / etc."
  },

  "opening_hook": {
    "hook_type": "Visual shock / Question / Bold claim / Problem / Curiosity / Benefit / Story / Other",
    "hook_effectiveness_score": 0,
    "establishes_relevance": true,
    "aligns_with_pain_points": true,
    "hook_description": "Full description of first 3 seconds"
  },

  "transcription": {
    "spoken_content": [
      {
        "timestamp": "00:00-00:03",
        "text": "Exact spoken words"
      }
    ],
    "on_screen_text": [
      {
        "timestamp": "00:02",
        "text": "Text content",
        "styling": "Description of how text appears"
      }
    ]
  },

  "scene_breakdown": [
    {
      "scene_number": 1,
      "timestamp": "00:00-00:05",
      "visual_description": "What's shown",
      "on_screen_text": "Any text visible",
      "voiceover_dialogue": "What's said",
      "key_message": "What this scene communicates",
      "transition": "How it transitions to next"
    }
  ],

  "audio_elements": {
    "music": {
      "type": "Upbeat / Corporate / Inspirational / Dramatic / None / Ambient",
      "volume_level": "Background / Equal / No music",
      "effectiveness": "Enhancement or distraction assessment",
      "sound_effects": ["List of notable sound effects"]
    },
    "voiceover": {
      "present": "Yes / No / Partial",
      "voice_gender": "Male / Female / AI / Multiple",
      "tone": "Professional / Conversational / etc.",
      "accent_dialect": "If notable",
      "pacing": "Fast / Medium / Slow",
      "effectiveness": "Voice-brand-message fit assessment"
    }
  },

  "motion_animation": {
    "motion_style": "Static / Subtle / Dynamic / Fast-paced / Smooth",
    "camera_movement": "Fixed / Pan / Zoom / Tracking / Handheld / None",
    "animation_style": "Type of animation if applicable",
    "transitions": {
      "type": "Cut / Fade / Wipe / Zoom / Slide / Custom",
      "frequency": "Every X seconds",
      "effectiveness": "Assessment"
    },
    "visual_effects": {
      "effects_used": ["List notable effects"],
      "effect_purpose": "Emphasis / Branding / Style / Functional"
    }
  },

  "narrative_flow": {
    "story_arc": {
      "structure_type": "Problem→Solution / Before→After / etc.",
      "progression": "How narrative builds"
    },
    "emotional_journey": {
      "opening_emotion": "Emotion evoked at start",
      "mid_video_emotion": "Emotional shift",
      "closing_emotion": "Final emotional state",
      "alignment": "Does emotional arc match funnel stage?"
    },
    "message_clarity": {
      "primary_message": "Single sentence summary",
      "reinforcement_count": 0,
      "value_prop_timestamp": "When viewer understands value"
    }
  },

  "cta_strategy": {
    "timing": {
      "first_cta": "Timestamp",
      "final_cta": "Timestamp",
      "frequency": "Number of appearances"
    },
    "presentation": {
      "visual_cta": "How CTA appears on screen",
      "verbal_cta": "What's said to prompt action",
      "clarity_score": 0,
      "creates_urgency": "Yes/No + how"
    },
    "end_screen": {
      "present": true,
      "duration_seconds": 0,
      "elements": ["Logo, CTA, contact info, etc."],
      "effectiveness": "Clear next steps assessment"
    }
  },

  "visual_content_inventory": {
    "key_elements": {
      "product_screens": {
        "description": "Product visuals shown",
        "flexibility": "Not replaceable / Semi / Replaceable",
        "duration_visible": "X seconds"
      },
      "brand_logo": {
        "description": "Logo appearance and placement",
        "flexibility": "Not replaceable",
        "appearances": 0
      },
      "people_shown": {
        "description": "Who appears, their role",
        "flexibility": "Assessment",
        "duration_visible": "X seconds"
      },
      "b_roll_footage": {
        "description": "Supplementary footage",
        "flexibility": "Highly replaceable",
        "purpose": "What it illustrates"
      }
    },
    "company_specific_assets": [
      {
        "element": "Asset name",
        "asset_type": "Type of asset required",
        "reason": "Why it must be real/company-specific",
        "timestamps": "When it appears"
      }
    ]
  },

  "colors": {
    "brand_colors": ["List of brand colors"],
    "main_brand_color": "Primary brand color",
    "main_color_rationale": "Why this is the main brand color",
    "accent_colors": ["Highlighting colors"],
    "color_psychology": "Emotions evoked",
    "color_evolution": "Does palette shift throughout?",
    "brand_consistency": "Alignment with brand guidelines",
    "contrast_accessibility": "Sufficient contrast assessment"
  },

  "_SECTION_C_EFFECTIVENESS": "======================",

  "whats_working": {
    "video_strengths": "Paragraph on overall video effectiveness",
    "hook_effectiveness": "Paragraph on opening success",
    "visual_appeal": "Paragraph on production quality and aesthetics",
    "messaging_effectiveness": "Paragraph on message clarity and persuasiveness",
    "messaging_framework": "What framework is used and its effectiveness",
    "audio_effectiveness": "Paragraph on voiceover, music, sound quality",
    "pacing_retention": "Paragraph on engagement throughout",
    "audience_appeal": "Paragraph on target audience resonance"
  },

  "what_needs_improvement": {
    "video_production_issues": "Production/technical weaknesses",
    "hook_weaknesses": "Opening improvement opportunities",
    "messaging_problems": "Copy and value prop issues",
    "pacing_issues": "Speed, dead spots, dragging sections",
    "audio_issues": "Voiceover, music, mixing problems",
    "visual_confusion": "Unclear visuals, text overload, style inconsistency",
    "audience_alignment_issues": "Audience mismatch points",
    "cta_weaknesses": "Next steps clarity, urgency, placement issues"
  }
}
```

## Execution Guidelines

- Transcribe ALL dialogue and on-screen text completely
- Include timestamps for scenes, text, dialogue, key moments
- Write full paragraphs for effectiveness sections
- Assess replaceability for every visual element
- Analyze entire video from first to last frame
- Use only provided data
- Note missing data (empty fields)
- Return valid JSON
