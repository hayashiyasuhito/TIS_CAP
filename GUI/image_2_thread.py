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

def every(delay, task, lim,arg):
  start = time.time()
  next_time = time.time() + delay
  nowtime = 0
  while nowtime<lim:
    try:
      task(arg)
      nowtime = time.time()-start
    except Exception:
      traceback.print_exc()
    time.sleep(max(0, next_time - time.time()))
    next_time += (time.time() - next_time) // delay * delay + delay

menu_def = [['File',['Settings','Exit']]]
LAYOUT = [
    [sg.Menu(menu_def)],
    [sg.Text('Input video name (/dev/video0)'), sg.InputText('/dev/video0',key='-Input_Videodev-')],
    [sg.Text('Input experiment time (min)'), sg.InputText('10',key='-Input_expMIN_-')],
    [sg.Text('Input interval (sec)'), sg.InputText('5',key='-Input_intMIN_-')],
    [sg.Text('',key='-TIME-')],
    [sg.Image(filename='', key='-Image-')],
    [
        sg.Button('View',key = '-View-'),
        sg.Button('Record',key = '-Record-'),
    ]
    ]

global WINDOW
WINDOW = sg.Window(
    "Demo script", LAYOUT, finalize=True
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
        event, values = View_WINDOW.read(timeout=20)
        ret, frame = cap.read()
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
        View_WINDOW['-Image-'].update(data=imgbytes)

        if event == "-Stop-":
            finalize(View_WINDOW)
            break

def view_CAM():
    Viewing = True

def record(cap):
    sec_ = datetime.now().strftime("%Y%m%d_%H_%M_%S")
    date_ = datetime.now().strftime("%Y%m%d")
    os.makedirs('./{}/{}'.format(date_,sec_),exist_ok=True)
    for i in range(63): #20FPSで3秒取得
        ret, frame = cap.read()
        if i>2:
            cv2.imwrite('./{}/{}/{}_{}.jpg'.format(date_,sec_,sec_,i-3),frame)

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
        cap = cv2.VideoCapture(values['-Input_Videodev-'])
        View_window(cap)
        cap.release()
    elif event == '-Record-':
        cap = cv2.VideoCapture(values['-Input_Videodev-'])
        global exp_time,int_time
        exp_time = int(values['-Input_expMIN_-'])*60
        int_time = int(values['-Input_intMIN_-'])
        record_START(cap)
        cap.release()

def finalize(window):
    window.close()

def mainloop():
    global start
    start = time.time()
    Viewing = False
    while True:
        global values
        event, values = WINDOW.read()
        #cap = cv2.VideoCapture(values['-Input_Videodev-'])
        if event == 'Exit':
            finalize(WINDOW)
            break

        elif event in ('-Record-','-View-'):
            event_play_record(event,values)

if __name__ == '__main__':
    mainloop()
