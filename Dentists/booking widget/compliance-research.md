# Compliance Research: Dental/Med Spa Booking Widget + Patient CRM

*Last updated: 2026-03-05*

## TL;DR

**What you MUST do before launch:** You are a HIPAA Business Associate the moment you store patient name + appointment/treatment info. You need: (1) signed BAAs with every dental clinic customer, (2) BAAs with all vendors that touch PHI -- Anthropic, Twilio, Supabase, Vercel all offer them, (3) encryption at rest and in transit (TLS 1.2+ and AES-256), (4) access controls + audit logging, (5) TCPA-compliant SMS opt-in with documented consent and STOP keyword support, and (6) a written HIPAA security policies document. Budget ~$2-5K for initial compliance tooling and ~$500/yr for ongoing. This is table-stakes for dental SaaS -- every competitor (Arini, NexHealth, Weave) does this.

**Nice-to-have but not blocking launch:** SOC 2 Type II certification ($15-30K), formal HIPAA risk assessment by a third party, state-specific privacy compliance beyond HIPAA (Washington MHMDA, California CCPA), WhatsApp channel (adds complexity -- launch with SMS only), cyber liability insurance (get it soon but not day-one).

---

## 1. HIPAA: Business Associate Status

| Question | Answer |
|----------|--------|
| Are we a Business Associate? | **Yes.** Any entity that creates, receives, maintains, or transmits PHI on behalf of a covered entity (dental practice) is a BA. 45 CFR 160.103. |
| What triggers BA status? | Storing patient name + treatment/appointment type. Even "John Smith, cleaning, March 10" is PHI. |
| Is name + phone alone PHI? | **Not initially.** A name/phone left for scheduling is not PHI until linked to treatment records. But once you store appointment type alongside it, it becomes PHI. |
| Is "name + phone + appointment type" PHI? | **Yes.** Patient identifier + healthcare service = PHI. |
| Do we need a BAA with each clinic? | **Yes.** Required before any PHI transmission. Use a standard BAA template. |
| Do we need BAAs with sub-processors? | **Yes.** Every vendor touching PHI needs a BAA. |

### Vendor BAA Availability

| Vendor | BAA Available? | Tier/Notes |
|--------|---------------|------------|
| **Anthropic (Claude API)** | Yes | Requires API-level agreement or HIPAA-ready Enterprise plan. Contact sales. BAAs signed after Dec 2, 2025 cover both API + Enterprise. |
| **Twilio (SMS)** | Yes | Execute BAA addendum to ToS. Only specific products eligible (Programmable SMS, Voice). |
| **Supabase (DB)** | Yes | Sign BAA. Hosted platform has HIPAA controls. Self-hosted does not. |
| **Vercel (Hosting)** | Yes | Enterprise = signed BAA. Pro = click-through BAA. |

### HIPAA Rules That Apply

| Rule | Key Requirements | Reference |
|------|-----------------|-----------|
| **Privacy Rule** | Minimum necessary use of PHI; patient rights to access/amend; no PHI for marketing without consent | 45 CFR 164.502-514 |
| **Security Rule** | Administrative, physical, technical safeguards for ePHI | 45 CFR 164.302-318 |
| **Breach Notification** | Notify affected individuals within 60 days; notify HHS; if 500+ records, notify media | 45 CFR 164.400-414 |

### Technical Requirements Checklist

- [ ] **Encryption in transit:** TLS 1.2+ for all data transmission
- [ ] **Encryption at rest:** AES-256 for stored PHI (Supabase supports this)
- [ ] **Access controls:** Role-based; unique user IDs; auto-logout
- [ ] **Audit logs:** Log all PHI access/modification with timestamps
- [ ] **Data backup:** Regular encrypted backups with tested recovery
- [ ] **Breach detection:** Monitoring for unauthorized access
- [ ] **Data retention policy:** Document how long PHI is kept and destruction method

### Penalty Tiers (2026 Adjusted)

| Tier | Culpability | Min/Violation | Max/Violation | Annual Cap |
|------|------------|---------------|---------------|------------|
| 1 | Did not know | $145 | $73,011 | $36,506 |
| 2 | Reasonable cause | $1,461 | $73,011 | $146,053 |
| 3 | Willful neglect (corrected) | $14,602 | $73,011 | $365,052 |
| 4 | Willful neglect (not corrected) | $73,011 | $2,190,294 | $2,190,294 |

Criminal penalties (DOJ): up to $250K fines and 10 years imprisonment for intentional misuse.

---

## 2. TCPA: SMS/Text Message Rules

### Consent Types

