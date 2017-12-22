import numpy as np

from Evaluation.EvaluationFunctionInterface import EvaluationFunction
from Training.NeuralFeatureManager import NeuralFeatureManager
from Training.NeuralModelReader import NeuralModelReader

from MIDIUtil.defaults import *

class NeuralEvaluator(EvaluationFunction):
    def __init__(self, input_model_path):

        # Load a pre-trained model from the file system
        model_reader = NeuralModelReader()
        self.model = model_reader.load_model(input_model_path)

        self.feature_manager = NeuralFeatureManager()

    def evaluate(self, melody):
        notes = melody.notes
        X_set, y_set = self.feature_manager.generate_sequential_training_data([melody])

        sample_size = int(np.ceil( float(len(notes)) / MAXIMUM_SEQUENCE_LENGTH))

        output = self.model.predict(X_set,
                                    batch_size=50,
                                    verbose=0)

        score = 0.
        for i in xrange(0, sample_size):
            for j in xrange(0, MAXIMUM_SEQUENCE_LENGTH-1):
                if i * MAXIMUM_SEQUENCE_LENGTH + j >= len(notes):
                    break

                following_note_index = np.argmax(y_set[i, j, :])
                score += - np.log( output[i, j, following_note_index] )



        return score


    def evaluate_batch(self, melodies):
        X_set, y_set = self.feature_manager.generate_sequential_training_data(melodies)



