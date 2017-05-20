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
    def __init__(self, hidden_layer_size=100, validation_split=0.1,
                 n_epochs=50, n_batches=100):
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

        # The masking layer is the single most important element of the neural network
        # Without it, the weights of the padding values would also be trained
        self.model.add(Masking(mask_value=0, input_shape=(self.maximum_sequence_length, self.feature_length)))
        self.model.add(LSTM(self.hidden_layer_size,
                            input_shape=(self.maximum_sequence_length, self.feature_length),
                            return_sequences=False,
                            unroll=False,
                            consume_less='mem'))
        self.model.add(Dropout(0.7))

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

        if shuffle == True:
            permutation = np.random.permutation(X_train.shape[0])
            X_train = X_train[permutation, :, :]
            y_train = y_train[permutation, :]

        early_stopping = EarlyStopping(monitor='val_loss', patience=5)

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

if __name__ == '__main__':
    import argparse, glob
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=str,
                        help="directory path with midi files to train a net")
    parser.add_argument("name", type=str, default='model',
                        help="name of file for settings + weights")
    parser.add_argument("--epochs", type=int, default=50,
                        help="Number of epochs to train the model for")
    parser.add_argument("--trainingLog", default='', type=str,
                        help='If set, a log of the training and validation loss per epoch will be'
                             'written to the given file.')

    args = parser.parse_args()

    midi_reader = MIDIReader()
    feature_manager = NeuralFeatureManager()
    model_writer = NeuralModelReader()

    target_folder = args.directory
    melodies = []
    for file_name in glob.glob(target_folder + "/*.mid"):
        print "Reading:", file_name
        melodies += midi_reader.read_file(file_name)[0]

    model_trainer = NeuralModelTrainer(n_epochs=args.epochs)
    X_train, y_train = feature_manager.generate_training_data(melodies)
    print "Training on %d samples" % X_train.shape[0]

    model_trainer.train_model(X_train, y_train,
                              log_file=args.trainingLog)

    model_writer.save_model(model_trainer.get_model(), target_folder + '/' + args.name)


    from MIDIUtil.Melody import Melody
    from Note import Note
    import random
    import numpy as np
    from MIDIUtil import MelodyWriter

    melody = Melody()
    notes = []
    notes_features = []
    start_note = Note()
    # start_note.setFromMidiPitch(random.randint(40, 80))
    start_note.setFromMidiPitch(55) # D4

    notes.append(start_note)
    notes_features.append(feature_manager.get_feature_from_note(start_note))
    for i in range(0, 20):
        input = feature_manager.generate_testing_data(notes)

        output = model_trainer.model.predict(input)
        most_likely_output_index = np.argmax(output[-1, :])

        print "Output: ", output[-1,most_likely_output_index], most_likely_output_index

        new_note = Note()
        new_note.setFromMidiPitch(most_likely_output_index)
        if new_note.pitch == notes[-1].pitch:
            new_note.articulated = True

        notes.append(new_note)
        notes_features.append(feature_manager.get_feature_from_note(new_note))

    melody.notes = notes

    w = MelodyWriter.MelodyWriter()
    w.writeToFile('trainingOutput.mid', melody)
