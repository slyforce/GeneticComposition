import copy
import operator
import os

from MIDIUtil.MelodyGeneratorFactory import MelodyGeneratorFactory
from MIDIUtil.MelodyWriter import MelodyWriter
from Mutation.Mutator import Mutator
from Evaluation.EvaluatorFactory import Evaluator

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

class MutationBeamSearch:
    def __init__(self,
                 max_iterations=20,
                 beam_size=10,
                 max_expansions=5,
                 model_path='',
                 model_evaluator_path='',
                 output_directory=''):
        self.max_iterations = max_iterations
        self.max_expansions = max_expansions
        self.beam_size = beam_size
        self.output_directory = output_directory

        # Create output file directory if needed
        if not os.path.isdir(self.output_directory):
            os.makedirs(self.output_directory)

        print "Iterations: ", max_iterations
        print "Expansions: ", max_expansions
        print "Beam size:  ", beam_size

        self.mutator = Mutator()
        self.mutator.addPitchMutation()
        #self.mutator.addNoteSwapMutation()
        #self.mutator.addNeuralMutation(model_path=model_path)

        self.regularEvaluator = Evaluator()
        self.regularEvaluator.addNeuralEvaluation(model_evaluator_path)

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
        filename = self.output_directory + '/greedyBeamSearch.iter' + str(iteration) + '.mid'
        print [str(note) for note in melody.notes]
        self.melodyWriter.writeToFile(filename, melody)






























