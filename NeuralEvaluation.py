from EvaluationFunctionInterface import EvaluationFunction
from defaults import *
import copy
from NeuralModelReader import NeuralModelReader
from NeuralFeatureManager import NeuralFeatureManager
from keras.preprocessing import sequence as keras_sequence

import numpy as np


class NeuralEvaluator(EvaluationFunction):
    def __init__(self, input_model_path):

        # Load a pre-trained model from the file system
        model_reader = NeuralModelReader()
        self.model = model_reader.load_model(input_model_path)

        self.feature_manager = NeuralFeatureManager()

    def evaluate(self, melody):
        notes = []
        for bar in melody.bars:
            notes += bar.notes

        X_set, y_set = self.feature_manager.generate_training_data([melody])

        output = self.model.predict(X_set,
                                    batch_size=50,
                                    verbose=0)

        score = 0.
        for sample_index in range(0, len(notes)):
            following_note_index = np.argmax(y_set[sample_index, :])
            score += - np.log( output[sample_index, following_note_index] )

        return score

