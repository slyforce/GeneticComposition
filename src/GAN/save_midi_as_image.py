from MIDIUtil.Melody import Melody
from MIDIUtil.Note import Note
import numpy as np

def save_output_to_file(self, output, filename):
    melody = Melody()
    for i in range(0, output.shape[0]):
        note = Note(midiPitch=np.argmax(output[i, :]))
        melody.notes.append(note)

    self.midi_writer.writeToFile(filename, melody)



