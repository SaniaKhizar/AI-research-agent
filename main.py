from agent import ask_agent

if __name__ == "__main__":
    conversation = []
    print("Agent ready. Type 'quit' to exit.\n")

    while True:
        question = input("You: ")
        if question.lower() == "quit":
            break
        answer = ask_agent(question, conversation)
        print(f"\nAgent: {answer}\n")