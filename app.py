from flask import Flask, request, jsonify
import openai
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # RenderはこのPORTを設定します
    app.run(host="0.0.0.0", port=port)

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

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
    data = request.get_json(force=True)
    print("Received data from Zoho:", data)

    # メッセージが存在するかを確認
    handler = data.get("handler")
    if handler == "message":
        user_msg = data.get("message", {}).get("text", "")
        if not user_msg:
            return jsonify({"replies": [{"type": "text", "text": "メッセージが見つかりませんでした。"}]}), 400

        # ChatGPT に送信して返信を生成（ダミー返信）
        reply_text = f"ご質問ありがとうございます。『{user_msg}』に関するご案内を準備中です。"

        return jsonify({
            "replies": [
                {"type": "text", "text": reply_text}
            ]
        }), 200

    # その他の handler（例: trigger）は無視
    return jsonify({"replies": [{"type": "text", "text": "メッセージ以外のイベントは処理していません。"}]}), 200

