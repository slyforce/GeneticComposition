from keras.callbacks import EarlyStopping
from keras.layers import Dense, Dropout, Activation, Masking
from keras.layers import LSTM
from keras.models import Sequential

from MIDIUtil.MIDIReader import MIDIReader
from Training.NeuralFeatureManager import NeuralFeatureManager
from Training.NeuralModelReader import NeuralModelReader
from MIDIUtil.defaults import *

import numpy as np

class NeuralModelTrainer:
    def __init__(self, hidden_layer_size=500, validation_split=0.1,
                 n_epochs=50, n_batches=30):
        # Model object
        self.model = None

        # The size of the hidden layer for each LSTM layer
        self.hidden_layer_size = hidden_layer_size

        # The possible outputs of the model
        # 12 tones + a silence probability
        self.outputs = N_PITCHES * N_OCTAVES + 1

        # The maximum time sequence for the LSTM network
        self.maximum_sequence_length = MAXIMUM_SEQUENCE_LENGTH

        # Input feature length
        self.feature_length = self.outputs

        # How many batches should be sent to the gpu at once
        self.n_batches = n_batches

        # Number of epochs for training
        self.n_epochs = n_epochs

        # Portion of the training set that is used for validation
        # Percentual number
        self.validation_split = validation_split

        self.setup_model()

    def setup_model(self):
        # Build the model
        self.model = Sequential()

        self.model.add(Masking(mask_value=0, input_shape=(self.maximum_sequence_length, self.feature_length)))
        self.model.add(Dense(200))

        self.model.add(LSTM(self.hidden_layer_size,
                            return_sequences=True,
                            unroll=False,
                            implementation=1))
        self.model.add(Dropout(0.3))
        self.model.add(LSTM(self.hidden_layer_size / 2,
                            input_shape=(self.maximum_sequence_length, self.feature_length),
                            return_sequences=True,
                            unroll=False,
                            implementation=1))
        self.model.add(Dropout(0.3))

        # Output layer
        self.model.add(Dense(self.outputs))
        self.model.add(Activation('softmax'))

        # Debug model information
        print(self.model.summary())

        # Prepare the model
        self.model.compile(loss='categorical_crossentropy',
                           optimizer='rmsprop',
                           metrics=['accuracy'])

    def train_model(self, X_train, y_train,
                    log_file='',
                    shuffle=True):

        early_stopping = EarlyStopping(monitor='val_loss', patience=10)

        training_history = self.model.fit(X_train,
                  y_train,
                  validation_split=self.validation_split,
                  batch_size=self.n_batches,
                  epochs=self.n_epochs,
                  shuffle=shuffle,
                  callbacks=[early_stopping])

        if log_file != '':
            with open(log_file, 'w') as f:
                print training_history.history

                f.write(str(training_history.history))

    def get_model(self):
        return self.model

