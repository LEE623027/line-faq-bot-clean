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

    print("🟡 收到 LINE Webhook：")
    print("Headers:", dict(request.headers))
    print("Body:", body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("❌ 簽章錯誤：CHANNEL_SECRET 錯")
        return "Invalid signature", 400
    except Exception as e:
        print("❌ 發生例外錯誤：", e)
        return f"Error: {str(e)}", 400

    return "OK", 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("📩 使用者訊息：", event.message.text)
    try:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="✅ 測試回覆成功")
        )
    except Exception as e:
        print("❌ 回覆時錯誤：", e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
