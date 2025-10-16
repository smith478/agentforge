import os
import json
import argparse
from ollama import Client

class CalculatorTool():
    """A tool for performing mathematical calculations"""

    def get_schema(self):
        return {
            "name": "calculator",
            "description": "Use this tool to evaluate mathematical expressions. It can handle addition, subtraction, multiplication, and division. Always use this tool for any math question to ensure accuracy.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate (e.g., '2+2', '10*5')"
                    }
                },
                "required": ["expression"]
            }
        }

    def execute(self, expression):
        """
        Evaluate mathematical expressions.
        WARNING: This tutorial uses eval() for simplicity but it is not recommended for production use.

        Args:
            expression (str): The mathematical expression to evaluate
        Returns:
            float: The result of the evaluation
        """
        try:
            print(f"DEBUG: Using calculator tool to evaluate: {expression}")
            result = eval(expression)
            return {"result": result}
        except:
            return {"error": "Invalid mathematical expression"}

class Agent:
    """A simple AI agent that can use tools to answer questions in a multi-turn conversation"""

    def __init__(self, model='granite4:tiny-h', tools=None):
        self.client = Client()
        self.model = model
        self.messages = [{'role': 'system', 'content': "You are a helpful assistant. You MUST use the calculator tool for any mathematical calculations to ensure accuracy. For all other questions, answer directly."}]
        self.tools = tools or []
        self.tool_map = {tool.get_schema()["name"]: tool for tool in self.tools}

    def _get_tool_schemas(self):
        return [tool.get_schema() for tool in self.tools]

    def chat(self, message):
        self.messages.append({"role": "user", "content": message})

        response = self.client.chat(
            model=self.model,
            messages=self.messages,
            tools=self._get_tool_schemas(),
        )

        self.messages.append(response['message'])

        while response['message'].get("tool_calls"):
            tool_calls = response['message']["tool_calls"]
            for tool_call in tool_calls:
                print(f"DEBUG: Received tool call object: {tool_call}")
                tool_name = tool_call['function']['name']
                tool_args = tool_call['function']['arguments']
                
                if tool_name in self.tool_map:
                    tool = self.tool_map[tool_name]
                    result = tool.execute(**tool_args)
                    
                    self.messages.append({
                        'role': 'tool',
                        'content': json.dumps(result)
                    })
                else:
                    print(f"Unknown tool: {tool_name}")

            response = self.client.chat(
                model=self.model,
                messages=self.messages,
                tools=self._get_tool_schemas(),
            )
            self.messages.append(response['message'])

        return response['message']['content']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple AI agent using Ollama with tool-use capabilities.")
    parser.add_argument("--model", type=str, default="granite4:tiny-h", help="The Ollama model to use.")
    args = parser.parse_args()

    calculator_tool = CalculatorTool()
    agent = Agent(model=args.model, tools=[calculator_tool])

    print("Agent is ready. Ask a question that might require calculation. Type 'exit' or 'quit' to end.")

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
