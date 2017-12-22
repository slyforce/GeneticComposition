from Evaluation.NeuralEvaluation import NeuralEvaluator

class Evaluator:
    def __init__(self):
        self.evaluators = []

    def evaluate(self, melody):
        score = 0.
        for evaluator in self.evaluators:
            score += evaluator.evaluate(melody)

        return score

    def evaluate_batch(self, melodies):
        score = 0.
        for evaluator in self.evaluators:
            score += evaluator.evaluate_batch(melodies)

        return score

    def addNeuralEvaluation(self, path):
        self.evaluators.append(NeuralEvaluator(path))

