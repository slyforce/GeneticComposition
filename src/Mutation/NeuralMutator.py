import random

import numpy as np

from Mutation.MutationFunctionInterface import MutationFunction
from Training.NeuralFeatureManager import NeuralFeatureManager
from Training.NeuralModelReader import NeuralModelReader
from MIDIUtil.defaults import *


class NeuralMutation(MutationFunction):
    def __init__(self, model_path=''):

        # how many outputs are considered for mutation
        self.sample_number = 2

        # Number of pitches to mutate
        self.number_pitch_changes = 2

        # object to retrieve sequences to feed into the neural model
        self.feature_manager = NeuralFeatureManager()

        # neural model for mutation selection
        self.load_model(model_path)

        print "Neural mutation settings:"
        print "Number of notes mutated:", self.number_pitch_changes
        print "Range of choice:", self.sample_number

    def mutate(self, melody):
        notes = melody.notes

        for iter in range(0, self.number_pitch_changes):
            # Pick a random note in the melody
            note_index = random.randint(0, len(notes)-1)

            # generate model input and evaluate
            input = self.feature_manager.generate_input_from_sequence(notes[0:note_index])
            output = self.model.predict(input)

            # sort the output as to have access to the highest probabilities
            sorted_output = list(reversed(np.argsort(output[0, :], kind='quicksort')))
            sampling_idx = random.randint(0, self.sample_number-1)

            #print "Sum of most likely tones:", np.sum(output[0, sorted_output[0:self.sample_number]])
            # Modify the note accordingly
            if sorted_output[sampling_idx] >= N_OCTAVES * N_PITCHES:
                notes[note_index].pitch = SILENCE
                notes[note_index].octave = 0
            else:
                notes[note_index].setFromMidiPitch(sorted_output[sampling_idx])

            if note_index == 0:
                notes[0].articulated = False
            else:
                if notes[note_index-1].pitch == notes[note_index].pitch and \
                   notes[note_index-1].octave == notes[note_index].octave:
                    notes[note_index].articulated = True
                else:
                    notes[note_index].articulated = False

    def load_model(self, file):
        model_reader = NeuralModelReader()
        self.model = model_reader.load_model(file)
