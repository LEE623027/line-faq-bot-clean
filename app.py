from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from query import query_knowledge
import config  # 放你自己的 Channel secret 與 access token

app = Flask(__name__)
line_bot_api = LineBotApi(config.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.CHANNEL_SECRET)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")  # ✅ 安全讀取
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("⚠️ 無效的 LINE 簽章，請檢查 CHANNEL_SECRET 是否正確")
        return "Invalid signature", 400
    except Exception as e:
        print("⚠️ Webhook 處理例外：", str(e))
        return "Error", 500

    return "OK", 200


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    query = event.message.text
    results = query_knowledge(query)
    if results:
        reply = results[0]
    else:
        reply = "❓ 查無相關知識，請確認問題格式或補充知識庫。"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
