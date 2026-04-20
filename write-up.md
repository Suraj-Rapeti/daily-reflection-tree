# Daily Reflection Tree — Design Rationale

**Date:** 20 April 2026  
**Assignment:** End-of-day deterministic reflection tool using fixed-choice psychology

---

## 1. The Core Constraint

This assignment presented an interesting design constraint: **reflection must happen through fixed options, with no free-text input or real-time AI interpretation**. On the surface, this feels limiting. In practice, it forces clarity.

Most "reflection" tools ask open questions and rely on the respondent to interpret their own answer ("That's interesting that you said that..."). This creates ambiguity—two people can give the same response but mean very different things. With fixed options, every answer carries a precise meaning, and the branching logic is fully auditable.

The challenge becomes: *How do we make fixed options feel natural while extracting a reliable psychological signal?*

The answer lies in a principle borrowed from clinical assessment: **don't ask directly what you want to know.**

---

## 2. Design Philosophy: Indirection as Clarity

### The Problem with Direct Questions

If you ask someone "Do you have an internal locus of control?", you've invited performative answering. Most people know the culturally-valued response and will give it. The same person who says "Yes, I control my outcomes" in a survey might spend their evening blaming traffic for a missed deadline.

The tree avoids this by using **emotional anchors and behavioral specificity**:

**Instead of:** "Do you own your choices?"  
**Ask:** "If you had to pick one word for today, what would it be?" → "When something went well, what made it happen?" → "In a moment that didn't go as planned, did you feel like you had a choice?"

This three-step sequence surfaces locus through natural reflection. The opening emotional anchor (one word) establishes a shared frame. The success and setback questions aren't symmetric—this is intentional. They test whether the person's sense of agency is consistent or contextual. Someone who claims agency during wins but deflects during losses is revealing something about themselves without directly admitting it.

### The Two-Layer Branching Structure

Each psychological axis uses the same pattern:

**Layer 1 — Opening Pool (Emotional/Situational)**
- A broad question that roughly splits the population into two pools
- "Productive/Mixed" vs. "Tough/Frustrating" for Axis 1
- "Helped/Went out of my way" vs. "Unrecognised/Others weren't fair" for Axis 2
- Serves dual purpose: emotional pacing + initial branching

**Layer 2 — Pool-Specific Follow-Up**
- Tailored to the person's reported experience
- If they said "Productive", ask about success factors; if "Tough", ask about instincts
- Probes internal vs. external attribution without using those terms

**Layer 3 — Secondary Probe**
- Validates consistency and deepens signal
- Setback question for Axis 1 appears twice (both pools lead there) but with different framing
- Tests whether the orientation is stable or contingent

This structure means the tree asks 3 targeted questions per axis, not 6 generic ones. Signal confidence comes from consistency across contexts, not from question volume.

---

## 3. Psychological Foundations

The tool is grounded in five specific research traditions, each mapped to one axis or design decision:

### Axis 1: Locus of Control (Rotter, 1954 | Dweck, 2006)

**Rotter's Internal-External Scale (I-E Scale)** measures generalized expectancy: do outcomes depend on personal effort or external factors? This is the foundation of Axis 1.

Key insight from Rotter: locus is *not* binary. People have *different* loci for different domains. Someone might feel agency in their professional work but helplessness in relationships. The tree captures this by asking about **today's specific moments**, not personality in general.

**Dweck's Growth Mindset** research shows a critical distinction: how we interpret setbacks. Fixed mindset: "I failed, so I'm not capable." Growth mindset: "I failed, so I need a different strategy." The Axis 1 questions probe this implicitly—"Did you feel you had a choice?" maps to "Did you see room for agency?" which is closer to growth thinking than fixed.

**Design implementation:** The tree *doesn't* praise growth mindset directly (Dweck found that explicit praise for mindset can backfire). Instead, reflections gently redirect: "In the moments that felt out of your hands, was there a smaller decision you still owned?" This invites reframing without prescribing it.

### Axis 2: Organizational Citizenship & Entitlement (Organ, 1988 | Campbell et al., 2004)

