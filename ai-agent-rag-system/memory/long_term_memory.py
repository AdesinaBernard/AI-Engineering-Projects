import json
import os

MEMORY_FILE = "data/long_term_memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def store_fact(fact):
    memory = load_memory()
    memory.append(fact)
    save_memory(memory)


def get_facts():
    return load_memory()