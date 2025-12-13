import platform
import os
import threading
import subprocess
import shutil

_STOP_FLAG = False
_current_proc = None
_lock = threading.Lock()


def _play_one_file_blocking(filename):
    global _current_proc

    system = platform.system()

    if system == "Windows":
        import winsound
        try:
            winsound.PlaySound(filename, winsound.SND_FILENAME)
        except Exception:
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
        has_ffmpeg = shutil.which("ffmpeg") is not None

        if has_ffmpeg:
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

        _current_proc.wait()
        return


def play(filename):
    t = threading.Thread(
        target=_play_one_file_blocking,
        args=(filename,),
        daemon=True
    )
    t.start()


def stop_all():
    global _current_proc

    with _lock:
        if _current_proc and _current_proc.poll() is None:
            try:
                _current_proc.terminate()
            except Exception:
                pass
        _current_proc = None

    system = platform.system()

    if system == "Windows":
        import winsound
        winsound.PlaySound(None, winsound.SND_PURGE)

    elif system == "Darwin":
        os.system("killall afplay 2>/dev/null")

    elif system == "Linux":
        if shutil.which("ffmpeg"):
            os.system("killall ffplay 2>/dev/null")
        else:
            os.system("killall aplay 2>/dev/null")


def is_playing():
    if _current_proc is None:
        return False
    return _current_proc.poll() is None
