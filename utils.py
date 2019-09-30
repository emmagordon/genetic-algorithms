import random


def generate_random_string(character_list, max_length):
    string_len = random.randint(1, max_length)
    return "".join([random.choice(character_list) for _ in range(string_len)])


def breed_strings(parent1, parent2, character_list, mutation_rate,
                  replace_only=True, crossover=True, random_split=False):
    if crossover:
        (a1, a2) = split_string(parent1, random_split=random_split)
        (b1, b2) = split_string(parent2, random_split=random_split)
        child = mutate_string(a1 + b2, character_list, mutation_rate,
                              replace_only=replace_only)
    else:
        child = mutate_string(parent1, character_list, mutation_rate,
                              replace_only=replace_only)
    return child


def split_string(dna, random_split=False):
    if random_split:
        split_point = random.randint(1, (len(dna) - 1))
    else:
        split_point = int(len(dna) / 2)

    return dna[:split_point], dna[split_point:]


def mutate_string(dna, character_list, mutation_rate, replace_only=True,
                  flip_rate=0.01):
    if replace_only:
        mutation_type = "replacement"
    else:
        mutation_type = random.choice(["replacement", "insertion", "deletion"])

    if random.random() < mutation_rate:
        if mutation_type == "replacement":
            dna = "".join([random.choice(character_list)
                           if random.random() < flip_rate else gene
                           for gene in dna])
        elif mutation_type == "insertion":
            dna = random.choice(character_list) + dna
        else:
            dna = dna[1:]

    return dna
