import copy

import numpy as np

from MIDIUtil.Melody import Melody
from MIDIUtil.defaults import *
from MIDIUtil.Note import SilenceNote, Note


class NeuralFeatureManager:
    def __init__(self, feature_length=N_PITCHES*N_OCTAVES+1):

        # Length of each feature
        self.feature_length = feature_length

        # Padding of the note sequence for LSTM inputs
        self.maximum_sequence_length = MAXIMUM_SEQUENCE_LENGTH

    def get_feature_from_note(self, note):
        # BoW representation of the pitch being currently played
        out = np.zeros(self.feature_length)

        if note.pitch == SILENCE:
            out[-1] = 1
        else:
            out[N_PITCHES * note.octave + note.pitch] = 1

        return out

    def generate_input_from_sequence(self, note_sequence):
        X_test = np.zeros((1, self.maximum_sequence_length, self.feature_length))

        sequence_start = max(0, len(note_sequence) - self.maximum_sequence_length)
        for sequence_index in range(sequence_start, len(note_sequence)):
            X_test[0, sequence_index - sequence_start, :] = self.get_feature_from_note(note_sequence[sequence_index])

        return X_test

    def generate_testing_data(self, note_sequence):
        X_test = np.zeros((len(note_sequence), self.maximum_sequence_length, self.feature_length))
        for sample_index, note in enumerate(note_sequence):
            sequence_start = max(0, sample_index - self.maximum_sequence_length)
            for sequence_index in range(sequence_start, sample_index):
                X_test[sample_index, sequence_index - sequence_start, :] = self.get_feature_from_note(
                                                                                  note_sequence[sequence_index])


        return X_test

    def generate_sequential_training_data(self, melodies, debug=False):
        notes = []
        for i, melody in enumerate(melodies):
            notes += melody.notes

        sample_size = int(np.ceil( float(len(notes)) / MAXIMUM_SEQUENCE_LENGTH))
        X_train = [ [] for _ in xrange(0, sample_size)]
        y_train = [ [] for _ in xrange(0, sample_size)]

        for i in xrange(0, sample_size):
            for j in xrange(0, MAXIMUM_SEQUENCE_LENGTH-1):
                try:
                    prev_note = notes[i * MAXIMUM_SEQUENCE_LENGTH + j]
                    note = notes[i * MAXIMUM_SEQUENCE_LENGTH + j + 1]

                    X_train[i].append(self.get_feature_from_note(prev_note))
                    y_train[i].append(self.get_feature_from_note(note))
                except:
                    X_train[i].append(np.zeros(self.feature_length))
                    y_train[i].append(np.zeros(self.feature_length))

            try:
                final_note = notes[(i+1) * MAXIMUM_SEQUENCE_LENGTH]
                silence = SilenceNote()
                X_train[i].append(self.get_feature_from_note(final_note))
                y_train[i].append(self.get_feature_from_note(silence))
            except:
                X_train[i].append(np.zeros(self.feature_length))
                y_train[i].append(np.zeros(self.feature_length))

        X_train = np.array(X_train)
        y_train = np.array(y_train)

        assert(X_train.shape == y_train.shape)

        if debug == True:
            print ""
            print "Training content"
            n_silence, n_total = 0, 0
            for i in xrange(0, X_train.shape[0]):
                for j in xrange(0, X_train.shape[1]):
                    note = Note(np.argmax(X_train[i, j, :]))

                    if X_train[i, j, :].sum() == 0:
                        print "*MASK*",
                    else:
                        print str(note),

                    if note.getPitch() == SILENCE:
                        n_silence += 1

                    n_total += 1

            print "Silence vs. non-silence", n_silence, n_total

            print ""
            print "Labels content"
            for i in xrange(0, y_train.shape[0]):
                for j in xrange(0, y_train.shape[1]):
                    note = Note(np.argmax(y_train[i, j, :]))
                    if y_train[i, j, :].sum() == 0:
                        print "*MASK*",
                    else:
                        print str(note),


            print X_train.shape, y_train.shape
        return X_train, y_train


    def generate_training_data(self, melodies):
        # Avoid too long melodies by limiting the number of bars
        # melodies = split_melodies(melodies, DEF_NUMBER_NOTES)

        notes = []
        for i, melody in enumerate(melodies):
            notes += melody.notes

        X_train = np.zeros((len(notes), self.maximum_sequence_length, self.feature_length))
        y_train = np.zeros((len(notes), self.feature_length))

        for sample_index, note in enumerate(notes):
            sequence_start = max(0, sample_index - self.maximum_sequence_length)
            for sequence_index in range(sequence_start, sample_index):
                X_train[sample_index, sequence_index-sequence_start, :] = self.get_feature_from_note(notes[sequence_index])

            y_train[sample_index, :] = self.get_feature_from_note(note)


        #for i in range(0, len(notes)):
        #    print "Sample", str(i)
        #    print "X:",
        #    for j in range(0, self.maximum_sequence_length):
        #        print np.argmax(X_train[i, j, :]),
        #    print "\ny:", np.argmax(y_train[i,:])


        return X_train, y_train

    def generate_stateful_training_data(self, melodies):
        # Splitting is necessary for using states in the sequence neural training
        # Increase the maximum sequence length to include more context
        melodies = split_melodies(melodies, MAXIMUM_SEQUENCE_LENGTH)

        X_train = []
        y_train = []
        for melody in melodies:
            X_train_melody, y_train_melody = self.create_stateful_data_for_melody(melody)
            X_train.append(X_train_melody)
            y_train.append(y_train_melody)

        return X_train, y_train


    def create_stateful_data_for_melody(self, melody):
        X_train = np.zeros((MAXIMUM_SEQUENCE_LENGTH, 1, self.feature_length))
        y_train = np.zeros((MAXIMUM_SEQUENCE_LENGTH, self.feature_length))
        for i in range(1, len(melody.notes)):
            X_train[i - 1, 0, :] = self.get_feature_from_note(melody.notes[i - 1])
            y_train[i - 1, :] = self.get_feature_from_note(melody.notes[i])

        return X_train, y_train



def split_melodies(melodies, max_number_of_notes_per_melody):
    result = []
    new_melody = Melody()
    for melody in melodies:

        for note in melody.notes:
            new_melody.notes.append(note)

            if len(new_melody.notes) >= max_number_of_notes_per_melody:
                result.append(copy.copy(new_melody))
                new_melody = Melody()

    return result
