import evdev
from evdev import ecodes
import sys

def getDevice():
    if len(sys.argv) != 2:
        print('Syntax : python3 keyboard.py <device>')
        exit(1)
    return sys.argv[1]

def readJoypad(device):
    for event in device.read_loop():
        print('Type evt : {} - Code : {} - état {}'.format(event.type, event.code, event.value))

if __name__ == '__main__':
    dev = getDevice()
    device = evdev.InputDevice(dev)
    print('Connected to', dev)

    readJoypad(device)
