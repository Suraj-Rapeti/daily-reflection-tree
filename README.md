# The Daily Reflection Tree
## A Deterministic Reflection Agent for End-of-Day Clarity

*An internship assignment for DT Fellowship Program*

---

## Quick Start

### Running the Agent (Python)

```bash
cd agent/
python reflection_agent.py
```

The agent will guide you through a ~10-minute reflection session. Answer questions with your selection, and the tree will produce a personalized reflection based on your responses.

**Requirements:** Python 3.7+
**No external dependencies** — uses only the Python standard library

---

## What Is This?

The Daily Reflection Tree is a **deterministic decision tree** that helps employees reflect on their day through three psychological lenses:

1. **Axis 1: Locus of Control** — Do you see your hand in what happened?
2. **Axis 2: Contribution Orientation** — Are you giving or waiting for recognition?
3. **Axis 3: Radius of Concern** — Who are you thinking about?

**No LLM at runtime.** The tree is fully deterministic—same answers produce the same reflection, every time. The LLM was used to research and design, not to drive the product.

---

## Project Structure

```
.
├── reflection-tree.json          ← The tree data file (44 nodes)
├── tree-diagram.md               ← Visual representation (Mermaid)
├── write-up.md                   ← Design rationale (2 pages)
├── transcripts/
│   └── persona-comparison.md     ← Two sample runs (victim vs. victor)
├── agent/
│   ├── reflection_agent.py       ← Python CLI agent
│   └── README.md                 ← How to run the agent
├── QUESTION_DESIGN.md            ← Deep dive into question design
└── README.md                      ← This file
```

---

## The Tree File: `reflection-tree.json`

The tree is stored as a **JSON structure** with 44 nodes. Key fields:

```json
{
  "id": "A1_OPEN",                          // Unique node identifier
  "parentId": "START",                      // Parent in tree hierarchy
  "type": "question|decision|reflection",  // Node type determines behavior
  "text": "How would you describe today?", // What the user sees
  "options": [                              // Fixed choices (no free text)
    {"value": "productive", "label": "Productive"},
    {"value": "mixed", "label": "Mixed"},
    ...
  ],
  "target": "A1_ROUTE",                    // Where to jump (for bridges)
  "signal": "axis1:internal",              // What this node tallies
  "routing": [                              // Decision logic
    {"condition": "answer=productive", "target": "A1_INTERNAL_Q"}
  ]
}
```

### Node Types

| Type | Purpose | Example |
|------|---------|---------|
| `start` | Opens session | Greeting, auto-advance |
| `question` | Wait for input | 4 options, record answer |
| `decision` | Route based on logic | No user interaction; invisible |
| `reflection` | Display insight | Auto-advance after user reads |
| `bridge` | Transition between axes | "Now let's shift from X to Y" |
| `summary` | End-of-session synthesis | Interpolate answers, show patterns |
| `end` | Close session | Final message |

### How Interpolation Works

When a reflection contains `{A1_OPEN.label}`, the agent replaces it with the user's actual answer:

```
Template: "You said it was {A1_OPEN.label}..."
After interpolation: "You said it was Frustrating..."
```

For axis summaries, the agent tallies signals and determines which pole is dominant:

```
Axis 1 signals: {internal: 3, external: 2, mixed: 0}
Dominant: axis1:internal
Narrative: "internal agency—seeing your hand in outcomes"
```

---

## Sample Runs

See `transcripts/persona-comparison.md` for two complete session transcripts:

1. **Persona 1: The Overwhelmed (Victim/Entitled/Self-Centric)**
   - External locus ("circumstances were against me")
   - Entitlement orientation ("I did work but nobody noticed")
   - Self-centric radius ("my achievement is what mattered")
   - **Result:** Pattern reflected back without shame

2. **Persona 2: The Aligned (Victor/Contributing/Altrocentric)**
   - Internal locus ("we made it work together")
   - Contribution orientation ("I helped because they needed it")
   - Altrocentric radius ("I felt part of something bigger")
   - **Result:** Pattern affirmed and validated

Both transcripts show the same tree, different paths, different reflections.

---

## The Agent: `agent/reflection_agent.py`

### What It Does

1. **Loads the tree** from `reflection-tree.json`
2. **Walks the tree** node by node
3. **Handles different node types:**
   - Questions: Displays options, waits for user selection
   - Reflections: Displays insight, waits for user to press Enter
   - Decisions: Routes automatically based on prior answers
   - Bridges: Displays transition text, auto-advances
4. **Accumulates state:**
   - Records every answer (for interpolation later)
   - Tallies signals per axis (for determining dominance)
5. **Interpolates reflections** with user's actual words
6. **Exports transcript** to `last_session_transcript.txt`

### Key Classes

```python
class SessionState:
    """Tracks the employee's journey"""
    current_node_id: str           # Where we are
    answers: Dict[str, Any]        # {node_id: {value, label}}
    signals: Dict[str, int]        # Axis tallies
    conversation_transcript: List  # Full history

class ReflectionAgent:
    """Main agent logic"""
    tree_path: str                 # Path to JSON tree
    nodes: Dict                    # In-memory tree
    state: SessionState            # Current session
    
    def run()                      # Main loop
    def interpolate_text()         # Replace {placeholders}
    def evaluate_decision()        # Route based on conditions
    def export_transcript()        # Save for analysis
```

