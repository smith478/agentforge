import os
import argparse
from ollama import Client

class Agent:
    """A simple AI agent that can answer questions"""

    def __init__(self, model='granite4:tiny-h'):
        self.client = Client()
        self.model = model
        self.system_message = "You are a helpful assistant that breaks down problems into steps and solves them systematically."

    def chat(self, message):
        """Process a user message and return a response"""

        response = self.client.chat(
            model=self.model,
            messages=[
                {'role': 'system', 'content': self.system_message},
                {"role": "user", "content": message}
            ],
        )

        return response

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple AI agent using Ollama.")
    parser.add_argument("--model", type=str, default="granite4:tiny-h", help="The Ollama model to use.")
    parser.add_argument("message", type=str, help="The message to send to the agent.")
    args = parser.parse_args()

    agent = Agent(model=args.model)

    response = agent.chat(args.message)
    print(response['message']['content'])
