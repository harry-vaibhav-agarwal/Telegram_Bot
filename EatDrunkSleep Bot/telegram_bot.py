import requests,json

from config import TELEGRAM_SEND_MESSAGE_URL
from config import TELEGRAM_SEND_VIDEO_URL

class TelegramBot:

    def __init__(self):

        self.chat_id = None
        self.text = None
        self.first_name = None
        self.last_name = None
        self.username= None
        self.incoming_message_text = None
        self.animation = None
        self.sticker=None
        self.photo=None
        self.command=None
        self.commandlist=["/start","/add_item","/delete_item","/get_items","/done","/video"]
        self.commandlistdescription=['MAKE YOUR TODO LIST','ADD ITEMS TO YOUR TODOLIST','DELETE ITEMS','GET ITEMS','FINISH','REQUEST A VIDEO']

    def parse_webhook_data(self, data):

        #data=json.loads(data)
        message = data['message']

        self.chat_id = message['chat']['id']


        if 'text' in message :
            if message['text'].startswith('/'):
                self.command=message['text'].lower()
            else:
                self.incoming_message_text = message['text'].lower()

        if 'first_name' in message['from']:
            self.first_name = message['from']['first_name']

        if 'last_name' in message['from']:
            self.last_name = message['from']['last_name']

        if 'username' in message['from']:
             self.username=message['from']['username']

        if 'animation' in message:
            self.animation=message['animation']

        if 'sticker' in message:
            self.sticker=message['sticker']

        if 'photo' in message:
            self.photo=message['photo']



    def action(self):

        success = None

        if self.incoming_message_text is not None:


            if self.incoming_message_text in ('hey','hi','hello'):
                self.outgoing_message_text = 'HI {} WELCOME TO TELEGRAM UTILITY BOT '.format(self.first_name.upper())
                success = self.send_message()


            else :
                user=None
                if self.username is not None:
                    user=self.username
                else:
                    user=self.first_name

                self.outgoing_message_text ='@{} Echoing back {} '.format(user,self.incoming_message_text.upper())
                success=self.send_message()

            return success

        elif self.animation is not None:
            self.outgoing_message_text='Nice animation filename is {} ,mime_type is  {} and duration of animation is {}'.format(self.animation['file_name'],self.animation['mime_type'],self.animation['duration'])
            success=self.send_message()

            return success

        elif self.sticker is not None:
            emoji=None
            if 'set_name' in self.sticker:
                emoji=self.sticker['set_name']
            else :
                emoji=' '

            self.outgoing_message_text = 'Nice emoji ! emoji  is {} '.format(str(emoji))
            success = self.send_message()

            return success

        elif self.photo is not None:
            self.outgoing_message_text = 'Nice photo !! '
            success = self.send_message()

            return success

        elif self.command is not None:
            success=self.handle_command()
            return success
        else :
            return success

    def send_message(self,reply_markup=None):
        res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(self.chat_id, self.outgoing_message_text,''))
        print(res)
        return True if res.status_code == 200 else False


    def send_video(self):
        res=requests.get(TELEGRAM_SEND_VIDEO_URL.format(self.chat_id,'http://techslides.com/demos/sample-videos/small.mp4'))
        print(res)
        return True if res.status_code == 200 else False



    def handle_command(self):
        if self.command in self.commandlist:
            if self.command == '/video':
                self.outgoing_message_text='Here is a video for you'
                self.send_message()
                self.send_video()
            else :
                pass

        else:
            self.outgoing_message_text = 'Invalid command!'
            self.send_message()


    @staticmethod
    def init_webhook(url):
        requests.get(url)    # setting up the webhook any request came to localhost
