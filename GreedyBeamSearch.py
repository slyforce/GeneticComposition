from MelodyWriter import MelodyWriter
from MelodyGeneratorFactory import MelodyGeneratorFactory
from Mutator import Mutator
from EvaluatorFactory import EvaluatorFactory

import operator, copy

class Beam:
    def __init__(self,
                 max_size=10):
        self.melodies_and_scores = []
        self.worst_score = 0.
        self.max_size = max_size

    def __str__(self):
        res = ''
        for entry in self.melodies_and_scores:
            melody = entry[0]
            score = entry[1]
            res += str(melody) + ' ' + str(score) + '\n'

        return res

    def add_melody(self, melody, score):
        if score >= self.worst_score and len(self.melodies_and_scores) == self.max_size:
            # Score too bad to enter beam
            return
        else:
            new_entry = (melody, score)
            self.melodies_and_scores.append(new_entry)

            # Remove worst melody if over the beam size
            if len(self.melodies_and_scores) > self.max_size:
                worst_melody = max(self.melodies_and_scores, key=operator.itemgetter(1))
                self.melodies_and_scores.remove(worst_melody)

            # update worst score
            self.worst_score = max(self.melodies_and_scores, key=operator.itemgetter(1))[1]

    def get_best_melody(self):
        return min(self.melodies_and_scores, key=operator.itemgetter(1))[0]

class GreedyBeamSearch:
    def __init__(self,
                 max_iterations=20,
                 beam_size=10,
                 max_expansions=5):
        self.max_iterations = max_iterations
        self.max_expansions = max_expansions
        self.beam_size = beam_size

        print "Iterations: ", max_iterations
        print "Expansions: ", max_expansions
        print "Beam size:  ", beam_size

        self.mutator = Mutator()
        #self.mutator.addPitchMutation()
        #self.mutator.addNoteSwapMutation()
        self.mutator.addNeuralMutation(model_path='training_metallica/model.iter50')

        # Evaluator that will evaluate the population in each generation
        # Compututionally cheap fitness functions should be used for this object
        self.regularEvaluator = EvaluatorFactory.createRegularEvaluator()
        #self.regularEvaluator.addScaleEvaluator()
        #self.evaluator.addSilenceEvaluator()
        #self.evaluator.addOnBeatEvaluation()
        #self.evaluator.addNoteDistanceEvaluation()
        self.regularEvaluator.addNeuralEvaluation('training_metallica/model.iter50')

        self.melodyWriter = MelodyWriter()

        #self.melodyGenerator = MelodyGeneratorFactory.create_random_melody_generator()
        #self.melodyGenerator = MelodyGeneratorFactory.create_file_melody_generator()
        #self.melodyGenerator.load_from_directory('training_ironMaiden')
        self.melodyGenerator = MelodyGeneratorFactory.create_flatline_melody_generator()

    def search(self):
        previous_beam = Beam()

        initial_melody = self.melodyGenerator.generate()
        initial_score = self.regularEvaluator.evaluate(initial_melody)
        previous_beam.add_melody(initial_melody, initial_score)

        self.save_melody(initial_melody, 0)

        for i in range(0, self.max_iterations):
            new_beam = Beam()

            for melody, score in previous_beam.melodies_and_scores:
                for j in range(0, self.max_expansions):
                    new_melody = copy.copy(melody)
                    new_melody.notes = copy.copy(melody.notes)
                    self.mutator.mutateMelody(new_melody)
                    new_score = self.regularEvaluator.evaluate(new_melody)

                    new_beam.add_melody(new_melody, new_score)

            del previous_beam
            previous_beam = new_beam

            #print previous_beam

            self.save_melody(previous_beam.get_best_melody(), i+1)

    def save_melody(self,
                    melody,
                    iteration):
        filename = 'greedyBeamOutputDir/greedyBeamSearch.iter' + str(iteration) + '.mid'
        self.melodyWriter.writeToFile(filename, melody)


if __name__ == '__main__':
    import argparse, time
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=30,
                        help="")
    parser.add_argument("--expansions", type=int, default=5,
                        help="")
    parser.add_argument("--beamSize", type=int, default=10,
                        help="")

    args = parser.parse_args()
    opt = GreedyBeamSearch(max_iterations=args.iterations,
                    max_expansions=args.expansions,
                    beam_size=args.beamSize)

    start_time = time.clock()
    opt.search()
    print "Optimization took: %f seconds" % ((time.clock() - start_time))
































