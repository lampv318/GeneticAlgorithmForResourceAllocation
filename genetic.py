import random
import statistics
import sys
import time
from bisect import bisect_left
from enum import Enum
from math import exp


def _generate_parent(get_fitness, length, geneSet,generate_genes):
    genes = generate_genes(length, geneSet)
    fitness = get_fitness(genes)
    return Chromosome(genes, fitness, Strategies.Create)

def _mutate(parent, geneSet, get_fitness):
    return 0

def _mutate_custom(parent, custom_mutate, get_fitness):
    return 0

def _crossover(parentGenes, index, parents, get_fitness, crossover, mutate,
               generate_parent):
    return 0

# get_best will be responsible for displaying improvements and breaking the loop
def get_best(generate_genes, get_fitness, length, optimalFitness, geneSet, display,
             custom_mutate=None, custom_create=None, maxAge=None,
             poolSize=1, crossover=None):
    def fnGenerateParent():
        return _generate_parent(get_fitness, length, geneSet, generate_genes)

    def fnNewChild():
        return _generate_parent(get_fitness, length, geneSet, generate_genes) #bad

    i =1 
    for improvement in _get_improvement(fnNewChild, fnGenerateParent,
                                        maxAge, poolSize):
        display(improvement)
        i += 1
        if i == poolSize:
            return improvement

def _get_improvement(new_child, generate_parent, maxAge, poolSize):
    bestParent = generate_parent()
    yield bestParent
    parents = [bestParent]
    # initialize parents with the best parent.

    for _ in range(poolSize - 1): # an array of parent
        parent = generate_parent()
        parents.append(parent)
    
    # replace the best parent and update the list of historical best fitnesses.
    # import pdb; pdb.set_trace()
    

class Chromosome:
    def __init__(self, genes, fitness, strategy):
        self.Genes = genes
        self.Fitness = fitness
        self.Strategy = strategy
        self.Age = 0


class Strategies(Enum):
    # print("strategies")
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
