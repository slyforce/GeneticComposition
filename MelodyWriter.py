from defaults import *
import midi

class MelodyWriter:
    def __init__(self):
        self.tempo = DEFAULT_TEMPO

    def getMidiPitch(self, note):
        #return midi.NOTE_VALUE_MAP_SHARP[note.octave * N_PITCHES + note.pitch]
        return note.octave * N_PITCHES + note.pitch

    def writeToFile(self, fileName, melody, tick_step_size=int(4. / SHORTEST_NOTE_LENGTH * DEF_TICK_DURATION)):
        print "Note window size:", tick_step_size
        pattern = midi.Pattern()
        track = midi.Track()

        notes = []
        for bar in melody.bars:
            notes = notes + bar.notes

        nextTickDuration = 0
        nextTickStart = 0
        i = 0
        while i < len(notes):
            note = notes[i]
            #nextTickDuration += step

            if note.pitch != SILENCE and note.articulated == False:
                pitch = self.getMidiPitch(note)
                on = midi.NoteOnEvent(tick=nextTickStart, velocity=127, pitch=pitch)
                track.append(on)

                # Count for the time-frame that the note was played
                nextTickDuration = tick_step_size

                # Count further articulations
                j = i + 1
                while j < len(notes) - 1 and notes[j].articulated == True:
                    nextTickDuration += tick_step_size
                    j += 1

                # Append the end of the note
                pitch = self.getMidiPitch(note)
                off = midi.NoteOffEvent(tick=nextTickDuration, pitch=pitch)
                track.append(off)

                nextTickStart = 0

                # Set i to the new position
                i = j
                continue
            elif note.pitch == SILENCE:
                nextTickStart += tick_step_size

            i += 1

        eot = midi.EndOfTrackEvent(tick=1)
        track.append(eot)

        pattern.append(track)
        midi.write_midifile(fileName, pattern)