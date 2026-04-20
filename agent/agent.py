#!/usr/bin/env python3
"""
Daily Reflection Tree — CLI Agent
Loads reflection-tree.json and walks the employee through a deterministic
reflection session. No LLM calls at runtime. Fully deterministic.

Usage:
    python agent.py
    python agent.py --tree ../tree/reflection-tree.json
    python agent.py --transcript  (saves session to /transcripts/)
"""

import json
import sys
import time
import argparse
from datetime import datetime
from pathlib import Path


# ─── Colours ──────────────────────────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    CYAN    = "\033[96m"
    YELLOW  = "\033[93m"
    GREEN   = "\033[92m"
    MAGENTA = "\033[95m"
    BLUE    = "\033[94m"
    GREY    = "\033[90m"
    WHITE   = "\033[97m"


def clear_line():
    print()


def print_banner():
    print(f"\n{C.CYAN}{'─' * 60}{C.RESET}")
    print(f"{C.BOLD}{C.WHITE}  🌙  Daily Reflection Tree{C.RESET}")
    print(f"{C.GREY}  An end-of-day reflection session{C.RESET}")
    print(f"{C.CYAN}{'─' * 60}{C.RESET}\n")


def slow_print(text, delay=0.018, color=""):
    """Print text character by character for a more reflective pace."""
    for char in text:
        print(f"{color}{char}{C.RESET}", end="", flush=True)
        time.sleep(delay)
    print()


