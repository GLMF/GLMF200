from xdo import Xdo
import ctypes

if __name__ == '__main__':
    xdo = Xdo()
    current_window = ctypes.c_ulong(0)

    xdo.send_keysequence_window(current_window, b'F1')
