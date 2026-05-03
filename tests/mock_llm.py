from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/v1/chat/completions", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("messages", [{}])[-1].get("content", "")

    return jsonify({
        "id": "mock-response",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": f"Mocked response for: {prompt}"
                }
            }
        ]
    })

app.run(host="0.0.0.0", port=5000)