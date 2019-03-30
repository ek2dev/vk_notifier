import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import json

from threading import Thread


class VKNotifier(Thread):
    def __init__(self):
        Thread.__init__(self)
        try:
            with open('auth.json', 'r') as f:
                self.auth = json.loads(" ".join(f.readlines()))
        except Exception:
            raise Exception('invalid auth data')
        self.vk_session_ = vk_api.VkApi(token=self.auth['token_debug'])
        self.vk_debug = self.vk_session_.get_api()

        self.vk_session = vk_api.VkApi(token=self.auth['token_notifier'])
        self.vk_notifier = self.vk_session.get_api()

    def alarm(self, message='unknown alarm'):
        try:
            self.vk_notifier.messages.send(user_id=self.auth['user_id'],
                                           message=message, random_id=random.randint(0, 9223372036854775808))
        except Exception as e:
            self.log(e.__str__())

    def debug_message(self, message='debug message'):
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

