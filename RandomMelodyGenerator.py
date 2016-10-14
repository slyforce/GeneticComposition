import operator

from Melody import Melody
from Bar import Bar
from Note import Note
from defaults import *

import random
import MelodyGeneratorFactory

class RandomMelodyGenerator(MelodyGeneratorFactory.MelodyGenerator):
    def __init__(self):
        self.melody = None
        self.numberBars = DEF_NUMBER_BARS

    def generate(self):
        self.melody = Melody()
        for i in range(0, self.numberBars):
            bar = self.generateBar()
            self.melody.addBar(bar)

    def generateBar(self):
        bar = Bar()

        # Estimate the max. number of notes based of a 4 by 4 time signature
        maximumNumberOfNotes = int(bar.shortestLength)

        # Decide to play a note or not at random
        playedNotes = [False for i in range(maximumNumberOfNotes)]
        for i in range(0, maximumNumberOfNotes):
            if random.random() > 0.2:
                playedNotes[i] = True

        # Fill the bar with the notes or silence if needed
        for i in range(0, maximumNumberOfNotes):
            if playedNotes[i] == True:
                note = self.generateNote(bar)
            else:
                note = self.generateSilence(bar)

            bar.addNote(note)
        return bar

    def generateNote(self, bar):
        result = Note()

        result.pitch = random.randint(0, N_PITCHES - 1)
        #result.octave = random.randint(0, N_OCTAVES - 1)
        # Melodies with such a high octave range are hard very hard to optimize with simple mutation functions
        result.octave = random.randint(4, 6)
        result.articulated = False
        result.length = bar.shortestLength

        #if len(bar.notes) != 0:
        #    result.pitch = (bar.notes[-1].pitch + 1 ) % 12

        return result

    def generateSilence(self, bar):
        result = Note()

        result.pitch = SILENCE
        result.octave = 0
        result.articulated = False
        result.length = bar.shortestLength

        return result

    def replace(self, melody_scores_dict):
        sortedPopulation = sorted(melody_scores_dict.items(), key=operator.itemgetter(1), reverse=True)
        count = 0
        for melody in sortedPopulation:
            self.generate()
            melody_scores_dict[self.melodyGenerator.melody] = 0.0
            count += 1

            melody_scores_dict.pop(melody[0])
            if count >= len(sortedPopulation) / 2.:
                break

if __name__ == '__main__':
    mg = RandomMelodyGenerator()
    mg.generate()
    print "Generated melody: "
    print mg.melody.getFeature()

    print len(mg.melody.getFeature())
    import MelodyWriter
    mw = MelodyWriter.MelodyWriter()

    mw.writeToFile("test.mid", mg.melody)
    import midi
    print midi.read_midifile("test.mid")