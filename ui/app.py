#!/usr/local/bin/iotenv python


from kivy.app import App
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

import paho.mqtt.client as mqtt


class RegisterScreen(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count(
                "@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                # todo
                print("ok")

                self.reset()

                self.parent.current = "Login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        self.parent.current = "Login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class LoginScreen(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if self.email.text == 'cnd1':
            print(self.email.text)

            MainScreen.current = self.email.text
            ChatScreen.current = self.email.text
            self.reset()

            self.parent.current = "Main"
        else:
            invalidLogin()

    def registerBtn(self):
        self.reset()

        self.parent.current = "Register"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class MainScreen(Screen):
    nas = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    chat = ObjectProperty(None)
    bot = ObjectProperty(None)
    current = ""

    def go_chat(self):
        self.parent.current = "Chat"

    def logOut(self):
        self.parent.current = "Login"

    def on_enter(self, *args):

        password, name, created = "", "", ""

        self.nas.text = "Account Name: " + name
        self.email.text = "Email: " + self.current
        self.created.text = "Created On: " + created


class ChatScreen(Screen):
    messages = ObjectProperty(None)
    to_send = ObjectProperty(None)

    current = ""

    def disconect(self):
        mqtt_client.disconnect()

    def on_enter(self, *args):
        self.configure_mqtt()
        mqtt_client.loop_start()
        mqtt_client.subscribe("/chat/cnd2")

    def on_connect(self, client, userdata, flags, rc):
        # called when the broker responds to our connection request

        print(rc)

    def sendBtn(self):
        print(self.current)
        print(self.to_send.text)
        topic = "/chat/" + self.current
        mqtt_client.publish(topic, self.to_send.text)
        self.messages.text = self.messages.text + "\n" + f"{topic}:{self.to_send.text}"
        self.to_send.text = ""

    def on_message(self, client, pub_top,
                   message):  # Called when a message has been received on a topic that the client has subscirbed to.
        # print(pub_top)
        message_contain = str(message.payload.decode("utf-8"))
        print(message.topic)
        self.messages.text = self.messages.text + "\n" + f"{message.topic}:{message_contain}"

    def on_subscribe(self, client, userdata, mid,
                     granted_qos):  ##Called when the broker responds to a subscribe request.
        print("Subscribed:", str(mid), str(granted_qos))

    def on_unsubscirbe(self, client, userdata, mid):  # Called when broker responds to an unsubscribe request.
        print("Unsubscribed:", str(mid))

    def on_disconnect(client, userdata, rc):  # called when the client disconnects from the broker
        if rc != 0:
            print("Unexpected Disconnection")

    def configure_mqtt(self):
        mqtt_client.on_connect = self.on_connect
        mqtt_client.on_subscribe = self.on_subscribe
        mqtt_client.on_unsubscribe = self.on_unsubscirbe
        mqtt_client.on_message = self.on_message
        mqtt_client.on_disconnect = self.on_disconnect
        mqtt_client.connect("broker.hivemq.com", 1883)


class SKreenManager(ScreenManager):

    def __init__(self,id, **kwargs):
        self.id=id
        super(SKreenManager, self).__init__(**kwargs)


def invalidLogin():
    pop = Popup(title='Invalid Login',
                content=Label(text='Invalid username or password.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                content=Label(text='Please fill in all inputs with valid information.'),
                size_hint=(None, None), size=(400, 400))

    pop.open()


# kv = Builder.load_file("app.kv")

mqtt_client = mqtt.Client()


class mqttApp(MDApp):


    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file('app.kv')





if __name__ == '__main__':
    mqttApp().run()
