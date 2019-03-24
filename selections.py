import random
import operator

def random_selection(parents, index):
    donorIndex = random.randrange(0, len(parents))
    if donorIndex == index:
        donorIndex = (donorIndex + 1) % len(parents)

    # import pdb; pdb.set_trace()
    return parents[donorIndex]

def roulette_selection(parents):
    '''
    Selects individuals to be parents based on their fitness proportion 
    '''

    # sorted_pop = sorted(parents, key=operator.attrgetter('Fitness')) 
    # parents_pop's first is the best distance 

    sum_fits = 0
    # import pdb; pdb.set_trace()
    for ind in parents:
        sum_fits +=  ind.Fitness

    pick = random.uniform(0, sum_fits)
    current = 0
    for ind in parents:
        current += ind.Fitness
        if current > pick:
            return ind

    # sum_fits = sum(operator.attrgetter('Fitness'))

    # max_fitness = max(population, key=operator.attrgetter(fitness_name))
    # if minimization:
    #     sum_fits = sum(max_fitness - operator.attrgetter(fitness_name)(ind) for ind in population)
    # else:
    #     sum_fits = sum(operator.attrgetter(fitness_name)(ind) for ind in population)

    # pick = random_state.uniform(0, sum_fits)
    # current = 0
    # for ind in sorted_pop:
    #     if minimization:
    #         current += (max_fitness - ind.fitness)
    #     else:
    #         current += ind.fitness

    #     if current > pick:
    #         return ind