| Message Type | Examples | Consent Required | Standard |
|-------------|----------|-----------------|----------|
| **Transactional** | Appointment confirmations, reminders, pre-care instructions | Prior express consent (verbal OK) | Patient provided phone number for healthcare purposes |
| **Marketing** | Review requests, referral asks, promotions, re-engagement | **Prior express written consent** | Signed/electronic form with clear disclosure |
| **Informational** | Post-care tips related to recent treatment | Prior express consent | Tied to treatment relationship |

### Healthcare Exemption (47 CFR 64.1200)

Appointment confirmations, exam reminders, wellness checkups, and pre-registration instructions are exempt from written consent IF: (1) patient provided the number, (2) message states provider name, (3) no telemarketing content, (4) opt-out mechanism included.

**Review requests are NOT exempt** -- they are marketing. You need written consent.

### Required Implementation

- [ ] **Opt-in documentation:** Record consent timestamp, method, and exact language shown
- [ ] **STOP keyword:** Honor immediately; send one confirmation reply only
- [ ] **Opt-out honoring:** Process within 10 business days (FCC rule effective April 11, 2025)
- [ ] **Any reasonable revocation:** "Stop", "cancel", "leave me alone", email, voicemail all count
- [ ] **Message frequency disclosure:** Tell patients how often they will receive messages
- [ ] **"Message and data rates may apply"** disclosure in opt-in
- [ ] **Sender identification:** Every message must identify the practice

### Practical Approach for Review Requests

Embed consent in the booking widget: "I agree to receive appointment reminders and follow-up messages including feedback requests from [Practice Name]. Msg & data rates may apply. Reply STOP to opt out." This covers both transactional and marketing with one written consent.

---

## 3. State Privacy Laws Beyond HIPAA

| State | Law | Relevance | Action Needed |
|-------|-----|-----------|---------------|
| **Washington** | My Health My Data Act (MHMDA) | Applies to any entity collecting "consumer health data" from WA residents. Requires opt-in consent. Private right of action. | Add consent mechanism for WA users. Not blocking for launch. |
| **California** | CCPA/CPRA | Applies if you have 100K+ CA consumers or $25M+ revenue. Health data covered. New automated decision-making rules effective Jan 2026. | Likely exempt at launch (revenue/volume thresholds). Monitor as you scale. |
| **Texas** | Texas Medical Records Privacy Act | Stricter than HIPAA on certain disclosures. 15-day breach notification. | Follow HIPAA and you are mostly covered. |
| **New York** | SHIELD Act | Requires "reasonable safeguards" for private info. Broader definition than HIPAA. | Follow HIPAA security rule and you are covered. |
| **Colorado** | Colorado AI Act (2026) | Requires disclosure when "high-risk" AI is used in healthcare decisions. | Relevant if AI makes scheduling/triage decisions. Add disclosure. |

**Bottom line:** HIPAA compliance covers ~90% of state requirements. Washington MHMDA is the biggest outlier risk due to private right of action.

---

## 4. WhatsApp Business API Compliance

| Requirement | Details |
|------------|---------|
| Opt-in | Explicit opt-in required before sending any message. Separate from SMS consent. |
| Template approval | All outbound messages must use pre-approved templates. Healthcare messages reviewed more strictly. |
| HIPAA compatibility | **WhatsApp is NOT inherently HIPAA compliant.** No BAA available from Meta. No audit logging. Missing access controls. |
| Recommendation | **Do not send PHI over WhatsApp.** Use only for generic messages ("Your appointment is confirmed") without treatment details. Or skip WhatsApp at launch. |

---

## 5. AI-Specific Compliance

### Disclosure Requirements

| Jurisdiction | Requirement |
|-------------|-------------|
| **California (SB 243, eff. Jan 2026)** | Must disclose users are interacting with AI, not a human |
| **Utah (HB 452)** | Disclosure required for mental health chatbots (may extend to health) |
| **Colorado AI Act** | Disclosure + patient notification for AI-driven healthcare decisions |
| **FTC (Section 5)** | Deceptive to represent AI as human; must not mislead consumers |
| **Best practice** | Always disclose: "This is an AI assistant for [Practice Name]" at conversation start |

### Sending PHI to AI APIs

- Anthropic offers BAAs for Claude API -- **sign one before sending any PHI**
- Use data minimization: send only what Claude needs (first name + service type), not full records
- Never use PHI for model training -- Anthropic's API does not train on inputs by default, but confirm in BAA
- Log all AI interactions for audit trail

---

## 6. What Competitors Do

