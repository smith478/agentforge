import os
import argparse
from ollama import Client

class Agent:
    """A simple AI agent that can answer questions"""

    def __init__(self, model='granite4:tiny-h'):
        self.client = Client()
        self.model = model
        # Initialize with system message
        self.messages = [{'role': 'system', 'content': "You are a helpful assistant that breaks down problems into steps and solves them systematically."}]

    def chat(self, message):
        """Process a user message and return a response"""

        # Store user input in memory
        self.messages.append({"role": "user", "content": message})

        response = self.client.chat(
            model=self.model,
            messages=self.messages
        )

        assistant_response = response['message']['content']
        # Store assistant's response in memory
        self.messages.append({"role": "assistant", "content": assistant_response})

        return assistant_response

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple AI agent using Ollama with conversational memory.")
    parser.add_argument("--model", type=str, default="granite4:tiny-h", help="The Ollama model to use.")
    args = parser.parse_args()

    agent = Agent(model=args.model)
    print("Agent is ready. Type 'exit' or 'quit' to end the conversation.")

    while True:
        try:
            user_message = input("You: ")
            if user_message.lower() in ["exit", "quit"]:
                break
            assistant_message = agent.chat(user_message)
            print(f"Agent: {assistant_message}")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
