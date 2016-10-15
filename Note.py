from defaults import *
import numpy as np
import midi

class Note:
    def __init__(self):
        # The pitch of the note
        self.pitch = PITCH_C

        # The octave of the note
        self.octave = 0

        # The length of the note
        self.length = DEF_TICK_STEP_SIZE

        # Whether the note is being played or articulated
        self.articulated = False

    def setFromMidiPitch(self, midiPitch):
        self.octave = midiPitch / N_PITCHES
        self.pitch = midiPitch % N_PITCHES

    def getLength(self):
        return self.length

    def getPitch(self):
        return self.pitch

    def getOctave(self):
        return self.octave

    def getFeature(self):
        result = np.array({self.pitch, self.octave})

        return result

    def __str__(self):
        return midi.NOTE_NAMES[self.pitch] + " " + str(self.octave)