| Company | HIPAA Compliant | Signs BAA | AI + PHI Approach |
|---------|----------------|-----------|-------------------|
| **Arini** | Yes | Yes, with each practice | AI accesses minimum necessary PHI; strict data minimization; no cross-client training |
| **NexHealth** | Yes | Yes | Platform-level HIPAA compliance; encrypted everything |
| **Weave** | Yes | Yes | HIPAA-compliant texting, calls, video; full audit trails |

All three sign BAAs with clinics and sub-processors. This is non-negotiable in the dental SaaS space.

---

## 7. Insurance Needed

| Type | Why | Estimated Cost |
|------|-----|---------------|
| **Cyber Liability Insurance** | Covers breach notification costs, legal defense, regulatory fines | $1,000-3,000/yr for startup |
| **E&O (Professional Liability)** | Covers claims of negligence in your software/service | $1,000-2,500/yr |
| **General Liability** | Standard business coverage | $500-1,000/yr |

---

## MVP Compliance Checklist (Minimum to Launch Legally)

### Before Writing Code

- [ ] Draft a standard BAA template (use HHS sample as base)
- [ ] Sign BAAs with: Anthropic, Twilio, Supabase, Vercel
- [ ] Write HIPAA Security Policies document (access control, encryption, breach response)
- [ ] Designate a HIPAA Security Officer (you, the founder)

### Technical Implementation

- [ ] TLS 1.2+ on all connections (Vercel/Supabase handle this by default)
- [ ] AES-256 encryption at rest for PHI in Supabase
- [ ] Role-based access controls (clinic can only see their patients)
- [ ] Audit logging on all PHI access (who, what, when)
- [ ] Unique user authentication (no shared passwords)
- [ ] Auto-session timeout after inactivity
- [ ] STOP keyword handling for SMS opt-out
- [ ] Consent capture in widget (timestamp + exact language + checkbox)

### Patient-Facing

- [ ] AI disclosure: "I'm an AI assistant for [Practice Name]" at conversation start
- [ ] Privacy notice link in widget
- [ ] SMS consent language: covers both transactional + marketing messages
- [ ] Clear data retention statement in privacy policy
- [ ] Opt-out mechanism in every SMS/WhatsApp message

### Documentation

- [ ] Privacy Policy (website)
- [ ] Terms of Service (for clinic customers)
- [ ] BAA template (for clinic customers)
- [ ] Breach Notification Procedure (internal document)
- [ ] Data Retention Policy (internal document)
- [ ] Risk Assessment (can be self-conducted initially, document findings)

### Post-Launch (Within 90 Days)

- [ ] Conduct formal HIPAA risk assessment
- [ ] Get cyber liability + E&O insurance
- [ ] Begin SOC 2 Type II process if pursuing enterprise clients
- [ ] Monitor Washington MHMDA and Colorado AI Act compliance

---

## Key Sources

- [HHS HIPAA Privacy Rule Summary](https://www.hhs.gov/hipaa/for-professionals/privacy/laws-regulations/index.html)
- [HIPAA for SaaS - Konfirmity](https://www.konfirmity.com/blog/hipaa-for-saas)
- [HIPAA Violation Fines 2026 - HIPAA Journal](https://www.hipaajournal.com/hipaa-violation-fines/)
- [Anthropic BAA Info](https://privacy.claude.com/en/articles/8114513-business-associate-agreements-baa-for-commercial-customers)
- [Twilio HIPAA](https://www.twilio.com/en-us/hipaa)
- [Supabase HIPAA](https://supabase.com/docs/guides/security/hipaa-compliance)
- [Vercel BAA](https://vercel.com/legal/baa)
- [TCPA Healthcare Texting Rules - Solum](https://getsolum.com/glossary/tcpa-healthcare-texting-rules)
- [FCC Opt-Out Rules 2025 - BCLP](https://www.bclplaw.com/en-US/events-insights-news/the-tcpas-new-opt-out-rules-take-effect-on-april-11-2025-what-does-this-mean-for-businesses.html)
- [Washington MHMDA - AG](https://www.atg.wa.gov/protecting-washingtonians-personal-health-data-and-privacy)
- [Arini HIPAA Approach](https://www.arini.ai/blog/ai-phone-systems-dental-practices)
- [NexHealth HIPAA Scheduling](https://www.nexhealth.com/resources/hipaa-compliant-scheduling-software)
- [AI Chatbot Compliance - Cooley](https://www.cooley.com/news/insight/2025/2025-10-21-ai-chatbots-at-the-crossroads-navigating-new-laws-and-compliance-risks)
- [What is PHI - HIPAA Journal](https://www.hipaajournal.com/considered-phi-hipaa/)
- [HIPAA for Startups - Sprinto](https://sprinto.com/blog/hipaa-for-startups/)
