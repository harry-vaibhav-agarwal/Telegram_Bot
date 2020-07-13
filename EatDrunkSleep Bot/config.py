TOKEN=''
BASE_TELEGRAM_URL='https://api.telegram.org/bot{}'.format(TOKEN)

NGROK=''
NGROK_URL='https://{}.ngrok.io'.format(NGROK)
LOCAL_WEBHOOK_ENDPOINT='{}/webhook'.format(NGROK_URL)

TELEGRAM_INIT_WEBHOOK_URL='{}/setWebhook?url={}'.format(BASE_TELEGRAM_URL,NGROK_URL)
TELEGRAM_SEND_MESSAGE_URL= BASE_TELEGRAM_URL + '/sendMessage?chat_id={}&text={}&reply_markup={}'
TELEGRAM_SEND_VIDEO_URL = BASE_TELEGRAM_URL + '/sendVideo?chat_id={}&video={}'