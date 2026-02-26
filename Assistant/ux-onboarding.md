# Onboarding UX — 3 Approaches

**Date**: 2026-02-17 | **Goal**: Get Nir from "first message" to "holy shit" as fast as possible

## TL;DR

Three onboarding flows for a WhatsApp-only AI assistant. All prioritize **time to wow** (how fast the user feels value) over completeness of setup. The core insight: **OAuth converts best when it unlocks something the user just said they want — not as a prerequisite.** Never use the word "setup." The onboarding IS the product.

| Approach | Time to Wow | Friction | Memory Richness | Best For |
|---|---|---|---|---|
| 1. Instant Demo | ~30 sec | Low | Thin at first | Maximum wow speed |
| 2. One Big Question | ~60-90 sec | Very low | Rich from context | Personal feel, natural |
| 3. The Setup Wizard | ~3 min | Higher | Very rich | Completeness |
| **Recommended: Hybrid (1+2)** | **~30-45 sec** | **Low** | **Rich** | **Best of both** |

---

## Approach 1: "The Instant Demo"

**Concept**: Show, don't tell. Alex's first message IS a demo of the daily brief — a mock version that looks so real the user immediately gets it. Value before setup.

**Inspiration**: Duolingo (shows a lesson before signup), Arc browser (just works differently from moment one)

### Flow

```
[User sends first message: "היי" / "Hey" / anything]

ALEX (immediate, no delay):
  בוקר טוב נתן 👋

  ככה נראה בוקר איתי:

  היום (שלישי, 18.2):
  9:00 — סטנדאפ צוות (30 דק׳)
  10:30 — שיחה עם דוד על Q1
  12:00 — פנוי
  14:00 — סקירת עיצוב עם יעל

  3 מיילים דחופים:
  1. שרה — שלחה דו״ח Q4, צריך לעבור עליו עד רביעי
  2. משפטי — חתימה על NDA
  3. AWS — חיוב $127 (עלה מ-$95)

  משימות להיום:
  — לסגור טיוטת הצעה
  — לשלוח חוזה לעמית

  זה דמו. רוצה את הגרסה האמיתית עם המייל והיומן שלך?

  [כפתור CTA: "🔗 לחבר Gmail ויומן"]
  [כפתור: "ספר לי עוד"]
```

```
[User clicks OAuth CTA → browser opens → Google auth → returns to WhatsApp]

ALEX:
  מחובר ✓

  תן לי 10 שניות...

ALEX (after fetching real data):
  הנה הבוקר האמיתי שלך:

  [Real daily brief with actual calendar + emails]

  זה מה שתקבל כל בוקר ב-7:30.
  מה השם שלך? (שאני לא אקרא לך "User")
```

```
[User: "נתן"]

ALEX:
  נתן, נעים להכיר. אני אלכס.

  אני כאן 24/7 — מיילים, יומן, תזכורות, משימות,
  וכל דבר שתגיד לי לזכור.

  תנסה — תגיד לי "תזכור שדוד אלרגי לבוטנים"
  או "מה יש לי מחר?"
```

### Where Wow Happens
- **Second 5**: The fake brief looks incredible — "wait, it already knows my schedule?"
- **Second 30**: Realization it's a demo → curiosity spike → high motivation to connect real data
- **Second 60**: Real data appears → "this is actually my life, organized for me"

### Rationale
- **Shows value before asking for anything.** The user sees what they'll get BEFORE they invest effort.
- **OAuth is positioned as an unlock**, not a requirement. "Want the REAL version?" — of course they do.
- **Demo-to-real pipeline.** The contrast between demo and real data creates a second wow moment.
- **Only 1 question asked** (name). Everything else is deferred or inferred.

### Tradeoffs
| Pro | Con |
|---|---|
| Fastest time to wow (30 sec) | Demo might set wrong expectations if real data is very different |
| OAuth conversion high (user wants the real thing) | Memory is thin — only has name after onboarding |
| Minimal friction | Demo content needs to feel realistic but not misleading |
| Works in any language | Second wow depends on user actually having emails/events |

---

## Approach 2: "The One Big Question"

**Concept**: Start with a single powerful question that simultaneously reveals what Alex can do, captures context, and creates motivation for OAuth. The question does triple duty.

**Inspiration**: Superhuman's onboarding call ("What's broken about your email?"), therapy's opening question pattern

### Flow

