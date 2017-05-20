import random

from MIDIUtil.MelodyGeneratorFactory import MelodyGenerator
from Melody import Melody
from Note import Note
from defaults import *


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
        for j in range(0, DEF_NUMBER_NOTES):
            # Always create a new object
            new_note = Note()
            new_note.pitch = reference_note.pitch
            new_note.octave = reference_note.octave

            if j != 0:
                new_note.articulated = True

            melody.notes.append(new_note)

        return melody
