import vk_api
import random
import json


class VKNotifier:
    def __init__(self):
        try:
            with open('cities.json', 'r') as f:
                self.auth = json.loads(" ".join(f.readlines()))
        except Exception:
            raise Exception('invalid auth data')
        vk_session = vk_api.VkApi(token=auth['token'])
        self.vk = vk_session.get_api()

    def alarm(self, message = 'unkonwn alarm'):

        self.vk.messages.send(user_id=self.auth['user_id'],
                            message=message, random_id = random.randint(0, 10**100000))