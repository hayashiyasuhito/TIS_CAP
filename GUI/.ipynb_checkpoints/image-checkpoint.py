#　https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_OpenCV_Webcam.py
#!usr/bin/env python
# -*- coding: utf-8 -*-

import PySimpleGUI as sg
import cv2
import numpy as np

# メイン関数
def main():

    sg.theme('Black')

    # レイアウト（1行目：テキスト、2行目：映像画面、3行目：ボタン、ボタン、ボタン）
    layout = [[sg.Text('OpenCVによるカメラデモ ', size=(40, 1), justification='center', font='Helvetica 20')],
                  [sg.Image(filename='', key='image')],
                  [sg.Button('Record', size=(10, 1), font='Helvetica 14'),sg.Button('Stop', size=(10, 1), font='Any 14'),sg.Button('Exit', size=(10, 1), font='Helvetica 14'), ]]

    # ウィンドウの生成
    window = sg.Window(' デモアプリ - OpenCVによるカメラアプリ',layout, location=(800, 400))

    # キャプチャするカメラを設定
    cap = cv2.VideoCapture(0)

    recording = False

    #　イベントループ
    while True:

        #　イベント取得
        event, values = window.read(timeout=20)

        #　「Exit」ボタン押下時、ウィンドウ右上の×押下時の処理
        if event == 'Exit' or event == sg.WIN_CLOSED:
            cap.release()
            window.close()
            return

        #　「Record」ボタン押下時の処理
        elif event == 'Record':
            #　撮影を開始する
            recording = True

        #　「Stop」ボタン押下時の処理
        elif event == 'Stop':
            # 撮影を停止する
            recording = False

            #　映像を消す
            img = np.full((480, 640), 255)
            imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window['image'].update(data=imgbytes)

        #　録画フラグがTrueなら、撮影を開始する
        if recording:
            #　カメラ映像を取得する
            ret, frame = cap.read()
            #　映像をメモリにエンコードする
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
            #　映像を表示する
            window['image'].update(data=imgbytes)

#　メイン関数をCALL
main()