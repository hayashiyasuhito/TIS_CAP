import PySimpleGUI as sg
import time
import threading
import signal
import os


def long_function_thread(window):
    for i in range(10):
        time.sleep(0.5)
        window.write_event_value('-THREAD PROGRESS-', i)
    window.write_event_value('-THREAD DONE-', '')

def takosig(window):
    signal.signal(signal.SIGALRM, long_function_thread)
    signal.setitimer(signal.ITIMER_REAL,1,10)
    while t < 10:
        sleep(1)

def long_function():
    child_pid = os.fork()
    if child_pid == -1:
        raise "failed to fork"
    if child_pid == 0:
        threading.Thread(target=takosig, args=(window,), daemon=True).start()

    else:
        signal.signal(signal.SIGALRM, long_function_thread)
        signal.setitimer(signal.ITIMER_REAL,1,10)
        while t < 10:
            sleep(1)

layout = [[sg.Output(size=(60,10))],
          [sg.Button('Go'), sg.Button('Nothing'), sg.Button('Exit')]  ]

window = sg.Window('Window Title', layout)

while True:             # Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Go':
        print('About to go to call my long function')
        long_function()
        print('Long function has returned from starting')
    elif event == '-THREAD DONE-':
        print('Your long operation completed')
    else:
        print(event, values)
window.close()
