# JSON Output Examples for 4c and 4e Prompts

## 4c - Video Ad Analysis - Example 1: SaaS Product Demo

```json
{
  "video_num": "v_001",
  "ad_link": "https://linkedin.com/ads/example-saas-demo",

  "_SECTION_A_FOUNDATION": "======================",

  "CTA_title": "Transform Your Sales Pipeline in 30 Days",
  "CTA_area": "title and button",
  "uvp_usp": "AI-powered sales automation that doubles qualified meetings without hiring SDRs",
  "target_audience": "B2B sales leaders at 50-500 person companies struggling with pipeline generation and SDR productivity",

  "style": {
    "tags": ["Modern", "Professional", "Clean", "Data-driven"],
    "style_description": "Contemporary corporate aesthetic with bright blues and whites, clean sans-serif typography (Montserrat), smooth transitions, and polished screen recordings showcasing product UI with subtle drop shadows and glassmorphic elements",
    "brand_alignment": "Professional production quality signals enterprise credibility while maintaining approachability through conversational voiceover and real-world use cases, perfectly aligned with mid-market SaaS buyer expectations"
  },

  "funnel_stage": "Middle",
  "ad_archetype": "Product Demo",
  "compositional_elements": "Title, logo, CTA, product screens/UI, motion graphics, screen recording, big number/stat, minimal/elegant",

  "_SECTION_B_VIDEO_SPECIFIC": "======================",

  "video_fundamentals": {
    "duration_seconds": 32,
    "pacing": "Medium",
    "optimal_length": "Yes - 30-35 seconds is ideal for LinkedIn attention span while showing 3 key features",
    "aspect_ratio": "1:1",
    "production_quality": "Professional",
    "video_type": "Mixed - Screen recording with motion graphics overlays"
  },

  "opening_hook": {
    "hook_type": "Problem",
    "hook_effectiveness_score": 8,
    "establishes_relevance": true,
    "aligns_with_pain_points": true,
    "hook_description": "Opens with frustrated sales leader staring at empty pipeline dashboard while text overlay reads '73% of sales time wasted on unqualified leads' - immediately resonates with target audience pain"
  },

  "transcription": {
    "spoken_content": [
      {
        "timestamp": "00:00-00:04",
        "text": "Your SDRs spend 73% of their time chasing dead ends"
      },
      {
        "timestamp": "00:04-00:09",
        "text": "What if AI could identify your best prospects before your competitors do?"
      },
      {
        "timestamp": "00:09-00:16",
        "text": "Pipeline AI analyzes 50 million B2B signals daily to surface accounts ready to buy"
      },
      {
        "timestamp": "00:16-00:23",
        "text": "Automatically prioritizes leads by intent, enriches contacts, and generates personalized outreach"
      },
      {
        "timestamp": "00:23-00:28",
        "text": "Teams using Pipeline AI book 2.3x more qualified meetings in their first 30 days"
      },
      {
        "timestamp": "00:28-00:32",
        "text": "Stop chasing. Start closing. Book your demo today"
      }
    ],
    "on_screen_text": [
      {
        "timestamp": "00:01",
        "text": "73% of sales time wasted",
        "styling": "Large white text, bold, centered on dark overlay"
      },
      {
        "timestamp": "00:10",
        "text": "50M B2B signals analyzed daily",
        "styling": "Animated counter, blue accent color, medium size"
      },
      {
        "timestamp": "00:24",
        "text": "2.3x more qualified meetings",
        "styling": "Large bold number with subtle glow effect, centered"
      },
      {
        "timestamp": "00:29",
        "text": "Book Your Demo",
        "styling": "CTA button, bright blue, white text, rounded corners"
      }
    ]
  },

  "scene_breakdown": [
    {
      "scene_number": 1,
      "timestamp": "00:00-00:04",
      "visual_description": "Frustrated sales leader at desk, empty pipeline dashboard visible on screen",
      "on_screen_text": "73% of sales time wasted",
      "voiceover_dialogue": "Your SDRs spend 73% of their time chasing dead ends",
      "key_message": "Establishes the pain point - wasted time on unqualified leads",
      "transition": "Fade to product interface"
    },
    {
      "scene_number": 2,
      "timestamp": "00:04-00:09",
      "visual_description": "Product dashboard appears with AI icon, animated data flowing",
      "on_screen_text": "Pipeline AI",
      "voiceover_dialogue": "What if AI could identify your best prospects before your competitors do?",
      "key_message": "Introduces solution with competitive advantage angle",
      "transition": "Zoom into data visualization"
    },
    {
      "scene_number": 3,
      "timestamp": "00:09-00:16",
      "visual_description": "Animated visualization of 50M signals being analyzed, heat map of target accounts",
      "on_screen_text": "50M B2B signals analyzed daily",
      "voiceover_dialogue": "Pipeline AI analyzes 50 million B2B signals daily to surface accounts ready to buy",
      "key_message": "Quantifies capability and establishes credibility through scale",
      "transition": "Slide to feature showcase"
    },
    {
      "scene_number": 4,
      "timestamp": "00:16-00:23",
      "visual_description": "Screen recording of product: lead scoring, contact enrichment, and AI-generated email templates",
      "on_screen_text": "Auto-prioritize • Enrich • Personalize",
      "voiceover_dialogue": "Automatically prioritizes leads by intent, enriches contacts, and generates personalized outreach",
      "key_message": "Demonstrates three key automated workflows",
      "transition": "Cut to results screen"
    },
    {
      "scene_number": 5,
      "timestamp": "00:23-00:28",
      "visual_description": "Graph showing meeting volume increase, happy sales team in background",
      "on_screen_text": "2.3x more qualified meetings",
      "voiceover_dialogue": "Teams using Pipeline AI book 2.3x more qualified meetings in their first 30 days",
      "key_message": "Provides social proof and quantified outcome",
      "transition": "Fade to end card"
    },
    {
      "scene_number": 6,
      "timestamp": "00:28-00:32",
      "visual_description": "Clean end card with logo, CTA button, and company tagline",
      "on_screen_text": "Book Your Demo",
      "voiceover_dialogue": "Stop chasing. Start closing. Book your demo today",
      "key_message": "Clear call-to-action with memorable tagline",
      "transition": "N/A - Final frame"
    }
  ],

  "audio_elements": {
    "music": {
      "type": "Corporate",
      "volume_level": "Background",
      "effectiveness": "Subtle upbeat instrumental supports professional tone without competing with voiceover, building momentum toward CTA",
      "sound_effects": ["Whoosh on transitions", "Soft 'ping' when numbers appear", "Subtle click on CTA button"]
    },
    "voiceover": {
      "present": "Yes",
      "voice_gender": "Female",
      "tone": "Professional yet conversational",
      "accent_dialect": "General American",
      "pacing": "Medium",
      "effectiveness": "Clear articulation and confident tone builds credibility while remaining approachable; vocal energy rises slightly toward CTA creating natural momentum"
    }
  },

  "motion_animation": {
    "motion_style": "Dynamic",
    "camera_movement": "Zoom",
    "animation_style": "Kinetic type and object animation - text slides in, numbers count up, UI elements highlight",
    "transitions": {
      "type": "Fade and Slide",
      "frequency": "Every 5-7 seconds",
      "effectiveness": "Smooth transitions maintain professional feel while keeping visual interest high"
    },
    "visual_effects": {
      "effects_used": ["Glassmorphic overlays on text", "Subtle glow on key numbers", "Animated data flow visualization", "Highlighted UI elements with pulse effect"],
      "effect_purpose": "Emphasis - draws eye to key metrics and product capabilities"
    }
  },

  "narrative_flow": {
    "story_arc": {
      "structure_type": "Problem→Solution",
      "progression": "Opens with relatable pain (wasted sales time), introduces AI solution, demonstrates capabilities with scale proof, shows product features in action, validates with results, closes with actionable CTA"
    },
    "emotional_journey": {
      "opening_emotion": "Frustration - empathy with current struggle",
      "mid_video_emotion": "Curiosity and hope - AI capability seems powerful",
      "closing_emotion": "Confidence and urgency - proven results drive desire to act",
      "alignment": "Yes - emotional arc perfectly matches middle-funnel goal of moving from problem-aware to solution-interested"
    },
    "message_clarity": {
      "primary_message": "AI-powered sales automation identifies ready-to-buy accounts and automates outreach to book 2.3x more qualified meetings",
      "reinforcement_count": 3,
      "value_prop_timestamp": "00:16 - by this point viewer understands both what it does and the quantified outcome"
    }
  },

  "cta_strategy": {
    "timing": {
      "first_cta": "00:04 - implicit CTA via rhetorical question",
      "final_cta": "00:28-00:32",
      "frequency": "2 - soft hook at beginning, strong explicit CTA at end"
    },
    "presentation": {
      "visual_cta": "Bright blue button with white text 'Book Your Demo' on clean end card, prominent and centered",
      "verbal_cta": "Stop chasing. Start closing. Book your demo today",
      "clarity_score": 9,
      "creates_urgency": "Yes - implied competitive disadvantage ('before your competitors do') and time-bound result ('first 30 days')"
    },
    "end_screen": {
      "present": true,
      "duration_seconds": 4,
      "elements": ["Company logo", "CTA button", "Tagline: 'Stop chasing. Start closing'"],
      "effectiveness": "Very clear - single action, bold button, memorable tagline reinforces value prop"
    }
  },

  "visual_content_inventory": {
    "key_elements": {
      "product_screens": {
        "description": "Dashboard UI showing lead scoring, contact enrichment panel, AI email composer",
        "flexibility": "Not replaceable - requires actual product interface",
        "duration_visible": "15 seconds total across scenes 2-4"
      },
      "brand_logo": {
        "description": "Blue and white logo appears in corner throughout and prominently on end card",
        "flexibility": "Not replaceable",
        "appearances": 7
      },
      "people_shown": {
        "description": "Sales leader in opening scene, happy sales team in results scene",
        "flexibility": "Replaceable - stock footage or re-shoot with different actors",
        "duration_visible": "8 seconds total"
      },
      "b_roll_footage": {
        "description": "Abstract data visualization, animated graphs and charts",
        "flexibility": "Highly replaceable",
        "purpose": "Illustrates AI analysis and scale of signal processing"
      }
    },
    "company_specific_assets": [
      {
        "element": "product_interface_screens",
        "asset_type": "Screen recording of actual product",
        "reason": "Shows proprietary UI - cannot be faked or invented, must be real product screens",
        "timestamps": "[00:09-00:23]"
      },
      {
        "element": "company_logo_and_branding",
        "asset_type": "Brand assets",
        "reason": "Company-specific visual identity required throughout",
        "timestamps": "[00:00-00:32] - present throughout"
      },
      {
        "element": "performance_metrics",
        "asset_type": "Customer data/results",
        "reason": "2.3x claim requires real customer data for credibility",
        "timestamps": "[00:23-00:28]"
      }
    ]
  },

  "colors": {
    "brand_colors": ["#0066FF (primary blue)", "#FFFFFF (white)", "#F8F9FA (light gray)", "#1A1A1A (dark gray/black)"],
    "main_brand_color": "#0066FF",
    "main_color_rationale": "Bright blue dominates all key moments (logo, CTA button, accent highlights) and appears in 80% of frames, signaling trust, technology, and professionalism",
    "accent_colors": ["#00D9FF (cyan for data visualizations)", "#FF6B35 (warm orange for heat map highlights)"],
    "color_psychology": "Blue evokes trust and intelligence (appropriate for AI product), white creates clean professional space, cyan adds energy to data visualizations, orange creates visual interest without overwhelming",
    "color_evolution": "Starts darker/muted in problem scene, brightens as solution introduced, peaks with vibrant blues and data visualizations in feature showcase, settles into clean blue/white for end card",
    "brand_consistency": "Strong - blue consistently used for all branded moments, creating clear visual association with company",
    "contrast_accessibility": "Excellent - white text on dark backgrounds, dark text on white/light backgrounds, CTA button has 7.2:1 contrast ratio"
  },

  "_SECTION_C_EFFECTIVENESS": "======================",

  "whats_working": {
    "video_strengths": "Extremely effective product demo that balances emotion (opening frustration) with logic (quantified capabilities and results), maintains engagement through varied pacing and visual interest, and delivers clear value proposition within optimal time frame for LinkedIn viewing",
    "hook_effectiveness": "Strong opening hook immediately resonates with target audience pain point using specific statistic (73%) that feels credible and research-backed, visual of frustrated sales leader creates instant identification with problem",
    "visual_appeal": "Professional production quality with polished screen recordings, smooth animations, and contemporary design aesthetic signals enterprise credibility; glassmorphic effects and data visualizations feel modern without being gimmicky",
    "messaging_effectiveness": "Crystal clear Problem→Solution→Proof structure with quantified claims at each stage (50M signals, 2.3x meetings, 30 days); every sentence advances the narrative and builds case for product",
    "messaging_framework": "Classic PAS (Pain-Agitate-Solution) executed excellently - opens with pain (wasted time), agitates with competitive angle ('before competitors'), resolves with solution and proof",
    "audio_effectiveness": "Voiceover pacing matches visual tempo perfectly, professional yet approachable tone builds trust, background music enhances without distracting, sound effects provide satisfying punctuation to key moments",
    "pacing_retention": "Medium pacing with scene changes every 5-7 seconds maintains interest without overwhelming; strategic use of pauses after key stats allows information to land before moving forward",
    "audience_appeal": "Speaks directly to sales leader pain points (wasted SDR time, unqualified leads, competitive pressure) with language and metrics this persona cares about; product UI shown reinforces credibility for tech-savvy buyers"
  },

  "what_needs_improvement": {
    "video_production_issues": "None significant - production quality is consistently high throughout",
    "hook_weaknesses": "Hook could be stronger with actual person speaking the stat rather than just text overlay - voice earlier would increase immediate engagement",
    "messaging_problems": "Could benefit from brief customer quote or logo in results scene to add social proof beyond self-reported metrics",
    "pacing_issues": "Feature showcase scene (00:16-00:23) feels slightly rushed trying to cover three capabilities - could focus on one key differentiator instead",
    "audio_issues": "Music is generic corporate stock - custom audio branding could increase memorability",
    "visual_confusion": "Data visualization in scene 3 is visually interesting but abstract - showing actual account list with scores might be more concrete and credible",
    "audience_alignment_issues": "End card tagline 'Stop chasing. Start closing' is catchy but slightly generic - could be more specific to AI/automation value prop",
    "cta_weaknesses": "Single CTA option (book demo) may be too high-commitment for cold traffic - could benefit from softer alternative like 'See How It Works' for top-funnel viewers"
  }
}
```

