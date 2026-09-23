# DeutschIQ product-readiness baseline

Status: active baseline  
Scope: Telegram Mini App, backend learning engine, curriculum, deployment and beta operations  
Rule: no page-level redesign is accepted unless it conforms to this document.

## 1. Product outcome

DeutschIQ must help a learner make measurable progress in German through short, practical, adaptive phone sessions. A user should always understand:

1. what to do now;
2. why this task was selected;
3. whether the answer was correct;
4. what exact point needs correction;
5. what progress changed as a result.

The core journey is:

`Telegram entry → onboarding → diagnostic → preliminary result → recommended plan → lesson → targeted feedback → review → measurable progress`

## 2. Non-negotiable product rules

- Phone first: every critical action works comfortably at 360 × 640 CSS pixels.
- One screen, one primary action.
- One exercise, one interaction model. Never display competing ways to produce the same answer.
- Do not reveal an answer before submission unless the activity is explicitly a worked example.
- No unnecessary full-sentence typing in controlled practice.
- A lesson must test transfer with more than one sentence and context.
- Exercise score, topic mastery, retention and CEFR progress are separate concepts.
- Never report an unassessed skill as measured.
- A wrong answer receives one specific diagnosis and one useful next action.
- UI copy is concise and professionally localized. Product release scope is Russian and German; English remains an internal fallback until separately approved.
- Bottom navigation, Telegram chrome, keyboard and safe areas may not cover content or actions.
- Loading, empty, offline, retry and restored-progress states are part of every feature.

## 3. Current-system audit

### Architecture findings

| Finding | Impact | Priority |
|---|---|---|
| Lesson, Review and Checkpoint contain separate exercise renderers | Interactions and feedback drift between flows | P0 |
| Styles are distributed across `global.css`, `product.css`, `v20.css`, `v24.css`, `v29.css` and `v30.css` | Overrides are difficult to predict and device fixes regress other screens | P0 |
| `Lesson.tsx` owns loading, persistence, exercise rendering, speech, scoring feedback and completion in one component | High regression risk and slow iteration | P0 |
| Curriculum builders generate five nominal stages but reuse the same model answer across several stages | Memorisation can look like learning | P0 |
| RU/DE/EN strings are embedded directly in components and content builders | Copy cannot be audited or released consistently | P1 |
| Dashboard, Plan, Analytics and Lesson use overlapping progress terms | Learners cannot distinguish completion, performance and mastery | P0 |
| Critical frontend journeys have only a small reliability E2E suite | Visual and state regressions can reach production | P0 |
| The floating beta reporter competes with navigation and lesson controls | It obstructs core use on small phones | P1 |
| Render free-instance wake-up remains visible to users | First-open reliability feels broken | P1 |

### Route audit

| Route/state | Intended job | Current risk | Required correction |
|---|---|---|---|
| `/` new user | Explain value and start diagnostic | Beta setup, language choice and welcome can feel like separate onboarding products | One short onboarding sequence; no bottom navigation |
| `/` returning user | Resume learning immediately | Daily intro adds an extra gate before the dashboard | Keep only if it adds useful daily context; otherwise route directly to Today |
| `/diagnostic` | Estimate starting level | 16 auto-advancing questions provide no pause or answer recovery | Clear scope, stable progress, accessible audio, safe submit recovery |
| `/result` | Explain preliminary placement | Percentage can be mistaken for CEFR certainty | Label estimate, assessed/unassessed skills and three priority areas clearly |
| `/dashboard` | Start the best next activity | Today card, weak dimension, session phases, review and mistakes compete | One dominant Continue action; secondary information collapsed or moved |
| `/plan` | Explain route and access | CEFR journey, next lesson, modules and lesson list duplicate hierarchy | Show current level and next lesson first; disclose full roadmap progressively |
| `/lesson/:id` | Teach and validate one skill | Monolithic renderer, repeated examples and dense feedback | Replace with shared exercise shell and approved lesson loop |
| `/review` | Retrieve previously learned material | Separate UI supports only choose or text answer | Use the same shared exercise components as Lesson |
| `/checkpoint/:level` | Confirm level readiness | Third exercise renderer and weak recovery connection | Use shared shell; explain evidence gate and recovery route |
| `/analytics` | Show actionable learning evidence | Many score systems and details remain cognitively dense | Default to one progress story and one next action; advanced evidence in accordions |
| `/mistakes` | Understand and repair errors | Static history does not repair the error on the same screen | Add a direct targeted retry using the shared exercise shell |
| `/tutor` | Get contextual help quickly | Generic chat can disconnect from the current lesson | Open with lesson/mistake context and three useful actions |
| `/profile` | Preferences, account and legal controls | Learning, beta, destructive testing and account controls are mixed | Separate learner settings, beta tools and destructive actions |

## 4. Approved information architecture

Primary navigation contains five stable destinations:

1. **Today** — the single best next action.
2. **Progress** — level evidence, mastery and retention.
3. **Plan** — accessible levels, modules and lessons.
4. **Tutor** — contextual help.
5. **Profile** — preferences, data and legal controls.

Lesson, Review, Mistake repair, Diagnostic and Checkpoint are focused modes. They do not show the bottom navigation. They always provide a reliable exit or Telegram Back action.

## 5. Shared exercise system

All learning flows must render the same typed exercise model.

