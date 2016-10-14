from EvaluationFunctionInterface import EvaluationFunction
from defaults import *

class ScaleEvaluation(EvaluationFunction):
    def __init__(self):
        self.minorScaleSteps = [2, 1, 2, 2, 1, 2, 2]
        self.outOfScalePenalty = 20

    def evaluate(self, melody):
        score = 0

        # key = melody.key
        key = PITCH_E
        scale = self.getMajorScaleForKey(key)

        for bar in melody.bars:
            for note in bar.notes:
                if not note.pitch in scale:
                    # Punish out of scale notes
                    score += self.outOfScalePenalty

        return score

    def getMajorScaleForKey(self, key):
        currentKey = key

        result = [currentKey]
        for step in self.minorScaleSteps:
            result.append( (result[-1] + step) % 12 )

        return result