```
[User sends first message: "היי"]

ALEX:
  היי, אני אלכס — העוזר האישי שלך.

  לפני הכל, שאלה אחת:
  מה הדבר שהכי מעמיס עליך עכשיו שהיית רוצה שמישהו פשוט יטפל בו?

  [כפתור: "📧 מיילים שמצטברים"]
  [כפתור: "📅 יומן כאוטי"]
  [כפתור: "🧠 יותר מדי דברים לזכור"]
```

```
[User picks "מיילים שמצטברים" or types freely — e.g., "המייל שלי בבלאגן ויש לי ישיבה מחר שאני לא מוכן אליה"]

ALEX:
  בדיוק בשביל זה אני פה.

  תחבר את המייל ואני מיד:
  — אסנן לך את מה שבאמת דחוף
  — אתעלם מניוזלטרים
  — ואראה אם יש משהו שקשור לישיבה של מחר

  [כפתור CTA: "🔗 לחבר Gmail"]
```

```
[OAuth completes → returns to WhatsApp]

ALEX:
  מחובר ✓ בודק את התיבה שלך...

ALEX (15 seconds later):
  מצאתי 23 מיילים חדשים. הנה מה שחשוב:

  1. דוד — רוצה לדחות את הישיבה של מחר ל-15:00. צריך תשובה.
  2. משפטי — NDA מחכה לחתימה
  3. AWS — חיוב חודשי עלה ל-$127

  השאר — 8 FYI, 12 ניוזלטרים (דילגתי).

  רוצה שאטפל במשהו מהרשימה?
  למשל — "תגיד לדוד שזה בסדר, 15:00 עובד"
```

```
[User: "כן, תגיד לדוד שזה בסדר"]

ALEX:
  טיוטה לדוד:
  "היי דוד, 15:00 עובד מבחינתי. נתראה מחר."

  לשלוח?

  [כפתור: "✅ שלח"]
  [כפתור: "✏️ תשנה"]
```

```
[User: "שלח"]

ALEX:
  נשלח ✓

  אגב, מה השם שלך? אני צריך לדעת למי אני עובד.

[User: "נתן"]

ALEX:
  נתן, אני אלכס.
  מחר בבוקר ב-7:30 תקבל ממני סיכום של היום — יומן, מיילים, ומשימות.

  בינתיים — אפשר לבקש ממני כל דבר.
  "תזכיר לי", "מה יש ביומן", "תזכור ש...", או סתם לדבר.
```

### Where Wow Happens
- **Second 15**: "It asked the RIGHT question" — feels like it understands me
- **Second 60**: Real emails, filtered and prioritized — actual value delivered on MY problem
- **Second 90**: Drafted a reply for me — "I just handled email through WhatsApp"

### Rationale
- **The question creates context AND motivation.** When user says "my email is a mess," Alex says "let me fix it" — OAuth becomes a solution, not a step.
- **User's own words drive the experience.** Whatever they answer, Alex tailors the first real interaction to THAT thing.
- **Memory seeding is passive.** From "יש לי ישיבה מחר" Alex already knows: the user has meetings, works with others, is stressed about preparation. No form needed.
- **Progressive disclosure.** Name is asked AFTER Alex has proven value, not before.

### Tradeoffs
| Pro | Con |
|---|---|
| Feels personal and human | Slightly slower wow than Approach 1 (~60-90 sec) |
| OAuth conversion very high (solves stated problem) | Open-ended answer requires Alex to handle any response well |
| Rich context from first interaction | If user gives vague answer, flow stumbles |
| Memory builds naturally | Engineering complexity: need robust free-text → action mapping |

---

## Approach 3: "The Guided Setup"

**Concept**: Classic onboarding wizard adapted for WhatsApp. Walk through setup steps using interactive buttons. Comprehensive, predictable, complete.

**Inspiration**: Notion's onboarding (choose your use case), Slack's workspace setup

### Flow

```
[User sends first message: "היי"]

ALEX:
  שלום! אני אלכס, העוזר האישי שלך ב-WhatsApp 🤖

  אני יכול לנהל לך מיילים, יומן, משימות, תזכורות,
  ולזכור כל דבר שתגיד לי.

  בוא נתחיל — ייקח דקה וחצי.
  מה השם שלך?
```

```
[User: "נתן"]

ALEX:
  נתן, נעים מאוד.

  באיזו שפה נדבר בדרך כלל?

  [כפתור: "🇮🇱 עברית"]
  [כפתור: "🇬🇧 English"]
  [כפתור: "🔄 שתיהן"]
```

