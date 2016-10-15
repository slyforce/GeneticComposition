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
    def __init__(self,
                 iterations=10,
                 population=100,
                 log_each_n_iterations=5):

        self.iterations = iterations
        self.maxPopulation = population
        self.log_each_n_iterations = log_each_n_iterations
        self.factor_of_melody_generations_per_iterations = 0.3

        self.mutator = Mutator()
        #self.mutator.addPitchMutation()
        #self.mutator.addNoteSwapMutation()
        #self.mutator.addNeuralMutation(model_path='training_ironMaiden/model-300it-200h')

        self.evaluator = Evaluator()
        self.evaluator.addScaleEvaluator()
        #self.evaluator.addSilenceEvaluator()
        #self.evaluator.addOnBeatEvaluation()
        #self.evaluator.addNoteDistanceEvaluation()
        #self.evaluator.addNeuralEvaluation('training_ironMaiden/model-300it-200h')

        self.melodyWriter = MelodyWriter()

        self.melodyGenerator = MelodyGeneratorFactory.create_random_melody_generator()
        #self.melodyGenerator = MelodyGeneratorFactory.create_file_melody_generator()
        #self.melodyGenerator.load_from_directory('training_ironMaiden')
        #self.melodyGenerator = MelodyGeneratorFactory.create_flatline_melody_generator()

        self.bestMelody = None
        self.bestMelodyScore = 2**32

    def optimize(self):
        print "Population size:", self.maxPopulation
        print "Number of total iterations:", self.iterations

        self.population = {}
        self.generatePopulation(self.maxPopulation)

        for iteration in range(0, self.iterations):
            # Progress output
            if iteration % self.log_each_n_iterations == 0 and iteration != 0:
                bestMelodyScore = min(self.population.iteritems(), key=operator.itemgetter(1))[1]
                print "Current iteration", iteration, "best score:", bestMelodyScore

            # Add new members to the population
            # No scores are assigned to the melodies, since they will be mutated in the next step
            # TODO: Don't hard code stuff
            self.generatePopulation( int(self.factor_of_melody_generations_per_iterations * self.maxPopulation) )

            # Apply mutations
            self.mutatePopulation()

            # Score each melody
            self.evaluatePopulation()

            # Remove melodies with bad scores
            self.prunePopulation()

            # Save the best melody at a given iteration,
            # in case the optimization returns worse scores later on
            self.saveBestMelody()

    def prunePopulation(self):
        sortedPopulation = sorted(self.population.items(), key=operator.itemgetter(1), reverse=True)

        for melody, score in sortedPopulation:
            if len(self.population) == self.maxPopulation:
                break
            else:
                self.population.pop(melody)

    def generatePopulation(self, number_of_samples):
        for i in range(0, number_of_samples):
            new_melody = self.melodyGenerator.generate()
            self.population[new_melody] = 0.

            # self.evaluator.evaluate(new_melody)

    def mutatePopulation(self):
        bestMelody = min(self.population.iteritems(), key=operator.itemgetter(1))[0]
        for melody, score in self.population.items():
            if melody == bestMelody:
                # Do not mutate the best melody to guarantee monotonicity
                continue

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
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=10,
                        help="")
    parser.add_argument("--population", type=int, default=100,
                        help="")
    parser.add_argument("--logIteration", type=int, default=1,
                        help="")

    args = parser.parse_args()
    opt = Optimizer(iterations=args.iterations,
                    population=args.population,
                    log_each_n_iterations=args.logIteration)

    start_time = time.clock()
    opt.optimize()
    print "Optimization took: %f seconds" % ((time.clock() - start_time))

    opt.outputBestMelody()
