from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        print("Received data from Zoho:", data)  # デバッグ用

        # ユーザーの質問を取得（Zohoの形式に合わせる）
        user_msg = data.get("visitor", {}).get("question", "")

        # 念のため空チェック
        if not user_msg:
            return jsonify({"replies": [{"type": "text", "text": "質問が見つかりませんでした。"}]}), 400

        # OpenAIに問い合わせ
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"あなたはYUMO PARTSのカスタマーサポートAIです。以下のFAQに基づいて回答してください。\n{faq_context}"},
                {"role": "user", "content": user_msg}
            ]
        )

        reply_text = response.choices[0].message.content.strip()

        # Zoho SalesIQの形式で返す
        return jsonify({
            "replies": [
                {"type": "text", "text": reply_text}
            ]
        })
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
