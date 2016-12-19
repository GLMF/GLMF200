import evdev
from evdev import ecodes, UInput
import key
from configparser import ConfigParser
import ast
from gui.KeyboardLeds import KeyboardLeds
from gui.Notify import Notify
import logging
import logging.config

class MacroKeyboard:

    def __init__(self, dev, activeLog=False, configFile='keyboardrc.ini', logFile='keyboardlogrc.ini'):
        self.__device = evdev.InputDevice(dev)

        self.leds = KeyboardLeds(self.__device)
        self.leds.reset()

        self.notify = Notify('Keyboard Macros')
        self.notify.send('Running and connected to <b>{}</b>'.format(dev))

        self.__activeLog = activeLog
        if self.__activeLog:
            logging.config.fileConfig(logFile)
            self.__logger = logging.getLogger('root')

        self.__recording_buffer = []
        self.__recording = False
        self.__attribute_key = False
        self.__protect = False
        self.__unprotect = False

        self.__configFile = configFile
        self.__macros = {} # defined in readConfig()
        self.readConfig()

        self.__ui = UInput()


    ########
    ### Logging management

    def log(self, message, cat='info'):
        if self.__activeLog:
            #getattr(self.logger, cat)(message)
            if cat == 'info':
                self.__logger.info(message)
            elif cat == 'debug':
                self.__logger.debug(message)
            elif cat == 'debug':
                self.__logger.debug(message)
            elif cat == 'error':
                self.__logger.debug(message)

    ########
    ### Recording management

    def startRecording(self):
        self.log('Start recording macro')
        self.notify.send('Start recording macro')
        self.leds.numLockOn()
        self.__recording = True

    def stopRecording(self):
        self.log('Buffer: {}'.format(self.__recording_buffer))
        self.leds.numLockOff()
        self.leds.capsLockOn()
        self.notify.send('Stop recording macro\nHit a key to save the buffer')
        self.__recording = False

    def saveMacro(self, key):
        if key in self.__macros and 'lock' in self.__macros[key]:
            self.notify.send('Macro on <b>{}</b> is protected'.format(key))
        else:
            self.__macros[key] = {'key_down': self.__recording_buffer}
            self.log('Macros: {}'.format(self.__macros), cat='debug')
            self.writeConfig()

    def protectKey(self, key):
        self.__macros[key]['lock'] = True
        self.log('Macros: {}'.format(self.__macros), cat='debug')
        self.writeConfig()

    def unprotectKey(self, key):
        if 'lock' in self.__macros[key]:
            del self.__macros[key]['lock']
            self.log('Macros: {}'.format(self.__macros), cat='debug')
            self.writeConfig()


    ########
    ### Configuration file management

    def readConfig(self):
        self.__macros = {}
        config = ConfigParser()
        config.read(self.__configFile)

        for keysym in config.sections():
            self.log(config[keysym], cat='debug')
            actions_list = {}
            for action in config[keysym]:
                actions_list[action] = ast.literal_eval(config[keysym][action])
            self.__macros[keysym] = actions_list
            self.log('Macro pour {} => {}'.format(keysym, self.__macros[keysym]), cat='debug')
            self.log('Macros: {}'.format(self.__macros), cat='debug')

    def writeConfig(self):
        config = ConfigParser()

        for keysym, action in self.__macros.items():
            config[keysym] = action

        try:
            with open(self.__configFile, 'w') as fic:
                config.write(fic)
        except:
            self.log('Write error on config file'.format(self.__configFile), cat='error')
            self.notify.send('Write error on config file <b>{}</b>'.format(self.__configFile))
            exit(2)


    ########
    ### Keys management

    def pressKey(self, keysym):
        self.__ui.write(ecodes.EV_KEY, ecodes.ecodes[keysym], 1)
        self.__ui.write(ecodes.EV_KEY, ecodes.ecodes[keysym], 0)
        self.__ui.syn()

    def pressKeys(self, keysymList):
        for keysym in keysymList:
            self.pressKey(keysym)


    ########
    ### Keyboard main management

    def read(self):
        for event in self.__device.read_loop():
            if event.type == ecodes.EV_KEY:
                # Recording management with key.RECORDING
                if event.code == key.RECORDING and not self.__attribute_key and event.value == 1:
                    if not self.__recording:
                        self.startRecording()
                    else:
                        self.stopRecording()
                        self.__attribute_key = True
                # Recording keys
                if self.__recording and event.code != key.RECORDING and event.value == 1:
                    self.notify.flash('Appui sur <b>{}</b>'.format(ecodes.KEY[event.code]))
                    self.__recording_buffer.append(ecodes.KEY[event.code])
                # Set attribute to a macro
                elif self.__attribute_key and event.code != key.RECORDING and event.value == 1:
                    self.__attribute_key = False
                    self.saveMacro(ecodes.KEY[event.code])
                    self.notify.send('Macro saved in <b>{}</b>'.format(ecodes.KEY[event.code]))
                    self.leds.capsLockOff()
                    self.__recording_buffer = []
                    self.log('Macros: {}'.format(self.__macros), cat='debug')
                # Protect a macro
                elif event.code == ecodes.KEY_TAB and event.value == 1:
                    self.notify.send('Hit a key to indicate macro to protect')
                    self.leds.capsLockOn()
                    self.__protect = True
                elif self.__protect and event.value == 1:
                    if ecodes.KEY[event.code] in self.__macros:
                        self.protectKey(ecodes.KEY[event.code])
                        self.notify.send('Macro <b>{}</b> is protected'.format(ecodes.KEY[event.code]))
                    else:
                        self.notify.send('Macro not found')
                    self.leds.capsLockOff()
                    self.__protect = False
                # Unprotect a macro
                elif event.code == ecodes.KEY_CAPSLOCK and event.value == 1:
                    self.notify.send('Hit a key to indicate macro to unprotect')
                    self.leds.capsLockOn()
                    self.__unprotect = True
                elif self.__unprotect and event.value == 1:
                    if ecodes.KEY[event.code] in self.__macros:
                        self.unprotectKey(ecodes.KEY[event.code])
                        self.notify.send('Macro <b>{}</b> is no more protected'.format(ecodes.KEY[event.code]))
                    else:
                        self.notify.send('Macro not found')
                    self.leds.capsLockOff()
                    self.__unprotect = False
                # Execute macros
                else:
                    for keysym, action in self.__macros.items():
                        if event.code == ecodes.ecodes[keysym] and event.value == 1:
                            self.pressKeys(action['key_down'])
