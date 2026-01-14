import pygame
import random
from typing import Optional

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
    

    def __init__(self, population_size: int = 20):
        self.population_size = population_size
        self.reset_manual()


    def _current_pipe_distance(self, score: int) -> int:
        if score >= 30:
            return random.randint(RANDOM_DISTANCE_MIN, RANDOM_DISTANCE_MAX)
        return BASE_PIPE_DISTANCE

    def _spawn_pipe_pair_at(self, x: int):
        gap_y = random.randint(120, 300)

        top_h = max(10, gap_y - PIPE_GAP // 2)
        bottom_y = gap_y + PIPE_GAP // 2
        bottom_h = max(10, WINDOW_H - bottom_y)

        top = pygame.Rect(x, 0, PIPE_WIDTH, top_h)
        bottom = pygame.Rect(x, bottom_y, PIPE_WIDTH, bottom_h)

        # scored flag is per-bird in auto mode, so here we keep just rects.
        self.pipes.append({"top": top, "bottom": bottom})

    def _reset_pipes(self):
        self.pipes = []
        self._next_pipe_x = WINDOW_W + 40
        self._spawn_pipe_pair_at(self._next_pipe_x)
        self._next_pipe_x += BASE_PIPE_DISTANCE

    def _move_pipes(self, dt: float, score_for_spacing: int):
        # Move
        for pair in self.pipes:
            pair["top"].x -= int(PIPE_SPEED * dt)
            pair["bottom"].x -= int(PIPE_SPEED * dt)

        # Remove off-screen
        while self.pipes and self.pipes[0]["top"].right < 0:
            self.pipes.pop(0)

        # Spawn when last pipe reaches threshold
        if not self.pipes:
            self._next_pipe_x = WINDOW_W + 40
            self._spawn_pipe_pair_at(self._next_pipe_x)
            self._next_pipe_x += self._current_pipe_distance(score_for_spacing)
            return

        last_x = self.pipes[-1]["top"].x
        # If last pipe is sufficiently left, spawn new at scheduled x
        if last_x <= self._next_pipe_x - self._current_pipe_distance(score_for_spacing):
            self._spawn_pipe_pair_at(self._next_pipe_x)
            self._next_pipe_x += self._current_pipe_distance(score_for_spacing)

    # Manual mode
    def reset_manual(self):
        self.mode = "MANUAL"
        self.bird_rect = pygame.Rect(120, 220, 40, 40)
        self.velocity = 0.0
        self.jump_locked = False

        self.score = 0
        self.alive = True

        # pipes
        self._reset_pipes()

        # For manual scoring: track which pipe index has been scored
        self._manual_next_score_index = 0

    def update(self, dt: float, flap: bool):
        if self.mode != "MANUAL":
            self.reset_manual()

        if not self.alive:
            return

        # Bird physics
        self.velocity += GRAVITY * dt
        self.bird_rect.y += int(self.velocity * dt)

        if flap and not self.jump_locked:
            self.velocity = JUMP_FORCE
            self.jump_locked = True

        # Unlock once falling
        if self.velocity > 0:
            self.jump_locked = False

        # Collisions with bounds
        if self.bird_rect.top <= 0 or self.bird_rect.bottom >= WINDOW_H:
            self.alive = False
            return

        # Move pipes (spacing depends on score)
        self._move_pipes(dt, self.score)

        # Collisions with pipes
        for pair in self.pipes:
            if self.bird_rect.colliderect(pair["top"]) or self.bird_rect.colliderect(pair["bottom"]):
                self.alive = False
                return

        # Scoring: when bird passes a pipe pair (once per pair)
        # Use next unscored pipe index approach
        if self._manual_next_score_index < len(self.pipes):
            next_pair = self.pipes[self._manual_next_score_index]
            if self.bird_rect.left > next_pair["top"].right:
                self.score += 1
                self._manual_next_score_index += 1

    # Autonomous mode 
    
    def reset_population(self, population):
        
        self.mode = "AUTO"
        self.population = population

        # Each bird has its own rect/velocity/alive and a set of scored pipe ids.
        self.birds = []
        for b in self.population:
            self.birds.append({
                "index": b.index,
                "rect": pygame.Rect(120, 220, 40, 40),
                "vel": 0.0,
                "alive": True,
                "jump_locked": False,
                "scored_pipe_ids": set(),  # store id(pair) for pipes already scored
            })

        self.best_score_any_bird = 0

        self._reset_pipes()

    def _get_next_pipe_pair(self, bird_rect: pygame.Rect) -> Optional[dict]:
        bird_x = bird_rect.x
        for pair in self.pipes:
            if pair["top"].right >= bird_x:
                return pair
        return None

    def _ai_inputs_for(self, bird_rect: pygame.Rect, vel_y: float) -> dict:
   
        vel_n = max(-1.0, min(1.0, vel_y / 600.0))

        pair = self._get_next_pipe_pair(bird_rect)
        if pair is None:
            return {"dist_top": 0.0, "horiz_dist": 1.0, "dist_bottom": 0.0, "vel_y": vel_n}

        top = pair["top"]
        bottom = pair["bottom"]

        bird_cy = bird_rect.centery

        dist_top = (bird_cy - top.bottom) / WINDOW_H
        dist_bottom = (bottom.top - bird_cy) / WINDOW_H
        horiz_dist = (top.left - bird_rect.right) / WINDOW_W

        return {"dist_top": dist_top, "horiz_dist": horiz_dist, "dist_bottom": dist_bottom, "vel_y": vel_n}


    def update_auto(self, dt: float, auto_controller):
        
        if self.mode != "AUTO":
            # If not initialized, initialize from controller population
            self.reset_population(auto_controller.population)

        # Move pipes based on "best score" for spacing after 30
        self._move_pipes(dt, self.best_score_any_bird)

        # For each bird simulate
        for state in self.birds:
            if not state["alive"]:
                continue

            rect = state["rect"]
            vel = state["vel"]

            # Decide flap
            inputs = self._ai_inputs_for(rect, vel)
            flap = auto_controller.decide_for_bird(state["index"], inputs)

            # Apply physics
            vel += GRAVITY * dt
            rect.y += int(vel * dt)

            if flap and not state["jump_locked"]:
                vel = JUMP_FORCE
                state["jump_locked"] = True

            if vel > 0:
                state["jump_locked"] = False

            state["vel"] = vel
            auto_controller.update_fitness(state["index"], value=dt)  

            # Bounds collision
            if rect.top <= 0 or rect.bottom >= WINDOW_H:
                state["alive"] = False
                auto_controller.notify_bird_dead(state["index"])
                continue

            # Pipe collision
            dead = False
            for pair in self.pipes:
                if rect.colliderect(pair["top"]) or rect.colliderect(pair["bottom"]):
                    dead = True
                    break

            if dead:
                state["alive"] = False
                auto_controller.notify_bird_dead(state["index"])
                continue
            # When bird passes a pipe, increase its fitness by 1.
            for pair in self.pipes:
                if rect.left > pair["top"].right:
                    pid = id(pair)
                    if pid not in state["scored_pipe_ids"]:
                        state["scored_pipe_ids"].add(pid)
                        auto_controller.update_fitness(state["index"], value=1)

                        # Track best score in this run for spacing/UI
                        self.best_score_any_bird = max(self.best_score_any_bird, len(state["scored_pipe_ids"]))

        # If everyone is dead, evolve + reset world automatically
        if auto_controller.all_dead():
            auto_controller.evolve()
            auto_controller.start_generation()
            self.reset_population(auto_controller.population)

    def get_alive_bird_rects(self):
        if self.mode != "AUTO":
            return []
        return [b["rect"] for b in self.birds if b["alive"]]
