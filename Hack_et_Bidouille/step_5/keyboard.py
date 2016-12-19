import evdev
from evdev import ecodes, UInput
import sys
import key
from configparser import ConfigParser
import ast

def getDevice():
    if len(sys.argv) != 2:
        print('Syntax : python3 keyboard.py <device>')
        exit(1)
    return sys.argv[1]


########
### Leds management

def setLock(device, key, action='off'):
    if action == 'off':
        device.set_led(key, 0)
    elif action == 'on':
        device.set_led(key, 1)

def setNumLock(device, action='off'):
    setLock(device, ecodes.LED_NUML, action)

def setCapsLock(device, action='off'):
    setLock(device, ecodes.LED_CAPSL, action)

def resetLeds(device):
    setNumLock(device, 'off')
    setCapsLock(device, 'off')


########
### Recording management

def startRecording(device):
    print('Start recording macro')
    setNumLock(device, 'on')
    return True

def stopRecording(device, recording_buffer):
    print('Stop recording macro')
    print('Buffer:', recording_buffer)
    setNumLock(device, 'off')
    setCapsLock(device, 'on')
    print('Hit a key to save the buffer')
    return False

def saveMacro(key, recording_buffer, macros):
    macros[key] = {'key_down': recording_buffer}
    print(macros)
    writeConfig(macros)


########
### Configuration file management

def readConfig(configFile='keyboardrc.ini'):
    macros = {}
    config = ConfigParser()
    config.read(configFile)

    for keysym in config.sections():
        print(config[keysym])
        actions_list = {}
        for action in config[keysym]:
            actions_list[action] = ast.literal_eval(config[keysym][action])
        macros[keysym] = actions_list
        print('Macro pour', keysym, '=>', macros[keysym])
        print(macros)

    return macros

def writeConfig(macros, configFile='keyboardrc.ini'):
    config = ConfigParser()

    for keysym, action in macros.items():
        config[keysym] = action

    try:   
        with open(configFile, 'w') as fic:
            config.write(fic)
    except:
        print('Write error on config file', configFile)
        exit(2)

    return macros


########
### Keys management

def pressKey(keysym, ui):
    ui.write(ecodes.EV_KEY, ecodes.ecodes[keysym], 1)
    ui.write(ecodes.EV_KEY, ecodes.ecodes[keysym], 0)
    ui.syn()

def pressKeys(keysymList, ui):
    for keysym in keysymList:
        pressKey(keysym, ui)


########
### Keyboard main management

def readKeyboard(device, ui):
    recording = False
    recording_buffer = []
    attribute_key = False
    macros = readConfig()

    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            # Recording management with key.RECORDING
            if event.code == key.RECORDING and not attribute_key and event.value == 1:
                if not recording:
                    recording = startRecording(device)
                else:
                    recording = stopRecording(device, recording_buffer)
                    attribute_key = True
            # Keys management
            if recording and event.code != key.RECORDING and event.value == 1:
                print('Appui sur', ecodes.KEY[event.code])
                recording_buffer.append(ecodes.KEY[event.code])
            elif attribute_key and event.code != key.RECORDING and event.value == 1:
                attribute_key = False
                saveMacro(ecodes.KEY[event.code], recording_buffer, macros)
                print('Macro saved in <{}>'.format(ecodes.KEY[event.code]))
                setCapsLock(device, 'off')
                recording_buffer = []
                print(macros)
            else:
                for keysym, action in macros.items():
                    if event.code == ecodes.ecodes[keysym] and event.value == 1:
                        pressKeys(action['key_down'], ui)


if __name__ == '__main__':
    dev = getDevice()
    device = evdev.InputDevice(dev)
    resetLeds(device)
    print('Connected to', dev)

    ui = UInput()
    readKeyboard(device, ui)
