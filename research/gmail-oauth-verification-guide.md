# Gmail OAuth Verification Guide — Personal Assistant Project

**TL;DR:** Reading Gmail = "restricted scope" = expensive CASA security audit ($500-$4,500+/yr) + 2-6 month timeline. Sending-only = "sensitive scope" = simple brand verification (2-3 days, free). Consider alternatives before committing to restricted scopes.

---

## Your Situation
- Consent screen: already configured
- Need: Read + Send Gmail
- Problem: Reading Gmail triggers **restricted scope** verification

## Gmail Scopes Classification

| Scope | Level | Verification Needed |
|-------|-------|-------------------|
| `gmail.send` | **Sensitive** | Brand verification only (2-3 days, free) |
| `gmail.compose` | **Sensitive** | Brand verification only |
| `gmail.readonly` | **Restricted** | CASA audit ($500-4,500+/yr, 2-6 months) |
| `gmail.modify` | **Restricted** | CASA audit |
| `gmail.labels` | **Sensitive** | Brand verification only |

## Option A: Avoid Restricted Scopes (Recommended if possible)

**Use `gmail.send` only (sensitive scope)** + alternative for reading:
- Use **IMAP/SMTP** via app passwords for reading (no OAuth needed)
- Use **Google Workspace service account** with domain-wide delegation (no user consent screen needed — but only works for Workspace accounts, not consumer Gmail)
- Use **Pub/Sub push notifications** + `gmail.readonly` on a limited basis

**Pros:** 2-3 day verification, free, simple
**Cons:** Reading workaround may be less clean

## Option B: Full Restricted Scope Verification

### What You Need

1. **Privacy Policy** (hosted on your domain)
   - Must disclose how you access, use, store, share Google user data
   - Must be on same domain as your app's homepage

2. **Homepage** (publicly accessible)
   - App description
   - Link to privacy policy
   - Cannot be behind a login

3. **Demo Video** (unlisted YouTube)
   - Show the OAuth consent flow in English
   - Show your app name on the consent screen
   - Show the browser address bar during OAuth (showing client ID)
   - Demo every feature that uses each restricted scope
   - Show what happens with the Gmail data

4. **Domain Verification** via Google Search Console

5. **CASA Security Assessment**
   - Annual audit by approved assessor
   - Cost: $500-$4,500+ depending on tier/assessor
   - Approved assessors: TAC Security, Leviathan Security, Prescient Security, DEKRA
   - Google has negotiated discounted Tier 2 rates with TAC Security
   - Timeline: weeks to months

### Step-by-Step Submission

1. Go to [Google Cloud Console → APIs & Services → OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent)
2. Verify all info is correct (app name, logo, support email, homepage, privacy policy)
3. Go to **Verification Center**: `https://console.developers.google.com/auth/verification?project=YOUR_PROJECT_ID`
4. Click **"Edit App"**
5. Complete OAuth consent screen → Save and continue
6. **Add scopes**: `gmail.readonly` + `gmail.send` (or `gmail.modify` for both)
7. Provide documentation links (up to 3)
8. Answer questions about app type and restricted scope usage
9. **Explain WHY** you need each restricted scope (be specific: "We read emails to summarize them for the user" etc.)
10. Submit
11. Google contacts you → may request CASA assessment
12. Complete CASA audit with approved assessor
13. Submit Letter of Assessment (LOA) to Google
14. Verification approved → scopes unlocked

### CASA Assessor Contacts
- **TAC Security** (Google-negotiated discount): tacsecurity.com
- **Leviathan Security**: leviathansecurity.com
- **Prescient Security**: prescientsecurity.com
- **DEKRA**: dekra.com

## Option C: Google Workspace Add-on

If users are on Google Workspace (not consumer Gmail):
- Build as a Workspace Add-on
- Different verification path
- Can use `gmail.addons.current.message.readonly` (less restricted)

---

## Recommendation

If this is for a small user base or internal use:
→ **Keep it in "Testing" mode** (up to 100 test users, no verification needed)

If you need public access:
→ **Start with `gmail.send` only** (sensitive, fast verification)
→ Explore IMAP for reading, or accept the CASA cost

## Sources
- [Brand Verification](https://developers.google.com/identity/protocols/oauth2/production-readiness/brand-verification)
- [Restricted Scope Verification](https://developers.google.com/identity/protocols/oauth2/production-readiness/restricted-scope-verification)
- [Gmail API Scopes](https://developers.google.com/workspace/gmail/api/auth/scopes)
- [CASA Assessment Info](https://deepstrike.io/blog/google-casa-security-assessment-2025)
- [CASA Cost Reality Check](https://medium.com/reversebits/the-50k-email-api-nightmare-why-your-simple-gmail-integration-just-became-a-compliance-hell-6071300b09b4)
