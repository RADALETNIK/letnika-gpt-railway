from openai import OpenAI
from flask import Flask, request, Response
import os
import json
from dotenv import load_dotenv

# ——— Загрузка переменных среды
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY не задан в .env!")

client = OpenAI(api_key=OPENAI_API_KEY)

PORT = int(os.environ.get("PORT", 8080))
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "🔥 Railway API работает с openai>=1.0.0!", 200

@app.route("/api", methods=["POST"])
def handle():
    try:
        data = request.get_json(force=True)
        text = data.get("text", "")
        style = data.get("style", "дружелюбный")

        allowed_styles = ["дружелюбный", "деловой", "дерзкий"]
        if style not in allowed_styles:
            style = "дружелюбный"

        messages = [
            {"role": "system", "content": f"Ты — ассистент. Стиль общения: {style}"},
            {"role": "user", "content": text}
        ]

        chat_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.8
        )

        reply = chat_response.choices[0].message.content.strip()
        return Response(
            json.dumps({"messages": [{"text": reply}]}),
            content_type="application/json; charset=utf-8"
        )
    
    except Exception as e:
        return Response(
            json.dumps({"error": str(e)}),
            content_type="application/json; charset=utf-8"
        ), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
