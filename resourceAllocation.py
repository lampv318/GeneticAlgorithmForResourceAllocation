import datetime
import math
import random
import unittest
import numpy as np
from itertools import chain

import genetic

def generate_genes(length, geneSet, arrayOfDependencies, arrayOfDuration):
    genes = { k: [] for k in range(1, length +1 )}
    for i in range(0, length):
        genesTask, taskInfor = [], []
        timeSched = generate_time_sched(genes, i, arrayOfDependencies, arrayOfDuration)
        genesTask.append(timeSched)
        while len(taskInfor) < length:
            sampleSize = min(length - len(genesTask), len(geneSet))
            taskInfor.extend(random.sample(geneSet, sampleSize))
        taskInfor = ''.join(taskInfor)
        genesTask.append(taskInfor) 
        genes[i+1] = genesTask
    return genes

def generate_time_sched(genes, index, arrayOfDependencies, arrayOfDuration):
    timeSched = 0  
    for i in range(len(arrayOfDependencies)):
        if arrayOfDependencies[i][1] == index:
            timeTemp = genes[arrayOfDependencies[i][0]][0] # time schedule of task j
            res = random.randrange(timeTemp, 90)
            return res
    return timeSched


def get_fitness(genes):
    return 0

def get_fitness_of_duration(genes, numberOfTask, arrayOfDependencies, 
                            arrayOfDuration):
    totalDelay = 0 
    for i in range(1, numberOfTask+1):
        timeSched = genes[i][0] # time schedule of task i
        timeStart = get_time_start(genes, i, arrayOfDependencies, arrayOfDuration)
        timeDelay = get_time_delay(timeSched, timeStart)
        totalDelay += timeDelay
    return totalDelay/numberOfTask

def get_time_start(genes, taskIndex, arrayOfDependencies, arrayOfDuration):
    timeStartMax = 0 
    for i in range(len(arrayOfDependencies)):
        if arrayOfDependencies[i][1] == taskIndex:
            timeSched = genes[arrayOfDependencies[i][0]][0] # time schedule of task j
            timeDuration = arrayOfDuration[arrayOfDependencies[i][0]]
            timeTemp = get_time_finish(timeSched, timeDuration)
            if timeStartMax < timeTemp:
                timeStartMax = timeTemp
    return timeStartMax

def get_time_finish(timeSched, timeDuration):
    return timeSched + timeDuration

def get_time_idle(timeSched, timeStart):
    return timeSched - timeStart

def get_time_delay(timeSched, timeStart):
    if timeSched < timeStart:
        return 0
    else: 
        return float(1)/(1 + (timeSched - timeStart))

def display(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime
    print("{}\t{}\t{}\t{}".format(
        candidate.Genes,
        candidate.Fitness,
        candidate.Strategy.name,
        timeDiff))


def get_distance(locationA, locationB):
    return 0


def mutate(genes, fnGetFitness, arrayOfDependencies, arrayOfDuration, bestParent):
    initialFitness = fnGetFitness(genes)
    # a = 0 
    index = random.randrange(1, len(genes)+1)
    for _ in range(0,40):
        a = genes[index][0] 
        # import pdb; pdb.set_trace()
        genes[index][0] = ball_mutation(a, 15)
        if genes[index][0] < 0:
            genes[index][0] = 0
        fitness = fnGetFitness(genes)
        if fitness > initialFitness:
            return genes
        genes[index][0] = a
    return genes

def ball_mutation(point, radius):
    return random.randint(point-radius, point+radius)
    # return np.array([random_state.uniform(low=coordinate - radius, high=coordinate + radius) 
    #     for coordinate in point])

def crossover(genes, donorGenes, fnGetFitness):
    initialFitness = fnGetFitness(genes) if (fnGetFitness(genes) > fnGetFitness(donorGenes)) else fnGetFitness(donorGenes)

    for i in range(1,11):

        genes[i][0], donorGenes[i][0] = donorGenes[i][0], genes[i][0]
        childGenes = genes if (fnGetFitness(genes) > fnGetFitness(donorGenes)) else donorGenes

        if fnGetFitness(childGenes) > initialFitness:
            return childGenes
        donorGenes[i][0], genes[i][0] = genes[i][0], donorGenes[i][0]
    return genes

class ResourceAllocationTest(unittest.TestCase):
    geneSet = "01"

    def test_solve(self):
        numberOfTask = 10
        arrayOfDependencies = load_task_dependency("resource.ra")
        arrayOfDuration = load_task_duration("duration.ra")

        def fnGenerateGenes(length, geneSet):
            return generate_genes(numberOfTask, geneSet, arrayOfDependencies,
                                arrayOfDuration)

        def fnCreate():
            return random.sample(geneset, len(geneset))

        def fnDisplay(candidate):
            display(candidate, startTime)

        def fnGetFitness(genes):
            return get_fitness_of_duration(genes,numberOfTask, arrayOfDependencies, 
                            arrayOfDuration)

        def fnMutate(genes, bestParent):
            return mutate(genes, fnGetFitness, arrayOfDependencies, arrayOfDuration, bestParent)

        def fnCrossover(genes, donor):
            return crossover(genes, donor, fnGetFitness)

        startTime = datetime.datetime.now()
        best = genetic.get_best(fnGenerateGenes, fnGetFitness, 10, None, self.geneSet,
                                fnDisplay, fnMutate, fnCreate, maxAge=500,
                                poolSize=70, crossover=fnCrossover)

def load_task_duration(localFileName):
    with open(localFileName, mode='r') as infile:
        content = infile.read().splitlines()
    durationOfTask = {}
    for row in content:
        if row[0] != ' ':  # HEADERS
            continue
        if row == " EOF":
            break

        id, x = row.split(' ')[1:3]
        durationOfTask[int(id)] = int(x)
    return durationOfTask
    
def load_task_dependency(localFileName):
    with open(localFileName, mode='r') as infile:
        content = infile.read().splitlines()
    arr = []
    for row in content:
        if row[0] != ' ':  # HEADERS
            continue
        if row == " EOF":
            break

        x, y = row.split(' ')[1:3]
        arr.append([int(x), int(y)])
    return arr


class Fitness:
    def __init__(self, totalDistance):
        self.TotalDistance = totalDistance

    def __gt__(self, other):
        return self.TotalDistance < other.TotalDistance

    def __str__(self):
        return "{:0.2f}".format(self.TotalDistance)

if __name__ == '__main__':
    unittest.main()
