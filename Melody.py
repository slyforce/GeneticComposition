from defaults import *
import numpy as np

class Melody:
    def __init__(self):
        # Tempo of the melody
        self.tempo = DEFAULT_TEMPO

        # The key of the melody
        self.key = PITCH_C

        # The bars in the melody
        self.bars = []

    def setKey(self, pitch):
        self.key = pitch

    def setTempo(self, tempo):
        self.tempo = tempo

    def addBar(self, bar):
        self.bars.append(bar)

    def getFeature(self):
        result = []
        for bar in self.bars:
            result.extend(bar.getFeature())

        result = np.array(result)
        return result

    def getNotes(self):
        notes = []
        for bar in self.bars:
            notes += bar.notes

        return notes

