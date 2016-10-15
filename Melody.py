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

    def setKey(self, pitch):
        self.key = pitch

    def setTempo(self, tempo):
        self.tempo = tempo

