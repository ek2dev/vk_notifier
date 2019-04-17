import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import json
import time
import datetime
import requests
from queue import Queue

from threading import Thread, Timer


class Message:
    def __init__(self, messenger, text, name, user_id):
        self.messenger = messenger
        self.text = text
        self.name = name
        self.user_id = user_id

    def send(self):
        self.messenger.messages.send(user_id=self.user_id,
                                     message=f"{self.name}: {self.text}",
                                     random_id=random.randint(0, 9223372036854775808))

class VKNotifier(Thread):
    def __init__(self, name='unknown vk_notifier', sleep_time=3600):
        Thread.__init__(self)
        try:
            with open('auth.json', 'r') as f:
                self.auth = json.loads(" ".join(f.readlines()))
        except Exception as e:
            raise Exception('invalid auth data')
        self.name = name
        self.sleep_time = sleep_time

        self.vk_session_ = vk_api.VkApi(token=self.auth['token_debug'])
        self.vk_debug = self.vk_session_.get_api()
        self.start_date = datetime.datetime.now()
        self.vk_session = vk_api.VkApi(token=self.auth['token_notifier'])
        self.vk_notifier = self.vk_session.get_api()
        self.message_Queue = Queue()



    def send_alive_notifications(self):
        while True:
            self.debug_message(f"I'm up for {str(datetime.datetime.now() - self.start_date).split('.', 2)[0]}")
            time.sleep(self.sleep_time)

    def alarm(self, message):
        self.message_Queue.put(Message(self.vk_notifier, message, user_id=self.auth['user_id'], name=self.name))


    def debug_message(self, message):
        self.message_Queue.put(Message(self.vk_debug, message, user_id=self.auth['user_id'], name=self.name))



    def log(self, message):
        print(message)

    def handle_queue(self):
        while True:
            message = self.message_Queue.get()
            try:
                message.send()
            except Exception as e:
                self.message_Queue.put(message)
                self.log(f"Queue handler error: {e.__str__()}")
            finally:
                time.sleep(10)

    def run(self):
        queue_handler = Thread(target=self.handle_queue, args=[])
        queue_handler.start()

        alive_notifier = Thread(target=self.send_alive_notifications(), args=[])
        alive_notifier.start()
        # echo#
       # longpoll = VkLongPoll(self.vk_session)
       # for event in longpoll.listen():
        #    if event.type == VkEventType.MESSAGE_NEW and event.text:
        #        self.log(f"user ({event.user_id}): {event.text}")
          #      if event.user_id != self.auth['user_id']:
            #        self.alarm(f"user ({event.user_id}): {event.text}")
