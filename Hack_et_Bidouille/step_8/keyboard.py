from MacroKeyboard import MacroKeyboard
import sys

def getDevice():
    if len(sys.argv) != 2:
        print('Syntax : python3 keyboard.py <device>')
        exit(1)
    return sys.argv[1]

if __name__ == '__main__':
    dev = getDevice()
    macroKeyboard = MacroKeyboard(dev, activeLog=True)

    macroKeyboard.read()
