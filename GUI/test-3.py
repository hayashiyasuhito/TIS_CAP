import threading
import time
import schedule
import time, traceback

def hello():
    time_ = time.time() - start
    print("time: {}".format(time_))

# https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds
# Alfe's way
def every(delay, task):
  next_time = time.time() + delay
  while True:
    try:
      task()
    except Exception:
      traceback.print_exc()
    time.sleep(max(0, next_time - time.time()))
    next_time += (time.time() - next_time) // delay * delay + delay

start = time.time()
#every(5, hello)
threading.Thread(target=lambda: every(5, hello)).start()
