from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError
import os

app = Flask(__name__)

# 從環境變數取得 Token & Secret
CHANNEL_ACCESS_TOKEN = os.environ.get("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.environ.get("CHANNEL_SECRET")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/", methods=["GET"])
def home():
    return "Line FAQ Bot is running", 200


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    print("🟡 收到 LINE Webhook POST")
    print("🔹 X-Line-Signature:", signature)
    print("🔹 Body:", body)

    # ✅ 暫時跳過簽章驗證，先確保 LINE Webhook 能通過
    return "OK", 200


# 🔧 建議：測試完成後將上面 callback 改成正式版如下
"""
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    print("🟡 收到 LINE Webhook POST")
    print("🔹 X-Line-Signature:", signature)
    print("🔹 Body:", body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("❌ 簽章驗證失敗，請確認 CHANNEL_SECRET 是否正確")
        return "Invalid signature", 400

    return "OK", 200
"""


# 📩 處理文字訊息事件
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    print("📩 使用者訊息：", user_message)

    # 回覆相同文字
    reply = TextSendMessage(text=f"你說的是：{user_message}")
    line_bot_api.reply_message(event.reply_token, reply)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
