import requests,json

from config import TELEGRAM_SEND_MESSAGE_URL
from config import TELEGRAM_SEND_VIDEO_URL
from dbhelper import DBHelper





class TelegramBot:

    def __init__(self):

        db = DBHelper()
        db.setup()
        self.db=db
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
        self.commandlist=[('/start','MAKE YOUR TODO LIST'),("/add_item",'ADD ITEMS TO YOUR TODOLIST.SEND THE ITEM_NAME ALONG WITH COMMAND'),("/delete_item","DELETE ITEM"),("/get_items","GET ITEMS"),("/done","FINISH"),("/video","REQUEST A VIDEO")]
        self.commandtype=['/start','/add_item','/delete_item','/get_items','/done','/video']

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
                self.outgoing_message_text = 'HI {} \n WELCOME TO TELEGRAM UTILITY BOT\n.YOU CAN SEND ME NORMAL MESSAGES OR COMMANDS LISTED BELOW :\n'.format(self.first_name.upper())
                success = self.send_message(command_list=self.commandlist)


            else :
                user=None
                if self.username is not None:
                    user=self.username
                else:
                    user=self.first_name

                items=self.db.get_items(owner=self.chat_id)

                if self.incoming_message_text in items:
                    self.command='/delete_item'+" "+self.incoming_message_text
                    success=self.handle_command()
                else:
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

    def send_message(self,reply_markup=None,command_list=None):

        if reply_markup is None:
            reply_markup = ''

        str=""
        if command_list is not None :
            for command,desc in command_list:
                str=str+"\n" + command +  " : " + desc

        self.outgoing_message_text=self.outgoing_message_text+str

        res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(self.chat_id, self.outgoing_message_text,reply_markup))
        print(res)
        return True if res.status_code == 200 else False


    def send_video(self):
        res=requests.get(TELEGRAM_SEND_VIDEO_URL.format(self.chat_id,'http://techslides.com/demos/sample-videos/small.mp4'))
        print(res)
        return True if res.status_code == 200 else False

    def build_keyboard(self,items):
        keyboard = [[item] for item in items]
        reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
        return json.dumps(reply_markup)

    def handle_command(self):
        if self.command in self.commandtype or self.command.startswith('/add_item') or self.command.startswith('/delete_item'):
            if self.command == '/video':
                self.outgoing_message_text='Here is a video for you'
                self.send_message()
                return self.send_video()
            else :

                items = self.db.get_items(owner=self.chat_id)
                if self.command == '/start':
                    self.outgoing_message_text="Let's get started with our todolist\n"
                    return self.send_message(command_list=self.commandlist)

                elif self.command == '/done':

                    self.outgoing_message_text = 'HERE IS YOUR LIST :\n'
                    items=self.db.get_items(owner=self.chat_id)
                    for item in items:
                        self.outgoing_message_text =self.outgoing_message_text + item.upper()+"\n"

                    return self.send_message()


                elif self.command == '/delete_item':
                    keyboard = self.build_keyboard(items)
                    self.outgoing_message_text='SELECT AN ITEM TO DELETE\n'
                    return self.send_message(reply_markup=keyboard)

                elif self.command.startswith('/delete_item'):
                    text = self.command.partition("/delete_item ")[2].lower()
                    self.db.delete_item(item_text=text,owner=self.chat_id)
                    items=self.db.get_items(owner=self.chat_id)
                    self.outgoing_message_text = "\n".join(items)
                    return self.send_message()

                elif self.command.startswith('/add_item'):
                    text=self.command.partition("/add_item ")[2].lower()
                    try:
                        self.db.add_item(item_text=text, owner=self.chat_id)
                    except:
                        pass

                    items = self.db.get_items(owner=self.chat_id)  ##
                    self.outgoing_message_text = "\n".join(items)
                    return self.send_message()

                else:
                    self.outgoing_message_text = "\n".join(items)
                    return self.send_message()



        else:
            self.outgoing_message_text = 'Invalid command!'
            self.send_message()





    @staticmethod
    def init_webhook(url):
        requests.get(url) # setting up the webhook any request came to localhost

