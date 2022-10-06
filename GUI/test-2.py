import threading
import time
import schedule

def hello():
    time_ = time.time() - start
    print("time: {}".format(time_))

start = time.time()

schedule.every(5).seconds.do(hello)
while True:
    schedule.run_pending()
    time.sleep(1)
