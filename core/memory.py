import json
import os

def load_memory(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

def save_memory(path, memory):
    with open(path, "w") as f:
        json.dump(memory, f, indent=2)

def add_to_memory(memory, role, content):
    memory.append({"role": role, "content": content})
    return memory
