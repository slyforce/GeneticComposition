from EvaluationFunctionInterface import EvaluationFunction
from defaults import *

class OnBeatEvaluation(EvaluationFunction):
    def __init__(self):
        self.offBeatPenalty = 5

    def evaluate(self, melody):
        print "OnBeatEvaluation function is not implemented yet."
        raise NotImplemented
        return