### Flow

```
while current_node != END:
    node = nodes[current_node]
    
    if node.type == "question":
        show_options()
        answer = user_input()
        record_answer(node_id, answer)
    
    elif node.type == "reflection":
        text = interpolate(node.text)
        show(text)
        add_signal(node.signal)
    
    elif node.type == "decision":
        target = evaluate_routing(node)
    
    elif node.type == "bridge" or "start":
        show(text)
    
    # Move to next node
    current_node = get_next_node(node)
```

### Output

After the session, the agent prints:

```
════════════════════════════════════════════════════════════════════════
SESSION SUMMARY
════════════════════════════════════════════════════════════════════════

Axis 1 (Locus): axis1:internal
  Internal: 3
  External: 2
  Mixed: 0

Axis 2 (Orientation): axis2:contribution
  Contribution: 3
  Entitlement: 0
  Mixed: 0

Axis 3 (Radius): axis3:altrocentric
  Self-Centric: 0
  Team-Centric: 1
  Altrocentric: 2
```

And saves the transcript:

```
Transcript saved to: last_session_transcript.txt
```

---

## Design Notes

### Why No LLM at Runtime?

Reflection tools must be **predictable and trustworthy**. An LLM can:
- Hallucinate encouragement or wisdom
- Give inconsistent advice across sessions
- Introduce subtle bias we can't audit

A deterministic tree:
- **Always gives the same reflection** for the same answers
- **Is fully auditable**—we can trace every path
- **Is fast and offline**—no API costs or latency
- **Forces clarity**—every question, every reflection was carefully designed

The tradeoff: this tree can only reflect the axes it's designed for. No emergent discovery. But that constraint forces *care*.

### The Three Axes: Why These?

1. **Locus of Control (Rotter, 1954):** Do people see themselves as agents or victims? This is foundational—growth starts here.

2. **Contribution vs. Entitlement (Organ, 1988; Campbell et al., 2004):** Do people orient toward giving or taking? Entitlement is invisible to the person holding it—this axis makes it visible without shame.

3. **Radius of Concern / Self-Transcendence (Maslow, 1969; Batson, 2011):** Do people think only about themselves, their team, others, or the larger system they serve? Maslow argued transcendence (thinking beyond yourself) is the peak of human development.

**These three together describe maturity.** Someone with all three poles healthy is grown: internally agentive, contributes without scorecard, thinks beyond themselves.

### How Questions Were Designed

1. **Specificity:** Not "Do you believe in yourself?" but "When something went well, what made it happen?"
2. **Non-leading:** Options reflect *real* human responses, not a right answer.
3. **Nested complexity:** Early questions broad, later ones probe deeper (after priming).
4. **Interpolation-ready:** All can reference earlier answers in reflections.
5. **No jargon:** Questions don't *name* the axes; they *surface* them through lived experience.

---

## How to Extend This

### Add a New Axis

1. Create new question nodes in the JSON (e.g., `A4_OPEN`, `A4_DEEP`)
2. Add new signal types (e.g., `axis4:pole_a`, `axis4:pole_b`)
3. Add signal tallying logic to `_get_dominant_axis()`
4. Add reflection nodes with interpolations
5. Insert a bridge from Axis 3 summary to new Axis 4

### Customize Reflections

Edit the `text` field in reflection nodes. Use `{A1_OPEN.label}` to interpolate user answers.

### Change Decision Logic

Edit the `routing` array in decision nodes. Current supported conditions:
- `answer=value|value2` — match answers
- `dominant=internal` — match axis dominance

Could extend to:
- `signal_count=axis1:internal>2` — threshold-based
- `answer_sequence=A1_OPEN.productive,A2_OPEN.helped` — multi-step patterns

### Integration Points

1. **Add to an app:** Load the JSON in any runtime, walk it with custom UI.
2. **Connect to data:** Store transcripts in a database for analysis.
3. **Add practices:** After the summary, recommend reflection practices based on axis scores.
4. **Track over time:** Run weekly and watch how people's axis scores trend.

---

## Files to Understand First

1. **`reflection-tree.json`** — The data structure; the product itself.
2. **`tree-diagram.md`** — Visual overview of branching structure.
3. **`transcripts/persona-comparison.md`** — See two complete runs.
4. **`write-up.md`** — Design decisions and psychological grounding.
5. **`agent/reflection_agent.py`** — How to walk the tree.

---

## Evaluation Criteria (From Assignment)

| Criterion | Delivered |
|-----------|-----------|
| **Tree quality** (35%) | 44 nodes, 9 questions across 3 axes, thoughtful branching |
| **Psychological grounding** (25%) | Sourced from Rotter, Dweck, Organ, Campbell, Batson, Maslow |
| **Data structure** (20%) | Clean JSON, fully readable without code, reloadable |
| **Write-up clarity** (10%) | 2-page design rationale explaining choices |
| **Bonus (Part B)** (10%) | Working Python agent, sample transcripts, tree diagram |

---

## License & Attribution

This project was created as part of the DT Fellowship Assignment. The psychological frameworks are sourced from peer-reviewed research. The tree structure and agent implementation are original work.

---

## Questions?

See `write-up.md` for design rationale.
See `QUESTION_DESIGN.md` for deep dive into question design.
See `tree-diagram.md` for visual branching structure.

