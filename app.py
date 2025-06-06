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

    print("🟡 [Webhook Debug] 收到 LINE POST")
    print("🔹 Headers:", dict(request.headers))
    print("🔹 X-Line-Signature:", signature)
    print("🔹 Body:", body)
    print("🔹 環境變數 CHANNEL_SECRET:", config.CHANNEL_SECRET[:10])  # 只印前 10 碼
    print("🔹 環境變數 CHANNEL_ACCESS_TOKEN:", config.CHANNEL_ACCESS_TOKEN[:10])

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("❌ [錯誤] 簽章驗證失敗：請確認 CHANNEL_SECRET 是否正確")
        return "Invalid signature", 400
    except Exception as e:
        print("❌ [錯誤] webhook 發生例外：", e)
        return "Error", 400

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
