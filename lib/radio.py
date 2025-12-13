import pygame
from threading import Lock

pygame.mixer.init()

_lock = Lock()

def play(filename):
    with _lock:
        sound = pygame.mixer.Sound(str(filename))
        sound.play()

def stop_all():
    with _lock:
        pygame.mixer.stop()

def is_playing():
    return pygame.mixer.get_busy()