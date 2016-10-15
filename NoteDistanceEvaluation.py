from EvaluationFunctionInterface import EvaluationFunction
from defaults import *

class NoteDistanceEvaluation(EvaluationFunction):
    def __init__(self):
        self.tooShortPenalty = 1
        self.tooLongPenalty = 6

        self.minDistance = 2
        self.maxDistance = 4

    def evaluate(self, melody):
        score = 0

        lastNotePitch = None
        for note in melody.notes:
            currentNotePitch = note.pitch

            if currentNotePitch == SILENCE or lastNotePitch == SILENCE or lastNotePitch == None:
                lastNotePitch = currentNotePitch
                continue

            # TODO: Current a C and B are 11 steps apart. Octaves are NOT considered.
            if abs(currentNotePitch - lastNotePitch) < self.minDistance:
                score += self.tooShortPenalty
            elif abs(currentNotePitch - lastNotePitch) > self.maxDistance:
                score += self.tooLongPenalty

            lastNotePitch = currentNotePitch

        return score

