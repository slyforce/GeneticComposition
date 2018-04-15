from defaults import *
import numpy as np
import midi

class Note:
    def __init__(self, midiPitch=None):

        if midiPitch is None:
            # The pitch of the note
            self.pitch = PITCH_C
            # The octave of the note
            self.octave = 0
        else:
            self.setFromMidiPitch(midiPitch)

        # The length of the note
        self.length = DEF_TICK_STEP_SIZE

        # Whether the note is being played or articulated
        self.articulated = True

    def setFromMidiPitch(self, midiPitch):
        if midiPitch == 120:
            self.octave = 0
            self.pitch = SILENCE
        else:
            self.octave = midiPitch / N_PITCHES
            self.pitch = midiPitch % N_PITCHES

    def getMIDIIndex(self):
        if self.pitch == SILENCE:
            return N_PITCHES * N_OCTAVES
        else:
            return self.octave * N_PITCHES + self.pitch

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
        if self.pitch == SILENCE:
            return "S_" + str(self.octave)
        else:
            return midi.NOTE_NAMES[self.pitch] + "_" + str(self.octave)

    def isSilence(self):
        return self.pitch == SILENCE

class SilenceNote(Note):
    def __init__(self):
        Note.__init__(self)
        self.octave = 0
        self.pitch = SILENCE