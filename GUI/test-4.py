from time import sleep
import threading
import PySimpleGUI as sg

def action(window, punch_time, wait_time):
    print("Key Pressed - Space")
    print("Key Pressed - Right")
    print(f"Wait {punch_time} seconds")
    sleep(punch_time)
    print("Key Released - Right")
    print(f"Wait {wait_time} seconds")
    sleep(wait_time)
    print("Key Released - Space")
    print("Thread finished\n")
    # Call window.write("EVENT", "VALUE") in thread to update GUI if required

layout = [
    [sg.Text("Punch time", size=10), sg.Input("", size=10, key='Punch Time')],
    [sg.Text("Wait time",  size=10), sg.Input("", size=10, key='Wait Time')],
    [sg.Button('Punch'), sg.Button('Exit')],
]

window = sg.Window('App', layout)

while True:

    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Punch':
        try:
            punch_time, wait_time = float(values['Punch Time']), float(values['Wait Time'])
        except ValueError:
            print('Wrong value for time')
            continue
        threading.Thread(target=action, args=(window, punch_time, wait_time), daemon=True).start()
    elif event == 'EVENT':
        value = values[event]
        """ Update GUI here """

window.close()
