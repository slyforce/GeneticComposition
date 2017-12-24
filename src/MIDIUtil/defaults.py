PITCH_C = 0
PITCH_Cis = 1
PITCH_D = 2
PITCH_Dis = 3
PITCH_E = 4
PITCH_F = 5
PITCH_Fis = 6
PITCH_G = 7
PITCH_Gis = 8
PITCH_A = 9
PITCH_Ais = 10
PITCH_B = 11
SILENCE = 12

N_PITCHES = 12
N_OCTAVES = 10
DEFAULT_TEMPO = 160

DEF_NUMBER_NOTES = 100
DEF_TICK_STEP_SIZE = 30
MAXIMUM_SEQUENCE_LENGTH = 128

# limit the notes to the range of a standard tuned 24-fret 6-string guitar
# starting from E2 (40) to E7 (88)
MIDI_GUITAR_BEGIN = 40
MIDI_GUITAR_END = 88
MIDI_GUITAR_RANGE = MIDI_GUITAR_END - MIDI_GUITAR_BEGIN + 1

# 24-fret 4-string bass in standard tuning
# starting from E1 (28) to D5 (62)
MIDI_BASS_BEGIN = 28
MIDI_BASS_END = 62
MIDI_BASS_RANGE = MIDI_BASS_END - MIDI_BASS_BEGIN + 1

