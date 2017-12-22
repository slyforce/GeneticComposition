from defaults import *
import numpy as np

class Melody:
    def __init__(self):
        # Tempo of the melody
        self.tempo = DEFAULT_TEMPO

        # The key of the melody
        self.key = PITCH_C

        # The notes in the melody
        self.notes = []

        # General information to the track stored in the MIDI file
        self.description = ''

    def setKey(self, pitch):
        self.key = pitch

    def setTempo(self, tempo):
        self.tempo = tempo

    def splitBasedOnSequenceLength(self, maxLength):
        result = []

        for i in range(0, len(self.notes)):
            # create new melody object
            if i % maxLength == 0:
                result.append(Melody())

            # append the current note to the most-recent melody
            result[-1].notes.append(self.notes[i])

        # all melodies should have at least one note
        assert(len(result) != 0)

        return result
