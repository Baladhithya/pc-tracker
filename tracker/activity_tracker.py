import ctypes

class IdleMonitor:
    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32

    def get_idle_duration(self):
        class LASTINPUTINFO(ctypes.Structure):
            _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

        lii = LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
        self.user32.GetLastInputInfo(ctypes.byref(lii))

        # Use GetTickCount64 instead of GetTickCount
        get_tick_count64 = self.kernel32.GetTickCount64
        get_tick_count64.restype = ctypes.c_ulonglong

        millis = get_tick_count64() - lii.dwTime
        return millis / 1000.0  # in seconds
