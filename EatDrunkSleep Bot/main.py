from flask import Flask, request, jsonify
import json
from telegram_bot import TelegramBot
from config import TELEGRAM_INIT_WEBHOOK_URL
from dbhelper import DBHelper


app = Flask(__name__)
TelegramBot.init_webhook(TELEGRAM_INIT_WEBHOOK_URL)
db = DBHelper()
db.setup()

@app.route('/', methods=['POST'])
def index():
    req = request.get_json()
    print(json.dumps(req))
    bot = TelegramBot(db)
    bot.parse_webhook_data(req)
    success = bot.action()
    return jsonify(success=success) # TODO: Success should reflect the success of the reply  it is important else it will continue to send up message

if __name__ == '__main__':
    app.run(port=7000)
