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
    print("📩 LINE webhook 收到：", body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("❌ 簽章錯誤")
        return "Invalid signature", 400
    except Exception as e:
        print("❌ 發生錯誤：", str(e))
        return "Error", 500

    return "OK", 200  # ✅ 一定要有

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="✅ 成功回應！這是測試回覆")
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
