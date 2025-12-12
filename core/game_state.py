from enum import Enum, auto


# ----------- SCREEN STATES (UI navigation) -----------

class Screen(Enum):
    TITLE = auto()
    SINGER_SELECT = auto()  
    TUTORIAL = auto()
    PLAYING = auto()
    GAME_OVER = auto()


# ----------- GAME MODES (PDF requirement) -----------

class GameMode(Enum):
    MANUAL = auto()
    AUTO = auto()

#------------ Special mode ------------


class Singer(Enum):
    TR = auto()   # Trestariu
    DB = auto()   # Dan Balan
    CR = auto()   # Cristi din Banat



# ----------- GLOBAL GAME STATE -----------

class GameState:
    """
    Shared state between UI screens and game logic.
    This class does NOT implement physics or AI.
    """

    def __init__(self):
        # UI navigation
        self.current_screen = Screen.TITLE
        self.next_screen = None          # 👈 ADD THIS

        # Game mode
        self.game_mode = GameMode.MANUAL

        # Scores
        self.score = 0
        self.best_manual = 0
        self.best_auto = 0

        # UI flags
        self.show_score_popup = False

        self.selected_singer = Singer.TR   # ✅ valid default




    # ----------- HELPERS -----------

    def reset_run(self):
        """Reset score at the start of a new run"""
        self.score = 0

    def apply_game_over(self):
        """Update best score depending on mode"""
        if self.game_mode == GameMode.MANUAL:
            self.best_manual = max(self.best_manual, self.score)
        else:
            self.best_auto = max(self.best_auto, self.score)
