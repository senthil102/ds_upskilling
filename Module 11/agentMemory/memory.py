import json
import os


class AgentMemory:

    def __init__(self):
        # Short-term memory
        self.conversation = []

        # Long-term memory
        self.file = "memory.json"

        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                self.memory = json.load(f)
        else:
            self.memory = {
                "episodes": [],
                "facts": {},
                "procedures": {}
            }

    # -------------------------
    # Short-term memory
    # -------------------------
    def add_conversation(self, role, message):
        self.conversation.append({
            "role": role,
            "message": message
        })

    def get_conversation(self):
        return self.conversation

    # -------------------------
    # Long-term memory
    # -------------------------
    def save_memory(self):
        with open(self.file, "w") as f:
            json.dump(self.memory, f, indent=2)

    # -------------------------
    # Episodic memory
    # What happened?
    # -------------------------
    def add_episode(self, task, result):
        self.memory["episodes"].append({
            "task": task,
            "result": result
        })

        self.save_memory()

    # -------------------------
    # Semantic memory
    # What is true?
    # -------------------------
    def add_fact(self, name, value):
        self.memory["facts"][name] = value
        self.save_memory()

    def get_fact(self, name):
        return self.memory["facts"].get(name)

    # -------------------------
    # Procedural memory
    # How to do something?
    # -------------------------
    def add_procedure(self, name, steps):
        self.memory["procedures"][name] = steps
        self.save_memory()

    def get_procedure(self, name):
        return self.memory["procedures"].get(name)