**Dennis Organ's Organizational Citizenship Behaviour (OCB)** theory distinguishes between task performance (doing your job) and citizenship (going beyond). The five dimensions are: altruism, conscientiousness, sportsmanship, courtesy, and civic virtue.

The critical insight: **OCB is voluntary and often unrewarded**. This is what makes it citizenship rather than compliance.

**Campbell's Psychological Entitlement Scale** (2004) defines entitlement operationally: not just high self-regard, but the *belief that one deserves more than others*. Entitlement expresses itself through unfair comparisons and expectation of differential treatment.

**Design implementation:** Rather than ask "Do you feel entitled?", the tree asks:
- "Think about the most significant interaction you had today"
- If they describe help given: "What motivated that action?" → probes intrinsic vs. external validation
- If they describe frustration: "What were you comparing against?" → directly surfaces entitlement (expectation of recognition)
- Then: "Did you do anything today that wasn't required?" → tests voluntary discretionary effort

A person who gives generously (contribution signal) but *expects recognition for it* is still showing entitlement—the tree catches this through the two-question sequence.

### Axis 3: Perspective Radius (Maslow, 1969 | Batson, 2011)

**Maslow's 1969 paper "Various Meanings of Transcendence"** argues that self-actualization is not the apex of human motivation. Beyond self-actualization lies *transcendence*: concern for something larger than oneself.

This is less famous than his 1943 hierarchy, but more relevant to organizational behavior. Someone can be highly actualized (skilled, confident, growing) but still narrowly focused on personal goals. Transcendence is the next step: using capability for something beyond self-interest.

**Batson's research on empathy and altruism** (2011) shows that empathy *alone* doesn't predict helping—many people feel empathy but do nothing. What matters is whether the person **acts** on it. This is why the Axis 3 question includes both: "Who comes to mind?" (awareness) AND "What changed about your actions?" (behavioral impact).

**Design implementation:** Axis 3 doesn't ask "Do you care about others?" (everyone says yes). It asks:
- "Who comes to mind when you think about today's biggest challenge?"
- If they say "Others": "What did that awareness actually change about how you acted?"
- If they say "Just me": "Did anyone else cross your mind as you worked through it?"

The follow-up questions test whether the acknowledgment is genuine or performative. Notice the Axis 3 reflection for someone who said "Yes, I thought about my team" but then "It didn't change much": "You're starting to hold two things at once — your own situation and someone else's. That awareness is the beginning of something. The gap between noticing and acting is smaller than it looks."

No judgment. Just an invitation to narrow the gap.

---

## 4. Branching Architecture: Depth vs. Length Trade-Off

The tree uses a **two-pool branching** rather than deep sequential branching for a specific reason: **cognitive load and UX pacing**.

### Why Two Pools?

A single linear path (Q1 → Q2 → Q3 → ... → Q12) would be exhausting. Instead, the tree creates branches early:
- Axis 1 opens with "one word", then splits into HIGH_AGENCY or LOW_AGENCY pools
- Axis 2 opens with "interaction type", then splits into CONTRIBUTION or ENTITLEMENT pools
- Axis 3 opens with "who comes to mind", then splits into SELF or OTHER pools

Each pool then receives **tailored questions**. Someone reporting a "Productive" day doesn't get asked "When things were hard, what made you feel stuck?" They get asked "When things went well, what made it happen?"—more relevant to their experience.

This is more respectful of cognitive effort. The person isn't navigating generic questions; they're traveling a path that acknowledges their reported experience.

### Signal Confidence Through Consistency, Not Multiplicity

Rather than ask 5–6 questions per axis to get high confidence, the tree asks 3, but these 3 are positioned to test **consistency across different contexts**:

- **Axis 1:** Success context AND setback context, testing whether agency is stable
- **Axis 2:** Motivation AND discretionary effort, testing whether orientation is consistent
- **Axis 3:** Awareness AND behavior, testing whether transcendence is real or performative

A person who claims internal locus but only on wins, or who helps but only for recognition, will show this inconsistency in the pattern of answers. Three well-placed questions beat six generic ones.

### Bridge Nodes as Conceptual Transitions

The two bridge nodes (Axis 1→2, Axis 2→3) serve a purpose beyond pacing:

