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

def _mutate_custom(parent, custom_mutate, get_fitness, bestParent):
    childGenes = parent.Genes
    custom_mutate(childGenes, bestParent)
    fitness = get_fitness(childGenes)
    return Chromosome(childGenes, fitness, Strategies.Mutate)

def _crossover(parent, parentDonor, parents,get_fitness, crossover):
    childGenes = crossover(parent.Genes, parentDonor.Genes)
    fitness = get_fitness(childGenes)
    return Chromosome(childGenes, fitness, Strategies.Crossover)


def get_best(generate_genes, get_fitness, length, optimalFitness, geneSet, display,
             custom_mutate=None, custom_create=None, maxAge=None,
             poolSize=1, crossover=None):

    def fnMutate(parent, bestParent):
        return _mutate_custom(parent, custom_mutate, get_fitness, bestParent)

    def fnGenerateParent():
        return _generate_parent(get_fitness, length, geneSet, generate_genes)

    strategyLookup = {
        Strategies.Create: lambda p, o, i: fnGenerateParent(),
        Strategies.Mutate: lambda p, o, i: fnMutate(p, i),
        Strategies.Crossover: lambda p, o, i : _crossover(p, o, i, get_fitness, crossover)
    }
    usedStrategies = [strategyLookup[Strategies.Mutate]]
    usedStrategies.append(strategyLookup[Strategies.Crossover])

    def fnNewChild(parent, parentDonor, bestParent):
        return random.choice(usedStrategies)(parent, parentDonor, bestParent) #bad

    for improvement in _get_improvement(fnNewChild, fnGenerateParent,
                                        maxAge, poolSize):
        display(improvement)
        if improvement.Fitness == 1:
            return improvement

def select_parent(parents):
    return 0

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
    for i in range(30000):
        # print(i)
        parent = selections.roulette_selection(parents)
        parentDonor = selections.roulette_selection(parents)
        # import pdb; pdb.set_trace()
        while parent == parentDonor:
            parentDonor = selections.roulette_selection(parents)
        ind = parents.index(parent)
        child = new_child(parent, parentDonor, bestParent)
        if child.Fitness > parent.Fitness:
            parents[ind] = child

        if child.Fitness == parent.Fitness:
            parents[ind] = child
        if child.Fitness == 1:
            import pdb; pdb.set_trace()
        
        if child.Fitness > bestParent.Fitness:
            bestParent = child
            yield bestParent
            # parents.append(bestParent)
    

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
