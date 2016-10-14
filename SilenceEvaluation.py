from EvaluationFunctionInterface import EvaluationFunction
from defaults import *

class SilenceEvaluation(EvaluationFunction):
    def __init__(self):
        self.silencePenalty = 1

    def evaluate(self, melody):
        score = 0
        for bar in melody.bars:
            for note in bar.notes:
                if note.pitch == SILENCE:
                    score += self.silencePenalty

        return score
