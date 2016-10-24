import operator

from Melody import Melody
from Note import Note
from defaults import *

import random
import MelodyGeneratorFactory

class RandomMelodyGenerator(MelodyGeneratorFactory.MelodyGenerator):
    def __init__(self):
        self.melody = None

    def generate(self):
        melody = Melody()
        # Decide to play a note or not at random
        playedNotes = [False for i in range(DEF_NUMBER_NOTES)]
        for i in range(0, DEF_NUMBER_NOTES):
            if random.random() > 0.2:
                playedNotes[i] = True

        # Fill the bar with the notes or silence if needed
        for i in range(0, DEF_NUMBER_NOTES):
            if playedNotes[i] == True:
                note = self.generateNote()
            else:
                note = self.generateSilence()

            melody.notes.append(note)

        return melody

    def generateNote(self):
        result = Note()

        result.pitch = random.randint(0, N_PITCHES - 1)
        # Melodies with such a high octave range are very hard to optimize with simple mutation functions
        result.octave = random.randint(4, 6)
        result.articulated = False

        return result

    def generateSilence(self):
        result = Note()

        result.pitch = SILENCE
        result.octave = 0
        result.articulated = False

        return result

if __name__ == '__main__':
    mg = RandomMelodyGenerator()
    mg.generate
    print "Generated melody: "
    print mg.melody.getFeature()

    print len(mg.melody.getFeature())
    import MelodyWriter
    mw = MelodyWriter.MelodyWriter()

    mw.writeToFile("test.mid", mg.melody)
    import midi
    print midi.read_midifile("test.mid")
