from evdev import ecodes

class KeyboardLeds:

    def __init__(self, device):
        self.__device = device
        self.__numLock = 'off'
        self.__capsLock = 'off'

    def __setLock(self, key, action='off'):
        if action == 'off':
            self.__device.set_led(key, 0)
        elif action == 'on':
            self.__device.set_led(key, 1)

    def __setNumLock(self, action='off'):
        self.__setLock(ecodes.LED_NUML, action)
        self.__numLock = action

    def __setCapsLock(self, action='off'):
        self.__setLock(ecodes.LED_CAPSL, action)
        self.__capsLock = action

    def numLockOn(self):
        self.__setNumLock('on')

    def numLockOff(self):
        self.__setNumLock('off')

    def capsLockOn(self):
        self.__setCapsLock('on')

    def capsLockOff(self):
        self.__setCapsLock('off')

    def reset(self):
        self.numLockOff()
        self.capsLockOff()
