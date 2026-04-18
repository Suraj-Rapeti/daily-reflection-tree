#!/usr/bin/env python3
"""
The Daily Reflection Tree - Deterministic Reflection Agent
No LLM at runtime. Walks a structured tree, accumulates state, produces reflection.
"""

import json
import os
import sys
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field
from enum import Enum


@dataclass
class SessionState:
    """Tracks the employee's journey through the tree"""
    current_node_id: str = "START"
    answers: Dict[str, Any] = field(default_factory=dict)  # node_id -> selected answer
    signals: Dict[str, int] = field(default_factory=lambda: {
        "axis1:internal": 0,
        "axis1:external": 0,
        "axis1:mixed": 0,
        "axis2:contribution": 0,
        "axis2:entitlement": 0,
        "axis2:mixed": 0,
        "axis3:self_centric": 0,
        "axis3:team_centric": 0,
        "axis3:altrocentric": 0,
        "axis3:transcendent": 0,
    })
    conversation_transcript: List[str] = field(default_factory=list)

    def record_answer(self, node_id: str, answer_value: str, answer_label: str):
        """Record when user answers a question"""
        self.answers[node_id] = {"value": answer_value, "label": answer_label}
        self.conversation_transcript.append(f"Q: {node_id}\nA: {answer_label}\n")

    def add_signal(self, signal: str):
        """Tally a signal for axis scoring"""
        if signal and signal in self.signals:
            self.signals[signal] += 1