# ─── Tree Loader ──────────────────────────────────────────────────────────────
class ReflectionTree:
    def __init__(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.meta = data["meta"]
        self.nodes = {n["id"]: n for n in data["nodes"]}

    def get(self, node_id: str) -> dict:
        node = self.nodes.get(node_id)
        if not node:
            raise ValueError(f"Node '{node_id}' not found in tree.")
        return node


# ─── State Manager ────────────────────────────────────────────────────────────
class SessionState:
    def __init__(self):
        self.answers: dict[str, str] = {}       # node_id → answer text
        self.signals: dict[str, int] = {}       # signal_key → tally
        self.path: list[str] = []               # node IDs visited
        self.transcript: list[dict] = []        # full transcript for export

    def record_answer(self, node_id: str, answer: str):
        self.answers[node_id] = answer

    def record_signal(self, signal: str):
        if signal:
            self.signals[signal] = self.signals.get(signal, 0) + 1

    def dominant(self, axis: str, pole_a: str, pole_b: str) -> str:
        a = self.signals.get(f"{axis}:{pole_a}", 0)
        b = self.signals.get(f"{axis}:{pole_b}", 0)
        if a >= b:
            return pole_a
        return pole_b

    def interpolate(self, text: str, templates: dict = None) -> str:
        """Replace {node_id.answer} placeholders and {axis.dominant} tokens."""
        result = text

        # Replace {node_id.answer}
        for node_id, answer in self.answers.items():
            result = result.replace("{" + node_id + ".answer}", answer)

        # Replace {axisN.dominant} tokens
        axis_map = {
            "axis1.dominant": self.dominant("axis1", "internal", "external"),
            "axis2.dominant": self.dominant("axis2", "contribution", "entitlement"),
            "axis3.dominant": self.dominant("axis3", "altrocentric", "self"),
        }
        for token, value in axis_map.items():
            result = result.replace("{" + token + "}", value)

        # Replace {axisN.summary} and {overall.insight} from templates
        if templates:
            dom1 = axis_map["axis1.dominant"]
            dom2 = axis_map["axis2.dominant"]
            dom3 = axis_map["axis3.dominant"]

            result = result.replace(
                "{axis1.summary}",
                templates.get("axis1", {}).get(dom1, "")
            )
            result = result.replace(
                "{axis2.summary}",
                templates.get("axis2", {}).get(dom2, "")
            )
            result = result.replace(
                "{axis3.summary}",
                templates.get("axis3", {}).get(dom3, "")
            )
            insight_key = f"{dom1}_{dom2}_{dom3}"
            result = result.replace(
                "{overall.insight}",
                templates.get("insights", {}).get(insight_key, "Carry forward whatever felt most true tonight.")
            )

        return result

    def add_transcript(self, role: str, content: str):
        self.transcript.append({"role": role, "content": content})


# ─── Node Handlers ────────────────────────────────────────────────────────────
class Agent:
    def __init__(self, tree: ReflectionTree, save_transcript: bool = False):
        self.tree = tree
        self.state = SessionState()
        self.save_transcript = save_transcript

    def run(self):
        print_banner()
        self._walk("START")
        if self.save_transcript:
            self._export_transcript()

    def _walk(self, node_id: str):
        """Main recursive walk. Follows the tree from node_id."""
        node = self.tree.get(node_id)
        self.state.path.append(node_id)

        handler = getattr(self, f"_handle_{node['type']}", None)
        if not handler:
            raise NotImplementedError(f"No handler for node type '{node['type']}'")

        next_id = handler(node)

        if next_id:
            self._walk(next_id)

    # ── start ──
    def _handle_start(self, node: dict) -> str:
        slow_print(f"\n  {node['text']}\n", color=C.DIM)
        self.state.add_transcript("system", node["text"])
        time.sleep(0.5)
        input(f"  {C.GREY}Press Enter when you're ready...{C.RESET}")
        clear_line()
        return node.get("target") or self._first_child(node["id"])

    # ── question ──
    def _handle_question(self, node: dict) -> str:
        text = self.state.interpolate(node["text"])
        print(f"\n  {C.BOLD}{C.WHITE}{text}{C.RESET}\n")
        self.state.add_transcript("question", text)

        options = node["options"]
        for i, opt in enumerate(options, 1):
            print(f"  {C.CYAN}{i}.{C.RESET} {opt}")

        print()
        choice = self._prompt_choice(len(options))
        answer = options[choice - 1]

        self.state.record_answer(node["id"], answer)
        self.state.record_signal(node.get("signal"))
        self.state.add_transcript("answer", answer)

        print(f"\n  {C.GREY}✓ Got it.{C.RESET}")
        time.sleep(0.4)
        clear_line()

        return node.get("target") or self._first_child(node["id"])

    # ── decision ──
    def _handle_decision(self, node: dict) -> str:
        """Invisible routing node. Reads prior answers and signals to route."""
        options = node["options"]

        # Check if rules reference a specific 'from' node (multi-parent decisions)
        # or just look at the previous question's answer
        prev_answer_node_id = self.state.path[-2] if len(self.state.path) >= 2 else None
        prev_answer = self.state.answers.get(prev_answer_node_id, "")

        for rule in options:
            # Rules with explicit 'from' field
            if "from" in rule:
                from_answer = self.state.answers.get(rule["from"], "")
                if from_answer in rule["match"]:
                    return rule["goto"]
            # Rules based on the immediately prior node's answer
            elif "match" in rule:
                if prev_answer in rule["match"]:
                    return rule["goto"]

        # Fallback: return first option's goto
        return options[0]["goto"]

    # ── reflection ──
    def _handle_reflection(self, node: dict) -> str:
        text = self.state.interpolate(node["text"])
        print(f"\n  {C.YELLOW}{'─' * 50}{C.RESET}")
        slow_print(f"\n  {text}\n", color=C.YELLOW, delay=0.022)
        print(f"  {C.YELLOW}{'─' * 50}{C.RESET}\n")
        self.state.record_signal(node.get("signal"))
        self.state.add_transcript("reflection", text)
        input(f"  {C.GREY}Take a moment. Press Enter to continue...{C.RESET}")
        clear_line()
        return node.get("target") or self._first_child(node["id"])

    # ── bridge ──
    def _handle_bridge(self, node: dict) -> str:
        print(f"\n  {C.MAGENTA}· · ·{C.RESET}")
        slow_print(f"\n  {node['text']}\n", color=C.MAGENTA, delay=0.020)
        self.state.add_transcript("bridge", node["text"])
        time.sleep(0.8)
        return node.get("target") or self._first_child(node["id"])

    # ── summary ──
    def _handle_summary(self, node: dict) -> str:
        templates = node.get("summary_templates", {})
        text = self.state.interpolate(node["text"], templates)

        print(f"\n  {C.GREEN}{'═' * 50}{C.RESET}")
        print(f"  {C.BOLD}{C.GREEN}Your Reflection{C.RESET}")
        print(f"  {C.GREEN}{'═' * 50}{C.RESET}\n")

        for line in text.split("\n"):
            slow_print(f"  {line}", color=C.GREEN, delay=0.015)
            if line.strip():
                time.sleep(0.1)

        print(f"\n  {C.GREEN}{'═' * 50}{C.RESET}\n")
        self.state.add_transcript("summary", text)
        input(f"  {C.GREY}Press Enter to close your session...{C.RESET}")
        clear_line()
        return node.get("target") or self._first_child(node["id"])

    # ── end ──
    def _handle_end(self, node: dict) -> str:
        slow_print(f"\n  {node['text']}\n", color=C.DIM, delay=0.03)
        self.state.add_transcript("system", node["text"])
        print(f"  {C.CYAN}{'─' * 60}{C.RESET}\n")
        return None  # terminates the walk

    # ── helpers ──
    def _first_child(self, parent_id: str) -> str | None:
        """Find the first node whose parentId matches parent_id."""
        for node in self.tree.nodes.values():
            if node.get("parentId") == parent_id:
                return node["id"]
        return None

    def _prompt_choice(self, max_choice: int) -> int:
        while True:
            raw = input(f"  {C.BOLD}Your choice (1–{max_choice}): {C.RESET}").strip()
            if raw.isdigit():
                val = int(raw)
                if 1 <= val <= max_choice:
                    return val
            print(f"  {C.GREY}Please enter a number between 1 and {max_choice}.{C.RESET}")

    def _export_transcript(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_dir = Path(__file__).parent.parent / "transcripts"
        out_dir.mkdir(exist_ok=True)
        out_path = out_dir / f"session_{ts}.md"

        lines = [f"# Reflection Session — {datetime.now().strftime('%d %B %Y, %H:%M')}\n"]
        lines.append(f"**Path taken:** {' → '.join(self.state.path)}\n")
        lines.append(f"**Signals:** {self.state.signals}\n\n---\n")

        for entry in self.state.transcript:
            role = entry["role"].upper()
            if role == "QUESTION":
                lines.append(f"\n**Q:** {entry['content']}\n")
            elif role == "ANSWER":
                lines.append(f"**A:** {entry['content']}\n")
            elif role == "REFLECTION":
                lines.append(f"\n> *{entry['content']}*\n")
            elif role == "SUMMARY":
                lines.append(f"\n### Summary\n\n{entry['content']}\n")
            else:
                lines.append(f"\n_{entry['content']}_\n")

        with open(out_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        print(f"\n  {C.GREY}Session saved to: {out_path}{C.RESET}\n")


# ─── Entry Point ──────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Daily Reflection Tree — CLI Agent")
    parser.add_argument("--tree", default=None, help="Path to reflection-tree.json")
    parser.add_argument("--transcript", action="store_true", help="Save session transcript to /transcripts/")
    args = parser.parse_args()

    # Resolve tree path
    if args.tree:
        tree_path = args.tree
    else:
        here = Path(__file__).parent
        tree_path = here.parent / "tree" / "reflection-tree.json"

    if not Path(tree_path).exists():
        print(f"Error: tree file not found at {tree_path}")
        sys.exit(1)

    tree = ReflectionTree(str(tree_path))
    agent = Agent(tree, save_transcript=args.transcript)

    try:
        agent.run()
    except KeyboardInterrupt:
        print(f"\n\n  {C.GREY}Session ended early. See you tomorrow.{C.RESET}\n")


if __name__ == "__main__":
    main()
