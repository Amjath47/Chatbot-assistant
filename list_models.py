import requests

api_key = "sk-380a85f89aa546839c92e1b8c0a8e09f"  # your key

response = requests.get(
    "https://api.deepseek.com/v1/models",
    headers={"Authorization": f"Bearer {api_key}"}
)

print(response.status_code)
print(response.json())
