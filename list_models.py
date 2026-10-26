import requests

api_key = "sk-c7ce2334505a43b5b763cff1ad538f63"

response = requests.get(
    "https://api.deepseek.com/v1/models",
    headers={"Authorization": f"Bearer {api_key}"}
)

print(response.status_code)
print(response.json())