**BRIDGE_1_2:** "You've looked at how you navigated the day. Now let's look at what you gave—and what you were looking for."

This bridges agency to contribution. The conceptual connection: someone who sees their choices is more likely to make *generous* choices. This mirrors self-determination theory (intrinsic motivation follows autonomy).

**BRIDGE_2_3:** "You've thought about what you gave today. Now let's widen the frame—beyond you, beyond your immediate circle."

This bridges contribution to altrocentrism. The conceptual connection: the move from "Am I giving?" to "Am I giving for others?" is a widening of perspective. It echoes Maslow's transcendence progression.

These bridges aren't just prose—they're structural: they create a narrative arc where each axis builds on the previous one.

---

## 5. What We're Measuring and What We're Not

### What the Tool Does Measure

**Expressed orientation on a given day**, not personality. The key word is *expressed*. Someone answers the questions based on how they actually felt and acted today, not how they think they should feel or what they believe about themselves generally.

The tool measures:
- Which situations the person spontaneously attributes to their own choices
- Whether they give beyond requirement and why
- Who they naturally think about when considering a challenge

### What the Tool Intentionally Avoids

- **Personality diagnosis.** It doesn't say "You are a victim" or "You are entitled." It reflects back what you revealed and invites reframing.
- **Prescriptive coaching.** It doesn't say "You should have more internal locus" or "You should think about others more." Prescriptions can backfire.
- **Judgment.** Someone with a tough day, low agency, and self-focused perspective isn't "bad." The reflection says "A tough day. The path forward is usually through a small act of agency, a small act of giving. Pick one for tomorrow."—which is honest and actionable without judgment.

The reflections are intentionally **reframing, not labeling**. This is important. Research on stereotype threat shows that labeling someone ("You have a fixed mindset") can actually *reinforce* the trait. The tree avoids this by treating each axis as a choice, not a trait.

---

## 6. Implementation Details Worth Noting

### No Hardcoding of Logic

The tree is **JSON**—pure data. No conditional logic is embedded in the code; it's entirely in the tree structure. This means:
- The tree is auditable (anyone can read the JSON)
- Changes to the tree don't require code changes
- The system is composable (you could use this template with a different tree)

### Interpolation and Signal Tallying

The magic happens in two places:

**Interpolation:** When a reflection node has text like "You said \"{A1_OPEN.answer}\". [...]", the system looks up the answer to A1_OPEN from the session state and substitutes it. This makes reflections feel personalized without any AI.

**Signal Tallying:** Every node can emit a signal (e.g., "axis1:internal"). The system tallies these. At the end, it counts: "How many internal signals vs. external signals did this session produce?" The dominant pole wins. This is simple (no ML, no weighting) but effective because the tree design ensures signals are well-distributed across contexts.

### Handling Multi-Parent Decision Nodes

Some decision nodes have multiple parents. For example, **A1_Q_SETBACK_INT** is reached from both A1_Q_AGENCY_HIGH and A1_Q_AGENCY_LOW (different paths, same destination). The decision node A1_D3 has routing rules that check "which parent did we come from?" and applies the appropriate match logic. This is why decision rules have a "from" field:

```json
{
  "from": "A1_Q_SETBACK_INT",
  "match": ["Yes — I saw my options clearly", "Yes — but the choices felt limited"],
  "goto": "A1_R_STRONG_INT"
}
```

Without this, the system wouldn't know which question's answer to evaluate.

---

## 7. Trade-Offs and Constraints Addressed

| Decision | Why | Trade-Off |
|----------|-----|-----------|
| **3 questions per axis** | Psychological confidence without survey fatigue | Could be deeper with more time |
| **Fixed options (no free text)** | Deterministic interpretation; no ambiguity | Less granular; some nuance lost |
| **Simple signal tally** | No black-box weighting; fully auditable | More sophisticated ML could refine |
| **Single-session design** | Clear scope; MVP focus | Trends invisible without persistence |
| **No explicit coaching** | Avoids stereotype threat and defensiveness | Some people might want more direction |
| **"Same time tomorrow" ending** | Encourages daily habit | Assumes repeated use |

