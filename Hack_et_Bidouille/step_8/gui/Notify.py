import subprocess

class Notify:
    TIME_FLASH = 500

    def __init__(self, title, time = '1500'):
        self.__time = time
        self.__title = title

    def setTitle(self, title):
        self.__title = title

    def send(self, message):
        subprocess.Popen(['notify-send', '-t', str(self.__time), self.__title, message])

    def flash(self, message):
        subprocess.Popen(['notify-send', '-t', str(Notify.TIME_FLASH), self.__title, message])
