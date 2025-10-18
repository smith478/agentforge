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
        except Exception as e:
            return {"error": f"Invalid mathematical expression: {str(e)}"}

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
        """Process a user message and return a response"""
        self.messages.append({"role": "user", "content": message})

        response = self.client.chat(
            model=self.model,
            messages=self.messages,
            tools=self._get_tool_schemas(),
        )

        self.messages.append(response['message'])

        # Process tool calls in a loop until we get a final response
        while response['message'].get("tool_calls"):
            tool_calls = response['message']["tool_calls"]
            
            for tool_call in tool_calls:
                print(f"DEBUG: Received tool call object: {tool_call}")
                tool_name = tool_call['function']['name']
                tool_args = tool_call['function']['arguments']
                
                # Handle empty tool names or mismatched arguments
                if not tool_name or tool_name not in self.tool_map:
                    print(f"DEBUG: Tool name '{tool_name}' not found, attempting to infer...")
                    
                    # If we only have one tool and arguments are provided, use it
                    if len(self.tool_map) == 1:
                        tool_name = list(self.tool_map.keys())[0]
                        tool = self.tool_map[tool_name]
                        schema = tool.get_schema()
                        
                        # Try to map the arguments to the expected format
                        expected_props = schema['input_schema']['properties']
                        
                        # Check if arguments match expected properties
                        if 'expression' in expected_props and 'expression' in tool_args:
                            print(f"DEBUG: Using tool '{tool_name}' with expression argument")
                        elif 'expression' in expected_props and ('num1' in tool_args or 'num2' in tool_args):
                            # Convert num1 and num2 to expression format
                            if 'num1' in tool_args and 'num2' in tool_args:
                                tool_args = {'expression': f"{tool_args['num1']} * {tool_args['num2']}"}
                                print(f"DEBUG: Converted num1/num2 to expression: {tool_args['expression']}")
                        else:
                            print(f"DEBUG: Could not map arguments to tool schema")
                            continue
                    else:
                        # Try to match based on argument keys
                        for name, tool in self.tool_map.items():
                            schema = tool.get_schema()
                            required_props = schema['input_schema'].get('properties', {}).keys()
                            if any(key in tool_args for key in required_props):
                                tool_name = name
                                print(f"DEBUG: Inferred tool name as '{tool_name}' from arguments")
                                break
                        
                        if tool_name not in self.tool_map:
                            print(f"Unknown tool: {tool_name}")
                            continue
                
                if tool_name in self.tool_map:
                    tool = self.tool_map[tool_name]
                    result = tool.execute(**tool_args)
                    
                    self.messages.append({
                        'role': 'tool',
                        'content': json.dumps(result)
                    })
                else:
                    print(f"Unknown tool: {tool_name}")

            # Get next response from the model
            response = self.client.chat(
                model=self.model,
                messages=self.messages,
                tools=self._get_tool_schemas(),
            )
            self.messages.append(response['message'])

        return response['message']['content']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple AI agent using Ollama with tool-use capabilities.")
    parser.add_argument("--model", type=str, default="qwen3:8b", help="The Ollama model to use.")
    parser.add_argument("question", type=str, help="The question to ask the agent.")
    args = parser.parse_args()

    calculator_tool = CalculatorTool()
    agent = Agent(model=args.model, tools=[calculator_tool])

    print(f"\nQuestion: {args.question}")
    assistant_message = agent.chat(args.question)
    print(f"\nAgent: {assistant_message}")