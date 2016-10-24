from MutationFunctionInterface import MutationFunction
from defaults import *
from itertools import chain

import random

class NoteSwapMutation(MutationFunction):
     def __init__(self):
         self.noteToSwap = 1

     def mutate(self, melody):
        # Take a random note and shift it up / down
        noteIndex = random.randint(0, len(melody.notes) - 1)

        if len(melody.notes) == 1 or len(melody.notes) == 0:
            # Nothing to swap
            return
        elif len(melody.notes) == 2:
            # We can only swap one note
            noteIndex = 0
        else:
            # Choose a random note in the bar to swap
            noteIndex = random.randint(0, len(melody.notes) - 2)

        # Swap the notes
        melody.notes[noteIndex], melody.notes[noteIndex+1] = melody.notes[noteIndex+1], melody.notes[noteIndex]

if __name__ == '__main__':
    from RandomMelodyGenerator import MelodyGenerator
    mg = MelodyGenerator()
    mg.generate
    melody = mg.melody
    print "Generated melody: "
    print melody.getFeature()

    mutation = NoteSwapMutation()
    mutation.mutate(melody)

    print "Mutated melody: "
    print melody.getFeature()