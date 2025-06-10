from query import search_answer  # 假設 query.py 跟 app.py 同目錄
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError
import os

app = Flask(__name__)


# 環境變數讀取 Channel Token & Secret
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

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("❌ 簽章驗證失敗：請確認 CHANNEL_SECRET 是否與 LINE 後台一致")
        abort(400)

    return "OK", 200


# 📩 處理文字訊息事件
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    print("📩 使用者訊息：", user_message)

    try:
        answer = search_answer(user_message)
        if not answer:
            answer = "目前查無對應資料，請稍後再試，或聯絡工程師～"
    except Exception as e:
        print("❌ 查詢發生錯誤：", e)
        answer = "發生錯誤，請稍後再試～"

    reply = TextSendMessage(text=answer)
    line_bot_api.reply_message(event.reply_token, reply)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
