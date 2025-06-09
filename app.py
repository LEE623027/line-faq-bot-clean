from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import config  # 讀剛剛修好的 config.py

app = Flask(__name__)

line_bot_api = LineBotApi(config.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.CHANNEL_SECRET)


@app.route("/", methods=["GET"])
def index():
    return "Line FAQ Bot is running"


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    # ----------  DEBUG ----------
    print("🟡 LINE Webhook POST 進來了")
    print("🔹 Signature:", signature)
    print("🔹 Body:", body)
    print("🔹 CHANNEL_SECRET:", config.CHANNEL_SECRET[:10] if config.CHANNEL_SECRET else "❌ None")
    print("🔹 CHANNEL_ACCESS_TOKEN:", config.CHANNEL_ACCESS_TOKEN[:10] if config.CHANNEL_ACCESS_TOKEN else "❌ None")
    # -----------------------------

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("❌ InvalidSignatureError：簽章驗證失敗")
        return "Invalid signature", 400
    except Exception as e:
        print("❌ 其他 webhook 錯誤：", e)
        return f"Webhook Error: {e}", 500

    return "OK", 200


@handler.add(MessageEvent, message=TextMessage)
def handle_text(event):
    user_msg = event.message.text
    print("📩 使用者訊息：", user_msg)

    try:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"✅ 測試成功！你剛才說：「{user_msg}」")
        )
    except Exception as e:
        print("❌ 回覆訊息錯誤：", e)


if __name__ == "__main__":
    # Render 會在環境變數 PORT 指定埠口
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
