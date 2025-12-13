class Species:
    def __init__(self, representative):
        self.representative = representative  # Brain
        self.members = []
        self.fitness = 0

    @staticmethod
    def weight_difference(b1, b2):
        """Sum of absolute differences between weights."""
        return sum(abs(a - b) for a, b in zip(b1.weights, b2.weights))
