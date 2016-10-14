from PitchMutation import PitchMutation
from NoteSwapMutation import NoteSwapMutation
from NeuralMutator import NeuralMutation
class Mutator:
    def __init__(self):
        # Array of mutation functions
        self.mutations = []

    def mutateMelody(self, melody):
        for mutator in self.mutations:
            mutator.mutate(melody)

    def addPitchMutation(self):
        self.mutations.append(PitchMutation())

    def addNoteSwapMutation(self):
        self.mutations.append(NoteSwapMutation())

    def addNeuralMutation(self, model_path=''):
        self.mutations.append(NeuralMutation(model_path=model_path))
