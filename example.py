import time
import datetime
from threading import Thread

from vk_notifier import VKNotifier


def main():
    vk = VKNotifier(name = 'debug', sleep_time=5)
    vk.start()
    vk.alarm('alarm message')



if __name__ == "__main__":
    main()