import copy
import operator
import time

from Evaluation.EvaluatorFactory import EvaluatorFactory
from MIDIUtil.MelodyGeneratorFactory import MelodyGeneratorFactory
from MIDIUtil.MelodyWriter import MelodyWriter
from Mutation.Mutator import Mutator


class Optimizer:
    def __init__(self,
                 iterations=10,
                 population=100,
                 log_each_n_iterations=5):

        self.iterations = iterations
        self.maxPopulation = population
        self.log_each_n_iterations = log_each_n_iterations
        self.factor_of_melody_generations_per_iterations = 0.1

        self.mutator = Mutator()
        self.mutator.addPitchMutation()
        #self.mutator.addNoteSwapMutation()
        #self.mutator.addNeuralMutation(model_path='training_metallica/model')

        # Evaluator that will evaluate the population in each generation
        # Compututionally cheap fitness functions should be used for this object
        self.regularEvaluator = EvaluatorFactory.createRegularEvaluator()
        self.regularEvaluator.addScaleEvaluator()
        #self.evaluator.addSilenceEvaluator()
        #self.evaluator.addOnBeatEvaluation()
        #self.evaluator.addNoteDistanceEvaluation()
        #self.evaluator.addNeuralEvaluation('training_metallica/model')

        # Additional evaluator that only evaluates after a certain number of calls
        # Computationally expensive fitness functions should be called by this object
        # TODO: don't hard code
        self.periodicEvaluator = EvaluatorFactory.createPeriodicEvaluator(10)
        self.periodicEvaluator.addNeuralEvaluation('training_metallica/model')

        self.melodyWriter = MelodyWriter()

        #self.melodyGenerator = MelodyGeneratorFactory.create_random_melody_generator()
        self.melodyGenerator = MelodyGeneratorFactory.create_file_melody_generator()
        self.melodyGenerator.load_from_directory('training_ironMaiden')
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
            self.population[melody] = self.regularEvaluator.evaluate(melody)

    def evaluatePopulation(self):
        self.periodicEvaluator.updateCounter()

        for melody, score in self.population.items():
            new_score = self.regularEvaluator.evaluate(melody)

            # Check if the period evaluator should evaluate
            if self.periodicEvaluator.isReadyToEvaluate():
                new_score += self.periodicEvaluator.evaluate(melody)

            # Set the score of the melody
            self.population[melody] = new_score

        # Reset the counter of the periodic evaluator if it has scored
        if self.periodicEvaluator.isReadyToEvaluate():
            self.periodicEvaluator.iterationCounter = 0

    def outputBestMelody(self):
        sortedPopulation = sorted(self.population.items(), key=operator.itemgetter(1), reverse=False)

        print "Score of the best melody at the end of the optimization:", sortedPopulation[0][1]
        print "Score of the best melody seen in optimization:          ", self.bestMelodyScore
        self.melodyWriter.writeToFile("best.mid", sortedPopulation[0][0])
        self.melodyWriter.writeToFile("overallBest.mid", self.bestMelody)

        for note in sortedPopulation[0][0].notes:
            print note

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
