import random

from Mutation.MutationFunctionInterface import MutationFunction
from MIDIUtil.defaults import *


class PitchMutation(MutationFunction):
    def __init__(self):
        self.maxPitchChange = 2
        self.number_pitch_changes = 10

        self.maxIterationsBeforeRandomOctaveAssignment = 10

    def mutate(self, melody):
        for iter in range(0, self.number_pitch_changes):
            # Take a random note and shift it up / down
            noteIndex = self.getNoteIndex(melody)
            note = melody.notes[noteIndex]

            # print "Mutating note " + str(noteIndex) + " at bar " + str(barIndex)

            pitchShift = random.randint(-self.maxPitchChange, self.maxPitchChange)
            if pitchShift == 0:
                note.pitch = SILENCE
            else:
                was_silence = note.pitch == SILENCE
                note.pitch = (note.pitch + pitchShift) % 12

                if was_silence:
                    # If the previous pitch was silence then assign the current note the octave of a note
                    # that isn't silence
                    note.octave = self.getNonSilenceNoteOctave(melody)

                # Due to possible octave shifts, it is possible for the pitch + note not to in
                # the allowed range, therefore we correct this by adjusting the octave
                if note.octave == N_OCTAVES:
                    note.octave -= 1

    def getNoteIndex(self, melody):
        noteIndex = random.randint(0, len(melody.notes) - 1)
        if len(melody.notes) == 0:
            # Nothing to mutate
            assert "Empty melody at PitchMutation"
        elif len(melody.notes) == 1:
            # We can only mutate one note
            noteIndex = 0
        else:
            # Choose a random note in the bar to mutate
            noteIndex = random.randint(0, len(melody.notes) - 1)
        return noteIndex

    def getNonSilenceNoteOctave(self, melody):
        for i in range(0, self.maxIterationsBeforeRandomOctaveAssignment):
            idx = self.getNoteIndex(melody)
            if melody.notes[idx].pitch != SILENCE:
                return melody.notes[idx].octave

        return random.randint(0, N_OCTAVES-1)


if __name__ == '__main__':
    from RandomMelodyGenerator import RandomMelodyGenerator
    mg = RandomMelodyGenerator()
    melody = mg.generate()
    print "Generated melody: "
    print melody.getFeature()

    mutation = PitchMutation()
    mutation.mutate(melody)

    print "Mutated melody: "
    print melody.getFeature()