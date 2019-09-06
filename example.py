import time
import datetime
from threading import Thread

from vk_notifier import VKNotifier


def main():
    try:
        with open('auth.json', 'r') as f:
            auth = json.loads(" ".join(f.readlines()))
    except Exception as e:
        raise Exception('invalid auth data')

    vk = VKNotifier(auth, name = 'debug', sleep_time=5)
    vk.start()
    vk.alarm('alarm message')



if __name__ == "__main__":
    main()