## 4c - Video Ad Analysis - Example 2: Customer Testimonial

```json
{
  "video_num": "v_002",
  "ad_link": "https://linkedin.com/ads/example-testimonial",

  "_SECTION_A_FOUNDATION": "======================",

  "CTA_title": "How Acme Corp Cut Support Costs by 60% in 90 Days",
  "CTA_area": "title and description",
  "uvp_usp": "Customer support automation that delivers enterprise ROI within one quarter",
  "target_audience": "Customer success and support leaders at B2B SaaS companies experiencing scaling pains with ticket volume and support costs",

  "style": {
    "tags": ["Authentic", "Documentary", "Professional", "Customer-centric"],
    "style_description": "Documentary-style testimonial with natural office setting, authentic interview framing, minimal color grading preserving real environment, clean lower-third graphics in brand purple, and subtle B-roll of product in use",
    "brand_alignment": "Authentic production style (not overly polished) builds trust and relatability, while clean graphics and professional editing maintain enterprise credibility - perfect for showcasing real customer success"
  },

  "funnel_stage": "Bottom",
  "ad_archetype": "Testimonial",
  "compositional_elements": "Title, logo, CTA, supporting text, talking head, product screens/UI, minimal/elegant, big number/stat",

  "_SECTION_B_VIDEO_SPECIFIC": "======================",

  "video_fundamentals": {
    "duration_seconds": 45,
    "pacing": "Slow-burn",
    "optimal_length": "Yes - 45 seconds allows customer to tell complete story with before/after/results while remaining within LinkedIn's sweet spot for bottom-funnel content",
    "aspect_ratio": "16:9",
    "production_quality": "Semi-professional",
    "video_type": "Live-action with screen recording inserts"
  },

  "opening_hook": {
    "hook_type": "Direct benefit",
    "hook_effectiveness_score": 9,
    "establishes_relevance": true,
    "aligns_with_pain_points": true,
    "hook_description": "Opens with customer's bold claim to camera: 'We cut our support costs by 60% in the first 90 days' while graphic shows $240K → $96K cost reduction - immediately quantifies value for similar buyers"
  },

  "transcription": {
    "spoken_content": [
      {
        "timestamp": "00:00-00:05",
        "text": "We cut our support costs by 60% in the first 90 days using SupportAI"
      },
      {
        "timestamp": "00:05-00:12",
        "text": "Before SupportAI, we had 12 support agents handling 8,000 tickets monthly. Response times were over 24 hours and customers were frustrated"
      },
      {
        "timestamp": "00:12-00:20",
        "text": "SupportAI's automation handles 70% of our repetitive tickets instantly - password resets, account questions, basic troubleshooting"
      },
      {
        "timestamp": "00:20-00:28",
        "text": "Our team now focuses on complex issues that actually need human expertise. Response time dropped to under 2 hours, CSAT jumped from 72% to 91%"
      },
      {
        "timestamp": "00:28-00:35",
        "text": "The ROI was immediate. We went from 12 agents to 7 without sacrificing quality. Actually, quality improved dramatically"
      },
      {
        "timestamp": "00:35-00:40",
        "text": "If you're drowning in support tickets, SupportAI pays for itself in the first month"
      },
      {
        "timestamp": "00:40-00:45",
        "text": "It's the best investment we've made in our customer experience stack"
      }
    ],
    "on_screen_text": [
      {
        "timestamp": "00:02",
        "text": "Sarah Chen, VP Customer Success | Acme Corp",
        "styling": "Lower third - white text on semi-transparent purple bar"
      },
      {
        "timestamp": "00:03",
        "text": "$240K → $96K (60% reduction)",
        "styling": "Large white text with arrow, top right corner"
      },
      {
        "timestamp": "00:14",
        "text": "70% of tickets automated",
        "styling": "Medium purple text, centered overlay"
      },
      {
        "timestamp": "00:22",
        "text": "CSAT: 72% → 91%",
        "styling": "Animated stat with green arrow, right side"
      },
      {
        "timestamp": "00:30",
        "text": "12 agents → 7 agents | Quality ↑",
        "styling": "Side-by-side comparison with upward arrow"
      },
      {
        "timestamp": "00:42",
        "text": "See How SupportAI Works",
        "styling": "CTA button, purple background, white text"
      }
    ]
  },

  "scene_breakdown": [
    {
      "scene_number": 1,
      "timestamp": "00:00-00:05",
      "visual_description": "Sarah Chen (VP Customer Success) speaking to camera in modern office, confident posture",
      "on_screen_text": "Sarah Chen, VP Customer Success | Acme Corp + $240K → $96K",
      "voiceover_dialogue": "We cut our support costs by 60% in the first 90 days using SupportAI",
      "key_message": "Establishes credibility (real person, real company, real title) and quantified result immediately",
      "transition": "Cut to wider shot"
    },
    {
      "scene_number": 2,
      "timestamp": "00:05-00:12",
      "visual_description": "B-roll of busy support team at computers, cut with Sarah continuing interview",
      "on_screen_text": "Before: 12 agents, 8K tickets/month, 24hr response time",
      "voiceover_dialogue": "Before SupportAI, we had 12 support agents handling 8,000 tickets monthly. Response times were over 24 hours and customers were frustrated",
      "key_message": "Paints 'before' picture with specific metrics that buyers can compare to their own situation",
      "transition": "Fade to product screen"
    },
    {
      "scene_number": 3,
      "timestamp": "00:12-00:20",
      "visual_description": "Screen recording of SupportAI dashboard showing automated ticket resolution, workflow automation interface",
      "on_screen_text": "70% of tickets automated",
      "voiceover_dialogue": "SupportAI's automation handles 70% of our repetitive tickets instantly - password resets, account questions, basic troubleshooting",
      "key_message": "Shows product in action and explains what gets automated (helps buyers assess fit)",
      "transition": "Cut back to Sarah"
    },
    {
      "scene_number": 4,
      "timestamp": "00:20-00:28",
      "visual_description": "Sarah speaking, intercut with B-roll of support agents working calmly (less frantic than earlier B-roll)",
      "on_screen_text": "CSAT: 72% → 91%",
      "voiceover_dialogue": "Our team now focuses on complex issues that actually need human expertise. Response time dropped to under 2 hours, CSAT jumped from 72% to 91%",
      "key_message": "Quantifies improvement across multiple metrics (speed, satisfaction, employee experience)",
      "transition": "Slow zoom on Sarah"
    },
    {
      "scene_number": 5,
      "timestamp": "00:28-00:35",
      "visual_description": "Close-up of Sarah emphasizing point with hand gesture, passionate delivery",
      "on_screen_text": "12 agents → 7 agents | Quality ↑",
      "voiceover_dialogue": "The ROI was immediate. We went from 12 agents to 7 without sacrificing quality. Actually, quality improved dramatically",
      "key_message": "Addresses potential objection (reducing headcount) by emphasizing quality improvement",
      "transition": "Cut to medium shot"
    },
    {
      "scene_number": 6,
      "timestamp": "00:35-00:45",
      "visual_description": "Sarah delivering final recommendation directly to camera, then end card with logo and CTA",
      "on_screen_text": "See How SupportAI Works",
      "voiceover_dialogue": "If you're drowning in support tickets, SupportAI pays for itself in the first month. It's the best investment we've made in our customer experience stack",
      "key_message": "Peer recommendation from credible source creates strong social proof for similar buyers",
      "transition": "Fade to end card"
    }
  ],

  "audio_elements": {
    "music": {
      "type": "None",
      "volume_level": "No music",
      "effectiveness": "Intentional absence of music increases authenticity and allows Sarah's voice to carry full emotional weight - appropriate for testimonial format",
      "sound_effects": ["Ambient office sounds in B-roll (very subtle)", "Soft transition whoosh between scenes"]
    },
    "voiceover": {
      "present": "No",
      "voice_gender": "N/A - customer speaking direct to camera",
      "tone": "Conversational and authentic",
      "accent_dialect": "General American",
      "pacing": "Medium",
      "effectiveness": "Sarah's natural delivery without script creates high credibility; slight variations in pacing and emphasis feel genuine and uncoached, which strengthens trust"
    }
  },

  "motion_animation": {
    "motion_style": "Subtle",
    "camera_movement": "Fixed with occasional slow zoom",
    "animation_style": "Minimal - only lower third graphics and stat overlays animate in",
    "transitions": {
      "type": "Cut and Fade",
      "frequency": "Every 7-9 seconds",
      "effectiveness": "Simple cuts maintain documentary realism while subtle fades to product screens feel intentional"
    },
    "visual_effects": {
      "effects_used": ["Lower third animation (slide in from left)", "Stat overlays with subtle scale animation", "Light vignette on interview shots"],
      "effect_purpose": "Functional - graphics provide context and emphasize key metrics without distracting from testimonial"
    }
  },

  "narrative_flow": {
    "story_arc": {
      "structure_type": "Before→After",
      "progression": "Opens with result (hook), rewinds to 'before' state with problems, shows solution in action, quantifies multiple 'after' improvements, closes with peer recommendation"
    },
    "emotional_journey": {
      "opening_emotion": "Impressed - immediate credibility from quantified result",
      "mid_video_emotion": "Empathy - recognizes own pain in 'before' description, hope from seeing solution",
      "closing_emotion": "Confidence - multiple proof points and peer validation create conviction",
      "alignment": "Perfect for bottom-funnel - assumes problem awareness, focuses entirely on proof of ROI and results"
    },
    "message_clarity": {
      "primary_message": "Support automation delivers measurable ROI (60% cost reduction) while improving customer satisfaction and employee experience",
      "reinforcement_count": 5,
      "value_prop_timestamp": "00:05 - full value prop clear by this point (cost, speed, quality improvement)"
    }
  },

  "cta_strategy": {
    "timing": {
      "first_cta": "00:35 - verbal recommendation to consider product",
      "final_cta": "00:42-00:45",
      "frequency": "2 - soft recommendation then explicit visual CTA"
    },
    "presentation": {
      "visual_cta": "Purple button with 'See How SupportAI Works' in white text on end card with company logo",
      "verbal_cta": "If you're drowning in support tickets, SupportAI pays for itself in the first month",
      "clarity_score": 8,
      "creates_urgency": "Yes - 'pays for itself in first month' implies immediate ROI, 'drowning in tickets' creates present-tense pain"
    },
    "end_screen": {
      "present": true,
      "duration_seconds": 3,
      "elements": ["Company logo", "CTA button: 'See How SupportAI Works'", "Sarah's headshot and title"],
      "effectiveness": "Clear and credible - including Sarah's image on end card reinforces authenticity of testimonial"
    }
  },

  "visual_content_inventory": {
    "key_elements": {
      "product_screens": {
        "description": "Dashboard showing ticket automation workflows, resolution analytics",
        "flexibility": "Not replaceable - requires actual product",
        "duration_visible": "8 seconds in scene 3"
      },
      "brand_logo": {
        "description": "Purple and white logo on lower third and end card",
        "flexibility": "Not replaceable",
        "appearances": 3
      },
      "people_shown": {
        "description": "Sarah Chen (primary), support team members in B-roll",
        "flexibility": "Not replaceable - real customer testimonial requires real customer; support team B-roll is replaceable",
        "duration_visible": "Sarah: 35 seconds, B-roll team: 10 seconds"
      },
      "b_roll_footage": {
        "description": "Office environment, support agents at desks, product screens",
        "flexibility": "Partially replaceable - office B-roll could be reshot, but product screens must be real",
        "purpose": "Provides visual variety and context for Sarah's story"
      }
    },
    "company_specific_assets": [
      {
        "element": "customer_testimonial",
        "asset_type": "Interview footage of real customer",
        "reason": "Cannot be faked or scripted - requires actual customer willing to give testimonial on camera with real name and title",
        "timestamps": "[00:00-00:45] - entire video"
      },
      {
        "element": "product_dashboard_screens",
        "asset_type": "Screen recording of actual product",
        "reason": "Must show real product interface to demonstrate capabilities",
        "timestamps": "[00:12-00:20]"
      },
      {
        "element": "customer_company_context",
        "asset_type": "Customer's actual company environment/team",
        "reason": "B-roll of Acme Corp's actual office and team adds authenticity",
        "timestamps": "[00:05-00:28] - B-roll inserts"
      },
      {
        "element": "performance_data",
        "asset_type": "Customer's actual results",
        "reason": "Specific metrics (60% reduction, 72% to 91% CSAT) must be real customer data",
        "timestamps": "[00:00-00:35] - throughout"
      }
    ]
  },

  "colors": {
    "brand_colors": ["#6B46C1 (brand purple)", "#FFFFFF (white)", "#F3F4F6 (light gray)", "#1F2937 (dark gray)"],
    "main_brand_color": "#6B46C1",
    "main_color_rationale": "Purple appears in all branded moments (lower thirds, stat overlays, CTA button, logo) creating consistent brand association without overwhelming natural office environment",
    "accent_colors": ["#10B981 (green for positive metrics/arrows)"],
    "color_psychology": "Purple conveys innovation and sophistication appropriate for B2B SaaS, green accents signal positive change/improvement, neutral office tones maintain authenticity",
    "color_evolution": "Consistent throughout - brand purple only appears in graphics, preserving natural color palette of interview and office environment",
    "brand_consistency": "Strong - purple used consistently for all brand touchpoints while allowing natural environment to remain unaltered",
    "contrast_accessibility": "Good - white text on purple backgrounds maintains readability, though purple button on light end card could be darker for WCAG AAA compliance"
  },

  "_SECTION_C_EFFECTIVENESS": "======================",

  "whats_working": {
    "video_strengths": "Exceptionally credible testimonial with specific, verifiable metrics from real customer with visible title and company; before/after structure with quantified improvements across multiple dimensions (cost, speed, quality) creates comprehensive proof of value",
    "hook_effectiveness": "Powerful opening that leads with most compelling metric (60% cost reduction) immediately grabs attention of similar buyers facing support scaling challenges",
    "visual_appeal": "Documentary-style production feels authentic and trustworthy; intentional choice to avoid over-polishing maintains credibility while clean graphics provide professional structure",
    "messaging_effectiveness": "Sarah's specific language (exact ticket volumes, timeframes, percentage improvements) creates tangible comparison points for prospects; natural delivery without script enhances believability",
    "messaging_framework": "Before→After→Bridge executed perfectly with ROI proof - establishes painful 'before', demonstrates solution's impact across multiple metrics, bridges to viewer's situation with direct recommendation",
    "audio_effectiveness": "Absence of background music is strategic strength - amplifies authenticity and allows Sarah's voice inflection and conviction to carry emotional weight uninterrupted",
    "pacing_retention": "Slower pacing appropriate for bottom-funnel audience ready to consume detailed proof; each metric lands before moving to next, allowing processing time",
    "audience_appeal": "Speaks directly to support/CX leaders with familiar pain points (ticket volume, response times, headcount pressure) and metrics they track (CSAT, resolution time, cost per ticket)"
  },

  "what_needs_improvement": {
    "video_production_issues": "Slight audio reverb in office environment (especially during B-roll) could be tightened with better location audio or ADR; lighting on Sarah slightly underexposed in medium shots",
    "hook_weaknesses": "Could be marginally stronger by having Sarah state her title immediately before the stat for instant credibility framing",
    "messaging_problems": "No mention of implementation time or change management - prospects may wonder about deployment complexity",
    "pacing_issues": "Final 10 seconds (00:35-00:45) feel slightly repetitive - could tighten to 40 seconds total by combining final two statements",
    "audio_issues": "Ambient office noise occasionally competes with dialogue during B-roll sections - cleaner audio separation would help",
    "visual_confusion": "Product screen segment (00:12-00:20) moves quickly through interface - showing one clear automation example might be more digestible than multiple features",
    "audience_alignment_issues": "Missing context about company size - Acme Corp's scale would help viewers assess comparability to their own situation",
    "cta_weaknesses": "CTA button text 'See How SupportAI Works' is educational rather than conversion-focused for bottom-funnel viewer who's ready for demo/trial"
  }
}
```