```
[User picks "עברית"]

ALEX:
  מעולה. עכשיו הכי חשוב — לחבר את המייל והיומן שלך.
  ככה אוכל:
  — לסכם מיילים חשובים
  — להראות מה יש ביומן
  — לקבוע פגישות בשבילך
  — לשלוח בריף כל בוקר

  [כפתור CTA: "🔗 לחבר Gmail ויומן"]
  [כפתור: "אחר כך"]
```

```
[OAuth completes]

ALEX:
  מחובר ✓

  עוד שתי שאלות קצרות:

  באיזו שעה לשלוח לך בריף בוקר?

  [כפתור: "7:00"]
  [כפתור: "7:30"]
  [כפתור: "8:00"]
```

```
[User picks "7:30"]

ALEX:
  ואחרונה — מה הכי חשוב לך?

  [רשימה:
   📧 שהמיילים שלי יהיו מסודרים
   📅 שהיומן שלי ינוהל בצורה חכמה
   ✅ שלא אשכח משימות
   🧠 שמישהו יזכור דברים בשבילי]
```

```
[User picks option]

ALEX:
  הכל מוכן.

  הנה טעימה — היומן שלך להיום:
  [Real calendar summary]

  מחר ב-7:30 תקבל ממני את הבריף המלא.

  תנסה לכתוב לי משהו —
  "תזכור ש...", "מה יש לי מחר", או "תזכיר לי ב-5 לעשות X"
```

### Where Wow Happens
- **Minute 1.5**: Setup feels polished and professional (like a premium product)
- **Minute 2.5**: Real calendar data appears — "it actually works"
- **Minute 3**: First free interaction — testing the magic

### Rationale
- **Complete setup = rich experience from day 1.** Alex knows name, language, brief time, priorities.
- **Buttons reduce cognitive load.** User never needs to think about what to type.
- **Predictable flow.** No surprises, no confusion. Each step makes sense.
- **Professional feel.** Signals "this is a polished product, not a hack."

### Tradeoffs
| Pro | Con |
|---|---|
| Most complete memory seeding | Slowest time to wow (~3 min) |
| Button-driven = very easy | Feels like a form, not magic |
| Predictable, low engineering risk | "Setup" framing = friction before value |
| User feels in control | Drop-off risk at each step (especially OAuth) |
| Good for non-technical users | Least "wow" — expected, not surprising |

---

## Recommendation: Hybrid (Approach 1 + 2)

**The best onboarding steals from both the Instant Demo and the One Big Question.**

### Hybrid Flow

```
[User: "היי"]

ALEX:
  היי 👋 אני אלכס.

  ככה נראה בוקר טיפוסי איתי:

  8:00 — בריף: 3 פגישות היום, 2 מיילים דחופים, משימה אחת שפיגרת
  8:01 — "תגיד לדוד שאני מאשר"
  8:01 — אלכס: "נשלח ✓"
  8:15 — תזכורת: להכין מצגת ל-10:00

  מייל, יומן, משימות, תזכורות — הכל דרך הצ׳אט הזה.

  מה הדבר שהכי מעמיס עליך עכשיו?

  [כפתור: "📧 מיילים"]
  [כפתור: "📅 יומן"]
  [כפתור: "✅ סתם הרבה דברים לזכור"]
```

→ User picks or types freely
→ Alex connects the answer to OAuth ("בוא נפתור את זה — תחבר את המייל")
→ OAuth → immediate real value on the thing they said bothers them
→ Name asked after value is delivered
→ Brief time offered naturally ("מחר בבוקר אשלח לך סיכום — 7:30 טוב?")

**Time to wow**: ~30-45 seconds (demo hook) + ~60-90 seconds (real data)
**Memory at end**: name, language, priority, brief time — inferred naturally

### Why This Wins

| Factor | Score |
|---|---|
| Time to wow | 30 sec (demo shows what's possible) |
| OAuth motivation | High (unlocks solution to stated problem) |
| Friction | Very low (1 button + OAuth + name) |
| Memory richness | Good (inferred from conversation) |
| Wow factor | Double hit: demo at 30s + real data at 90s |
| Engineering complexity | Medium |

---

## Design Principles (All Approaches)

1. **Show before you ask.** Value first, setup second.
2. **OAuth is an unlock, not a toll.** Position it as "let me fix that for you" not "please authorize."
3. **One question at a time.** Never stack questions.
4. **The onboarding IS the product.** First interaction should feel like using Alex, not setting up Alex.
5. **Progressive profiling > intake forms.** Learn over days, not in the first minute.
6. **If they skip OAuth**: Alex still works for reminders, memory, tasks, Q&A. Calendar/email features prompt OAuth when first requested.
7. **Hebrew first, mirror language.** Default to Hebrew, switch if user writes English.
