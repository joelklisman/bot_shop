import os
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from telegram import Bot

# --- Load env ---
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# --- Flask App ---
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# --- Telegram Bot instance ---
bot = Bot(token=BOT_TOKEN)

@app.route("/nowpayments/webhook", methods=["POST"])
def nowpayments_webhook():
    data = request.get_json(force=True)
    logging.info(f"📩 Webhook received: {data}")

    payment_status = data.get("payment_status")
    order_id = data.get("order_id")
    payment_id = data.get("payment_id")

    user_id = None
    if order_id and "-" in order_id:
        user_id = order_id.split("-")[0]

    if payment_status == "finished" and user_id:
        try:
            bot.send_message(
                chat_id=user_id,
                text=f"✅ Payment *#{payment_id}* confirmed!\nThank you — your order is complete 🎉",
                parse_mode="Markdown"
            )
            logging.info(f"✅ Payment confirmed message sent to user {user_id}")
        except Exception as e:
            logging.error(f"Failed to send Telegram message: {e}")

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    logging.info("🌐 Starting Flask webhook server on port 5000...")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
