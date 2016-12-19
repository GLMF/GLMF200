from MacroKeyboard import MacroKeyboard
import sys

def getDevices():
    if len(sys.argv) != 3:
        print('Syntax : python3 keyboard.py <device_keyboard> <device_mouse>')
        exit(1)
    return (sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    devs = getDevices()
    macroKeyboard = MacroKeyboard(devs[0], devs[1], activeLog=True)

    macroKeyboard.read()
