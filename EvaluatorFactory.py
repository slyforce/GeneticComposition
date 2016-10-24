from ScaleEvaluation import ScaleEvaluation
from SilenceEvaluation import SilenceEvaluation
from OnBeatEvaluation import OnBeatEvaluation
from NoteDistanceEvaluation import NoteDistanceEvaluation
from NeuralEvaluation import NeuralEvaluator
class Evaluator:
    def __init__(self):
        self.evaluators = []

    def evaluate(self, melody):
        score = 0
        for evaluator in self.evaluators:
            score += evaluator.evaluate(melody)

        return score

    def addScaleEvaluator(self):
        self.evaluators.append(ScaleEvaluation())

    def addSilenceEvaluator(self):
        self.evaluators.append(SilenceEvaluation())

    def addOnBeatEvaluation(self):
        self.evaluators.append(OnBeatEvaluation())

    def addNoteDistanceEvaluation(self):
        self.evaluators.append(NoteDistanceEvaluation())

    def addNeuralEvaluation(self, path):
        self.evaluators.append(NeuralEvaluator(path))
