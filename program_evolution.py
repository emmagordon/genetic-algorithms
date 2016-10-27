#!/usr/bin/env python2

import contextlib
import sys
import StringIO

import ga
from brainfuck import bf_interpreter, simplify
from character_set import CHARACTER_TO_VALUE, CHARACTER_SET_SIZE
from ga_string_utils import generate_random_string, breed_strings
from timeout import timelimit, TimeoutError, OoopsError


MAX_PROGRAM_LEN = 200
PROGRAM_EXEC_TIMEOUT = 1
WEIGHTED_COMMANDS = (2 * ["+", "+++", "+++++", "-", "---", "-----"]) + [">>>", ">", "<", "<<<", "[", "]", "."]  # ","
TARGET_PROGRAM_OUTPUT = "hi"  # for speed, target characters are limited to lowercase letters (see character_set.py)
MUTATION_RATE = 1
POPULATION_SIZE = 40


@contextlib.contextmanager
def stdout_redirect(where):
    sys.stdout = where
    try:
        yield where
    finally:
        sys.stdout = sys.__stdout__


def generate_random_program():
    return generate_random_string(WEIGHTED_COMMANDS, MAX_PROGRAM_LEN)


@timelimit(PROGRAM_EXEC_TIMEOUT)
def run(program):
    bf_interpreter(program)


def character_fitness(output_char, target_char):
    if output_char == target_char:
        fitness = 1

    else:
        output_char_val = CHARACTER_TO_VALUE[output_char]
        target_char_val = CHARACTER_TO_VALUE[target_char]

        offset = abs(output_char_val - target_char_val)
        if output_char_val < target_char_val:
            wrapped_offset = (output_char_val + CHARACTER_SET_SIZE) - target_char_val
        else:
            wrapped_offset = (target_char_val + CHARACTER_SET_SIZE) - output_char_val
        char_offset = min(offset, wrapped_offset)

        fitness = 1.6 * (0.5 - (float(char_offset) / CHARACTER_SET_SIZE))

    return fitness


def calculate_fitness(program):
    fitness = 0

    try:
        with stdout_redirect(StringIO.StringIO()) as new_stdout:
            run(program)

    except (TimeoutError, OoopsError):
        print("timeout")
        fitness = -sys.maxint

    else:
        new_stdout.seek(0)
        output = new_stdout.read()
        print(output)

        for (output_char, target_char) in zip(output, TARGET_PROGRAM_OUTPUT):
            fitness += character_fitness(output_char, target_char)

        fitness += (1 - 0.1 * abs(len(output) - len(TARGET_PROGRAM_OUTPUT)))

    return fitness


def breed_programs(prog1, prog2):
    return breed_strings(prog1, prog2, WEIGHTED_COMMANDS, MUTATION_RATE, replace_only=False, random_split=False)


def stop_condition(candidate):
    return candidate.fitness == (len(TARGET_PROGRAM_OUTPUT) + 1)


if __name__ == "__main__":
    program = ga.run_genetic_algorithm(spawn_func=generate_random_program,
                                       breed_func=breed_programs,
                                       fitness_func=calculate_fitness,
                                       stop_condition=stop_condition,
                                       population_size=POPULATION_SIZE,
                                       roulette_selection=True)

    # result = simplify(program)
    # print(result)
    # run(result)

    run(program)
    print("\n")
