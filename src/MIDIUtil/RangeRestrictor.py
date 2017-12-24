from Melody import Melody
from Note import Note, SilenceNote

from defaults import MIDI_GUITAR_BEGIN, MIDI_GUITAR_END
from defaults import MIDI_BASS_BEGIN, MIDI_BASS_END

class RangeRestrictor:
  def restrict(self, melody):
    '''
    Restrict the notes in a melody to be between an implemented range.
    Notes out of this range are mapped to silence.
    :param melody:
      A melody object
    :return:
      A melody object with the replaced notes
    '''

    new_melody = Melody()

    for i, note in enumerate(melody.notes):
      if not self.in_range(note.getMIDIIndex()):
        new_melody.notes.append(SilenceNote())
      else:
        new_melody.notes.append(note)

    return new_melody

  def in_range(self, pitch):
    raise NotImplementedError

class GuitarRangeRestrictor(RangeRestrictor):
  def in_range(self, pitch):
    if MIDI_GUITAR_BEGIN <= pitch and pitch <= MIDI_GUITAR_END:
      return True

    return False

class BassRangeRestrictor(RangeRestrictor):
  def in_range(self, pitch):
    if MIDI_BASS_BEGIN <= pitch and pitch <= MIDI_BASS_END:
      return True

    return False

if __name__ == '__main__':
  melody = Melody()
  melody.notes = [ Note(pitch) for pitch in [10,20,0,40,50,100,150]]

  g_restrictor = GuitarRangeRestrictor()
  g_melody = g_restrictor.restrict(melody)

  print "Old melody:", [ str(note) for note in melody.notes ]
  print "New melody:", [ str(note) for note in g_melody.notes ]