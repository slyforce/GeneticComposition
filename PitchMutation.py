from MutationFunctionInterface import MutationFunction
from defaults import *
from itertools import chain

import random

class PitchMutation(MutationFunction):
    def __init__(self):
        self.maxPitchChange = 2
        self.number_pitch_changes = 2

    def mutate(self, melody):
        for iter in range(0, self.number_pitch_changes):
            # Take a random note and shift it up / down
            barIndex = random.randint(0, len(melody.bars) - 1)
            bar = melody.bars[barIndex]

            if len(bar.notes) == 0:
                # Nothing to mutate
                continue
            elif len(bar.notes) == 1:
                # We can only mutate one note
                noteIndex = 0
            else:
                # Choose a random note in the bar to mutate
                noteIndex = random.randint(0, len(bar.notes) - 1)

            note = bar.notes[noteIndex]

            # print "Mutating note " + str(noteIndex) + " at bar " + str(barIndex)

            pitchShift = random.randint(-self.maxPitchChange, self.maxPitchChange)
            if pitchShift == 0:
                note.pitch = SILENCE
            else:
                note.pitch = (note.pitch + pitchShift) % 12

                # Due to possible octave shifts, it is possible for the pitch + note not to in
                # the allowed range, therefore we correct this by adjusting the octave
                if note.octave == N_OCTAVES:
                    note.octave -= 1


if __name__ == '__main__':
    from RandomMelodyGenerator import RandomMelodyGenerator
    mg = RandomMelodyGenerator()
    mg.generate()
    melody = mg.melody
    print "Generated melody: "
    print melody.getFeature()

    mutation = PitchMutation()
    mutation.mutate(melody)

    print "Mutated melody: "
    print melody.getFeature()