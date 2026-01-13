print("MAIN FILE EXECUTED")

from core.brain import think
from core.memory import load_memory, save_memory, add_to_memory
from core.security import is_safe
from config import MEMORY_FILE

def main():
    memory = load_memory(MEMORY_FILE)

    print("AI Assistant started.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("AI: Goodbye.")
            break

        if not is_safe(user_input):
            print("AI: That request is blocked for safety.")
            continue

        memory = add_to_memory(memory, "user", user_input)
        reply = think(memory)
        memory = add_to_memory(memory, "assistant", reply)

        save_memory(MEMORY_FILE, memory)

        print("AI:", reply)

if __name__ == "__main__":
    main()
