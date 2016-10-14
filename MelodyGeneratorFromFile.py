from defaults import *
from MIDIReader import MIDIReader
from MelodyGeneratorFactory import MelodyGenerator

import NeuralFeatureManager
import random
import glob
import copy

class MelodyGeneratorFromFile(MelodyGenerator):
    def __init__(self):
        self.melodies = []
        self.numberBars = DEF_NUMBER_BARS
        self.midi_reader = MIDIReader()

    def generate(self):
        idx = random.randint(0, len(self.melodies)-1)

        # Save the melody as an attribute
        self.melody = copy.copy(self.melodies[idx])

        return self.melody

    def load_from_directory(self, dir_name):
        for file_name in glob.glob(dir_name + "/*.mid"):
            print "Reading: ", file_name
            self.melodies += self.midi_reader.read_file(file_name)[0]

        self.melodies = NeuralFeatureManager.split_melodies(self.melodies, DEF_NUMBER_BARS)


    def replace(self, melody_scores_dict):
        return melody_scores_dict