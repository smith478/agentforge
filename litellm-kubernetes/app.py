
import os
from flask import Flask, request, jsonify
from litellm import completion

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data.get('messages')
    temperature = data.get('temperature', 0.7)

    # LiteLLM setup
    model_name = os.environ.get("MODEL_NAME", "ollama/qwen3:8b")
    api_base = os.environ.get("API_BASE", "http://ollama.default.svc.cluster.local:11434")
    api_key = os.environ.get("API_KEY")

    try:
        response = completion(
            model=model_name,
            messages=messages,
            api_base=api_base,
            api_key=api_key,
            temperature=temperature
        )
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
