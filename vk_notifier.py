import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import json
import time
import datetime

from threading import Thread


class VKNotifier(Thread):
    def __init__(self, name='unknown vk_notifier', sleep_time = 3600):
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
        self.alive_notifier = Thread(target=self.alive_notification(), args=[self.name])
        self.alive_notifier.start()

    def alive_notification(self):
        while True:
            self.log(f"{self.name}'s up for {str(datetime.datetime.now() - self.start_date).split('.', 2)[0]}")
            time.sleep(self.sleep_time)

    def alarm(self, message):
        try:
            self.vk_notifier.messages.send(user_id=self.auth['user_id'],
                                           message=message, random_id=random.randint(0, 9223372036854775808))
        except Exception as e:
            self.log(e.__str__())

    def debug_message(self, message):
        try:
            self.vk_debug.messages.send(user_id=self.auth['user_id'],
                                        message=message, random_id=random.randint(0, 9223372036854775808))
        except Exception as e:
            self.log(e.__str__())

    def log(self, message):
        print(message)
        self.debug_message(message)

    def run(self):
        longpoll = VkLongPoll(self.vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.text:
                self.log(f"user ({event.user_id}): {event.text}")
                if event.user_id != self.auth['user_id']:
                    self.alarm(f"user ({event.user_id}): {event.text}")

