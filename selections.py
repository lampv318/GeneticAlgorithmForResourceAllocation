import random
import operator
import numpy

def random_selection(parents):
    index = random.randrange(0, len(parents))

    return parents[index]

def roulette_selection(parents):
    '''
    Selects individuals to be parents based on their fitness proportion 
    '''

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

def tournament_selection(parents, pressure):

    tournament_pool_size = int(len(parents)*pressure)
    tournamet_pool = numpy.random.choice(parents, size=tournament_pool_size, replace=False)
    # import pdb; pdb.set_trace()
    return max(tournamet_pool, key=operator.attrgetter('Fitness'))

def best_selection(parents):
    return parents[len(parents)-1]
