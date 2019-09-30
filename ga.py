import random
from collections import namedtuple

Candidate = namedtuple("Candidate", "dna fitness")
Population = namedtuple("Population", "average min max size best")


def run_genetic_algorithm(spawn_func, breed_func, fitness_func,
                          stop_condition, population_size=100,
                          roulette_selection=False):
    candidates = generate_population(spawn_func, fitness_func,
                                     population_size)
    num_iterations = 0
    while True:
        print(calculate_population_stats(candidates))
        for candidate in candidates:
            if stop_condition(candidate):
                print("Number of Iterations: %d" % num_iterations)
                return candidate.dna
        candidates = select_candidates(candidates,
                                       roulette_selection=roulette_selection)
        candidates = breed_population(candidates, breed_func, fitness_func)
        num_iterations += 1


def generate_population(generator_func, fitness_func, population_size=100):
    candidates = []
    for _ in range(population_size):
        dna = generator_func()
        fitness = fitness_func(dna)
        candidate = Candidate(dna=dna, fitness=fitness)
        candidates.append(candidate)
    return candidates


def calculate_population_stats(population):
    population = sorted(population, key=lambda x: -x.fitness)
    fitness_vals = [candidate.fitness for candidate in population]
    return Population(average=sum(fitness_vals) / len(population),
                      min=min(fitness_vals),
                      max=max(fitness_vals),
                      size=len(population),
                      best=population[0].dna)


def select_candidates(population, roulette_selection=False):
    half_population_size = int(len(population) / 2)
    ordered_population = sorted(population, key=lambda x: x.fitness)
    if roulette_selection:
        roulette_wheel = []
        for i, candidate in enumerate(ordered_population):
            roulette_wheel.extend(i * [candidate])
        selection = random.sample(roulette_wheel, half_population_size)
    else:
        selection = ordered_population[half_population_size:]
    return selection


def breed_population(candidates, breed_func, fitness_func):
    shuffled_candidates = sorted(candidates,
                                 key=lambda x: random.randint(1, 100))
    pairs = zip(candidates, shuffled_candidates)
    next_gen = []
    for parent1, parent2 in pairs:
        child_dna = breed_func(parent1.dna, parent2.dna)
        child_fitness = fitness_func(child_dna)
        child = Candidate(dna=child_dna, fitness=child_fitness)
        next_gen.extend([parent1, child])
    return next_gen
