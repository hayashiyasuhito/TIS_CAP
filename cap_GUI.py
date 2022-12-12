#!usr/bin/env python
# -*- coding: utf-8 -*-

import PySimpleGUI as sg
import cv2
import numpy as np
from time import sleep
import signal
from datetime import datetime
import os
import threading
import schedule
import traceback,time
from serial import Serial
import subprocess

def every(delay, task, lim,arg):
  start = time.time()
  next_time = time.time() + delay
  nowtime = 0
  while nowtime<lim:
    try:
      task(arg)
      nowtime = time.time()-start
    except Exception:
      break
    time.sleep(max(0, next_time - time.time()))
    next_time += (time.time() - next_time) // delay * delay + delay

menu_def = [['File',['Settings','Exit']]]
LAYOUT = [
    [sg.Menu(menu_def)],
    [sg.Text('Input video name (/dev/video0)'), sg.InputText('/dev/video2',key='-Input_Videodev-')],
    [sg.Text('Input serial name (/dev/ttyACM0)'), sg.InputText('/dev/ttyACM0',key='-Serialdev-')],
    [sg.Text('Input experiment time (min)'), sg.InputText('60',key='-Input_expMIN_-')],
    [sg.Text('Input interval (sec)'), sg.InputText('180',key='-Input_intMIN_-')],
    [sg.Text('RPM (7,15,22,47)'), sg.InputText('22',key='-RPM-'),sg.Text('REP'), sg.InputText('1',key='-REP-')],
    [sg.Text('',key='-TIME-')],
    [sg.Image(filename='', key='-Image-')],
    [
        sg.Button('View',key = '-View-'),
        sg.Button('Record',key = '-Record-'),
    ]
    ]

global WINDOW
WINDOW = sg.Window(
    "Capture", LAYOUT, finalize=True
)

def View_window(cap):
    LAYOUT_view = [
        [sg.Image(filename='', key='-Image-')],
        [
            sg.Button('Stop',key = '-Stop-'),
        ]
        ]
    View_WINDOW = sg.Window('Viewer', LAYOUT_view)
    while True:
        ser.write(serHigh)
        event, values = View_WINDOW.read(timeout=20)
        ret, frame = cap.read()
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
        View_WINDOW['-Image-'].update(data=imgbytes)

        if event == "-Stop-":
            ser.write(serLow)
            finalize(View_WINDOW)
            break

def record(cap):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)
    sec_ = datetime.now().strftime("%Y%m%d_%H_%M_%S")
    date_ = datetime.now().strftime("%Y%m%d")
    os.makedirs('./{}/{}_{}/{}'.format(date_,rpm,rep,sec_),exist_ok=True)
    ser.write(serHigh)
    for i in range(63): #20FPSで3秒取得
        ret, frame = cap.read()
        if i>2:
            cv2.imwrite('./{}/{}_{}/{}/{}_{}_{}_{}.jpg'.format(date_,rpm,rep,sec_,rpm,rep,sec_,i-3),frame)
    ser.write(serLow)


def record_START(arg):
    th1 = threading.Thread(target=lambda: every(int_time, record,exp_time,arg),daemon=True)
    th1.start()
    for i in range(1,exp_time):
        sleep(1)
        prog = sg.one_line_progress_meter('Recording', i+1, exp_time,orientation = 'h', no_titlebar=True)
        if prog ==False:
            break

    arg.release()

def record_STOP():
    finalize()

def event_play_record(event,values):
    if event == '-View-':

        WINDOW['-Record-'].update(disabled = True)
        WINDOW['-View-'].update(disabled = True)
        cap = cv2.VideoCapture(values['-Input_Videodev-'])
        View_window(cap)
        cap.release()
        WINDOW['-Record-'].update(disabled = False)
        WINDOW['-View-'].update(disabled = False)

    elif event == '-Record-':
        WINDOW['-Record-'].update(disabled = True)
        WINDOW['-View-'].update(disabled = True)
        cap = cv2.VideoCapture(values['-Input_Videodev-'])
        global exp_time,int_time
        exp_time = int(values['-Input_expMIN_-'])*60
        int_time = int(values['-Input_intMIN_-'])
        record_START(cap)
        cap.release()
        WINDOW['-Record-'].update(disabled = False)
        WINDOW['-View-'].update(disabled = False)


def finalize(window):
    window.close()

def mainloop():
    #global start
    #start = time.time()
    while True:
        global values
        event, values = WINDOW.read()
        global rpm,rep,ser
        rpm = int(values['-RPM-'])
        rep = int(values['-REP-'])
        ser = Serial(values['-Serialdev-'],9600, timeout=None)#linux
        ser.write(serLow)

        subprocess.run(["v4l2-ctl","-d",values['-Input_Videodev-'],"-p","{}".format(FPS)])
        subprocess.run(["v4l2-ctl","-d",values['-Input_Videodev-'],"-c","brightness=240"])
        subprocess.run(["v4l2-ctl","-d",values['-Input_Videodev-'],"-c","gain=0"])
        subprocess.run(["v4l2-ctl","-d",values['-Input_Videodev-'],"-v","width={},height={}".format(WIDTH,HEIGHT)])
        subprocess.run(["v4l2-ctl","-d",values['-Input_Videodev-'],"-c","exposure_time_absolute=3"])

        if event == 'Exit':
            finalize(WINDOW)
            break

        elif event in ('-Record-','-View-'):
            event_play_record(event,values)

if __name__ == '__main__':
    serHigh = bytes("h","utf-8")
    serLow = bytes("l","utf-8")
    # 4x2.5 cmを写し込む。もとのsonyは、5.2x3.5 cm。
    WIDTH = 1920
    HEIGHT = 1200
    FPS = 20 #FPSは20に固定

    mainloop()
