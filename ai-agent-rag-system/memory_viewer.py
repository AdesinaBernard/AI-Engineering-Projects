from long_term_memory import (
    get_facts
)


facts = get_facts()

print("\nStored Facts:\n")

for fact in facts:
    print("-", fact)