from MutationFunctionInterface import MutationFunction
from defaults import *
from itertools import chain

import random

class NoteSwapMutation(MutationFunction):
     def __init__(self):
         self.noteToSwap = 1

     def mutate(self, melody):
        # Take a random note and shift it up / down
        barIndex = random.randint(0, len(melody.bars) - 1)
        bar = melody.bars[barIndex]

        if len(bar.notes) == 1 or len(bar.notes) == 0:
            # Nothing to swap
            return
        elif len(bar.notes) == 2:
            # We can only swap one note
            noteIndex = 0
        else:
            # Choose a random note in the bar to swap
            noteIndex = random.randint(0, len(bar.notes) - 2)

        tmpNote = bar.notes[noteIndex + 1]
        bar.notes[noteIndex+1] = bar.notes[noteIndex]
        bar.notes[noteIndex]   = tmpNote

if __name__ == '__main__':
    from RandomMelodyGenerator import MelodyGenerator
    mg = MelodyGenerator()
    mg.generate()
    melody = mg.melody
    print "Generated melody: "
    print melody.getFeature()

    mutation = NoteSwapMutation()
    mutation.mutate(melody)

    print "Mutated melody: "
    print melody.getFeature()