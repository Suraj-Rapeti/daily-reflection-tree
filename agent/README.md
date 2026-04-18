# Reflection Agent - Quick Start

## Installation & Setup

### Requirements
- Python 3.7+
- No external packages (uses only Python stdlib)

### Running the Agent

From the `agent/` directory:

```bash
python reflection_agent.py
```

The script will:
1. Load the tree from `../reflection-tree.json`
2. Guide you through a ~10 minute reflection session
3. Prompt you at each question
4. Display your final axis scores
5. Save a transcript to `../last_session_transcript.txt`

---

## How to Use

### During a Session

```
[START]
Good evening. Before you go home, let's take 10 minutes to look at your day.

Press Enter to begin...
```

Press Enter to proceed.

### When You See a Question

```
[QUESTION]

How would you describe today in one word?

Choose one:
  1) Productive
  2) Mixed
  3) Tough
  4) Frustrating

Your choice (1-4): 
```

Type the number (1, 2, 3, or 4) and press Enter.

### When You See a Reflection

```
[REFLECTION]

You see your hand in what happened today. That's agency — not everything 
went your way, but you stayed in the driver's seat.

Press Enter to continue...
```

Read the reflection, then press Enter to move forward.

### At the End

You'll see:
```
════════════════════════════════════════════════════════════════════════
SESSION SUMMARY
════════════════════════════════════════════════════════════════════════

Axis 1 (Locus): axis1:internal
  Internal: 3
  External: 1
  Mixed: 0

Axis 2 (Orientation): axis2:contribution
  Contribution: 3
  Entitlement: 0
  Mixed: 0

Axis 3 (Radius): axis3:altrocentric
  Self-Centric: 0
  Team-Centric: 1
  Altrocentric: 2

════════════════════════════════════════════════════════════════════════
```

This shows your axis scores. A transcript will be saved to `../last_session_transcript.txt`.

---

## Understanding Your Results

### Axis 1: Locus of Control

**Internal** = You see your hand in what happens. You adapt, respond, take agency even when things are hard.

**External** = You see circumstances as driving. Others control outcomes. Things happen to you.

**Mixed** = Sometimes you act, sometimes you feel stuck. This is normal—humans aren't consistently one way.

### Axis 2: Contribution Orientation

**Contribution** = You give without keeping score. You help because people need it, or because it's right.

**Entitlement** = You expect recognition for effort. You feel invisible or resentful when unappreciated.

**Mixed** = Sometimes you contribute genuinely, sometimes you expect payback.

### Axis 3: Radius of Concern

**Self-Centric** = Your focus is personal—your achievement, your work, your success.

**Team-Centric** = You think about the team's problems. You solve things together.

**Altrocentric** = You think about another person's experience. You care about them specifically.

**(Transcendent)** = You feel part of something larger. Meaning comes from serving beyond yourself.

---

## What the Scores Mean

This tool is **not diagnostic**. It's a mirror.

- **All external locus?** Reflect: Where did you have a choice today, even a small one?
- **All entitlement?** Reflect: What would change if you contributed without expecting return?
- **All self-focused?** Reflect: Whose experience did you not consider today?

The goal is **clarity, not judgment.** Use these scores to ask yourself better questions, not to feel bad.

---

## Exporting & Analyzing Results

After each session, a transcript is saved to `../last_session_transcript.txt`. This file contains:

```
REFLECTION SESSION TRANSCRIPT
════════════════════════════════════════════════════════════════════════

Q: A1_OPEN
A: Frustrating

[Signal: axis1:external]

Q: A1_EXTERNAL_Q
A: I felt stuck and waited for the situation to change

[Signal: axis1:external]

...

FINAL AXIS SCORES:
Axis 1 (Locus): axis1:external
Axis 2 (Orientation): axis2:entitlement
Axis 3 (Radius): axis3:self_centric
```

You can:
- **Build a spreadsheet** of sessions over time and track personal growth
- **Identify patterns** ("I always lean external on Mondays")
- **Share with a mentor** to discuss growth areas
- **Set goals** based on axis scores you want to shift

---

## Customizing the Tree

The agent loads `../reflection-tree.json`, which is a standard JSON file. You can:

1. **Edit questions:** Change the `text` field in any question node
2. **Add/remove options:** Modify the `options` array
3. **Change reflections:** Edit `text` in reflection nodes
4. **Adjust routing:** Modify `routing` in decision nodes

After changes, just re-run the agent. It will reload the updated tree.

Example: To add a new option to Axis 1:

```json
{
  "id": "A1_OPEN",
  "type": "question",
  "text": "How would you describe today?",
  "options": [
    {"value": "productive", "label": "Productive"},
    {"value": "mixed", "label": "Mixed"},
    {"value": "tough", "label": "Tough"},
    {"value": "frustrating", "label": "Frustrating"},
    {"value": "energizing", "label": "Energizing"}  // New option
  ]
}
```

---

## Troubleshooting

### "Tree file not found"

Make sure you're running from the `agent/` directory:

```bash
cd agent/
python reflection_agent.py
```

The script looks for `../reflection-tree.json` relative to itself.

### Agent crashes or shows errors

Check `reflection-tree.json` for valid JSON syntax:

```bash
python -m json.tool ../reflection-tree.json
```

This will validate the JSON and show any syntax errors.

### Transcript not saved

Check that the `agent/` directory has write permissions.

---

## Development Notes

### Agent Architecture

The agent is a state machine:

1. **Load tree** → Deserialize JSON into node dictionary
2. **Initialize state** → Create `SessionState` with defaults
3. **Loop:**
   - Get current node
   - If question: display options, wait for input, record answer
   - If reflection: display text (with interpolation), wait for continue
   - If decision: evaluate routing logic, determine next node
   - If bridge/start/summary: display and auto-advance
   - Move to next node
   - Repeat until node == "END"
4. **Finalize** → Print axis scores, export transcript

### Key Methods

- `interpolate_text()` — Replace `{placeholders}` with actual answers
- `evaluate_decision()` — Parse routing conditions and determine target
- `get_next_node()` — Determine next node (follow target or children)
- `record_answer()` — Store user selection and add to transcript
- `add_signal()` — Tally signal for axis scoring
- `_get_dominant_axis()` — Determine which pole of an axis is strongest
- `export_transcript()` — Write session history to file

### Extending the Agent

To add new features (e.g., save to database, add LLM-based suggestions for reflection):

```python
class ReflectionAgent:
    # ... existing code ...
    
    def save_to_database(self, db_connection):
        """Example: persist session to a database"""
        db_connection.insert("sessions", {
            "timestamp": datetime.now(),
            "answers": self.state.answers,
            "axis_scores": {
                "axis1": self._get_dominant_axis("axis1"),
                "axis2": self._get_dominant_axis("axis2"),
                "axis3": self._get_dominant_axis("axis3"),
            }
        })
```

---

## Future Enhancements

Possible extensions (outside scope of current assignment):

1. **Web UI** — Replace CLI with Flask/Django web interface
2. **Multi-session tracking** — Store interviews in a database, show trends
3. **Adaptive branching** — Adjust questions based on prior sessions
4. **Metrics dashboard** — Visualize axis trends over time
5. **Peer comparison** — Anonymized aggregate stats ("How do I compare to my peers?")
6. **Export formats** — PDF reports, CSV compatibility, etc.
7. **Accessibility** — Screen reader support, voice input

All of these could leverage the tree structure without adding LLM runtime calls.

