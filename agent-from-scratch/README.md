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

**Component 3: Tools**

Tools: External functions or APIs the agent can call.