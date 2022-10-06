#!usr/bin/env python
# -*- coding: utf-8 -*-

import PySimpleGUI as sg
import cv2
import numpy as np
from time import sleep,time
import signal
from datetime import datetime
import os


def onoff(arg1,arg2):
    global t
    t = time() - start
    print('time: {}'.format(t))
#    cap = cv2.VideoCapture(-1)
    sec_ = datetime.now().strftime("%Y%m%d_%H_%M_%S")
    date_ = datetime.now().strftime("%Y%m%d")
    os.makedirs('./{}/{}'.format(date_,sec_),exist_ok=True)

    # はじめの3ファイルは0になってしまうので、これを無視して指定秒数分を取得。
    for i in range(63): #20FPSで3秒取得
        ret, frame = cap_L.read()
        if i>2:
            cv2.imwrite('./{}/{}/{}_{}.jpg'.format(date_,sec_,sec_,i-3),frame)

#    cap.release()

def main(cap_L,window):
    signal.signal(signal.SIGALRM, onoff)
    signal.setitimer(signal.ITIMER_REAL,1,10)

    while t < exp_time:
        sleep(1)
        #ret, frame = cap_L.read()
        #　映像をメモリにエンコードする
        #imgbytes_L = cv2.imencode('.png', frame)[1].tobytes()  # ditto
        #window['Image_L'].update(data=imgbytes_L)


# メイン関数
def GUI():

    sg.theme('Black')

    #Frameを設定
    frame_1 = sg.Frame('Left',[
        [sg.Text('Input video name (/dev/video0)'), sg.InputText(key='-Input_Videodev_Left-')],
        [sg.Text('Input serial name (/dev/ttyACM0)'), sg.InputText(key='-Input_Serialdev_Left-')],
        [sg.Text('Input RPM (7,15,22,47)'), sg.InputText(key='-Input_RPM_Left-')],
        [sg.Text('Input REP (1,2,3..?)'), sg.InputText(key='-Input_REP_Left-')],
        [sg.Text('Input experiment time (min)'), sg.InputText(key='-Input_MIN_Left-')],
        [sg.Image(filename='', key='Image_L')],
        [sg.Button('View_L', size=(10, 1), font='Helvetica 14'),sg.Button('Record_L', size=(10, 1), font='Helvetica 14'),sg.Button('Stop_L', size=(10, 1), font='Any 14')]
    ])

    frame_2 = sg.Frame('Right',[
        [sg.Text('Input video name (/dev/video2)'), sg.InputText(key='-Input_Videodev_Right-')],
        [sg.Text('Input serial name (/dev/ttyACM1)'), sg.InputText(key='-Input_Serialdev_Right-')],
        [sg.Image(filename = '', key='Image_R')],
        [sg.Button('View_R', size=(10, 1), font='Helvetica 14'),sg.Button('Record_R', size=(10, 1), font='Helvetica 14'),sg.Button('Stop_R', size=(10, 1), font='Any 14')]
    ])


    menu_def = [['File',['Settings','Exit']]]

    layout = [
        [sg.Menu(menu_def)],
        [frame_1,frame_2],
    ]

    # ウィンドウの生成
    window = sg.Window('Couette Device管理アプリ',layout,location=(800, 400),resizable=True, disable_close=True)

    recording_L = False
    recording_R = False
    View_L = False
    View_R = False
    #　イベントループ
    while True:
        #　イベント取得
        event, values = window.read(timeout=20)
        img = np.full((480, 640), 255)
        imgbytes = cv2.imencode('.png', img)[1].tobytes()

        window['Image_L'].update(data=imgbytes)
        window['Image_R'].update(data=imgbytes)


        #　「Exit」ボタン押下時、ウィンドウ右上の×押下時の処理
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break

        #　「Record」ボタン押下時の処理
        elif event == 'View_L':
            #　撮影を開始する
            global cap_L
            cap_L = cv2.VideoCapture(values['-Input_Videodev_Left-'])
            View_L = True

        elif event == 'Record_L':
            #　撮影を開始する
            cap_L.release()
            View_L = False
            cap_L = cv2.VideoCapture(values['-Input_Videodev_Left-'])
            recording_L = True

        #　「Stop」ボタン押下時の処理
        elif event == 'Stop_L':
            # 撮影を停止する
            cap_L.release()
            View_L = False
            #　映像を消す
            img = np.full((480, 640), 255)
            imgbytes_blank = cv2.imencode('.png', img)[1].tobytes()
            window['Image_L'].update(data=imgbytes_blank)

        #　録画フラグがTrueなら、撮影を開始する
        if View_L:
            #　カメラ映像を取得する
            ret, frame = cap_L.read()
            #　映像をメモリにエンコードする
            imgbytes_L = cv2.imencode('.png', frame)[1].tobytes()  # ditto
            #　映像を表示する
            window['Image_L'].update(data=imgbytes_L)

        if recording_L:
            global exp_time
            exp_time = int(values['-Input_MIN_Left-'])*60
            global start
            start = time()
            global t
            t = 0
            main(cap_L,window)

    window.close()

if __name__ == '__main__':
    GUI()
