import paho.mqtt.client as mqtt
import time
import os
from cli import Cli
from scrapping import search
import sys

User_Name = 'client1'


###########################################
class ChatClient:
    pub_topics = []
    sub_topics = []

    def __init__(self, _id, address, port):
        self._id = _id
        self.pub_topics.append(_id)
        self.client = mqtt.Client()
        self.address = address
        self.port = port
        self.chat = ''
        self.FLAG = True
        self.message = None

    def AddSubTopic(self, topic):
        """
        add a topic to subscribe
        :param topic: str the topic name

        """
        self.sub_topics.append(topic)

    def AddPubTopic(self, topic):
        """
        add a topic to publish
        :param topic: str :a

        """
        self.pub_topics.append(topic)

    ##########Defining all call back functions###################

    def on_connect(self, client, userdata, flags, rc):  # called when the broker responds to our connection request

        print("Connected - rc:", rc)
        print(self.pub_topics)
        print(self.sub_topics)

    def on_message(self, client, pub_top,
                   message):  # Called when a message has been received on a topic that the client has subscirbed to.
        # print(pub_top)
        message_contain = str(message.payload.decode("utf-8"))
        if str(message.topic) != self._id:
            self.message = message
            print(str(message.topic)+":", message_contain)
            if message_contain.capitalize() == "Stop":
                self.FLAG = False
            else:

                if message.topic.lower().find("bot") != -1:

                    self.chat = input("Ask:")
                else:
                    self.chat = input()
                    print(f"you:{self.chat}")
                client.publish(self._id, self.chat)
        else:
            print(f"you:{message_contain}")

    def on_subscribe(self, client, userdata, mid,
                     granted_qos):  ##Called when the broker responds to a subscribe request.
        print("Subscribed:", str(mid), str(granted_qos))

    def on_unsubscirbe(self, client, userdata, mid):  # Called when broker responds to an unsubscribe request.
        print("Unsubscribed:", str(mid))

    def on_disconnect(self, client, userdata, rc):  # called when the client disconnects from the broker
        if rc != 0:
            print("Unexpected Disconnection")

    def configure_chat(self):
        """
        configure the chat callbacks

        """

        self.client.on_subscribe = self.on_subscribe
        self.client.on_unsubscribe = self.on_unsubscirbe
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def Chat(self, chat_promt=""):
        """run the chat loop"""
        self.configure_chat()
        self.client.connect(self.address, self.port, keepalive=120)


        time.sleep(1)

        self.client.loop_start()
        for topic in self.sub_topics:
            self.client.subscribe(topic)

        #time.sleep(1)
        if self.message is not None:
            message_contain = str(self.message.payload.decode("utf-8"))
            print(str(self.message.topic), message_contain)
        self.chat = input(chat_promt)
        print(f"you:{self.chat}")

        self.client.publish(self._id, self.chat)
        while True:

            if self.FLAG == False or self.chat.capitalize() == "Stop":
                break

        self.client.disconnect()
        self.client.loop_stop()


chat_cli = Cli("chat")


@chat_cli.command(cmd_args={"other": {"type": str, "help": "the other person name"}})
def invite(other):
    print(User_Name)
    global chat_client
    chat_client.AddSubTopic("/chat/" + other)
    print(other.lower())
    if other.lower().find("bot") != -1:
        chat_client.Chat("Ask:")

    else:

        chat_client.Chat()


@chat_cli.command(cmd_args={"user_name": {"type": str, "help": "your user name"}})
def login(user_name):
    global User_Name
    global chat_client
    User_Name = user_name
    chat_client = ChatClient("/chat/" + User_Name, "broker.hivemq.com", 1883)


Ask_cli = Cli("Ask")


@Ask_cli.command(cmd_args={"user_name": {"type": str, "help": "your user name"}})
def ask(user_name):
    while True:
        question = input("Ask me:")
        if question.lower() in ["stop", "bye", "goodbye"]:
            break
        else:
            answer = search(question)
            if answer == '':
                print(f"sorry {user_name} i ignore the answer of your question")
            else:
                print(f"answer:{answer}")


@Ask_cli.command()
def back():
    os.system("python3.8 client.py")


Menu_cli = Cli("Menu")

if __name__ == '__main__':

    try:
        os.system('figlet  welcome to the chat')
    except:
        pass

    # Ask_cli.run()
    menu = input("what you want to do:")
    if menu.strip() == "chat":
        chat_cli.run()
    if menu.strip() == "ask":
        Ask_cli.run()

    if menu.strip() == "quit":
        exit()
