#!/usr/bin/python

import random

def randomMatrix(n, upperBound, alpha):
    random.seed(alpha) #Generate Random number iterator
    m = []
    for r in range(n):
        sm = []
        m.append(sm)
        for c in range(n):
             sm.append(upperBound * random.random())
    return m


def wrappedPath(path):
    return path[1:] + [path[0]]


def pathLength(place, path):
    pairs = zip(path, wrappedPath(path))   #Returns the tuple of path and Wrapped path 
    return sum([place[r][c] for (r,c) in pairs])


def updatePher(pher, path, beta):
    pairs = zip(path, wrappedPath(path))  #returns tuple of path and Wrapped path
    for (r,c) in pairs:
        pher[r][c] = pher[r][c] + beta


def evaporatePher(pher, maxIter, beta):
    decr = beta / float(maxIter)
    for r in range(len(pher)):
        for c in range(len(pher[r])):
            if pher[r][c] > decr:
                pher[r][c] = pher[r][c] - decr
            else:
                pher[r][c] = 0.0

# Sum weights for all paths to place adjacent to current.
# Matrix * Matrix * CitySet * int -> double
def doSumWeight(place, pher, used, current):
    runningTotal = 0.0
    for city in range(len(place)):
        if not used.has_key(city):
            runningTotal = (runningTotal + 
                            place[current][city] * (1.0 + pher[current][city]))
    return runningTotal

# Returns Total distance between the place with .
def findSumWeight(place, pher, used, current, soughtTotal):
    runningTotal = 0.0
    next = 0
    for city in range(len(place)):
        if runningTotal >= soughtTotal:
            break
        if not used.has_key(city):
            runningTotal = (runningTotal + 
                            place[current][city] * (1.0 + pher[current][city]))
            next = city
    return next

# Matrix * Matrix -> Path
def genPath(place, pher):
    current = random.randint(0, len(place)-1)
    path = [current]
    used = {current:1}
    while len(used) < len(place):
        sumWeight = doSumWeight(place, pher, used, current)
        rndValue = random.random() * sumWeight
        current = findSumWeight(place, pher, used, current, rndValue)
        path.append(current)
        used[current] = 1
    return path

# Matrix * int * int * int ->Path
def bestPath(place, alpha, maxIter, beta):
    pher = randomMatrix(len(place), 0, 0)
    random.seed(alpha)     #Genearating the Random aplha value to avoid stuck in the local maxima
    bestLen = 0.0
    bestPath = []
    for iter in range(maxIter):
        path = genPath(place, pher)
        pathLen = pathLength(place, path)
        if pathLen > bestLen:
            # Remember we are trying to maximize score.
            updatePher(pher, path, beta)
            bestLen = pathLen
            bestPath = path
        evaporatePher(pher, maxIter, beta)
    return bestPath

def main():
    alpha = 1.9
    beta = 0.9
    iter =25
    numplace = 10
    maxDistance = 100
    cityDistancealpha = 1
    print "Checking For optimal Path"
    place = randomMatrix(numplace, maxDistance, cityDistancealpha)
    path = bestPath(place, alpha, iter, beta)
    print path
    print "len = ", pathLength(place, path)

if __name__ == "__main__":
    main()

