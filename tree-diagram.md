# Daily Reflection Tree - Visual Structure

## Mermaid Diagram (Main Paths)

```mermaid
graph TD
    START["🌙 START<br/>Good evening.<br/>Let's look at your day."]
    
    A1_OPEN["📋 AXIS 1 OPEN<br/>How would you<br/>describe today?"]
    
    START --> A1_OPEN
    
    %% AXIS 1: Two main paths
    A1_OPEN -->|Productive/Mixed| A1_INTERNAL["❓ When something went well,<br/>what made the difference?"]
    A1_OPEN -->|Tough/Frustrating| A1_EXTERNAL["❓ When something didn't go as planned,<br/>what did you do?"]
    
    %% AXIS 1: Internal Path outcomes
    A1_INTERNAL -->|prepared/adapted| A1_R_INTERNAL["✨ REFLECT: You see your hand<br/>in what happened."]
    A1_INTERNAL -->|team| A1_R_COLLAB["✨ REFLECT: You brought people<br/>with you."]
    A1_INTERNAL -->|lucky| A1_R_LUCK["✨ REFLECT: Maybe you're<br/>underselling yourself."]
    
    %% AXIS 1: External Path outcomes
    A1_EXTERNAL -->|controlled/support| A1_R_FOUND["✨ REFLECT: You found your<br/>agency anyway."]
    A1_EXTERNAL -->|persisted| A1_R_EFFORT["✨ REFLECT: Effort is real.<br/>But did you have a choice?"]
    A1_EXTERNAL -->|stuck| A1_R_OVERWHELMED["✨ REFLECT: Even in being stuck,<br/>you're still here."]
    
    %% Converge on A1 Deep Question
    A1_R_INTERNAL --> A1_DEEP["❓ What's your story about<br/>why things happened?"]
    A1_R_COLLAB --> A1_DEEP
    A1_R_LUCK --> A1_DEEP
    A1_R_FOUND --> A1_DEEP
    A1_R_EFFORT --> A1_DEEP
    A1_R_OVERWHELMED --> A1_DEEP
    
    A1_DEEP -->|owned/collaborative| A1_SUMMARY_INT["✨ SUMMARY: You see yourself<br/>in what happened."]
    A1_DEEP -->|luck/others| A1_SUMMARY_EXT["✨ SUMMARY: Where did you<br/>have a choice?"]
    
    %% Bridge to Axis 2
    A1_SUMMARY_INT --> BRIDGE_1_2["🌉 BRIDGE<br/>Now let's shift from agency<br/>to what you gave."]
    A1_SUMMARY_EXT --> BRIDGE_1_2
    
    %% AXIS 2
    BRIDGE_1_2 --> A2_OPEN["📋 AXIS 2 OPEN<br/>What did you give?<br/>What did you need?"]
    
    A2_OPEN -->|helped/taught| A2_CONTRIB["❓ What made you take<br/>that action?"]
    A2_OPEN -->|frustrated/unsupported| A2_ENTITLE["❓ When you look at that,<br/>what did you feel?"]
    
    %% AXIS 2: Contribution Path
    A2_CONTRIB -->|empathy/principle| A2_R_TRUE["✨ REFLECT: Contribution without<br/>keeping score."]
    A2_CONTRIB -->|earned| A2_R_WITH_EXP["✨ REFLECT: Contribution with<br/>a ledger."]
    A2_CONTRIB -->|compliance| A2_R_PERFORMANCE["✨ REFLECT: Motivated by<br/>avoiding bad, not moving toward good."]
    
    %% AXIS 2: Entitlement Path
    A2_ENTITLE -->|responsible| A2_R_BOUNDARY["✨ REFLECT: Healthy boundary."]
    A2_ENTITLE -->|resentful/invisible/depleted| A2_R_RESENTMENT["✨ REFLECT: Entitlement is<br/>an invisible deal."]
    
    %% Converge on A2 Recognition
    A2_R_TRUE --> A2_RECOGNITION["❓ Did you need someone<br/>to notice?"]
    A2_R_WITH_EXP --> A2_RECOGNITION
    A2_R_PERFORMANCE --> A2_RECOGNITION
    A2_R_BOUNDARY --> A2_RECOGNITION
    A2_R_RESENTMENT --> A2_RECOGNITION
    
    A2_RECOGNITION -->|appreciated/intrinsic| A2_SUMMARY_CONTRIB["✨ SUMMARY: You're oriented<br/>toward contribution."]
    A2_RECOGNITION -->|frustrated/expected| A2_SUMMARY_ENTITLE["✨ SUMMARY: You're waiting<br/>for recognition."]
    
    %% Bridge to Axis 3
    A2_SUMMARY_CONTRIB --> BRIDGE_2_3["🌉 BRIDGE<br/>One last shift: who did<br/>you show up for?"]
    A2_SUMMARY_ENTITLE --> BRIDGE_2_3
    
    %% AXIS 3
    BRIDGE_2_3 --> A3_OPEN["📋 AXIS 3 OPEN<br/>Whose perspective comes<br/>to mind?"]
    
    A3_OPEN -->|just me| A3_SELF["SELF-CENTRIC PATH"]
    A3_OPEN -->|my team| A3_TEAM["TEAM-CENTRIC PATH"]
    A3_OPEN -->|someone else/customer| A3_OTHER["ALTROCENTRIC PATH"]
    
    A3_SELF --> A3_SELF_R["✨ REFLECT: Self-oriented<br/>vs Self-Transcendent"]
    A3_TEAM --> A3_TEAM_R["✨ REFLECT: Collective<br/>problem-solving"]
    A3_OTHER --> A3_OTHER_R["✨ REFLECT: Self-transcendence<br/>is real meaning"]
    
    %% Converge on Summary
    A3_SELF_R --> SUMMARY["📊 SUMMARY<br/>Agency + Contribution + Radius<br/>{interpolated reflection}"]
    A3_TEAM_R --> SUMMARY
    A3_OTHER_R --> SUMMARY
    
    %% Meta & End
    SUMMARY --> META["❓ What surprised you<br/>about your answers?"]
    META --> END["🌙 END<br/>Thank you.<br/>Come back tomorrow."]
    
    %% Styling
    classDef start fill:#d4f1d4,stroke:#2d5a2d,stroke-width:3px
    classDef question fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef reflection fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef summary fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef bridge fill:#ffe0b2,stroke:#e65100,stroke-width:2px
    classDef end fill:#ffcdd2,stroke:#c62828,stroke-width:3px
    
    class START start
    class A1_OPEN,A1_INTERNAL,A1_EXTERNAL,A1_DEEP,A2_OPEN,A2_CONTRIB,A2_ENTITLE,A2_RECOGNITION,A3_OPEN question
    class A1_R_INTERNAL,A1_R_COLLAB,A1_R_LUCK,A1_R_FOUND,A1_R_EFFORT,A1_R_OVERWHELMED,A1_SUMMARY_INT,A1_SUMMARY_EXT reflection
    class A2_R_TRUE,A2_R_WITH_EXP,A2_R_PERFORMANCE,A2_R_BOUNDARY,A2_R_RESENTMENT,A2_SUMMARY_CONTRIB,A2_SUMMARY_ENTITLE reflection
    class A3_SELF_R,A3_TEAM_R,A3_OTHER_R reflection
    class SUMMARY,META summary
    class BRIDGE_1_2,BRIDGE_2_3 bridge
    class END end
```

