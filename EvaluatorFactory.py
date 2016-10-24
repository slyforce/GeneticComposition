from ScaleEvaluation import ScaleEvaluation
from SilenceEvaluation import SilenceEvaluation
from OnBeatEvaluation import OnBeatEvaluation
from NoteDistanceEvaluation import NoteDistanceEvaluation
from NeuralEvaluation import NeuralEvaluator

class Evaluator:
    def __init__(self):
        self.evaluators = []

    def evaluate(self, melody):
        score = 0.
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

class RegularEvaluator(Evaluator):
    def __init__(self):
        Evaluator.__init__(self)
        self.fillerAttribute = None

class PeriodicEvaluator(Evaluator):
    def __init__(self, iterationsUntilEvaluation=100):
        Evaluator.__init__(self)

        self.iterationCounter = 0
        self.maxIterations = iterationsUntilEvaluation

    def evaluate(self, melody):
        if self.iterationCounter == self.maxIterations:
            return Evaluator.evaluate(self, melody)
        else:
            return 0.

    def updateCounter(self):
        self.iterationCounter += 1

    def isReadyToEvaluate(self):
        if self.iterationCounter >= self.maxIterations:
            return True
        else:
            return False

class EvaluatorFactory:
    @staticmethod
    def createRegularEvaluator():
        return RegularEvaluator()

    @staticmethod
    def createPeriodicEvaluator(iterationsUntilEvaluation):
        return PeriodicEvaluator(iterationsUntilEvaluation=iterationsUntilEvaluation)
