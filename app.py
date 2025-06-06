from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import config

app = Flask(__name__)

line_bot_api = LineBotApi(config.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.CHANNEL_SECRET)

@app.route("/", methods=["GET"])
def home():
    return "✅ LINE Bot is running!"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    print("📩 收到 LINE 請求內容：", body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("❌ 簽章錯誤，請檢查 CHANNEL_SECRET")
        return "Invalid signature", 400
    except Exception as e:
        print("❌ webhook 錯誤：", str(e))
        return "Internal Error", 500

    return "OK", 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text
    print(f"💬 使用者說：{user_msg}")

    # 目前先簡單回應 echo，可改接 query.py later
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"你剛剛說的是：{user_msg}")
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
