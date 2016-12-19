import evdev
from evdev import ecodes
import sys

def getDevice():
    if len(sys.argv) != 2:
        print('Syntax : python3 keyboard.py <device>')
        exit(1)
    return sys.argv[1]

def readKeyboard(device, ui):
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            if event.code == 16 and event.value == 1:
                print('Déclenche un appui sur <F1>')
                ui.write(ecodes.EV_KEY, ecodes.KEY_F1, 1)
                ui.write(ecodes.EV_KEY, ecodes.KEY_F1, 0)
                ui.syn()


if __name__ == '__main__':
    dev = getDevice()
    device = evdev.InputDevice(dev)
    print('Connected to', dev)

    ui = evdev.UInput()
    readKeyboard(device, ui)
