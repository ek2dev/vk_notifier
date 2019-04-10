import time
import datetime
from threading import Thread

from vk_notifier import VKNotifier


def main():
    vk = VKNotifier()
    vk.start()



if __name__ == "__main__":
    main()