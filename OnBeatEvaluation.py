from EvaluationFunctionInterface import EvaluationFunction
from defaults import *

class OnBeatEvaluation(EvaluationFunction):
    def __init__(self):
        self.offBeatPenalty = 5

    def evaluate(self, melody):
        score = 0

        for bar in melody.bars:
            # Assumption: Only works with 4 by 4 signatures
            noteLength = 0
            lastNote = None
            for note in bar.notes:
                if noteLength % bar.shortestLength == 0:
                    # If the note on beat continues a previous silence, then it is punished
                    if note.pitch == SILENCE and lastNote != None and lastNote.pitch == SILENCE:
                        score += self.offBeatPenalty

                noteLength += note.length
                lastNote = note

        return score
