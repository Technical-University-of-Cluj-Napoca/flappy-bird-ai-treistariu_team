from core.brain import Brain

class Bird:
    def __init__(self, brain=None):
        self.brain = brain or Brain()
        self.fitness = 0
        self.alive = True
        self.index = None

    def decide_flap(self, dist_top, horiz_dist, dist_bottom, vel_y):
        """
        Only flap if:
           - output > threshold
           - bird is falling (vel_y > 0)
        """
        output = self.brain.activate([dist_top, horiz_dist, dist_bottom, 1])
        if output > 0.5 and vel_y > 0:
            return True
        return False
