from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.environ.get("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.environ.get("CHANNEL_SECRET")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/", methods=['GET'])
def index():
    return "Line FAQ Bot is running"

@app.route("/callback", methods=['POST'])
def callback():
    try:
        signature = request.headers.get("X-Line-Signature", "")
        body = request.get_data(as_text=True)

        print("🟡 收到 LINE Webhook POST")
        print("🔹 X-Line-Signature:", signature)
        print("🔹 Body:", body)
        print("🔹 CHANNEL_SECRET:", CHANNEL_SECRET[:10] if CHANNEL_SECRET else "❌ None")
        print("🔹 CHANNEL_ACCESS_TOKEN:", CHANNEL_ACCESS_TOKEN[:10] if CHANNEL_ACCESS_TOKEN else "❌ None")

        handler.handle(body, signature)
    except InvalidSignatureError:
        print("❌ 簽章驗證失敗")
        return "Invalid signature", 400
    except Exception as e:
        print("❌ webhook 執行錯誤:", str(e))
        return f"Webhook Error: {e}", 500

    return "OK", 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        msg = event.message.text
        print("📩 使用者訊息：", msg)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"✅ 測試成功：你剛剛說的是「{msg}」")
        )
    except Exception as e:
        print("❌ 回覆訊息錯誤:", str(e))

# ✅ 關鍵補上這段，讓 Render 正確偵測服務埠口
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
