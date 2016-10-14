from defaults import *
import midi
from Melody import Melody
from Note import Note
from Bar import Bar

from MelodyWriter import MelodyWriter

import operator
class TickInformation:
    def __init__(self, pitch=SILENCE, start_tick=0, end_tick=0):
        self.pitch = pitch
        self.start_tick = start_tick
        self.end_tick = end_tick
        self.played = False

class MIDIReader:
    def __init__(self):
        self.test = None

    def read_file(self, file):
        # Array of Melody objects
        result = []

        pattern = midi.read_midifile(file)

        resolution = pattern.resolution
        note_window = 4. * resolution / SHORTEST_NOTE_LENGTH

        for idx, track in enumerate(pattern):
            new_melody = Melody()
            notes_played = []
            track.make_ticks_abs()
            for event in track:
                if (isinstance(event, midi.NoteOnEvent) or isinstance(event, midi.NoteOffEvent)):
                    if event.data[1] > 0:
                        # We got the duration of the pitch last played
                        tick_information = TickInformation()
                        tick_information.pitch = event.data[0]
                        tick_information.start_tick = event.tick

                    elif event.data[1] == 0:
                        # This gives us the duration of the pitch
                        tick_information.end_tick = event.tick
                        notes_played.append(tick_information)

            melody_notes = []
            last_tick = reversed(track).next().tick
            for i in range(0, last_tick, int(note_window)):
                new_note = Note()
                junk_elements = []

                for tick in notes_played:

                    # We already handled this time point
                    if i >= tick.end_tick:
                        junk_elements.append(tick)

                    if tick.start_tick <= i and i < tick.end_tick:
                        # A note is being played in the time frame
                        new_note.setFromMidiPitch(tick.pitch)
                        melody_notes.append(new_note)

                        # Do not repeat the note if it was already played once before
                        if tick.played == True:
                            new_note.articulated = True

                        tick.played = True
                        break
                    elif i < tick.start_tick:
                        # We have yet to check if there is a note or silence
                        new_note.pitch = SILENCE
                        melody_notes.append(new_note)
                        break

                # Reduce notes played container
                for el in junk_elements:
                    notes_played.remove(el)

            n_notes_per_bar = SHORTEST_NOTE_LENGTH

            if len(melody_notes) < 10:
                print "Too short track. Ignoring it."
                continue

            # Create a barred melody and add it to results
            bar = Bar()
            for i in range(0, len(melody_notes)):

                if i % n_notes_per_bar == 0:
                    # Enough notes per bar
                    new_melody.addBar(bar)
                    bar = Bar()

                # add a note to a bar
                bar.notes.append(melody_notes[i])

            # Add the bar to the melody if not empty
            if len(bar.notes) != 0:
                new_melody.addBar(bar)

            # Finally add the melody to the output
            result.append(new_melody)

        result = self.clean_melodies(result)
        return result, note_window

    def clean_melodies(self, melodies):
        result = []
        for melody in melodies:
            self.remove_silence_bars(melody)
            result.append(melody)

        return result

    def remove_silence_bars(self, melody):

        junk_bars = []
        for bar in melody.bars:

            # If a bar consists of just silence, remove it
            only_silence = True
            for note in bar.notes:
                if note.pitch != SILENCE:
                    only_silence = False
                    break

            if only_silence == True:
                junk_bars.append(bar)

        for bar in junk_bars:
            melody.bars.remove(bar)


if __name__ == '__main__':
    r = MIDIReader()
    song, songResolution = r.read_file('/home/slyforce/src/GeneticComposition/training_chromatic/mary_had_a_little_lamb.mid')

    print "Song has", len(song), "melodies"

    chosenMelody = song[0]

    nNotes = 0
    nSilence = 0.
    for bar in chosenMelody.bars:
        for note in bar.notes:
            nNotes += 1
            if note.pitch == SILENCE:
                nSilence += 1

            # print note.pitch, note.octave

    print "Percentual silence in song: ", (nSilence / nNotes) * 100
    print "Total notes", nNotes

    w = MelodyWriter()
    w.writeToFile('midiReaderTest.mid', chosenMelody, tick_step_size=int(songResolution))