## Tree Statistics

- **Total Nodes:** 44
- **Question Nodes:** 9
  - Axis 1: 3 questions (A1_OPEN, A1_INTERNAL/EXTERNAL, A1_DEEP)
  - Axis 2: 3 questions (A2_OPEN, A2_CONTRIBUTION/ENTITLEMENT paths, A2_RECOGNITION)
  - Axis 3: 3 questions (A3_OPEN, A3_PERSPECTIVE, A3_MEANING)

- **Decision Nodes:** 8
  - Route based on answer selection
  - Route based on accumulated signals

- **Reflection Nodes:** 11
  - Each major node leads to personalized reflection
  - Reflections reference answers via interpolation

- **Bridge Nodes:** 2
  - Connect Axis 1→2
  - Connect Axis 2→3

- **Summary & End Nodes:** 3
  - Final synthesis
  - Meta-reflection
  - Closing

## Key Branching Points

### Axis 1: External vs Internal Locus
```
A1_OPEN (1 question, 4 options)
├─ [Productive/Mixed] → A1_INTERNAL_Q
│  ├─ [prepared/adapted] → Reflects internal agency ✓
│  ├─ [team] → Reflects collaborative agency ✓
│  └─ [lucky] → Reflects external attribution ✗
└─ [Tough/Frustrating] → A1_EXTERNAL_Q
   ├─ [controlled/support] → Reflects found agency ✓
   ├─ [persisted] → Reflects mixed agency ~
   └─ [stuck] → Reflects external helplessness ✗
```

### Axis 2: Contribution vs Entitlement
```
A2_OPEN (1 question, 4 options)
├─ [helped/taught] → A2_CONTRIBUTION_PATH
│  └─ [empathy/principle] → True contribution
│  └─ [earned] → Contribution with expectation
│  └─ [compliance] → Performance-driven
└─ [frustrated/unsupported] → A2_ENTITLEMENT_PATH
   └─ [responsible] → Healthy boundary
   └─ [resentful/invisible/depleted] → Entitlement pattern
```

### Axis 3: Self-Centric vs Altrocentric
```
A3_OPEN (1 question, 4 options)
├─ [just me] → Self-centric (narrow radius)
├─ [my team] → Team-centric (widened radius)
├─ [someone else] → Other-centric (empathic)
└─ [customer] → Systemic-centric (widest radius)
```

## Example Paths

### "Victim" Path (All External Attribution)
```
START 
→ A1_OPEN: Tough
→ A1_EXTERNAL: stuck
→ A1_DEEP: others caused it
→ A2_OPEN: needed support, didn't get it
→ A2_ENTITLEMENT: invisible
→ A3_OPEN: just me
→ A3_MEANING: personal achievement
→ SUMMARY: "external...entitlement...self-centric"
```

### "Victor/Aligned" Path (Internal, Contribution, Transcendent)
```
START
→ A1_OPEN: Mixed
→ A1_INTERNAL: adapted
→ A1_DEEP: we made it together
→ A2_OPEN: taught someone
→ A2_CONTRIBUTION: saw need
→ A3_OPEN: someone struggling more
→ A3_MEANING: part of something bigger
→ SUMMARY: "internal...contribution...altrocentric (transcendent)"
```

## Design Principle: Convergence

Notice that all paths converge at **A1_DEEP** (the deep narrative question). This is intentional:

- **Paths before A1_DEEP** explore surface-level responses (what they did, how they felt)
- **A1_DEEP** asks: what *story* did they tell themselves?
- **Story is deeper than behavior.** A person can adapt (behavior = internal) but still feel like things happen to them (story = external). This question surfaces the narrative beneath the action.
- **All roads converge** to create a unified reflection from Axis 1

Similar structure repeats for Axes 2 and 3, but without over-converging. The goal is guidance, not funneling everyone to the same conclusion.

