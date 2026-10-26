import os
from flask import Flask, request, jsonify, render_template
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    model = request.json.get("model", "openrouter/free")
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    if "deepseek" in model.lower():
        provider = "deepseek"
        api_url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
    else:
        provider = "openrouter"
        api_url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "LocalChatbot"
        }

    try:
        response = requests.post(
            api_url,
            headers=headers,
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ]
            }
        )
        
        if response.status_code == 402:
            return jsonify({
                "error": f"API Provider Error (402): Insufficient balance on the {provider} API key. Please switch to a free OpenRouter model (e.g. Gemma 4) or top up your balance."
            }), 402
        elif response.status_code == 429:
            return jsonify({
                "error": f"API Provider Error (429): The model '{model}' is temporarily rate-limited. Please try again in a few seconds or switch to another model."
            }), 429
        elif response.status_code != 200:
            err_data = {}
            try:
                err_data = response.json()
            except:
                pass
            err_msg = err_data.get("error", {}).get("message", response.text)
            return jsonify({
                "error": f"API Provider Error ({response.status_code}): {err_msg}"
            }), response.status_code

        data = response.json()
        
        reply = data["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})

    except requests.exceptions.RequestException as req_err:
        print(f"=== DEBUG: Request Exception ===")
        print(str(req_err))
        print("================================")
        return jsonify({"error": f"Network Error: Unable to reach {provider} API. {str(req_err)}"}), 502

    except Exception as e:
        return jsonify({"error": f"Server Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)