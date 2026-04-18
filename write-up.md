# Design Rationale: The Daily Reflection Tree
## A Deterministic Reflection Agent for End-of-Day Clarity

---

## Overview

This tree encodes three psychological insights about how people grow: through **recognizing their agency** (Axis 1: Locus of Control), **orienting toward contribution** (Axis 2: Entitlement vs Citizenship), and **widening their radius of concern** (Axis 3: Self-Transcendence).

The design challenge was **not to score or rank employees**, but to make visible—without shame—the narratives they tell themselves about their days. A tired employee at 7pm is not ready for instruction. They're ready for a mirror.

---

## Question Design: Why These Questions?

### Axis 1: Locus of Control (13 nodes covering this axis)

**Psychological Foundation:** Julian Rotter's 1954 work on locus of control; Carol Dweck's growth mindset research. The question: does this person see their hand in outcomes?

**The Design Problem:** Asking "Do you believe you have control?" yields lies. Everyone wants to believe they have control. So I designed three questions that surface *behavior and narrative*, not beliefs:

1. **A1_OPEN** ("How would you describe today?"): Establishes the *frame*. If I start with "How did you handle it?", I'm already suggesting they had agency. "How would you describe it?" is frame-neutral—lets them choose their narrative.

2. **A1_INTERNAL/EXTERNAL** (branching follow-up): "When something went well, what made it happen?" vs. "When something didn't go as planned, what did you do?" This pair is asymmetrical intentionally. Positive events elicit *explanations* (attribution). Negative events elicit *responses* (agency). We're probing from two angles.

3. **A1_DEEP** (converge point): "What story did you tell yourself?" This gets at the *narrative beneath the behavior*. Someone can report "I adapted" (internal action) but still feel like the world happened to them (external narrative). This question bridges the gap.

**Trade-offs:** I considered asking directly about failure ("Tell me about a moment you couldn't control") but rejected it—that's accusatory at 7pm. I also considered a Likert scale ("Do you feel in control?") but that's external measurement, not internal discovery. The branching structure respects the employee's own framing first, then gently probes deeper.

### Axis 2: Contribution vs. Entitlement (Orientation) — 12 nodes

**Psychological Foundation:** Campbell et al.'s 2004 research on psychological entitlement (a stable belief that one deserves more than one's contributions justify); David Organ's organizational citizenship behavior research. 

**The Design Problem:** Entitlement is *invisible to the person holding it*. They don't wake up thinking, "I'm entitled." They think "Nobody appreciates me" or "I do more than others." So the tree surfaces it through *feeling-language*, not accusation:

1. **A2_OPEN**: "What did you give? What did you need?" The pairing is crucial—it's not "Are you a taker?" but a both/and question. Everyone gives and needs. The question is *which one was salient* today.

2. **A2_ENTITLEMENT_PATH** (follow-up): When someone says they needed support or did others' work, I ask about the *feeling*. "Resentful," "invisible," "depleted"—these are the tells of entitlement. But I pair them with "responsible" (healthy boundary-setting). This prevents false positives: someone might set a boundary (healthy) or resent being asked (entitlement). The feeling tells the story.

3. **A2_RECOGNITION**: "Did you need someone to notice?" This is the decision point. True contribution doesn't require external validation—it's intrinsically motivated. Entitlement requires recognition. By asking about *need*, I avoid moralizing ("You should want recognition!") and let them locate themselves.

**Trade-offs:** I considered adding a question about *frequency* of contribution ("How often do you help others?") but rejected it—a compulsive over-giver might answer the same way as a genuine contributor. Frequency ≠ motivation. The questions focus on *motivation and feeling*, not behavior count.

### Axis 3: Radius of Concern (Self → Team → Other → System) — 12 nodes

**Psychological Foundation:** Maslow's 1969 paper on self-transcendence (the layer above self-actualization, where humans find highest meaning by orienting toward something beyond themselves); Batson's perspective-taking research on empathy.

**The Design Problem:** "Do you care about others?" is tautological—everyone says yes. But *radius of concern* is measurable through *frame of reference*. When someone thinks about a tough moment, whose perspective comes to mind first—theirs, the team's, another individual's, or the system/customer they serve?

1. **A3_OPEN**: "Who comes to mind?" Not "Who matters?" but "Who comes to mind?" This taps spontaneous attention and concern, not values.

2. **A3_PERSPECTIVE**: "Did you wonder what it was like for someone else?" This measures *actual perspective-taking*. Wondering is passive; asking is active. The progression (self → team → customer) measures concentric circles of concern.

