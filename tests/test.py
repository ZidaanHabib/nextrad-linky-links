import threading
import time

def loop():
    global stop
    while not stop and :
        print("hello")
        time.sleep(0.5)

def delayed_stop_thread():
    global stop
    stop = True

def delay_stop():
    global stop
    thread_delay = threading.Timer(2,delayed_stop_thread)
    thread_delay.daemon = True
    thread_delay.start()



if __name__ == "__main__":
    global stop
    stop = False
    delay_stop()
    loop()