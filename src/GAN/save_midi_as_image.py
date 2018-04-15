from MIDIUtil.Melody import Melody
from MIDIUtil.Note import Note
from MIDIUtil.MIDIReader import MIDIReader

from utils import save_image

import numpy as np

reader = MIDIReader()
melody = reader.read_file('/home/miguel/src/GeneticComposition/data/training_test/mary_had_a_little_lamb.mid')[0][0]

image = np.zeros((len(melody.notes), 129), dtype=np.int32)
for i, note in enumerate(melody.notes):
  image[i, note.getMIDIIndex()] = 1

image = image.T

save_image(image, '/home/miguel/src/GeneticComposition/data/training_test/mary_had_a_little_lamb.png')


