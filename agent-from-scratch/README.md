This section follows along with this [blog](https://www.leoniemonigatti.com/blog/ai-agent-from-scratch-in-python.html) post.

## Setup

```bash
uv init
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Usage

To run the agent, you need to provide a message as a command-line argument.

### Basic Example

```bash
python simple_agent.py "What is the capital of France?"
```

### Specifying a Different Model

You can also specify a different Ollama model using the `--model` argument.

```bash
python simple_agent.py --model "llama3:latest" "Why is the sky blue?"
```

## Components

We will start with a simple LLM and build up to an agent.

**Component 1: LLM and Instructions - Simple Agent**

LLM and instructions: The LLM powering the agent’s reasoning and decision-making capabilities with explicit guidelines defining how the agent should behave.

```bash
python simple_agent.py "What is the capital of France?"
```

**Component 2: Conversational Memory**

Memory: Conversation history (short-term memory) the agent uses to understand the current interaction.

```bash
python conversational_memory.py 
```

Example conversation:
```bash
python conversational_memory.py
Agent is ready. Type 'exit' or 'quit' to end the conversation.
You: I have 4 apples. How many do you have?
Agent: Since I'm an AI, I don't have physical possessions like apples, so the number of apples you or anyone else has doesn't directly affect me. However, if you want to know how many apples you have, it remains at 4 as per your initial statement. If someone else had some apples too, then we would need more information about what they have in order to determine the total.
You: I ate 1 apple. How many are left?
Agent: If you started with 4 apples and you ate 1, then there would be:

4 (total apples initially) - 1 (apple eaten) = 3 apples remaining.

So, you have 3 apples left.
```

**Component 3: Tools**

Tools: External functions or APIs the agent can call.

To extend the agent’s capabilities, you can provide it with tools that can range from simple functions to using external APIs. For this tutorial, we will implement a simple `CalculatorTool` class, that can handle math problems.

The exact implemention of tool use is different across providers, but at the core always requires two key components:

- **Function implementation**: This is the actual function that executes the tool’s logic, such as performing a calculation, or making an API call.
- **Tool schema**: A structured description of the tool. The tool description is important because it tells the LLM what the tool does, when to use it, and what parameters it takes.

This tutorial follows the Anthropic documentation on tool use. If you’re using a different LLM API than this tutorial, I recommend to check out your LLM providers documentation on tool use. Note, that in this tutorial, we are just implementing a single tool. In production code, you’d typically use an abstract base class to ensure a consistent interface across tools.

### Usage

To see the agent use the calculator tool, you can run the `tool_use.py` script and ask it a math question.

```bash
python tool_use.py --model "gpt-oss:20b"
```

**Example Conversation:**

```
Agent is ready. Ask a question that might require calculation. Type 'exit' or 'quit' to end.
You: what is 12 * 4?
Agent: 12 * 4 is 48.
```

**Component 4: Agent Loop**

You might have already heard people say that “Agents are models using tools in a loop”. Without the loop, the agent can only handle single-turn without multi-turn interactions.

Barry Zhan, Anthropic, provides insightful pseudo code showing that agents are just LLMs making decisions in a loop, observing results, and deciding what to do next.

```python
env = Environment()
tools = Tools(env)
system_prompt = "Goals, constraints, and how to act"

while True:
  action = llm.run(system_prompt + env.state)
  env.state = tools.run(action)
```

For this simple agent implementation, that means, we have the following flow:

1. User sends message to agent
2. Agent decides it needs a tool and responds with a stop_reason of tool_use and a tool_useblock with the tool name and parameters. It’s saying “I’m pausing for you to execute this tool with these parameters”.
3. The user executes the tool and sends the tool result back to the agent in a follow-up message
4. The agent continues and gives the final response.

### Usage

To see the agent use the calculator tool in a loop, you can run the `agent_loop.py` script and ask it a math question that requires multiple steps.

```bash
python agent_loop.py --model qwen3:8b "what is 102.483 * 129.981?"
```

**Example output:**
```
DEBUG: Received tool call object: {'function': {'name': 'calculator', 'arguments': {'expression': '12 * 4'}}}
DEBUG: Using calculator tool to evaluate: 12 * 4
DEBUG: Received tool call object: {'function': {'name': 'calculator', 'arguments': {'expression': '48 + 10'}}}
DEBUG: Using calculator tool to evaluate: 48 + 10
Agent: 58
```
