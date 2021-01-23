import paho.mqtt.client as mqtt
import time

from scrapping import search
from client import ChatClient


class ChatBot(ChatClient):
    def __init__(self, _id, address, port):
        super(ChatBot, self).__init__(_id, address, port)

    def on_message(self, client, pub_top,
                   message):  # Called when a message has been received on a topic that the client has subscirbed to.

        if str(message.topic) != self._id:
            msg = str(message.payload.decode("utf-8"))
            print(str(message.topic), msg)

            if msg.capitalize() == "Stop":
                self.FLAG = False
            else:
                answer = search(msg)
                answer = f"answer:{answer}"
                client.publish(self._id, answer)


if __name__ == '__main__':
    chat_bot = ChatBot("/chat/chatbot", "broker.hivemq.com", 1883)

    chat_bot.AddSubTopic("/chat/client1")
    chat_bot.Chat()
