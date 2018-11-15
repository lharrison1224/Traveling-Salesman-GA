from random import randint
import random
import math

NUM_CITIES = 20  # how many cities we are travelling between
MAP_WIDTH = 50  # the width of the map where cities will be placed
MAP_HEIGHT = 30  # the height of the map where cities will be placed
POPULATION_SIZE = 1000  # the size of the population in each generation
# the percentage of the top chromosomes that will be be parents for the next generation
PARENT_POPULATION_RATIO = 0.5
MUTATION_CHANCE = 0.3  # probability that a new chromosome will mutate
GENERATIONS = 100  # the number of generations the evolution will go through


def main():
    best_cost = math.inf
    best_path = []
    cities = generate_cities()
    chromosomes = generate_base_chromosomes()

    for generation in range(GENERATIONS):

        # evaluate all current chromosomes
        fitness = evaluate_chromosomes(chromosomes, cities, fitness_sum_dists)

        # pair chromosomes with their fitness so we can sort them
        chromosomes_with_fitness = [(chromosomes[i], fitness[i])
                                    for i in range(POPULATION_SIZE)]

        # now sorted with best fitness early
        chromosomes_with_fitness.sort(key=(lambda x: x[1]))

        possible_parents = [chromosomes_with_fitness[i][0] for i in range(
            int(PARENT_POPULATION_RATIO*POPULATION_SIZE))]

        chromosomes = new_generation(possible_parents)

        if chromosomes_with_fitness[0][1] < best_cost:
            best_path = chromosomes_with_fitness[0][0]
            best_cost = chromosomes_with_fitness[0][1]

        print('End generation {}\t(best route: {})'.format(
            generation, best_cost))


def generate_cities():

    # Check to see if its possible to place cities without conflicts
    if NUM_CITIES > (MAP_HEIGHT * MAP_WIDTH):
        raise ValueError("Cannot put {} cities in a map of size {}x{}".format(
            NUM_CITIES, MAP_WIDTH, MAP_HEIGHT))

    cities = []
    for _ in range(NUM_CITIES):
        # generate a new city
        new_city = (randint(1, MAP_WIDTH), randint(1, MAP_HEIGHT))

        # check to see if there is already a city at the generated location
        while new_city in cities:
            print('hit')
            new_city = (randint(1, MAP_WIDTH), randint(1, MAP_HEIGHT))
        cities.append(new_city)

    # [(x_pos, y_pos), ... ]
    return cities


def generate_base_chromosomes():
    chromosomes = []
    for _ in range(POPULATION_SIZE):
        cities = [i for i in range(NUM_CITIES)]
        random.shuffle(cities)
        chromosomes.append(cities)
    return chromosomes


def linear_dist(a, b):
    return math.sqrt(((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2))


def fitness_sum_dists(chromosome, cities):
    total = 0
    for i in range(len(chromosome)-1):
        total += linear_dist(cities[chromosome[i]], cities[chromosome[i+1]])
    return total


def perform_crossover(parent_a, parent_b):
    '''
        Takes the first half of parent_a, then selects the remaining unused cities
        in the order that they appear in parent_b.

        ex. [1, 3, 5, 2, 6, 4] x [6, 3, 1, 5, 2, 4] -> [1, 3, 5, 6, 2, 4]
    '''
    num_to_keep = int(len(parent_a)/2)
    new_parent = parent_a[:num_to_keep]
    for i in range(len(parent_b)):
        if parent_b[i] not in new_parent:
            new_parent.append(parent_b[i])

    if randint(0, 99) < MUTATION_CHANCE * 100:
        new_parent = mutate_reverse_subsection(new_parent)
    return new_parent


def mutate_swap(chromosome):
    '''
        Swaps two random genes in the chromosome.

        ex. [5, 3, 2, 4, 6, 1] -> [5, 6, 2, 4, 3, 1]
    '''
    max_index = len(chromosome) - 1
    rand1 = randint(0, max_index)
    rand2 = randint(0, max_index)
    chromosome[rand1], chromosome[rand2] = chromosome[rand2], chromosome[rand1]


def mutate_reverse_subsection(chromosome):
    i = randint(0, len(chromosome)-1)
    j = len(chromosome) - 1 - i
    # guarantee that j is the bigger index
    if j < i:
        i, j = j, i

    reversed_segment = chromosome[i:j+1]
    reversed_segment.reverse()

    return chromosome[:i] + reversed_segment + chromosome[j+1:]


def new_generation(parents):
    return [perform_crossover(parents[randint(0, len(parents)-1)], parents[randint(0, len(parents)-1)]) for _ in range(POPULATION_SIZE)]


def evaluate_chromosomes(chromosomes, cities, fitness_fn):
    return [fitness_fn(chromosome, cities) for chromosome in chromosomes]


if __name__ == '__main__':
    main()
