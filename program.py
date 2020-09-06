from matplotlib import pyplot as plt
import os, sys, random

cityNumbers = []
database = []

class Cities:

  def read(file):
    all = []
    if os.path.isfile(file):
      for line in open(file):
        city = Cities.transfer(line)
        if (Cities.check(city[2])) == False:
          print("Distances can not be negative numbers.")
          return False
          break
        all.append(city)
      return all
    else:
      print("File \""+file+"\" not found.")
      return False
  
  def check(number):
    if (number < 0):
      return False
    else:
      return True
  
  def transfer(line):
    line = line.rstrip('\r\n').split('\t')
    parts = line[0].split(':')
    city = parts[0].split('-')
    distance = parts[1].strip()
    return [str(city[0]), str(city[1]), int(distance)]

  def prepareDatabase():
    global cityNumbers, database
    database = Cities.read(os.path.join(sys.path[0], "data.txt"))
    for city in database:
      if city[0] not in cityNumbers:
        cityNumbers.append(city[0])
      if city[1] not in cityNumbers:
        cityNumbers.append(city[1])

class Chromosome:

  def __init__(self, path=None):
    if path is None:
        self.generatePath()
    else:
        self.path = path
    self.calculateDistance()

  def generatePath(self):
    self.path = random.sample(cityNumbers, len(cityNumbers))

  def mutate(self):
    indices = range(len(self.path))
    i1, i2 = random.sample(indices, 2)
    self.path[i1], self.path[i2] = self.path[i2], self.path[i1]
    self.calculateDistance()

  def calculateDistance(self):
    self.totalDistance = 0
    for i in range(len(self.path)-1):
      self.totalDistance += getDistance(self.path[i], self.path[i+1])

def getDistance(first, second):
  for i in range(len(database)):
    if (database[i][0] == first and database[i][1] == second) or (database[i][0] == second and database[i][1] == first):
      return database[i][2]
  return 1000000000

def printPopulation(population):
	for pop in population:
		print("Path: ", pop.path, " Total Distance: ", pop.totalDistance)

def crossover(c1, c2):
    crossoverPoint = random.randint(1, len(cityNumbers)-1)
    offspring = []
    for i in range(crossoverPoint):
        offspring.append(c1.path[i])
    for i in range(crossoverPoint, len(cityNumbers)):
        offspring.append(c2.path[i])
    for i in range(len(offspring)):
        if offspring.count(offspring[i]) > 1:
            offspring[i] = findUniqueNumber(offspring)
    return offspring

def findUniqueNumber(path):
    numbers = list(set(cityNumbers) - set(path))
    return numbers[0]

def createOffspringAndReplaceWorst(population):
	offspringPath = crossover(population[0], population[1])
	offspring = Chromosome(offspringPath)
	population[-1] = offspring

def mutateAllPopulation(population):
    for pop in population:
        pop.mutate()

def main():
    Cities.prepareDatabase()
    populationSize = int(input("Please enter the population size: "))
    population = []
    for i in range(populationSize):
        population.append(Chromosome())
    print("Initial population:")
    printPopulation(population)
    noOfGenerations = int(input("Please enter the total number of generations: "))
    for i in range(noOfGenerations):
        population = sorted(population, key=lambda x: x.totalDistance)
        print("Sorting the ", i+1, "th generation based on total distances...")
        printPopulation(population)
        print("Creating offspring and replacing worst solution...")
        createOffspringAndReplaceWorst(population)
        printPopulation(population)
        print("Causing mutations in whole population...")
        mutateAllPopulation(population)
        printPopulation(population)
    print("Ordering final results...")
    population = sorted(population, key=lambda x: x.totalDistance)
    printPopulation(population)
    a = input('Press a key to exit')

main()