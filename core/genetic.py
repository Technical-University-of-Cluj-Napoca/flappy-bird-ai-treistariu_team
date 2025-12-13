import random
from core.species import Species
from core.bird import Bird

class GeneticAlgorithm:
    def __init__(self, speciation_threshold=1.5, mutation_scale=0.1):
        self.threshold = speciation_threshold
        self.mutation_scale = mutation_scale

    # Stage 1: speciation
    def create_species(self, birds):
        species_list = []

        for bird in birds:
            placed = False

            for s in species_list:
                diff = Species.weight_difference(bird.brain, s.representative)
                if diff <= self.threshold:
                    s.members.append(bird)
                    placed = True
                    break

            if not placed:
                new_s = Species(bird.brain.copy())
                new_s.members.append(bird)
                species_list.append(new_s)

        return species_list

    # Stage 2: fitness computation
    def compute_fitness(self, species_list):
        for s in species_list:
            total = sum(b.fitness for b in s.members)
            s.fitness = total / len(s.members)
            s.members.sort(key=lambda b: b.fitness, reverse=True)

    # Stage 3: sorting species
    def sort_species(self, species_list):
        species_list.sort(key=lambda s: s.fitness, reverse=True)

    # Stage 4: reproduction
    def reproduce(self, species_list, pop_size):
        if not species_list:
            return [Bird() for _ in range(pop_size)]

        new_population = []

        for s in species_list:
            if not s.members:
                continue
            champion = s.members[0]
            new_population.append(Bird(champion.brain.copy()))

        while len(new_population) < pop_size:
            parent_species = random.choice(species_list)
            parent = random.choice(parent_species.members)
            child_brain = parent.brain.copy()
            child_brain.mutate(scale=self.mutation_scale)
            new_population.append(Bird(child_brain))

        return new_population[:pop_size]
