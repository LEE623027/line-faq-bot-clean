from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import config

app = Flask(__name__)

line_bot_api = LineBotApi(config.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.CHANNEL_SECRET)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    # 🔍 DEBUG 訊息：觀察 LINE 發送的資料與你載入的變數是否正確
    print("🟡 收到 LINE Webhook POST")
    print("🔹 X-Line-Signature:", signature)
    print("🔹 Body:", body)
    print("🔹 config.CHANNEL_SECRET:", config.CHANNEL_SECRET[:10] if config.CHANNEL_SECRET else "❌ None")
    print("🔹 config.CHANNEL_ACCESS_TOKEN:", config.CHANNEL_ACCESS_TOKEN[:10] if config.CHANNEL_ACCESS_TOKEN else "❌ None")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("❌ InvalidSignatureError：簽章錯誤，請確認 CHANNEL_SECRET 是否正確")
        return "Invalid signature", 400
    except Exception as e:
        print("❌ webhook 發生例外錯誤：", str(e))
        return "Error", 400

    return "OK", 200


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("📩 使用者訊息：", event.message.text)
    try:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="✅ 測試成功！這是從 webhook 回來的回覆。")
        )
    except Exception as e:
        print("❌ 回覆訊息時錯誤：", str(e))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
