from defaults import *
import midi
from Melody import Melody
from Note import Note
from Bar import Bar

from MelodyWriter import MelodyWriter

import operator

'''
Helper class to store which pitch is being played a tick time interval
'''
class TickInformation:
    def __init__(self, note=SILENCE, start_tick=0, end_tick=0):
        self.note = note
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
        note_window = DEF_TICK_STEP_SIZE

        for idx, track in enumerate(pattern):
            new_melody = Melody()
            new_melody.setTempo(resolution)
            
            notes_played = []
            track.make_ticks_abs()
            for event in track:
                if (isinstance(event, midi.NoteOnEvent) or isinstance(event, midi.NoteOffEvent)):
                    if event.data[1] > 0:
                        # We got the duration of the pitch last played
                        tick_information = TickInformation()
                        tick_information.note = event.data[0]
                        tick_information.start_tick = event.tick

                    elif event.data[1] == 0:
                        # This gives us the duration of the pitch
                        tick_information.end_tick = event.tick
                        notes_played.append(tick_information)

            new_melody.notes = []
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
                        new_note.setFromMidiPitch(tick.note)
                        new_melody.notes.append(new_note)

                        # Do not repeat the note if it was already played once before
                        if tick.played == True:
                            new_note.articulated = True

                        tick.played = True
                        break
                    elif i < tick.start_tick:
                        # We have yet to check if there is a note or silence
                        new_note.pitch = SILENCE
                        new_melody.notes.append(new_note)
                        break

                # Reduce notes played container
                for el in junk_elements:
                    notes_played.remove(el)

            # Check if the track is too small
            # This can be the case for description tracks
            if len(new_melody.notes) < 10:
                print "Too short track. Ignoring it."
                continue

            result.append(new_melody)

        result = self.clean_melodies(result)

        return result, note_window

    def clean_melodies(self, melodies):
        result = []
        for melody in melodies:
            self.remove_silence_at_start_and_end(melody)
            result.append(melody)

        return result

    def remove_silence_at_start_and_end(self, melody):
        junk_indices = []

        # Accumulate silence at the beginning of the melody
        for i, note in enumerate(melody.notes):
            if note.pitch == SILENCE:
                junk_indices.append(i)
            else:
                break

        # Accumulate silence at the end of the melody
        # TODO: Come up with a better list to iterate...
        for i, note in enumerate(list(reversed(melody.notes))):
            if note.pitch == SILENCE:
                junk_indices.append(i)
            else:
                break

        # Now remove all indices
        # Note that the list must be reversed to be able to pop correctly
        for i in reversed(junk_indices):
            melody.notes.pop(i)



if __name__ == '__main__':
    r = MIDIReader()
    song, songResolution = r.read_file('training_metallica/killers_bass.mid')

    print "Song has", len(song), "melodies"

    chosenMelody = song[0]

    nNotes = 0
    nSilence = 0.
    for note in chosenMelody.notes:
        nNotes += 1
        if note.pitch == SILENCE:
            nSilence += 1

    print "Percentual silence in song: ", (nSilence / nNotes) * 100
    print "Total notes", nNotes

    w = MelodyWriter()
    w.writeToFile('midiReaderTest.mid', chosenMelody, tick_step_size=int(songResolution))