class ReflectionAgent:
    def __init__(self, tree_path: str):
        self.tree_path = tree_path
        self.tree_data = self._load_tree()
        self.nodes = {node["id"]: node for node in self.tree_data["nodes"]}
        self.state = SessionState()

    def _load_tree(self) -> Dict:
        """Load the tree structure from JSON"""
        with open(self.tree_path, 'r') as f:
            return json.load(f)

    def get_node(self, node_id: str) -> Optional[Dict]:
        """Retrieve a node by ID"""
        return self.nodes.get(node_id)

    def interpolate_text(self, text: str) -> str:
        """Replace {placeholders} with actual answers from conversation"""
        if not text:
            return text

        # Replace simple answer references: {A1_OPEN.label}, {A1_OPEN.value}
        for node_id, answer in self.state.answers.items():
            text = text.replace(f"{{{node_id}.label}}", answer.get("label", ""))
            text = text.replace(f"{{{node_id}.value}}", answer.get("value", ""))

        # Replace axis dominance: {axis1.dominant_narrative}, etc.
        axis1_dominant = self._get_dominant_axis("axis1")
        axis2_dominant = self._get_dominant_axis("axis2")
        axis3_dominant = self._get_dominant_axis("axis3")

        narratives = {
            "axis1:internal": "internal agency—seeing your hand in outcomes",
            "axis1:external": "external attribution—circumstances shaping events",
            "axis1:mixed": "mixed agency—sometimes you, sometimes fate",
            "axis2:contribution": "contributing without keeping score",
            "axis2:entitlement": "waiting for recognition and returns",
            "axis2:mixed": "contribution with expectation",
            "axis3:self_centric": "your own achievement and success",
            "axis3:team_centric": "collective problem-solving with your team",
            "axis3:altrocentric": "helping others and some transcendence",
        }

        text = text.replace(f"{{axis1.dominant_narrative}}", narratives.get(axis1_dominant, ""))
        text = text.replace(f"{{axis2.dominant_narrative}}", narratives.get(axis2_dominant, ""))
        text = text.replace(f"{{axis3.dominant_narrative}}", narratives.get(axis3_dominant, ""))

        return text

    def _get_dominant_axis(self, axis: str) -> str:
        """Determine which pole of an axis the person leans toward"""
        if axis == "axis1":
            signals = ["axis1:internal", "axis1:external", "axis1:mixed"]
        elif axis == "axis2":
            signals = ["axis2:contribution", "axis2:entitlement", "axis2:mixed"]
        else:  # axis3
            signals = ["axis3:self_centric", "axis3:team_centric", "axis3:altrocentric"]

        max_signal = max(signals, key=lambda s: self.state.signals.get(s, 0))
        return max_signal

    def evaluate_decision(self, node: Dict) -> str:
        """
        For a decision node, evaluate conditions and return the target node_id
        Handles routing logic like: 'answer=Productive|Mixed:A1_Q_AGENCY_HIGH'
        """
        if "routing" not in node or not node["routing"]:
            return node.get("target")

        for route in node["routing"]:
            condition = route.get("condition", "")
            target = route.get("target")

            # Parse simple condition: answer=value or answer=value1|value2
            if condition.startswith("answer="):
                answer_part = condition.split("answer=")[1]
                values = [v.strip() for v in answer_part.split("|")]

                # Get the parent question node
                parent_question = self._find_parent_question(node)
                if parent_question and parent_question["id"] in self.state.answers:
                    current_answer = self.state.answers[parent_question["id"]]["value"]
                    if current_answer in values:
                        return target

            # Parse axis-based condition: axis1.dominant=internal
            elif "dominant=" in condition:
                axis = condition.split(".")[0]
                target_value = condition.split("=")[1]
                if self._get_dominant_axis(axis) == f"{axis}:{target_value}":
                    return target

        # If no conditions matched, return explicit target
        return node.get("target")

    def _find_parent_question(self, decision_node: Dict) -> Optional[Dict]:
        """Find the question node that this decision routes from"""
        parent_id = decision_node.get("parentId")
        while parent_id:
            parent = self.get_node(parent_id)
            if parent and parent["type"] == "question":
                return parent
            parent_id = parent.get("parentId") if parent else None
        return None

    def get_next_node(self, current_node: Dict) -> str:
        """Determine the next node to visit"""
        node_type = current_node.get("type")

        if node_type == "decision":
            # Decision nodes handle routing internally
            return self.evaluate_decision(current_node)

        # All other nodes: follow target or children
        target = current_node.get("target")
        if target:
            return target

        # If no explicit target, find children in the tree
        node_id = current_node["id"]
        children = [n["id"] for n in self.tree_data["nodes"] if n.get("parentId") == node_id]
        return children[0] if children else "END"

    def display_node(self, node: Dict):
        """Render a node to the console"""
        print("\n" + "=" * 70)
        print(f"[{node['type'].upper()}]")
        print("=" * 70)

        if node.get("text"):
            text = self.interpolate_text(node["text"])
            print(text)

        if node.get("options"):
            print("\nChoose one:")
            for i, option in enumerate(node["options"], 1):
                print(f"  {i}) {option['label']}")

    def handle_question_node(self, node: Dict) -> str:
        """Prompt user to answer a question, return selected option value"""
        self.display_node(node)

        while True:
            try:
                choice = input("\nYour choice (1-{}): ".format(len(node["options"]))).strip()
                choice_idx = int(choice) - 1

                if 0 <= choice_idx < len(node["options"]):
                    selected = node["options"][choice_idx]
                    self.state.record_answer(node["id"], selected["value"], selected["label"])
                    return selected["value"]
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")

    def handle_reflection_node(self, node: Dict):
        """Display reflection, wait for user to continue"""
        self.display_node(node)

        # Record the signal for this reflection
        if node.get("signal"):
            self.state.add_signal(node["signal"])
            self.state.conversation_transcript.append(f"[Signal: {node['signal']}]\n")

        input("\nPress Enter to continue...")

    def handle_start_node(self, node: Dict):
        """Display start node, auto-advance"""
        self.display_node(node)
        input("\nPress Enter to begin...")

    def handle_bridge_node(self, node: Dict):
        """Display bridge node, auto-advance"""
        self.display_node(node)
        input("\nPress Enter to continue...")

    def handle_summary_node(self, node: Dict):
        """Display summary with interpolation"""
        self.display_node(node)

    def handle_end_node(self, node: Dict):
        """Display end message"""
        print("\n" + "=" * 70)
        print("[END]")
        print("=" * 70)
        if node.get("text"):
            print(self.interpolate_text(node["text"]))

    def run(self):
        """Main agent loop: walk the tree"""
        print("\n" + "╔" + "═" * 68 + "╗")
        print("║" + " " * 68 + "║")
        print("║" + "     The Daily Reflection Tree     ".center(68) + "║")
        print("║" + "      An End-of-Day Reflection      ".center(68) + "║")
        print("║" + " " * 68 + "║")
        print("╚" + "═" * 68 + "╝\n")

        while self.state.current_node_id != "END":
            node = self.get_node(self.state.current_node_id)

            if not node:
                print(f"ERROR: Node {self.state.current_node_id} not found.")
                break

            node_type = node.get("type")

            if node_type == "start":
                self.handle_start_node(node)
            elif node_type == "question":
                self.handle_question_node(node)
            elif node_type == "reflection":
                self.handle_reflection_node(node)
            elif node_type == "decision":
                # Decision nodes don't display; just route
                pass
            elif node_type == "bridge":
                self.handle_bridge_node(node)
            elif node_type == "summary":
                self.handle_summary_node(node)
            elif node_type == "end":
                self.handle_end_node(node)
                break

            # Move to next node
            self.state.current_node_id = self.get_next_node(node)

        self._show_final_summary()

    def _show_final_summary(self):
        """Show final reflection summary and statistics"""
        print("\n" + "=" * 70)
        print("SESSION SUMMARY")
        print("=" * 70)

        axis1 = self._get_dominant_axis("axis1")
        axis2 = self._get_dominant_axis("axis2")
        axis3 = self._get_dominant_axis("axis3")

        print(f"\nAxis 1 (Locus): {axis1}")
        print(f"  Internal: {self.state.signals['axis1:internal']}")
        print(f"  External: {self.state.signals['axis1:external']}")
        print(f"  Mixed: {self.state.signals['axis1:mixed']}")

        print(f"\nAxis 2 (Orientation): {axis2}")
        print(f"  Contribution: {self.state.signals['axis2:contribution']}")
        print(f"  Entitlement: {self.state.signals['axis2:entitlement']}")
        print(f"  Mixed: {self.state.signals['axis2:mixed']}")

        print(f"\nAxis 3 (Radius): {axis3}")
        print(f"  Self-Centric: {self.state.signals['axis3:self_centric']}")
        print(f"  Team-Centric: {self.state.signals['axis3:team_centric']}")
        print(f"  Altrocentric: {self.state.signals['axis3:altrocentric']}")

        print("\n" + "=" * 70)

    def export_transcript(self, filename: str):
        """Export the conversation transcript to a file"""
        with open(filename, 'w') as f:
            f.write("REFLECTION SESSION TRANSCRIPT\n")
            f.write("=" * 70 + "\n\n")
            f.writelines(self.state.conversation_transcript)
            f.write("\n\nFINAL AXIS SCORES:\n")
            f.write(f"Axis 1 (Locus): {self._get_dominant_axis('axis1')}\n")
            f.write(f"Axis 2 (Orientation): {self._get_dominant_axis('axis2')}\n")
            f.write(f"Axis 3 (Radius): {self._get_dominant_axis('axis3')}\n")


def main():
    """Entry point"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tree_path = os.path.join(script_dir, "..", "reflection-tree.json")

    if not os.path.exists(tree_path):
        print(f"ERROR: Tree file not found at {tree_path}")
        sys.exit(1)

    agent = ReflectionAgent(tree_path)
    agent.run()

    # Optionally save transcript
    transcript_path = os.path.join(script_dir, "..", "last_session_transcript.txt")
    agent.export_transcript(transcript_path)
    print(f"\nTranscript saved to: {transcript_path}")


if __name__ == "__main__":
    main()
