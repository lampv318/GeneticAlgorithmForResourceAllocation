import random
import statistics
import sys
import time
import numpy
import operator
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
    child = custom_mutate(childGenes)
    fitness = get_fitness(child)
    return Chromosome(child, fitness, Strategies.Mutate)

def _crossover(parent, parentDonor, parents, get_fitness, crossover):
    childGenes = crossover(parent.Genes, parentDonor.Genes)
    fitness = get_fitness(childGenes)
    return Chromosome(childGenes, fitness, Strategies.Crossover)


def get_best(generate_genes, get_fitness, length, optimalFitness, geneSet, display,
             custom_mutate=None, custom_create=None, maxAge=None,
             poolSize=1, crossover=None):

    def fnGenerateParent():
        return _generate_parent(get_fitness, length, geneSet, generate_genes)

    def fnMutate(parent):
        return _mutate_custom(parent, custom_mutate, get_fitness)

    # def fn():
    #     pass

    #     usedStrategies = [strategyLookup[Strategies.Mutate]]
    # if crossover is not None:
    #     usedStrategies.append(strategyLookup[Strategies.Crossover])

    bestParent = fnGenerateParent()
    display(bestParent)
    # yield bestParent
    parents = [bestParent]

    for _ in range(poolSize - 1): 
        parent = fnGenerateParent()
        parents.append(parent)
        if parent.Fitness > bestParent.Fitness:
            display(parent)
            bestParent = parent
    
    lastParentIndex = poolSize - 1
    pindex = 1
    selectedParents = []
    while True:
        # select parents

        parents = sorted(parents, key=operator.attrgetter('Fitness'))
        parentIndex = 49
        for _ in range(50):
            tempParent = parents[parentIndex]
            selectedParents.append(tempParent)
            parentIndex += 1

        # crossover with Pc

        # for _ in range(50):
        #     parent = selections.roulette_selection(selectedParents)
        #     # import pdb; pdb.set_trace()
        #     parentDonor = selections.roulette_selection(selectedParents)
        #     while parent == parentDonor:
        #         parentDonor = selections.roulette_selection(selectedParents)
        #     child = _crossover(parent, parentDonor, parents, get_fitness, crossover)
        #     display(child)
        #     # child = fnMutate(child)
        #     selectedParents.append(child)
        #     if child.Fitness > bestParent.Fitness:
        #         bestParent = child
                # display(bestParent)

        # mutate with Pm

        for _ in range(50):
            # import pdb; pdb.set_trace()
            k = random.choice('01')
            if k == '0':
                parent = selections.roulette_selection(selectedParents)
                child = fnMutate(parent)
                # display(child)
                if child.Fitness > bestParent.Fitness:
                    bestParent = child
                    display(bestParent)
                selectedParents.append(child)
                if child.Fitness == 1:
                    import pdb; pdb.set_trace()
                    break
            else:
                parent = selections.roulette_selection(selectedParents)
                # import pdb; pdb.set_trace()
                parentDonor = selections.roulette_selection(selectedParents)
                while parent == parentDonor:
                    parentDonor = selections.roulette_selection(selectedParents)
                child = _crossover(parent, parentDonor, parents, get_fitness, crossover)
                # display(child)
                # child = fnMutate(child)
                selectedParents.append(child)
                if child.Fitness > bestParent.Fitness:
                    bestParent = child
                    display(bestParent)


            # if child.Fitness > 0.7:
            #     import pdb; pdb.set_trace()
            # display(child)

        parents = selectedParents
        selectedParents = []



    



    # strategyLookup = {
    #     Strategies.Create: lambda p, o, i: fnGenerateParent(),
    #     Strategies.Mutate: lambda p, o, i: fnMutate(p, i),
    #     Strategies.Crossover: lambda p, o, i : _crossover(p, o, i, get_fitness, crossover)
    # }
    # usedStrategies = [strategyLookup[Strategies.Mutate]]
    # usedStrategies.append(strategyLookup[Strategies.Crossover])

    # def fnNewChild(parents, parent1):
    #     parent = selections.roulette_selection(parents)
    #     parentDonor = selections.random_selection(parents)
    #     while parent == parentDonor:
    #         parentDonor = selections.random_selection(parents)
    #     return random.choice(usedStrategies)(parent, parentDonor, parent1) #bad

    # for improvement in _get_improvement(fnNewChild, fnGenerateParent,
    #                                     maxAge, poolSize):
    #     display(improvement)
    #     if improvement.Fitness == 1:
    #         return improvement

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
        # select parents
        parentIndex = 100
        for _ in range(100):
            tempParent = parents[parentindex]
            selectedParents.append(tempParent)
            parentIndex += 1

        # crossover with Pc

        for _ in range(100):
            parent = selections.roulette_selection(parents)
            parentDonor = selections.random_selection(parents)
            while parent == parentDonor:
                parentDonor = selections.random_selection(parents)





        # pindex = pindex - 1 if pindex > 0 else lastParentIndex
        # parent = parents[pindex]
        # import pdb; pdb.set_trace()
        child = new_child(parents, parent)
        # if parent.Fitness < child.Fitness:
        #     ind = parents.index(min(parents, key=operator.attrgetter('Fitness')))
        #     parents[ind] = child
        #     parents[pindex] = child
        #     if maxAge is None:
        #         continue
        #     parent.Age += 1
        #     if maxAge > parent.Age:
        #         continue
        # parents[pindex] = child
        # print("1") 
        # parents.append(child)
        # ind = parents.index(max(parents, key=operator.attrgetter('Fitness')))
        # parents[ind] = child
        # if bestParent.Fitness > 0.8:
        #     import pdb; pdb.set_trace()
        if child.Fitness > bestParent.Fitness:
            bestParent = child
            yield bestParent
            # print('1')
            # ind = parents.index(min(parents, key=operator.attrgetter('Fitness')))
            # parents[ind] = child
            parents.append(bestParent)
    

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
