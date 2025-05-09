from flask import Flask, request, jsonify
from openai import OpenAI
import os
import logging

# ロギング設定
logging.basicConfig(level=logging.INFO)

# Flask アプリの初期化
app = Flask(__name__)

# OpenAI クライアントの初期化（v1形式）
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# FAQデータ（プロンプトとして渡す）
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

Q: YUMO PARTS（湯本電機株式会社）とは？
A: YUMO PARTS（湯本電機株式会社）は、大阪とベトナムに工場を構える特注部品のパーツメーカーです。樹脂切削加工・金属切削加工・3Dプリントの専門事業部からなり、1940年に創業以来、豊富な加工実績から得た加工ノウハウを駆使して、多くの試作・特注部品製作に携わっています。大阪本社工場と東京officeを中心に営業しており、全国への出荷に対応しています。

Q: YUMO PARTS（湯本電機株式会社）のサービス内容は？
A: YUMO PARTS（湯本電機株式会社）では、切削加工と3Dプリントによる特注部品の試作と製作を行っています。1個～1000個までの単品から量産に対応します。また、試作や製作に必要な図面の製作にも対応が可能です。

Q: YUMO PARTS（湯本電機株式会社）の特長は？
A: YUMO PARTS（湯本電機株式会社）は、最短2時間以内の見積もりと最短納期1日のスピード対応かつ短納期の部品加工が得意です。切削加工は80年以上の実績があり、高精度かつ短納期での加工が可能となっています。さらに、3Dプリントによるスピード試作にも対応しており、これまでに200材質以上の豊富な加工実績があります。

Q: 切削加工の対応材質は？
A: YUMO PARTSでは、以下の材質の切削加工が可能です。この中にない材質の場合も、一度ご相談ください。

アルミニウム、ステンレス鋼、S-C材、SCM材、SS材、NAK材、銅・真鍮、チタン、インコネル、モリブデン、タングステン、マグネシウム、PEEK、PPS、PTFE、PI、PBI、PEI、PAI、PPSU、PVDF、POM、MCナイロン、ポリカーボネート、UHMW-PE、PA、PBT、PET、PP、PVC、ABS、PMMA、PE、ベークライト、エポキシガラス、CFRP、ユニレート

Q: 3Dプリントの対応材質は？
A: YUMO PARTSでは、以下の材質の3Dプリントが可能です。この中にない材質の場合も、一度ご相談ください。

アルミニウム、ステンレス鋼、インコネル、マルエージング鋼、PEKK、ULTEM、Onyx、PC-ABS、PA、PC、エポキシ樹脂、ABS、ASA、レッドワックス、PP

Q: 短納期での依頼はできますか？
A: はい、工場の空き状況と材料の入荷時期にもよりますが、最短で1日納期での出荷が可能です。平均納期は7.3日と、短納期での部品加工を得意としています。

Q: 図面が無くても依頼できますか？
A: はい、できます。スケッチなどの形状と寸法が分かるものを頂ければ、それを元にデータ作成・製図いたします。

Q: 加工・検査設備の見学はできますか？
A: はい、できます。お客様の安全と他のお客様の機密情報保護のため、加工機械の近くまではお見せすることはできませんので、予めご了承ください。

Q: 最大ロットは？
A: 最大ロットは1000個です。

Q: 最小ロットは？
A: 最小ロットは1個です。

Q: 既製品への追加工の依頼はできますか？
A: はい、できます。メーカー標準部品（ボックスやフラットバーなど）への追加工も承っております。

Q: 送付したデータは安全に管理されますか？
A: はい。お見積り・加工依頼のために頂いたお客様のデータは、専任のエンジニアによる厳正な取扱いのもと、管理・保護させて頂きます。

Q: 試作品・部品の製作にかかる費用はいくらですか？
A: 費用は形状と材質、納期などの条件によって変動します。数量によっては単価も変動（一般的に多いほど安い）するため、一度見積りフォームからお問い合わせください。

Q: 部品加工の知識がありませんが、依頼しても良いですか？
A: もちろんです。一緒に条件をクリアしていきながらのものづくりを歓迎します。

Q: 学生ですが、利用できますか？
A: はい、利用できます。YUMO PARTSは大学・研究機関の方との取引実績が多数あります。口座開設などのお手続きにも柔軟に対応します。また、YUMO PARTSは、「研究機関における公的研究費の管理・監査のガイドライン」を遵守します。誓約書が必要な場合はお申し付けください。

Q: 樹脂材質の加工はできますか？
A: はい、できます。YUMO PARTSでは、切削加工と3Dプリントでの樹脂材質の加工が可能です。

切削加工
PEEK、PPS、PTFE、PI、PBI、PEI、PAI、PPSU、PVDF、POM、MCナイロン、ポリカーボネート、UHMW-PE、PA、PBT、PET、PP、PVC、ABS、PMMA、PE、ベークライト、エポキシガラス、CFRP、ユニレート

3Dプリント
PEKK、ULTEM、Onyx、PC-ABS、PA、PC、エポキシ樹脂、ABS、ASA、レッドワックス、PP

Q: 金属材質の加工はできますか？
A: はい、できます。YUMO PARTSでは、切削加工と3Dプリントでの金属材質の加工が可能です。

切削加工
アルミニウム、ステンレス鋼、S-C材、SCM材、SS材、NAK材、銅・真鍮、チタン、インコネル、モリブデン、タングステン、マグネシウム

3Dプリント
アルミニウム、ステンレス鋼、インコネル、マルエージング鋼

Q: 納期はどれくらいですか？
A: 最短で1営業日、通常は1週間以内で対応可能です。

Q: 学生や研究者でも依頼できますか？
A: はい、学生や研究者の方からのご依頼も歓迎しております。
"""

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(force=True)
    logging.info("Received data from Zoho: %s", data)

    handler = data.get("handler")
    logging.info("handler: %s", handler)

    if handler == "message":
        user_msg = data.get("message", {}).get("text", "")
        if not user_msg:
            return jsonify({"replies": [{"type": "text", "text": "メッセージが見つかりませんでした。"}]}), 400

        try:
            # OpenAI API 呼び出し
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "あなたはYUMO PARTSのカスタマーサポート担当者です。以下のFAQに基づいて、できる限り丁寧に回答してください:\n" + faq_context},
                    {"role": "user", "content": user_msg}
                ],
                temperature=0.3
            )
            reply_text = response.choices[0].message.content.strip()
        except Exception as e:
            logging.info(f"OpenAI APIエラー: {e}")
            reply_text = "回答の生成中にエラーが発生しました。もう一度お試しください。"

        return jsonify({
            "replies": [
                {"type": "text", "text": reply_text}
            ]
        }), 200

    # その他のイベントは無視
    return jsonify({
        "replies": [{"type": "text", "text": "ご質問内容を入力してください。"}]
    }), 200

# Render用ポート指定
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
