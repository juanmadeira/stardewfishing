import platform
import os
import threading
import subprocess

_STOP_FLAG = False
_current_proc = None
_lock = threading.Lock()

has_ffmpeg = subprocess.run(["which", "ffmpeg"], capture_output=True, text=True)

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
        if has_ffmpeg.returncode == 0:
            _current_proc = subprocess.Popen(
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", filename],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            _current_proc = subprocess.Popen(
                ["aplay", filename],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        print(_current_proc)
        _current_proc.wait()
        return

def play(filename):
    t = threading.Thread(target=_play_one_file_blocking, args=(filename,))
    t.daemon = True
    t.start()

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
        if has_ffmpeg.returncode == 0:
            os.system("killall ffplay 2>/dev/null")
        else:
            os.system("killall aplay 2>/dev/null")

def is_playing():
    global _current_proc
    if _current_proc is None:
        return False
    return _current_proc.poll() is None