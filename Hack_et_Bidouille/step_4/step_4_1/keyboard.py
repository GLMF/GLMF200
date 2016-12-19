import evdev
from evdev import ecodes
import sys
from xdo import Xdo
import ctypes

def getDevice():
    if len(sys.argv) != 2:
        print('Syntax : python3 keyboard.py <device>')
        exit(1)
    return sys.argv[1]

def readKeyboard(device, xdo):
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            if event.code == 16 and event.value == 1:
                print('Déclenche un appui sur <F1>')
                win_id = ctypes.c_ulong(0)
                xdo.send_keysequence_window(win_id, b'F1')


if __name__ == '__main__':
    dev = getDevice()
    device = evdev.InputDevice(dev)
    print('Connected to', dev)

    xdo = Xdo()
    readKeyboard(device, xdo)
