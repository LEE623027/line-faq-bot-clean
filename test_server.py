from flask import Flask, request

app = Flask(__name__)

@app.route("/callback", methods=["POST"])
def callback():
    print("[DEBUG] 收到 Webhook 請求")
    print("[DEBUG] Headers:", dict(request.headers))
    print("[DEBUG] Body:", request.get_data(as_text=True))
    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000)
