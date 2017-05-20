import copy
import glob
import random

from MIDIReader import MIDIReader
from MIDIUtil.MelodyGeneratorFactory import MelodyGenerator
from Training import NeuralFeatureManager
from defaults import *


class MelodyGeneratorFromFile(MelodyGenerator):
    def __init__(self):
        self.melodies = []
        self.midi_reader = MIDIReader()

    def generate(self):
        idx = random.randint(0, len(self.melodies)-1)

        # Return a copy of the melody since the optimizer may apply mutations to it
        return copy.copy(self.melodies[idx])

    def load_from_directory(self, dir_name):
        for file_name in glob.glob(dir_name + "/*.mid"):
            print "Reading: ", file_name
            self.melodies += self.midi_reader.read_file(file_name)[0]

        self.melodies = NeuralFeatureManager.split_melodies(self.melodies, DEF_NUMBER_NOTES)


    def replace(self, melody_scores_dict):
        return melody_scores_dict