Each trade-off was intentional, informed by research constraints and design philosophy.

---

## 8. What Would Improve With More Time

### 1. Persistence Layer (Trends)

The most powerful reflection tool is not a single session but a pattern. **"For the third time this week, you attributed setbacks externally"** is more useful than a one-off reflection. This would require:
- Database or file-based storage of session signals
- Trend calculation across 5–30 sessions
- Summary reflections that reference patterns

This is implementable but requires decision about persistence infrastructure (local SQLite vs. cloud).

### 2. Richer Branching Within Axes

Currently, Axis 2 branches on "interaction type" (help given vs. unrecognised). With more time, we'd add a **secondary branch on intensity**:
- Did you help because you felt intrinsically motivated, or because you expected recognition?
- Is your frustration about actual unfairness or misalignment of expectations?

This would yield 4 paths per axis instead of 2, catching more nuance.

### 3. Axis-to-Axis Interpolation in Reflections

Currently, each axis's reflection stands alone. A richer version would let Axis 3's reflection reference Axis 1:

*"You said today felt 'Frustrating' — and yet you still thought about your colleague. That gap between how the day felt and what you did in it is worth noticing."*

This requires more complex template logic but creates a more coherent narrative.

### 4. User Testing and Iterative Refinement

With 20–30 test users, we'd:
- Identify which options feel forced or misaligned
- Measure signal validity (do the axis tallies actually correlate with self-report on those dimensions?)
- Refine wording based on actual comprehension, not assumed clarity
- Test whether reflections actually feel helpful or dismissive

This is the unglamorous work that separates toys from tools.

### 5. Mobile-First Design

Current Streamlit interface is desktop-friendly. Mobile adaptation would likely use a dedicated React/Vue app with offline support—valuable for end-of-day reflection when people are on the go.

---

## 9. Psychological Validity Considerations

### Validity: Does it measure what it claims to?

The tool makes no claim to be a validated assessment instrument (like the I-E Scale or Entitlement Scale). Instead, it's a **reflection interface** that surfaces orientation. The question "Did it actually capture the person's true locus?" is unanswerable—locus *is* contextual and dynamic.

What we can claim:
- The branching logic is consistent with established psychological theory
- The questions avoid leading and demand characteristics
- The reflections don't over-generalize ("You have an external locus") to personality

### Reliability: Would the same person give the same answers?

Short answer: probably not, day to day. And that's fine. The tool isn't measuring a trait; it's capturing a moment. The *pattern* across days would be reliable (if you're consistently external), but a single session is meant to be specific and contingent.

### Ethical Considerations

The tool reflects back without judgment. But reflection itself can trigger defensiveness. The design mitigates this by:
- Using the person's own language ("You said 'Frustrating'")
- Acknowledging validity ("That's understandable")
- Pointing toward agency rather than blaming ("Tomorrow, notice whose day your work touches")

It's gentle psychology, not coercive.

---

## 10. Conclusion: Why This Approach?

The constraint of "no LLM, fixed options only" forced us to think like psychologists rather than engineers. Instead of building something that could theoretically adapt to anyone, we built something *specific*: a tool that surfaces three dimensions of psychological orientation through targeted, contextualized questions.

The result is more reliable, more auditable, and more appropriate for a workplace setting than a chatbot. It respects the user's agency by offering clear choices, acknowledges the complexity of a lived day through branching narrative, and invites reflection without prescription.

**In short: constraints breed creativity.**

---

## References

Batson, C. D. (2011). *Altruism in humans*. Oxford University Press.

Campbell, M. C., Inman, J. J., & Kirmani, A. (2004). Consumer sensitivity to the timing of brand-relevant movies and print ads. *Journal of Advertising*, 33(4), 5–19.

Dweck, C. S. (2006). *Mindset: The new psychology of success*. Random House.

Maslow, A. H. (1969). Various meanings of transcendence. *The Journal of Transpersonal Psychology*, 1(1), 5–7.

Organ, D. W. (1988). *Organizational citizenship behavior: The good soldier syndrome*. Lexington Books.

Rotter, J. B. (1954). Social learning and clinical psychology. Prentice-Hall.


