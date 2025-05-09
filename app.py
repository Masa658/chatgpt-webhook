from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

# YUMO PARTSのFAQ情報をsystemメッセージに含める
faq_context = """
YUMO PARTSのよくある質問：

Q: 支払い方法は何ですか？
A: 初回のお取引は基本的に前金での銀行振込をお願いしております。継続的なお取引となる場合は月締め翌月払いとなります。

Q: 1個だけの注文は可能ですか？
A: はい、1個からのご注文も承っております。

Q: 相談や見積もりに費用はかかりますか？
A: いいえ、無料でご相談・お見積もりを承っております。

Q: 図面がなくても相談できますか？
A: はい、手書きのスケッチやイラストからでも対応可能です。

Q: 納期はどれくらいですか？
A: 最短で1営業日、通常は1週間以内で対応可能です。

Q: 学生や研究者でも依頼できますか？
A: はい、学生や研究者の方からのご依頼も歓迎しております。
"""

@app.route('/webhook', methods=['POST'])
def webhook():
    user_msg = request.json.get("message")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"あなたはYUMO PARTSのカスタマーサポートAIです。以下のFAQに基づいて回答してください。\n{faq_context}"},
            {"role": "user", "content": user_msg}
        ]
    )

    return jsonify({"reply": response.choices[0].message['content']})

if __name__ == "__main__":
    app.run(port=5000)
