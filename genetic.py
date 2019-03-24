import random
import statistics
import sys
import time
from bisect import bisect_left
from enum import Enum
from math import exp

import selections


def _generate_parent(get_fitness, length, geneSet,generate_genes):
    genes = generate_genes(length, geneSet)
    fitness = get_fitness(genes)
    return Chromosome(genes, fitness, Strategies.Create)

def _mutate(parent, geneSet, get_fitness):
    return 0

def _mutate_custom(parent, custom_mutate, get_fitness):
    childGenes = parent.Genes
    custom_mutate(childGenes)
    fitness = get_fitness(childGenes)
    return Chromosome(childGenes, fitness, Strategies.Mutate)

def _crossover(parent, parentDonor, parents,get_fitness, crossover):
    childGenes = crossover(parent.Genes, parentDonor.Genes)
    fitness = get_fitness(childGenes)
    return Chromosome(childGenes, fitness, Strategies.Crossover)


def get_best(generate_genes, get_fitness, length, optimalFitness, geneSet, display,
             custom_mutate=None, custom_create=None, maxAge=None,
             poolSize=1, crossover=None):

    def fnMutate(parent):
        return _mutate_custom(parent, custom_mutate, get_fitness)

    def fnGenerateParent():
        return _generate_parent(get_fitness, length, geneSet, generate_genes)

    strategyLookup = {
        Strategies.Create: lambda p, o, i: fnGenerateParent(),
        Strategies.Mutate: lambda p, o, i: fnMutate(p),
        Strategies.Crossover: lambda p, o, i : _crossover(p, o, i, get_fitness, crossover)
    }
    usedStrategies = [strategyLookup[Strategies.Mutate]]
    usedStrategies.append(strategyLookup[Strategies.Crossover])

    def fnNewChild(parents):
        parent = selections.roulette_selection(parents)
        parentDonor = selections.roulette_selection(parents)
        while parent == parentDonor:
            parentDonor = selections.roulette_selection(parents)
        return random.choice(usedStrategies)(parent, parentDonor, parents) #bad

    for improvement in _get_improvement(fnNewChild, fnGenerateParent,
                                        maxAge, poolSize):
        display(improvement)
        if improvement.Fitness == 1:
            # import pdb; pdb.set_trace()
            return improvement

def _get_improvement(new_child, generate_parent, maxAge, poolSize):
    bestParent = generate_parent()
    yield bestParent
    parents = [bestParent]

    for _ in range(poolSize - 1): 
        parent = generate_parent()
        parents.append(parent)
        if parent.Fitness > bestParent.Fitness:
            yield parent
            bestParent = parent
    
    lastParentIndex = poolSize - 1
    pindex = 1
    while True:
        # import pdb; pdb.set_trace()
        # pindex = pindex - 1 if pindex > 0 else lastParentIndex
        # parent = parents[pindex]
    
        child = new_child(parents)
        # import pdb; pdb.set_trace()

        # if parent.Fitness > child.Fitness:
        #     # import pdb; pdb.set_trace()
        #     if maxAge is None: #retain the current functionality if maxAge is not provided.
        #         continue
        #     parent.Age += 1
        #     if maxAge > parent.Age:
        #         continue 

        # if not child.Fitness > parent.Fitness:
        #     import pdb; pdb.set_trace()
        #     child.Age = parent.Age + 1
        #     parents[pindex] = child
        #     continue
        # child.Age = 0
    #using parents[pindex] instead of parent when the parent is being replaced.
    
        # parents[pindex] = child
        if child.Fitness > bestParent.Fitness:
            bestParent = child
            parents.append(bestParent)
            yield bestParent
            # historicalFitnesses.append(bestParent.Fitness)
    

class Chromosome:
    def __init__(self, genes, fitness, strategy):
        self.Genes = genes
        self.Fitness = fitness
        self.Strategy = strategy
        self.Age = 0


class Strategies(Enum):
    Create = 0,
    Mutate = 1,
    Crossover = 2

class NullWriter():
    def write(self, s):
        pass

class Benchmark:
    @staticmethod
    def run(function):
        timings = []
        stdout = sys.stdout
        for i in range(100):
            sys.stdout = NullWriter()
            startTime = time.time()
            function()
            seconds = time.time() - startTime
            sys.stdout = stdout
            timings.append(seconds)
            mean = statistics.mean(timings)
            if i < 10 or i % 10 == 9:
                print("{} {:3.2f} {:3.2f}".format(
                    1 + i, mean,
                    statistics.stdev(timings, mean) if i > 1 else 0))