---

## 4e - Image Ad Analysis - Example 1: Contrarian LinkedIn Ad

```json
{
  "image_num": "img_001",
  "ad_link": "https://linkedin.com/ads/example-contrarian",

  "strategic_parameters": {
    "creative_angle": ["Enemy-Focused", "Insider Reference", "Visual Metaphor"],
    "contrarian_techniques": ["Enemy Creation", "Silence Breaking", "Temporal Inversion"],
    "human_truth_core_emotion": ["Frustration", "Status Anxiety", "Validation"],
    "copy_framework": ["PAS (Pain-Agitate-Solution)", "Anti-Pattern → Philosophy → Proof"],
    "rhetorical_devices": ["Paradox", "Specific Numbers", "Rhetorical Question", "Contrast"],
    "big_idea_category": "Status Quo as Enemy",
    "the_enemy": ["Meetings", "Status Quo", "Time Waste"],
    "emotional_win": ["Time Reclaimed", "Control Restored", "Relief from Burden"],
    "hook_shape": ["Contradiction", "Unspoken Truth"],
    "ad_archetype": "Thought Leadership",
    "ad_style": ["Bold Colors", "Typographic Treatment", "Minimalist"]
  },

  "CTA_title": "Your calendar is killing your company",
  "CTA_area": "title and button",
  "uvp_usp": "Meeting automation that eliminates 40% of unnecessary meetings and reclaims 12 hours per week per employee",
  "target_audience": "Executives and managers at high-growth companies drowning in meeting culture and seeking productivity improvements",
  "image_description": "Bold typographic treatment with large red 'STOP' sign overlaid on a completely black calendar grid, creating stark visual contrast",
  "Image_text": "Title: Your calendar is killing your company | Button: Reclaim 12 Hours/Week | Supporting: 67% of meetings exist because someone forgot to cancel the recurring invite",

  "style": {
    "tags": ["Bold", "Confrontational", "Minimalist", "High-contrast"],
    "style_description": "Aggressive red and black color palette with oversized sans-serif typography (Helvetica Bold), minimal whitespace creating tension, stark STOP sign visual metaphor dominates composition",
    "brand_alignment": "Bold, contrarian style signals disruptor brand willing to challenge corporate norms, perfectly aligned with target audience's frustration with status quo productivity theater"
  },

  "funnel_stage": "Top",

  "whats_working": {
    "image": "STOP sign visual metaphor is immediately recognizable and emotionally charged, creating pattern interrupt in professional LinkedIn feed",
    "messaging": "Provocative headline 'Your calendar is killing your company' breaks silence on universal pain point executives won't admit publicly, specific stat (67%) adds credibility to contrarian claim",
    "Messaging_Framework": "Anti-Pattern → Philosophy framework executed sharply - calls out broken status quo (recurring meetings), implies new philosophy (intentional calendar), hints at measurable proof (12 hours reclaimed)",
    "Audience_appeal": "Taps into executive frustration with productivity theater and meeting culture while offering status-safe solution (automation, not people/culture change)"
  },

  "what_needs_improvement": {
    "image": "STOP sign may feel aggressive or accusatory to risk-averse executives; could test softer visual metaphor like hourglass or clock",
    "messaging": "Headline blames 'calendar' rather than meetings/people, slightly abstract - could be more specific about enemy (e.g., 'Recurring meetings are killing your company')",
    "audience_alignment": "Missing role-specific benefit - executives care about company-wide productivity but need personal pain point connection (e.g., 'Your calendar is killing your focus')"
  },

  "Compositional_elements": "Title, CTA, supporting text, textual/minimal, user-focused, minimal/elegant, big number/stat",

  "Elements": {
    "colors": {
      "brand_colors": "Red (#E63946), Black (#000000), White (#FFFFFF)",
      "Highlighting_colors": "Red for urgency and attention, white for contrast and readability",
      "Main_brand_color": "#E63946",
      "Main_color_rational": "Aggressive red creates urgency and danger association (killing), demands attention in sea of blue/corporate LinkedIn ads, signals bold challenger brand positioning"
    },
    "main_headline": {
      "text": "Your calendar is killing your company",
      "flexibility": "Semi-replaceable - core message adaptable but provocative tone is brand differentiator"
    },
    "Company_Specific": [
      {
        "element": "Specific_ROI_metric",
        "asset_type": "Customer data",
        "reason": "'12 hours per week' claim requires real customer data or research to avoid false advertising"
      },
      {
        "element": "Meeting_statistics",
        "asset_type": "Research/survey data",
        "reason": "'67% of meetings exist because...' stat must come from credible source or internal research"
      }
    ]
  },

  "strategic_analysis_notes": {
    "creative_angle_rationale": "Enemy-Focused angle centers ad on defeating villain (meeting culture), Insider Reference uses corporate jargon (recurring invite) for credibility, Visual Metaphor makes abstract problem (wasted time) concrete (STOP sign)",
    "contrarian_approach": "Enemy Creation positions recurring meetings as tribal villain, Silence Breaking surfaces unspoken truth that most meetings are inertia not necessity, Temporal Inversion shows present cost not future gain",
    "emotional_architecture": "Taps Frustration with broken meeting culture → defeats enemy of Status Quo → delivers Time Reclaimed and Control Restored as emotional wins, creating relief narrative",
    "hook_analysis": "Contradiction ('your productivity tool is killing productivity') and Unspoken Truth (meetings persist from inertia) combine to create strong scroll-stop for target audience",
    "framework_execution": "PAS framework clear: Pain (calendar killing company), Agitate (67% unnecessary meetings), implicit Solution (automation); Anti-Pattern overlay challenges corporate norms effectively",
    "archetype_fit": "Thought Leadership archetype appropriate for top-funnel awareness - establishes unique POV without product-forward messaging, builds authority for brand",
    "style_strategy": "Bold red/black palette and oversized STOP metaphor create visceral reaction matching message urgency; minimalist composition ensures headline carries full weight without visual competition"
  }
}
```

