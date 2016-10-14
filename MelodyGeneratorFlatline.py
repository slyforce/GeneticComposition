from Bar import Bar
from Melody import Melody
from Note import Note
from defaults import *
from MIDIReader import MIDIReader
from MelodyGeneratorFactory import MelodyGenerator

import NeuralFeatureManager
import random
import glob
import copy

class MelodyGeneratorFlatline(MelodyGenerator):
    def __init__(self):
        self.melody = None

    def generate(self):
        pitch = random.randint(0, N_PITCHES - 1)
        octave = random.randint(3, 6)

        reference_note = Note()
        reference_note.pitch = pitch
        reference_note.octave = octave

        melody = Melody()
        for i in range(0, DEF_NUMBER_BARS):
            melody.bars.append(Bar())
            for j in range(0, SHORTEST_NOTE_LENGTH * 4):
                # Always create a new object
                new_note = Note()
                new_note.pitch = reference_note.pitch
                new_note.octave = reference_note.octave

                if i != 0 and j != 0:
                    new_note.articulated = True

                melody.bars[i].notes.append(new_note)

        # Save the melody as an attribute
        self.melody = copy.copy(melody)

        return self.melody

    def replace(self, melody_scores_dict):
        return melody_scores_dict