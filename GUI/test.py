import threading
import time

def hello():
    time_ = time.time() - start
    print("現在のスレッドの数: " + str(threading.activeCount()))
    print("time: {}".format(time_))

    print("[%s] helohelo!!" % threading.currentThread().getName())
    t=threading.Timer(1,hello)
    t.start()

if __name__=='__main__':
    global start
    start = time.time()
    t=threading.Thread(target=hello)
    t.start()
