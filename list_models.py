import requests
import os

API_KEY = os.getenv("DEEPSEEK_API_KEY")

response = requests.get(
    "https://api.deepseek.com/v1/models",
    headers={"Authorization": f"Bearer {api_key}"}
)

print(response.status_code)
print(response.json())
