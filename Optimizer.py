from MelodyWriter import MelodyWriter
from MelodyGeneratorFactory import MelodyGeneratorFactory
from Mutator import Mutator
from Evaluator import Evaluator
from defaults import *

import operator
import time
import numpy as np
import copy


class Optimizer:
    def __init__(self, iterations, population):
        self.iterations = iterations
        self.maxPopulation = population

        self.mutator = Mutator()
        #self.mutator.addPitchMutation()
        #self.mutator.addNoteSwapMutation()
        self.mutator.addNeuralMutation(model_path='training_ironMaiden/model-300it-200h')

        self.evaluator = Evaluator()
        #self.evaluator.addScaleEvaluator()
        #self.evaluator.addSilenceEvaluator()
        #self.evaluator.addOnBeatEvaluation()
        #self.evaluator.addNoteDistanceEvaluation()
        self.evaluator.addNeuralEvaluation('training_ironMaiden/model-300it-200h')

        self.melodyWriter = MelodyWriter()

        #self.melodyGenerator = MelodyGeneratorFactory.create_random_melody_generator()
        #self.melodyGenerator = MelodyGeneratorFactory.create_file_melody_generator()
        #self.melodyGenerator.load_from_directory('training_ironMaiden')
        self.melodyGenerator = MelodyGeneratorFactory.create_flatline_melody_generator()

        self.bestMelody = None
        self.bestMelodyScore = 2**32

    def optimize(self):
        print "Population size:", self.maxPopulation
        print "Number of total iterations:", self.iterations

        self.population = {}

        for i in range(0, self.maxPopulation):
            self.melodyGenerator.generate()
            self.population[self.melodyGenerator.melody] = self.evaluator.evaluate(self.melodyGenerator.melody)

        for iteration in range(0, self.iterations):
            # Progress output
            if iteration % 1 == 0:
                bestMelodyScore = min(self.population.iteritems(), key=operator.itemgetter(1))[1]
                print "Current iteration", iteration, "best score:", bestMelodyScore

            # Apply mutations
            self.mutatePopulation()

            # Let the melody generator decide whether a portion of the population should
            # or should not be replaced
            self.melodyGenerator.replace(self.population)
            self.evaluatePopulation()
            self.saveBestMelody()


    def mutatePopulation(self):
        bestMelody = min(self.population.iteritems(), key=operator.itemgetter(1))[0]
        for melody, score in self.population.items():
            # if melody == bestMelody:
                # Do not mutate the best melody to guarantee monotonicity
                #continue

            self.mutator.mutateMelody(melody)
            self.population[melody] = self.evaluator.evaluate(melody)

    def evaluatePopulation(self):
        for melody, score in self.population.items():
            if score <= 0.:
                self.population[melody] = self.evaluator.evaluate(melody)

    def outputBestMelody(self):
        sortedPopulation = sorted(self.population.items(), key=operator.itemgetter(1), reverse=False)

        print "Score of the best melody at the end of the optimization:", sortedPopulation[0][1]
        print "Score of the best melody seen in optimization:          ", self.bestMelodyScore
        self.melodyWriter.writeToFile("best.mid", sortedPopulation[0][0])
        self.melodyWriter.writeToFile("overallBest.mid", self.bestMelody)

    def saveBestMelody(self):
        bestMelodyAndScore = min(self.population.iteritems(), key=operator.itemgetter(1))
        if bestMelodyAndScore[1] < self.bestMelodyScore:
            self.bestMelodyScore = bestMelodyAndScore[1]
            self.bestMelody = copy.copy(bestMelodyAndScore[0])


if __name__ == '__main__':
    opt = Optimizer(30, 20)

    start_time = time.clock()
    opt.optimize()
    print "Optimization took: %f seconds" % ((time.clock() - start_time))

    opt.outputBestMelody()
