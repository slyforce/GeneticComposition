import numpy as np

from MIDIUtil.defaults import *
from MIDIUtil.MIDIReader import MIDIReader

import glob

class Loader:
    def __init__(self, path):
        self.path = path
        self.midi_reader = MIDIReader()
        self.read_melodies()

    def read_melodies(self):
        self.melodies = []
        print self.path + "/*.mid"
        for file_name in glob.glob(self.path + "/*.mid"):
            print "Reading:", file_name
            self.melodies += self.midi_reader.read_file(file_name)[0]

class FeatureManager:
    def __init__(self, feature_length=129):
        self.maximum_sequence_length = MAXIMUM_SEQUENCE_LENGTH

        # includes silence
        self.feature_length = feature_length

        self._index_in_epoch = 0

        self.data = None

    def generate_data(self, melodies):
        # assure that every melody is limited to the maximum sequence length
        splitMelodies = []
        for melody in melodies:
            splitMelodies += melody.splitBasedOnSequenceLength(self.maximum_sequence_length)


        # build the data set
        # BoW-encoding
        data = np.zeros((len(splitMelodies), self.maximum_sequence_length, self.feature_length, 1))
        for melodyIdx, melody in enumerate(splitMelodies):
            for noteIdx, note in enumerate(melody.notes):
                data[melodyIdx, noteIdx, note.getMIDIIndex(), 0] = 1

        self.data = data

        print self.data.shape

        return self.data

    def train_batch(self, n):
        if self._index_in_epoch + n >= self.get_number_samples():

            start1 = self._index_in_epoch
            end1 = self.get_number_samples()
            result1 = self.data[start1:end1,:,:]

            start2 = 0
            end2 = n - (self.get_number_samples() - self._index_in_epoch)
            result2 = self.data[start2:end2,:,:]

            self._index_in_epoch = end2
            result = np.concatenate((result1, result2), axis=0)
        else:
            start = self._index_in_epoch
            end = self._index_in_epoch + n
            self._index_in_epoch += n

            result = self.data[start:end,:,:]

        return result

    def get_number_samples(self):
        return self.data.shape[0]