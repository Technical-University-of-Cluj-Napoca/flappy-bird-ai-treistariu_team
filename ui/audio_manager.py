import pygame
from core.singer_config import SINGER_CONFIG


class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.current_track = None

    def play_singer_music(self, singer):
        cfg = SINGER_CONFIG[singer]
        track = cfg["music"]

        if self.current_track == track:
            return  # already playing

        pygame.mixer.music.stop()
        pygame.mixer.music.load(track)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # loop

        self.current_track = track

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_track = None
