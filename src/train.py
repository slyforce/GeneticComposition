#!/usr/bin/python

import argparse
import glob
import os

# Training modules
from MIDIUtil.MIDIReader import MIDIReader
from Training.NeuralModelReader import NeuralModelReader
from Training.NeuralModelTrainer import NeuralModelTrainer

# Sample output modules
from Training.NeuralFeatureManager import NeuralFeatureManager
from Search.MutationBeamSearch import MutationBeamSearch

CWD = os.path.dirname(os.path.realpath(__file__))

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

target_folder = CWD + "/" + args.directory
print "Reading from", target_folder
melodies = []
for file_name in glob.glob(target_folder + "/*.mid"):
    print "Reading:", file_name
    melodies += midi_reader.read_file(file_name)[0]

model_trainer = NeuralModelTrainer(n_epochs=args.epochs)
X_train, y_train = feature_manager.generate_training_data(melodies)
print "Training on %d samples" % X_train.shape[0]
if X_train.shape[0] == 0:
    raise ValueError, "Training set empty"

model_trainer.train_model(X_train, y_train,
                          log_file=args.trainingLog)

model_writer.save_model(model_trainer.get_model(),
                        target_folder + '/' + args.name)

print "#####################################"
print "Producing samples from trained model:"
opt = MutationBeamSearch(max_iterations=10,
                       max_expansions=5,
                       beam_size=10,
                       model_path=target_folder + '/' + args.name,
                       model_evaluator_path=target_folder + '/' + args.name,
                       output_directory=target_folder + '/training_samples/')
opt.search()