## 4e - Image Ad Analysis - Example 2: Minimalist Data-Driven Ad

```json
{
  "image_num": "img_002",
  "ad_link": "https://linkedin.com/ads/example-data-minimal",

  "strategic_parameters": {
    "creative_angle": ["Typographic Treatment", "Visual Metaphor"],
    "contrarian_techniques": ["None (Proven Pattern)"],
    "human_truth_core_emotion": ["Control", "Confidence", "Calm"],
    "copy_framework": ["AIDA (Attention-Interest-Desire-Action)", "Stat-Insight-Action"],
    "rhetorical_devices": ["Specific Numbers", "Contrast"],
    "big_idea_category": "Capability Unlock",
    "the_enemy": ["Uncertainty", "Data Overload"],
    "emotional_win": ["Clarity Achieved", "Control Restored", "Confidence Gained"],
    "hook_shape": ["None/Generic"],
    "ad_archetype": "Data-Backed Insight",
    "ad_style": ["Minimalist", "Bold Colors", "Infographic"]
  },

  "CTA_title": "74% of revenue teams miss quota because of bad data",
  "CTA_area": "title and description",
  "uvp_usp": "Revenue intelligence platform that ensures data accuracy and helps teams hit quota with AI-powered insights",
  "target_audience": "Revenue operations leaders and sales executives at B2B companies struggling with CRM data quality and forecast accuracy",
  "image_description": "Clean minimalist layout with large 74% statistic in bold blue typography on white background, small bar chart visualization showing quota attainment gap",
  "Image_text": "Title: 74% of revenue teams miss quota because of bad data | Description: Clean data = predictable revenue. See how top performers fix this | Button: Get the Data Quality Playbook",

  "style": {
    "tags": ["Clean", "Professional", "Data-centric", "Trustworthy"],
    "style_description": "Minimalist whitespace-heavy layout with professional blue (#0A66C2) and gray (#5E5E5E) palette, modern sans-serif typography (Inter), small bar chart adds data credibility without clutter",
    "brand_alignment": "Clean, professional aesthetic signals enterprise-grade reliability and analytical rigor appropriate for RevOps audience that values precision and data integrity"
  },

  "funnel_stage": "Middle",

  "whats_working": {
    "image": "Large 74% statistic creates immediate visual hierarchy and authority, minimalist composition prevents distraction from key message, small chart visualization adds credibility without overwhelming",
    "messaging": "Specific stat (74%) creates urgency without hyperbole, direct cause-effect claim (bad data → missed quota) resonates with revenue leader pain point, CTA offers educational asset not hard sell",
    "Messaging_Framework": "AIDA framework executed cleanly: Attention (74% stat), Interest (bad data insight), Desire (implied: don't be in the 74%), Action (playbook download); Stat-Insight-Action structure also visible",
    "Audience_appeal": "Speaks directly to RevOps metrics obsession (quota attainment) and operational pain (data quality), offering tactical resource (playbook) appropriate for problem-solving persona"
  },

  "what_needs_improvement": {
    "image": "Chart visualization is too small to read clearly, loses potential credibility boost - either enlarge or remove entirely for cleaner composition",
    "messaging": "Stat source not cited, reducing trust for analytical audience - adding '(Gartner 2024)' or similar attribution would strengthen claim significantly",
    "audience_alignment": "Description 'top performers fix this' creates us-vs-them framing but doesn't explain how they fix it, missing opportunity to tease playbook value"
  },

  "Compositional_elements": "Title, logo, CTA, supporting text, textual/minimal, user-focused, minimal/elegant, big number/stat, infographic",

  "Elements": {
    "colors": {
      "brand_colors": "LinkedIn Blue (#0A66C2), Charcoal Gray (#5E5E5E), White (#FFFFFF), Light Gray (#F3F4F6)",
      "Highlighting_colors": "LinkedIn Blue for emphasis and trust, Charcoal for readability",
      "Main_brand_color": "#0A66C2",
      "Main_color_rational": "Professional blue dominates via 74% number and CTA button, leveraging LinkedIn's native color for platform-native feel while signaling trust and corporate credibility"
    },
    "main_headline": {
      "text": "74% of revenue teams miss quota because of bad data",
      "flexibility": "Replaceable - stat-driven headline structure is reusable with different metrics/pain points"
    },
    "Company_Specific": [
      {
        "element": "74%_statistic",
        "asset_type": "Research/survey data",
        "reason": "Specific percentage claim requires credible data source (internal research, third-party study, or customer analysis) to avoid misleading advertising"
      },
      {
        "element": "Data_Quality_Playbook",
        "asset_type": "Gated content asset",
        "reason": "CTA references specific lead magnet that must exist and contain actual data quality frameworks"
      }
    ]
  },

  "strategic_analysis_notes": {
    "creative_angle_rationale": "Typographic Treatment makes 74% statistic the hero via size and color, Visual Metaphor uses small chart to represent data/analytics theme without elaborate illustration",
    "contrarian_approach": "Uses proven pattern (stat-driven insight ad) without contrarian elements; establishes credibility through conventional B2B SaaS playbook rather than challenging norms",
    "emotional_architecture": "Addresses Control (data uncertainty) and Confidence (quota predictability) needs, delivering Clarity Achieved and Control Restored through implied data quality solution",
    "hook_analysis": "Generic hook relying on stat authority rather than creative pattern break; effective for analytical audience but won't stand out in crowded feed",
    "framework_execution": "AIDA and Stat-Insight-Action frameworks well-executed with clear progression, though Desire stage could be strengthened with more specific benefit articulation",
    "archetype_fit": "Data-Backed Insight archetype perfect for middle-funnel RevOps audience seeking objective proof and analytical rigor over emotional appeals",
    "style_strategy": "Minimalist whitespace and professional blue palette match enterprise buyer expectations for revenue intelligence category; restraint signals confidence and substance over flash"
  }
}
```

