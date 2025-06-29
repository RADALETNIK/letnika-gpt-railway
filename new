import os
import json
import requests
from flask import Flask, request, Response
from dotenv import load_dotenv

# ——— Загрузка .env переменных ———
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY не задан в .env!")

PORT = int(os.environ.get("PORT", 8080))
AI_URL = "https://api.openai.com/v1/chat/completions"

app = Flask(__name__)

# ——— Проверка сервера ———
@app.route("/", methods=["GET"])
def home():
    return "🔥 Бот работает на Railway! Версия: /api + GPT", 200

# ——— Основной маршрут обработки запросов ———
@app.route("/api", methods=["POST"])
def handle():
    try:
        data = request.get_json(force=True)

        # Получаем переменные
        text = data.get("text", "")
        style = data.get("style", "дружелюбный")

        # Фоллбэк по стилю общения (если что-то не то — ставим default)
        allowed_styles = ["дружелюбный", "деловой", "дерзкий"]
        if style not in allowed_styles:
            style = "дружелюбный"

        # Формируем сообщения для GPT
        messages = [
            {"role": "system", "content": f"Ты — ассистент. Стиль общения: {style}"},
            {"role": "user", "content": text}
        ]

        # Запрос к OpenAI
        response = requests.post(
            AI_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": messages,
                "max_tokens": 500,
                "temperature": 0.8
            }
        )

        # Проверка статуса и парсинг
        if response.status_code != 200:
            raise RuntimeError(f"OpenAI error {response.status_code}: {response.text}")

        result = response.json()
        reply = result.get("choices", [{}])[0].get("message", {}).get("content", "🤖 Ошибка: пустой ответ от GPT.")

        # Ответ без экранирования кириллицы
        return Response(
            json.dumps({"messages": [{"text": reply}]}, ensure_ascii=False),
            content_type="application/json; charset=utf-8"
        )

    except Exception as e:
        # Ошибка в обработке
        return Response(
            json.dumps({"error": str(e)}, ensure_ascii=False),
            content_type="application/json; charset=utf-8"
        ), 500

# ——— Запуск сервера (на Railway не обязателен, но пусть будет) ———
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
