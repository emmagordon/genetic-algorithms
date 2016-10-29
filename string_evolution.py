#!/usr/bin/env python2.7

import ga
import string

from utils import generate_random_string, breed_strings


TARGET = "PYCON UK 2016: A P45 FROM C-3PO?"
CHARACTERS = string.printable
MUTATION_RATE = 0.75
MAX_STRING_LENGTH = 100
POPULATION_SIZE = 100


def generate_candidate():
    return generate_random_string(CHARACTERS, MAX_STRING_LENGTH)


def calculate_fitness(dna):
    fitness = sum([a == b for (a, b) in zip(dna, TARGET)])
    diff_in_length = abs(len(dna) - len(TARGET))
    fitness -= (diff_in_length * 1.1)
    return fitness


def crossover(string1, string2):
    return breed_strings(string1, string2, CHARACTERS, MUTATION_RATE)


def stop_condition(candidate):
    return candidate.dna == TARGET


if __name__ == "__main__":
    ga.run_genetic_algorithm(spawn_func=generate_candidate,
                             breed_func=crossover,
                             fitness_func=calculate_fitness,
                             stop_condition=stop_condition,
                             population_size=POPULATION_SIZE)
