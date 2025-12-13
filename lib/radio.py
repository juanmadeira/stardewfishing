import threading
import simpleaudio as sa

_lock = threading.Lock()
_current_play = None


def _play_one_file_blocking(filename):
    global _current_play

    try:
        wave = sa.WaveObject.from_wave_file(filename)
        play_obj = wave.play()

        with _lock:
            _current_play = play_obj

        play_obj.wait_done()
    except Exception:
        pass
    finally:
        with _lock:
            _current_play = None


def play(filename):
    t = threading.Thread(
        target=_play_one_file_blocking,
        args=(filename,),
        daemon=True
    )
    t.start()


def stop_all():
    global _current_play
    with _lock:
        if _current_play:
            try:
                _current_play.stop()
            except Exception:
                pass
            _current_play = None


def is_playing():
    with _lock:
        return _current_play is not None and _current_play.is_playing()
