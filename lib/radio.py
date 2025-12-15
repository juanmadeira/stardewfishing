import pyglet
from threading import Lock

_lock = Lock()
_players = []

def play(filename):
    with _lock:
        sound = pyglet.media.load(str(filename), streaming=False)
        player = pyglet.media.Player()
        player.queue(sound)
        player.play()
        _players.append(player)

def stop_all():
    with _lock:
        for p in _players:
            p.pause()
        _players.clear()

def is_playing():
    return any(p.playing for p in _players)