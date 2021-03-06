from defaults import *
import midi

class MelodyWriter:
    def __init__(self):
        self.tempo = DEFAULT_TEMPO

    def getMidiPitch(self, note):
        return note.octave * N_PITCHES + note.pitch

    def writeToFile(self, fileName, melody, tick_step_size=DEF_TICK_STEP_SIZE):
        pattern = midi.Pattern()
        pattern.resolution = melody.tempo

        track = midi.Track()

        notes = melody.notes

        nextTickStart = 0
        i = 0
        while i < len(notes):
            note = notes[i]

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
