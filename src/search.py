#!/usr/bin/python

import argparse
import os
from Search.MutationBeamSearch import MutationBeamSearch

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser()
parser.add_argument("--iterations", type=int, default=30,
                    help="")
parser.add_argument("--expansions", type=int, default=5,
                    help="")
parser.add_argument("--beamSize", type=int, default=10,
                    help="")
parser.add_argument("--modelPath", type=str, default='',
                    help="directory path with midi files to train a net")
parser.add_argument("--evaluatorModelPath", type=str, default='',
                    help="directory path with midi files to train a net")
parser.add_argument("--outputDirectory", type=str, default='',
                    help="directory path with midi files to train a net")

args = parser.parse_args()

CWD = os.path.dirname(os.path.realpath(__file__))

opt = MutationBeamSearch(max_iterations=args.iterations,
                       max_expansions=args.expansions,
                       beam_size=args.beamSize,
                       model_path= CWD + '/' + args.modelPath,
                       model_evaluator_path=CWD + '/' + args.evaluatorModelPath,
                       output_directory=CWD + '/' + args.outputDirectory)
opt.search()