| Type | Interaction | Suitable use | Avoid |
|---|---|---|---|
| `choice` | Tap one large answer | Recognition and meaning | Multiple almost-identical correct answers |
| `cloze` | Tap or enter only the missing element | Case, ending, verb form | Retyping an entire given sentence |
| `reorder` | Tap shuffled tokens; tap answer token to undo | Word order and clause structure | Displaying tokens in answer order |
| `match` | Pair two short items | Vocabulary and fixed combinations | Large paragraphs |
| `listen_choice` | Play audio, then tap meaning/form | Listening discrimination | Showing the transcript before submission |
| `repair` | Identify and replace the incorrect part | Misconception correction | Asking for an unexplained full rewrite |
| `speak` | Record one short response | Intelligibility and active recall | Calling word recognition a pronunciation score |
| `write` | One concise independent response | Transfer and production | Using it for every controlled exercise |

Every exercise contract contains:

- stable `id`;
- `type` and learning `stage`;
- one localized instruction;
- prompt/context;
- answer interaction data;
- accepted answer(s) or production rubric;
- misconception code;
- concise explanation;
- retry variant or repair instruction;
- accessibility label.

## 6. Approved lesson loop

A normal lesson contains six learner steps and should take 5–8 minutes:

1. **Goal** — one practical can-do statement.
2. **Notice** — one rule and two contrasting examples.
3. **Guided** — cloze, choice or reorder; minimal typing.
4. **Control** — repair or new-context selection.
5. **Transfer** — one new spoken or written response.
6. **Result** — exercise score, mastery change and next review separated.

Requirements:

- At least three genuinely different sentences per lesson.
- No model sentence appears in more than two steps.
- A retry changes the item or scaffolding, not only clears the same input.
- The final production task is evaluated against the task actually requested.
- Completion cannot be awarded solely from recognition tasks.

## 7. Progress vocabulary

These terms have one meaning everywhere:

| Term | Definition | Update cadence |
|---|---|---|
| Exercise score | Correctness within the current lesson | At lesson completion |
| Topic mastery | Evidence-weighted ability for one skill | After validated attempts |
| Retention | Estimated recall after time decay | Over time and reviews |
| Course completion | Completed lessons in a level | After lesson completion |
| CEFR estimate | Preliminary placement supported by checkpoints | Diagnostic and checkpoint only |

The UI must not combine these values into an unexplained percentage.

## 8. Visual-system consolidation

Create one token and component layer, then remove versioned CSS incrementally.

Required primitives:

- `PageShell`, `FocusHeader`, `ProgressHeader`;
- `PrimaryButton`, `SecondaryButton`, `TextButton`;
- `ChoiceOption`, `Token`, `TextAnswer`, `VoiceAnswer`;
- `FeedbackPanel`, `RetryPanel`, `ResultMetric`;
- `LoadingState`, `EmptyState`, `ErrorState`, `OfflineState`;
- `BottomNavigation`, `Sheet`, `Dialog`.

Visual rules:

- Deep navy is the base; gold marks the primary action; blue marks learning information; green/red are reserved for evaluated outcomes.
- Maximum one elevated card around the main task.
- Minimum interactive height: 48 px.
- Body text minimum: 14 px; auxiliary labels minimum: 11 px.
- No fixed control may overlap the keyboard, bottom navigation or lesson action.
- Respect reduced motion and dynamic text sizing.

## 9. Delivery sequence

### R1 — Reference lesson foundation (P0)

- Extract a shared `ExerciseShell` and typed exercise components.
- Implement choice, cloze, reorder, repair, speak and write.
- Rebuild one B1 reference lesson with six useful steps and varied content.
- Reuse it in Lesson, Review and Checkpoint.
- Add phone E2E coverage at 360 × 640 and 390 × 844.

Exit gate: the reference lesson is understandable without explanation, fits phone safe areas and passes learning-content review.

### R2 — B1 curriculum conversion (P0)

- Convert all 24 B1 lessons to the approved contract.
- Add retry variants and misconception-specific feedback.
- Remove duplicated model sentences and implausible distractors.
- Review all Russian and German copy.

Exit gate: automated content validation plus manual sampling of every lesson.

### R3 — Core journey consolidation (P0)

- Simplify Today, Plan and Progress around the approved vocabulary.
- Unify loading/error/offline states.
- Correct navigation, safe areas and reporter placement.
- Make diagnostic/result language explicitly preliminary.

Exit gate: new and returning user journeys pass automated mobile E2E tests.

### R4 — Remaining curriculum and adaptation (P1)

- Convert A1, A2, B2 and C1 in that order.
- Calibrate diagnostic and checkpoint evidence.
- Generate review from real misconception codes.
- Make Tutor context-aware.

Exit gate: every recommendation is traceable to learner evidence.

### R5 — Reliability and commercial readiness (P1/P2)

- Monitoring, backups, performance budgets and deployment gates.
- Entitlements, payment recovery and paywall only after learning gates pass.
- Legal/support review and beta-to-production cleanup.

## 10. Release gates

A release is ready only when all applicable gates pass:

- Frontend build and lint.
- Backend tests and content validation.
- Mobile E2E for new-user, returning-user, lesson, retry, review and offline recovery.
- No untranslated or mixed-language copy in RU/DE modes.
- No control overlap at supported viewports.
- Production health, database migration and Telegram webhook checks.
- Manual review of changed learning content.

## 11. Immediate next implementation

The next code change is **R1: Reference lesson foundation**.

Start with one B1 skill (`genitive_prepositions`) because it exposed the current repetition and phone-interaction problems. Do not convert the rest of B1 until this reference lesson is reviewed and accepted.

Deliverables:

1. typed exercise contract;
2. shared phone-native exercise components;
3. one complete reference lesson with distinct examples;
4. shared feedback and retry states;
5. mobile E2E screenshots/tests;
6. no changes to unrelated screens during this release.
