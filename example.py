import time
import datetime
from threading import Thread

from vk_notifier import VKNotifier


def main():
    vk = VKNotifier()
    vk.start()
    start_date = datetime.datetime.now()
    while True:
        vk.alarm(f"i'm awake for {str(datetime.datetime.now() - start_date).split('.', 2)[0]}")
        time.sleep(600)


if __name__ == "__main__":
    main()