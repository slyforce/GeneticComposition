
'''
Interface class for all melody generators which must implement the generate() function
'''
class MelodyGenerator:
    def __init__(self):
        self.melody = None

    def generate(self):
        raise NotImplemented
        return Melody()


import RandomMelodyGenerator
import MelodyGeneratorFromFile
import MelodyGeneratorFlatline

class MelodyGeneratorFactory:
    @staticmethod
    def create_random_melody_generator():
        return RandomMelodyGenerator.RandomMelodyGenerator()

    @staticmethod
    def create_file_melody_generator():
        return MelodyGeneratorFromFile.MelodyGeneratorFromFile()

    @staticmethod
    def create_flatline_melody_generator():
        return MelodyGeneratorFlatline.MelodyGeneratorFlatline()

