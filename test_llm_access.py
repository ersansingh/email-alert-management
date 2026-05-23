import requests
import json

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "Bearer ${OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
  },
  data=json.dumps({
    "model": "openrouter/free",
    "messages": [
      {
        "role": "user",
        "content": "What is the meaning of life?"
      }
    ],
    "max_tokens": 100
  })
)
print(response.status_code)
print(response.json())
