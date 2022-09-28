#coding:utf-8
from serial import Serial
from time import sleep, time
import signal
import re
import cv2
import subprocess
import numpy as np
from datetime import datetime
import os

def onoff(arg1,arg2):
    global t
    t = time() - start
    print('time: {}'.format(t))
    cap = cv2.VideoCapture(2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)
    ser.write(serHigh)
    sec_ = datetime.now().strftime("%Y%m%d_%H_%M_%S")
    date_ = datetime.now().strftime("%Y%m%d")
    os.makedirs('./{}/{}_{}/{}'.format(date_,rpm,rep,sec_),exist_ok=True)

    # はじめの3ファイルは0になってしまうので、これを無視して指定秒数分を取得。
    for i in range(63): #20FPSで3秒取得
        ret, frame = cap.read()
        if i>2:
            cv2.imwrite('./{}/{}_{}/{}/{}_{}_{}_{}.jpg'.format(date_,rpm,rep,sec_,rpm,rep,sec_,i-3),frame)

    cap.release()
    ser.write(serLow)
    # 撮影ののち、すぐにデータ化まで
    #exp_path = Path('./{}/{}_{}/{}'.format(date_,rpm_,rep,sec_))
    #Raw_BW_while.raw_bw(exp_path)

def main():
    signal.signal(signal.SIGALRM, onoff)
    signal.setitimer(signal.ITIMER_REAL,1,60)

    while t < exp_time:
        sleep(1)

if __name__ == '__main__':
    ser = Serial('/dev/ttyACM0',9600, timeout=None)#linux
    serHigh = bytes("h","utf-8")
    serLow = bytes("l","utf-8")
    ser.write(serLow)

    rpm = input('input rpm (7,15,22,47): ')
    rep = input('input rep:')

    exp_min = input('input experiment time (min): ')
    exp_time = int(exp_min)*60

    # 4x2.5 cmを写し込む。もとのsonyは、5.2x3.5 cm。
    WIDTH = 1920
    HEIGHT = 1200
    FPS = 20 #FPSは20に固定

    #cp = subprocess.run(["v4l2-ctl","--list-devices"] capture_output=True, text=True)
    subprocess.run(["v4l2-ctl","-d","/dev/video2","-p","{}".format(FPS)])
    subprocess.run(["v4l2-ctl","-d","/dev/video2","-c","brightness=240"])
    subprocess.run(["v4l2-ctl","-d","/dev/video2","-c","gain=0"])
    subprocess.run(["v4l2-ctl","-d","/dev/video2","-v","width={},height={}".format(WIDTH,HEIGHT)])
    subprocess.run(["v4l2-ctl","-d","/dev/video2","-c","exposure_time_absolute=3"])

    start = time()
    t = 0
    main()
