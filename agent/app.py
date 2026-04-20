"""
Daily Reflection Tree — Streamlit Web App
Loads reflection-tree.json and walks the employee through a deterministic
reflection session. No LLM calls at runtime. Fully deterministic.

Run with:
    streamlit run agent/app.py
"""

import json
import streamlit as st # type: ignore
from pathlib import Path

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Daily Reflection",
    page_icon="🌙",
    layout="centered"
)

# ─── Styling ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Overall background */
    .stApp { background-color: #0f1117; }

    /* Hide default streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }

    /* Main content width */
    .block-container { max-width: 680px; padding-top: 2rem; }

    /* Question text */
    .question-text {
        font-size: 1.25rem;
        font-weight: 600;
        color: #f1f5f9;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }

    /* Reflection box */
    .reflection-box {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        color: #fde68a;
        font-size: 1.05rem;
        line-height: 1.7;
        margin: 1rem 0 1.5rem 0;
    }

    /* Bridge text */
    .bridge-text {
        color: #94a3b8;
        font-style: italic;
        font-size: 0.95rem;
        text-align: center;
        margin: 0.5rem 0 1.5rem 0;
    }

    /* Summary box */
    .summary-box {
        background: linear-gradient(135deg, #1a1f2e, #0f172a);
        border: 1px solid #4ade80;
        border-radius: 12px;
        padding: 1.8rem;
        color: #bbf7d0;
        font-size: 1rem;
        line-height: 1.9;
        margin: 1rem 0;
    }

    /* Axis label pills */
    .axis-pill {
        display: inline-block;
        background: #1e293b;
        border-radius: 999px;
        padding: 2px 12px;
        font-size: 0.8rem;
        color: #94a3b8;
        margin-bottom: 1rem;
    }

    /* Progress bar colour override */
    .stProgress > div > div > div > div {
        background-color: #6366f1;
    }

    /* Radio button labels */
    div[data-testid="stRadio"] label {
        color: #cbd5e1 !important;
        font-size: 1rem;
    }
    div[data-testid="stRadio"] label:hover {
        color: #f1f5f9 !important;
    }

    /* Button */
    .stButton > button {
        background-color: #6366f1;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        margin-top: 0.5rem;
        transition: background 0.2s;
    }
    .stButton > button:hover {
        background-color: #4f46e5;
        color: white;
    }

    /* Divider */
    hr { border-color: #1e293b; }
</style>
""", unsafe_allow_html=True)


# ─── Tree Loader ──────────────────────────────────────────────────────────────
@st.cache_resource
def load_tree() -> dict:
    here = Path(__file__).parent
    tree_path = here.parent / "tree" / "reflection-tree.json"
    with open(tree_path) as f:
        data = json.load(f)
    return {n["id"]: n for n in data["nodes"]}


# ─── State Helpers ────────────────────────────────────────────────────────────
def init_state():
    if "current_node" not in st.session_state:
        st.session_state.current_node = "START"
    if "answers" not in st.session_state:
        st.session_state.answers = {}          # node_id → answer string
    if "signals" not in st.session_state:
        st.session_state.signals = {}          # "axis1:internal" → count
    if "path" not in st.session_state:
        st.session_state.path = []
    if "done" not in st.session_state:
        st.session_state.done = False
    if "pending_reflection" not in st.session_state:
        st.session_state.pending_reflection = None  # reflection/bridge node waiting for "Continue"


def record_signal(signal: str):
    if signal:
        st.session_state.signals[signal] = st.session_state.signals.get(signal, 0) + 1


def dominant(axis: str, pole_a: str, pole_b: str) -> str:
    a = st.session_state.signals.get(f"{axis}:{pole_a}", 0)
    b = st.session_state.signals.get(f"{axis}:{pole_b}", 0)
    return pole_a if a >= b else pole_b


def interpolate(text: str, templates: dict = None) -> str:
    result = text
    for node_id, answer in st.session_state.answers.items():
        result = result.replace("{" + node_id + ".answer}", answer)

    dom1 = dominant("axis1", "internal", "external")
    dom2 = dominant("axis2", "contribution", "entitlement")
    dom3 = dominant("axis3", "altrocentric", "self")

    result = result.replace("{axis1.dominant}", dom1)
    result = result.replace("{axis2.dominant}", dom2)
    result = result.replace("{axis3.dominant}", dom3)

    if templates:
        result = result.replace("{axis1.summary}", templates.get("axis1", {}).get(dom1, ""))
        result = result.replace("{axis2.summary}", templates.get("axis2", {}).get(dom2, ""))
        result = result.replace("{axis3.summary}", templates.get("axis3", {}).get(dom3, ""))
        insight_key = f"{dom1}_{dom2}_{dom3}"
        result = result.replace(
            "{overall.insight}",
            templates.get("insights", {}).get(insight_key, "Carry forward whatever felt most true tonight.")
        )
    return result


def first_child(nodes: dict, parent_id: str) -> str | None:
    for node in nodes.values():
        if node.get("parentId") == parent_id:
            return node["id"]
    return None


def resolve_decision(node: dict) -> str:
    path = st.session_state.path
    prev_node_id = path[-2] if len(path) >= 2 else None
    prev_answer = st.session_state.answers.get(prev_node_id, "")

    for rule in node["options"]:
        if "from" in rule:
            from_answer = st.session_state.answers.get(rule["from"], "")
            if from_answer in rule["match"]:
                return rule["goto"]
        elif "match" in rule:
            if prev_answer in rule["match"]:
                return rule["goto"]

    return node["options"][0]["goto"]


def advance_to(node_id: str, nodes: dict):
    """Move to next node, auto-skipping non-interactive nodes."""
    st.session_state.current_node = node_id
    st.session_state.path.append(node_id)

    node = nodes[node_id]

    if node["type"] == "decision":
        next_id = resolve_decision(node)
        advance_to(next_id, nodes)

    elif node["type"] in ("start", "bridge"):
        record_signal(node.get("signal"))
        # Store for display then auto-advance via "Continue"
        st.session_state.pending_reflection = node_id

    elif node["type"] == "end":
        st.session_state.done = True


# ─── Progress Calculation ─────────────────────────────────────────────────────
def get_progress() -> float:
    """Rough progress 0.0–1.0 based on path length vs expected total."""
    EXPECTED_STEPS = 18
    return min(len(st.session_state.path) / EXPECTED_STEPS, 1.0)


def get_axis_label() -> str:
    node_id = st.session_state.current_node
    if node_id.startswith("A1") or node_id == "START":
        return "🟡 Axis 1 — Locus"
    elif node_id.startswith("A2") or node_id == "BRIDGE_1_2":
        return "🔵 Axis 2 — Orientation"
    elif node_id.startswith("A3") or node_id == "BRIDGE_2_3":
        return "🟢 Axis 3 — Radius"
    elif node_id == "SUMMARY":
        return "✨ Your Reflection"
    return ""


# ─── Renderers ────────────────────────────────────────────────────────────────
def render_start(node: dict, nodes: dict):
    st.markdown("## 🌙 Daily Reflection")
    st.markdown(f"<p style='color:#94a3b8; font-size:1.05rem; line-height:1.7'>{node['text']}</p>",
                unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Begin →"):
        target = node.get("target") or first_child(nodes, node["id"])
        advance_to(target, nodes)
        st.rerun()


def render_question(node: dict, nodes: dict):
    label = get_axis_label()
    if label:
        st.markdown(f"<span class='axis-pill'>{label}</span>", unsafe_allow_html=True)

    text = interpolate(node["text"])
    st.markdown(f"<p class='question-text'>{text}</p>", unsafe_allow_html=True)

    choice = st.radio("", node["options"], index=None, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Continue →", disabled=choice is None):
            st.session_state.answers[node["id"]] = choice
            record_signal(node.get("signal"))
            next_id = node.get("target") or first_child(nodes, node["id"])
            advance_to(next_id, nodes)
            st.rerun()


def render_reflection(node: dict, nodes: dict):
    label = get_axis_label()
    if label:
        st.markdown(f"<span class='axis-pill'>{label}</span>", unsafe_allow_html=True)

    text = interpolate(node["text"])
    record_signal(node.get("signal"))

    st.markdown(f"<div class='reflection-box'>{text}</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Continue →"):
            target = node.get("target") or first_child(nodes, node["id"])
            if target:
                advance_to(target, nodes)
            st.rerun()


def render_bridge(node: dict, nodes: dict):
    st.markdown(f"<p class='bridge-text'>· · · · ·<br>{node['text']}</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Continue →"):
            target = node.get("target") or first_child(nodes, node["id"])
            if target:
                advance_to(target, nodes)
            st.rerun()


def render_summary(node: dict, nodes: dict):
    templates = node.get("summary_templates", {})
    text = interpolate(node["text"], templates)

    st.markdown("## ✨ Your Reflection")
    st.markdown("<br>", unsafe_allow_html=True)

    # Render summary line by line with formatting
    lines = [l for l in text.split("\n") if l.strip()]
    summary_html = "<br>".join(lines)
    st.markdown(f"<div class='summary-box'>{summary_html}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Finish session"):
            target = node.get("target") or first_child(nodes, node["id"])
            advance_to(target, nodes)
            st.rerun()


def render_end(node: dict):
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='text-align:center; color:#64748b; font-size:1.1rem;'>{node['text']}</p>",
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start a new session"):
            for key in ["current_node", "answers", "signals", "path", "done", "pending_reflection"]:
                del st.session_state[key]
            st.rerun()


# ─── Main App ─────────────────────────────────────────────────────────────────
def main():
    nodes = load_tree()
    init_state()

    # Progress bar (hidden on start/end screens)
    node_id = st.session_state.current_node
    if node_id not in ("START", "END"):
        st.progress(get_progress())
        st.markdown("<br>", unsafe_allow_html=True)

    node = nodes[node_id]

    # Dispatch to renderer
    if node["type"] == "start":
        render_start(node, nodes)

    elif node["type"] == "question":
        render_question(node, nodes)

    elif node["type"] == "reflection":
        render_reflection(node, nodes)

    elif node["type"] == "bridge":
        render_bridge(node, nodes)

    elif node["type"] == "summary":
        render_summary(node, nodes)

    elif node["type"] == "end":
        render_end(node)

    elif node["type"] == "decision":
        # Decisions are skipped instantly — auto-resolve and rerun
        next_id = resolve_decision(node)
        advance_to(next_id, nodes)
        st.rerun()


if __name__ == "__main__":
    main()