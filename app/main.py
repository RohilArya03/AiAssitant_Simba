from app.llm.client import generate, ModelServingError

def limit_conversation_history(messages, max_turns=10):
    """
    Limit the conversation history to the last `max_length` messages. 
    Always has to be an even number of messages, since we need to have a user message and an assistant
    message to have a coherent conversation. If we have an odd number of messages, we will drop the oldest user message.
    """
    max_length = max_turns * 2  # Each turn consists of a user message and an assistant message
    if len(messages) > max_length:
        return messages[-max_length:]
    return messages


def main():
    messages = []

    while True:
        user_input = input("You: ")
        
        #Exit condition for now... should be inactivity for x amount of time later
        if user_input.lower() in ["quit", "exit"]:
            break

        # Appending users input to conversation history
        messages.append({"role": "user", "content": user_input})

        # Get the Simbas reply from the LLM
        try:
            assistant_reply = generate(messages)
        except ModelServingError as e:
            print(f"Error: {e}")
            break

        print(f"Simba: {assistant_reply}")

        # Appending the assistant's reply to conversation history
        messages.append({"role": "assistant", "content": assistant_reply})
        # Limit the conversation history to the last 10 messages
        messages = limit_conversation_history(messages)

if __name__ == "__main__":
    main()