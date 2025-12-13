import math
import random

class Brain:
    def __init__(self, weights=None):
        if weights is None:
            # 4 weights for 4 inputs
            self.weights = [random.uniform(-1, 1) for _ in range(4)]
        else:
            self.weights = list(weights)

    def copy(self):
        return Brain(weights=self.weights[:])

    def activate(self, inputs):
        """Return sigmoid(W · X)."""
        z = sum(w * x for w, x in zip(self.weights, inputs))
        return 1 / (1 + math.exp(-z))

    def mutate(self, scale=0.1):
        for i in range(len(self.weights)):
            self.weights[i] += random.uniform(-scale, scale)
