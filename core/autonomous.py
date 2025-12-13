from core.bird import Bird
from core.genetic import GeneticAlgorithm

class AutonomousController:
    """
    Manages an entire population of Birds, runs generations, 
    triggers natural selection, reports the best brain for auto mode.
    """

    def __init__(self, population_size=20):
        self.population_size = population_size
        self.ga = GeneticAlgorithm()
        self.generation = 1
        self.population = []
        for i in range(population_size):
            bird = Bird()
            bird.index = i
            self.population.append(bird)

    def start_generation(self):
        for b in self.population:
            b.fitness = 0
            b.alive = True

    def all_dead(self):
        return all(not b.alive for b in self.population)

    def evolve(self):
        species = self.ga.create_species(self.population)
        self.ga.compute_fitness(species)
        self.ga.sort_species(species)

        self.population = self.ga.reproduce(species, self.population_size)
        self.generation += 1

    @property
    def best_fitness(self):
        if not self.population:
            return 0
        return max(b.fitness for b in self.population)
    
    def reset(self):
        self.population = [Bird() for _ in range(self.population_size)]
        for i, b in enumerate(self.population):
            b.index = i
        self.generation = 1

    def notify_bird_dead(self, index):
        self.population[index].alive = False

    # Lidia call this in UI pls
    def population_status(self):
        alive = sum(1 for b in self.population if b.alive)
        return {
            "generation": self.generation,
            "best_fitness": self.best_fitness,
            "alive": alive,
            "total": len(self.population)
        }

    # Mara call this when bird passes a pipe pls
    def update_fitness(self, index, value=1):
        self.population[index].fitness += value

    # Mara call this each frame pls
    def decide_for_bird(self, index, inputs):
        bird = self.population[index]
        return bird.decide_flap(
            inputs["dist_top"],
            inputs["horiz_dist"],
            inputs["dist_bottom"],
            inputs["vel_y"]
        )



