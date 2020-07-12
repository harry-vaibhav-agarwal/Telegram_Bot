import requests

from config import TELEGRAM_SEND_MESSAGE_URL
from config import TELEGRAM_SEND_VIDEO_URL


class TelegramBot:

    def __init__(self):

        self.chat_id = None
        self.text = None
        self.first_name = None
        self.last_name = None

    def parse_webhook_data(self, data):

        message = data['message']

        self.chat_id = message['chat']['id']
        self.incoming_message_text = message['text'].lower()
        self.first_name = message['from']['first_name']
        self.last_name = message['from']['last_name']

    def action(self):

        success = None



        if self.incoming_message_text == 'rad':
            self.outgoing_message_text = '🤙'
            success = self.send_message()

        elif self.incoming_message_text == 'video' :
            self.outgoing_message_text = ' Here is a video for you '
            success =self.send_message()
            success =self.send_video()

        else :
            self.outgoing_message_text =self.incoming_message_text.upper() +'   {} {}'.format(self.first_name,self.last_name)
            success=self.send_message()


        return success

    def send_message(self):
        res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(self.chat_id, self.outgoing_message_text))

        return True if res.status_code == 200 else False


    def send_video(self):
        res=requests.get(TELEGRAM_SEND_VIDEO_URL.format(self.chat_id,'http://techslides.com/demos/sample-videos/small.mp4'))
        return True if res.status_code == 200 else False

    @staticmethod
    def init_webhook(url):
        requests.get(url)    #setting up the webhook any request came to localhost