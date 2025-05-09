from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/webhook', methods=['POST'])
def webhook():
    user_msg = request.json.get("message")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたはYUMO PARTSのカスタマーサポートAIです。以下のFAQの内容だけに基づいて回答してください。"},
            {"role": "user", "content": user_msg}
        ]
    )

    return jsonify({"reply": response.choices[0].message['cont