3. **A3_MEANING**: "What gave you meaning today?" Maslow argued that humans find peak meaningfulness through transcendence—serving something beyond themselves. This question surfaces where the employee *actually* found meaning (achievement, team, helping, transcendence), not where they *think* they should.

**Trade-offs:** I considered framing this as "team collaboration" (many reflection tools do) but that misses the transcendence layer. Collaboration among equals is valuable but not self-transcendence. I kept the radius wide enough to distinguish team-thinking (we're in this together) from altrocentrism (I'm thinking about their experience) from transcendence (I'm part of something larger).

---

## Branching Logic: Design Decisions

### Principle 1: Honest Dichotomies

Each branching point reflects a *real* spectrum, not a false binary. For example:
- **Not** "Do you have agency?" (yes/no)
- **But** "What made the difference?" with options like "I prepared," "Team helped," "Lucky," "Adapted"
- Each option is genuinely different and places candidates at different points on the locus spectrum

### Principle 2: Convergence on Narrative

All Axis 1 paths converge at **A1_DEEP** (the narrative/story question) before moving to Axis 2. Why? Because *understanding your own story* is the prerequisite for growth. If I jump straight to contribution or transcendence without establishing narrative clarity, the reflections won't land.

The convergence pattern is not punitive—it's *scaffolding*. By the time someone reaches A1_DEEP, they've answered two questions from different angles, so the deeper question lands harder.

### Principle 3: Interpolation for Personalization

Every reflection uses `{answer.label}` to echo back the person's exact words:
```
"You said it was {A1_OPEN.label}. When things got difficult..."
```
This accomplishes two things:
- **Validation:** "I heard you."
- **Accountability:** The reflection is about *their* answer, not generic advice.

---

## Psychological Grounding: Sources

- **Rotter, J. B. (1954).** "Social learning and clinical psychology." Locus of control scale; foundational work on attribution.
- **Dweck, C. S. (2006).** "Mindset: The New Psychology of Success." Growth vs. fixed mindset; how people narrate ability.
- **Campbell, M. C., Inman, J. J., & Kirmani, A. (2004).** "The endowment effect as a self-affirmation phenomenon." Psychological entitlement; how people justify deserving rewards.
- **Organ, D. W. (1988).** "Organizational Citizenship Behavior." Discretionary effort beyond job description.
- **Batson, C. D. (2011).** "Altruism in Humans." Perspective-taking vs. sympathy; the cognitive act of imagining another's experience.
- **Maslow, A. H. (1969).** "The psychology of science" and related works. Self-transcendence as peak human development; meaning through service.

---

## What I'd Improve With More Time

1. **Branching sophistication:** Currently, some decision nodes use simple signal-tallying. With more time, I'd add *weighted signals* (some answers more predictive than others) and *temporal sequencing* (adjust follow-ups based on not just answers but answer patterns).

2. **Reflection depth:** Each reflection is 1-3 sentences. Ideal reflections would be **3-5 sentences with a concrete next-step question**: not prescriptive ("You should...") but invitational ("What would change if...?").

3. **Cultural adaptation:** The tree is currently written for a Western, individualist context. Transcendence looks different in a collectivist culture. Entitlement looks different across socioeconomic backgrounds. With time, I'd create culture-specific variants or at least flag points where the tree might land differently.

4. **Integration with action:** The tree ends with clarity. Next step: a *recommendation engine* that suggests practices based on axis scores. (Not LLM-driven—just static mappings: "If axis1:external + axis3:self_centric, here are 3 practices that build agency while expanding perspective.")

5. **Session history:** Track how an employee moves across 30 days. Are they trending toward internal locus? Contributing more? Widening radius? ***That's the real product***—not a single evening reflection, but a signal of trajectory.

---

## Why Determinism Matters

At DT, we believe deterministic systems are **trustworthy**. An LLM might hallucinate wisdom or give inconsistent advice across days. This tree gives the same reflection every time because *a human designed it carefully*. That care is the feature.

The cost: this tree can only reflect the axes it's designed for. It won't discover new psychological insights or adapt to individual idiom. But that constraint is a feature too—it forces clarity. Every word in every reflection had to be considered, not generated.

---

## Conclusion

This tree is an **artifact of knowledge engineering**—the core skill at DT. It takes three validated psychological insights (Locus, Entitlement, Transcendence) and encodes them into a branching conversation that helps people see themselves more clearly. No LLM. No ambiguity. Just structure, care, and the chance for an employee to know themselves a little better before they go home.