---

## 4e - Reference Template: All Possible Field Options

**Purpose:** This template shows all available options for each field in the 4e Image Ad Analysis prompt. Use as a reference when analyzing ads.

```json
{
  "image_num": "string - ad identifier",
  "ad_link": "string - URL to the ad",

  "strategic_parameters": {
    "creative_angle": [
      "OPTIONS (Multi-select):",
      "Analogy Ads",
      "Typographic Treatment",
      "Understatement",
      "Cliché + Twist",
      "Visual Metaphor",
      "Contrast/Before-After",
      "Enemy-Focused",
      "Insider Reference",
      "Hybrid",
      "None of the above"
    ],

    "contrarian_techniques": [
      "OPTIONS (Multi-select):",
      "Analogical Transfer",
      "Temporal Inversion",
      "Enemy Creation",
      "Silence Breaking",
      "Scale Manipulation",
      "Role Reversal",
      "Benefit Negation",
      "Cost Reframe",
      "Invisible Made Visible",
      "Contradiction Resolution",
      "None (Proven Pattern)"
    ],

    "human_truth_core_emotion": [
      "OPTIONS (Multi-select, 1-3 primary):",
      "Relief",
      "Fear",
      "Control",
      "Status Anxiety",
      "Calm",
      "Confidence",
      "Frustration",
      "Overwhelm",
      "Time Scarcity",
      "Identity/Belonging",
      "Validation",
      "Hope",
      "Pride",
      "Shame Avoidance",
      "Other"
    ],

    "copy_framework": [
      "OPTIONS (Multi-select):",
      "AIDA (Attention-Interest-Desire-Action)",
      "PAS (Pain-Agitate-Solution)",
      "JTBD (Jobs-To-Be-Done)",
      "Golden Circle (Why-How-What)",
      "Before-After-Bridge",
      "Problem-Promise-Proof-Proposal",
      "Feature-Advantage-Benefit (FAB)",
      "Anti-Pattern → Philosophy → Proof",
      "Hook-Story-Offer",
      "Question-Answer-CTA",
      "Stat-Insight-Action",
      "None/Unclear"
    ],

    "rhetorical_devices": [
      "OPTIONS (Multi-select):",
      "Paradox",
      "Chiasmus",
      "Asyndeton",
      "Alliteration",
      "Antithesis",
      "Metaphor",
      "Personification",
      "Hyperbole",
      "Understatement",
      "Rhetorical Question",
      "Repetition",
      "Specific Numbers",
      "Contrast",
      "Anaphora",
      "None detected"
    ],

    "big_idea_category": [
      "OPTIONS (Single-select):",
      "Time Theft/Recovery",
      "Invisible Problem Made Visible",
      "Anti-Category Stance",
      "Role Reversal",
      "Hidden Cost Exposure",
      "Status Quo as Enemy",
      "Scale Dramatization",
      "Transformation Promise",
      "Identity/Tribe Creation",
      "Simplification/Reduction",
      "Capability Unlock",
      "Risk Mitigation",
      "Other"
    ],

    "the_enemy": [
      "OPTIONS (Multi-select):",
      "Meetings",
      "Status Quo",
      "Complexity",
      "Tool Sprawl",
      "Data Overload",
      "Manual Process",
      "Competitor Category",
      "Industry Practice",
      "Time Waste",
      "Burnout",
      "Inefficiency",
      "Lack of Control",
      "Uncertainty",
      "Other"
    ],

    "emotional_win": [
      "OPTIONS (Multi-select, 1-3 primary):",
      "Time Reclaimed",
      "Control Restored",
      "Clarity Achieved",
      "Status Elevated",
      "Confidence Gained",
      "Relief from Burden",
      "Simplicity",
      "Peace of Mind",
      "Capability Unlocked",
      "Recognition/Validation",
      "Belonging",
      "Pride",
      "Other"
    ],

    "hook_shape": [
      "OPTIONS (Multi-select):",
      "Contradiction",
      "Unspoken Truth",
      "Pattern Break",
      "Reframe",
      "Personal Stake",
      "Odd Observation",
      "Economic Shift",
      "False Consensus",
      "Provocative Question",
      "None/Generic"
    ],

    "ad_archetype": [
      "OPTIONS (Single-select):",
      "Testimonial",
      "Thought Leadership",
      "Product Demo",
      "Data-Backed Insight",
      "Limited-Time Offer",
      "Case Study / Success Story",
      "Event Invitation",
      "Lead Magnet",
      "Competitive Comparison",
      "Founder Story",
      "Trend-Jacking",
      "Employee Spotlight",
      "Checklist / How-To",
      "Poll / Survey",
      "Pain-Point → Solution",
      "Before/After",
      "Press",
      "Prompt Demo",
      "Point Out",
      "Other"
    ],

    "ad_style": [
      "OPTIONS (Multi-select):",
      "Bold Colors",
      "Minimalist",
      "Authentic UGC",
      "Illustration-Led",
      "Cinematic",
      "Infographic",
      "Glassmorphism",
      "3D / CGI",
      "Gradient Overlay",
      "Duotone",
      "Dark Mode",
      "Retro / Vintage",
      "Motion Graphics",
      "Isometric",
      "Hand-Drawn Sketch",
      "Other"
    ]
  },

  "CTA_title": "Max 1 sentence - the headline or title of the ad",

  "CTA_area": [
    "OPTIONS (Single-select):",
    "title only",
    "title and button",
    "title and description"
  ],

  "uvp_usp": "Max 1 sentence - core benefit or promise",

  "target_audience": "Max 1 sentence - who this targets",

  "image_description": "Max 1 sentence - visual elements summary",

  "Image_text": "Title: ... | Description: ... | Button: ... (keep brief)",

  "style": {
    "tags": ["Concise style labels - array of strings"],
    "style_description": "Max 1 sentence on creative style, tone, palette, typography, layout",
    "brand_alignment": "Max 1 sentence - how style matches brand and audience"
  },

  "funnel_stage": [
    "OPTIONS (Single-select):",
    "Top",
    "Middle",
    "Bottom"
  ],

  "whats_working": {
    "image": "Max 1 sentence - visual strengths",
    "messaging": "Max 1 sentence - copy effectiveness",
    "Messaging_Framework": "Max 1 sentence - framework + effectiveness",
    "Audience_appeal": "Max 1 sentence - why it resonates"
  },

  "what_needs_improvement": {
    "image": "Max 1 sentence - visual weaknesses",
    "messaging": "Max 1 sentence - copy weaknesses",
    "audience_alignment": "Max 1 sentence - misalignment or gaps"
  },

  "Compositional_elements": [
    "OPTIONS (Multi-select, comma-separated list):",
    "Title",
    "logo",
    "CTA",
    "supporting text",
    "textual/minimal",
    "user-focused",
    "VS/split",
    "minimal/elegant",
    "product screens/UI",
    "full-frame imagery",
    "illustration/animation",
    "big number/stat",
    "point-out",
    "talking head",
    "screen recording",
    "motion graphics",
    "live action",
    "mixed media"
  ],

  "Elements": {
    "colors": {
      "brand_colors": "Max 1 sentence or comma-separated list",
      "Highlighting_colors": "Max 1 sentence or comma-separated list",
      "Main_brand_color": "Single color name or hex code",
      "Main_color_rational": "Max 1 sentence - why this color dominates"
    },

    "main_headline": {
      "text": "Exact headline text from the ad",
      "flexibility": [
        "OPTIONS (Single-select):",
        "Replaceable",
        "Semi-replaceable",
        "Not replaceable"
      ]
    },

    "Company_Specific": [
      {
        "element": "Element name/description",
        "asset_type": [
          "OPTIONS:",
          "Logo",
          "Product screenshot",
          "Brand color",
          "Customer data/results",
          "Research/survey data",
          "Gated content asset",
          "Screen recording",
          "Brand assets",
          "Other"
        ],
        "reason": "Max 1 sentence - why it's company-specific and cannot be faked/invented"
      }
    ]
  },

  "strategic_analysis_notes": {
    "creative_angle_rationale": "Max 2 sentences - why these angles were selected",
    "contrarian_approach": "Max 2 sentences - how ad challenges norms (if applicable) or what established conventions it follows",
    "emotional_architecture": "Max 2 sentences - how emotions and wins connect",
    "hook_analysis": "Max 2 sentences - effectiveness of hook shape(s) used",
    "framework_execution": "Max 2 sentences - how well copy framework is executed",
    "archetype_fit": "Max 2 sentences - why this archetype was chosen",
    "style_strategy": "Max 2 sentences - how visual style supports message"
  }
}
```

**Key Rules:**
- **Multi-select fields**: Can select multiple options (typically 1-4)
- **Single-select fields**: Select exactly ONE option
- **Sentence limits**: 1 sentence max (except strategic_analysis_notes: 2 sentences max)
- **Evidence-based**: Only select tags with clear evidence in the ad
- **Specificity**: Use concrete examples from the ad in analysis fields
