# core/game_engine.py
import pygame
import random

# Window size (matches main.py)
WINDOW_W = 600
WINDOW_H = 500

# Bird physics
GRAVITY = 1200.0
JUMP_FORCE = -400.0

# Pipes
PIPE_SPEED = 200.0
PIPE_WIDTH = 60
PIPE_GAP = 150

# Spacing rules
BASE_PIPE_DISTANCE = 300
RANDOM_DISTANCE_MIN = 260
RANDOM_DISTANCE_MAX = 380


class GameEngine:
    """
    Member 1: Core game logic.
    Exposes:
      - bird_rect: pygame.Rect
      - pipes: list of dicts: {"top": Rect, "bottom": Rect, "scored": bool}
      - score: int
      - alive: bool
    """

    def __init__(self):
        self.reset()

    def reset(self):
        self.bird_rect = pygame.Rect(120, 220, 40, 40)
        self.velocity = 0.0

        # Jump lock (page 11 style): prevents repeated flaps mid-jump
        self.jump_locked = False

        self.pipes = []
        self.score = 0
        self.alive = True

        # Spawn control
        self._next_pipe_x = WINDOW_W + 40  # start just off-screen
        self._spawn_pipe_pair_at(self._next_pipe_x)
        self._schedule_next_spawn()

    def _current_pipe_distance(self) -> int:
        # Required: after score >= 30, randomize spacing
        if self.score >= 30:
            return random.randint(RANDOM_DISTANCE_MIN, RANDOM_DISTANCE_MAX)
        return BASE_PIPE_DISTANCE

    def _schedule_next_spawn(self):
        self._next_pipe_x += self._current_pipe_distance()

    def _spawn_pipe_pair_at(self, x: int):
        # gap_y is the vertical center of the gap
        gap_y = random.randint(120, 300)

        top_h = max(10, gap_y - PIPE_GAP // 2)
        bottom_y = gap_y + PIPE_GAP // 2
        bottom_h = max(10, WINDOW_H - bottom_y)

        top = pygame.Rect(x, 0, PIPE_WIDTH, top_h)
        bottom = pygame.Rect(x, bottom_y, PIPE_WIDTH, bottom_h)

        self.pipes.append({"top": top, "bottom": bottom, "scored": False})

    def update(self, dt: float, flap: bool):
        if not self.alive:
            return

        # ---- Bird physics ----
        self.velocity += GRAVITY * dt
        self.bird_rect.y += int(self.velocity * dt)

        if flap and not self.jump_locked:
            self.velocity = JUMP_FORCE
            self.jump_locked = True

        # Unlock once bird starts falling again (simple, reliable lock)
        if self.velocity > 0:
            self.jump_locked = False

        # Ceiling + ground collision
        if self.bird_rect.top <= 0:
            self.alive = False
            return

        if self.bird_rect.bottom >= WINDOW_H:
            self.alive = False
            return

        # ---- Pipes movement + collision + scoring ----
        for pair in self.pipes:
            top = pair["top"]
            bottom = pair["bottom"]

            top.x -= int(PIPE_SPEED * dt)
            bottom.x -= int(PIPE_SPEED * dt)

            # Collision
            if self.bird_rect.colliderect(top) or self.bird_rect.colliderect(bottom):
                self.alive = False
                return

            # Score when bird passes the pipe (once per pair)
            if not pair["scored"] and self.bird_rect.left > top.right:
                pair["scored"] = True
                self.score += 1

        # Remove off-screen pipes
        while self.pipes and self.pipes[0]["top"].right < 0:
            self.pipes.pop(0)

        # Spawn new pipes when it's time
        # (based on last pipe x position)
        if not self.pipes:
            self._next_pipe_x = WINDOW_W + 40
            self._spawn_pipe_pair_at(self._next_pipe_x)
            self._schedule_next_spawn()
        else:
            last_x = self.pipes[-1]["top"].x
            if last_x <= self._next_pipe_x - self._current_pipe_distance():
                # ensure we don't drift; spawn based on scheduled x
                self._spawn_pipe_pair_at(self._next_pipe_x)
                self._schedule_next_spawn()
