import platform
import os
import threading
import subprocess

_STOP_FLAG = False
_current_proc = None
_lock = threading.Lock()


def _play_one_file_blocking(filename):
    global _STOP_FLAG, _current_proc

    system = platform.system()
    if system == "Windows":
        import winsound
        try:
            winsound.PlaySound(filename, winsound.SND_FILENAME)
        except:
            pass
        return

    elif system == "Darwin":
        _current_proc = subprocess.Popen(
            ["afplay", filename],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        _current_proc.wait()
        return

    elif system == "Linux":
        _current_proc = subprocess.Popen(
            ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", filename],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        _current_proc.wait()
        return


def _sequence_logic(file_list):
    global _STOP_FLAG
    _STOP_FLAG = False

    for filename in file_list:
        if _STOP_FLAG:
            break
        _play_one_file_blocking(filename)


def play(filename):
    t = threading.Thread(target=_play_one_file_blocking, args=(filename,))
    t.daemon = True
    t.start()


def play_sequence(file_list):
    t = threading.Thread(target=_sequence_logic, args=(file_list,))
    t.daemon = True
    t.start()
    return t


def stop_all():
    global _STOP_FLAG, _current_proc
    _STOP_FLAG = True

    with _lock:
        if _current_proc and _current_proc.poll() is None:
            try:
                _current_proc.terminate()
            except:
                pass
        _current_proc = None

    system = platform.system()

    if system == "Windows":
        import winsound
        winsound.PlaySound(None, winsound.SND_PURGE)

    elif system == "Darwin":
        os.system("killall afplay 2>/dev/null")

    elif system == "Linux":
        os.system("killall ffplay 2>/dev/null")


def is_playing():
    global _current_proc
    if _current_proc is None:
        return False
    return _current_proc.poll() is None
