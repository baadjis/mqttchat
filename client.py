import paho.mqtt.client as mqtt
import time
import os
from cli import Cli


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
        if str(message.topic) != self._id:
            msg = str(message.payload.decode("utf-8"))
            print(str(message.topic), msg)
            if msg.capitalize() == "Stop":
                self.FLAG = False
            else:
                prompt = "Enter Message: "
                if message.topic.lower().find("bot") != -1:
                    prompt = "Ask:"
                self.chat = input(prompt)
                client.publish(self._id, self.chat)

    def on_subscribe(self, client, userdata, mid,
                     granted_qos):  ##Called when the broker responds to a subscribe request.
        print("Subscribed:", str(mid), str(granted_qos))

    def on_unsubscirbe(self, client, userdata, mid):  # Called when broker responds to an unsubscribe request.
        print("Unsubscribed:", str(mid))

    def on_disconnect(self, client, userdata, rc):  # called when the client disconnects from the broker
        if rc != 0:
            print("Unexpected Disconnection")

    def start_chat(self):
        """
        configure the chat callbacks

        """

        self.client.on_subscribe = self.on_subscribe
        self.client.on_unsubscribe = self.on_unsubscirbe
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def Chat(self, chat_promt="Enter message:"):
        """run the chat loop"""
        self.client.connect(self.address, self.port)
        self.start_chat()

        time.sleep(1)

        self.client.loop_start()
        for topic in self.sub_topics:
            self.client.subscribe(topic)

        time.sleep(1)
        self.chat = input(chat_promt)
        self.client.publish(self._id, self.chat)
        while True:

            if self.FLAG == False or self.chat.capitalize() == "Stop":
                break

        self.client.disconnect()
        self.client.loop_stop()


chat_cli = Cli("chat")


@chat_cli.command(cmd_args={"user_name": {"type": str, "help": "your user name"},
                            "other": {"type": str, "help": "the other person name"}})
def chat(user_name, other):
    chat_client = ChatClient("/chat/" + user_name, "broker.hivemq.com", 1883)
    chat_client.AddSubTopic("/chat/" + other)
    print(other.lower())
    if other.lower().find("bot") != -1:
        chat_client.Chat("Ask:")

    else:

        chat_client.Chat()


if __name__ == '__main__':
    try:
        os.system('figlet  welcome to the chat')
    except:
        pass
    chat_cli.run()
