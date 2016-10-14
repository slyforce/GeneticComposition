from defaults import *
import numpy as np

class Bar:
    def __init__(self):

        # Array of notes in the bar
        self.notes = []

        # Shortest length of a note
        self.shortestLength = SHORTEST_NOTE_LENGTH

        # 4 by 4 time signature
        self.signature = 4

    def calculateShortestLength(self):
        """
        Calculates the shortest length of the notes in the bar.
        Currently this does make a difference, as the shortest note length
        is set in the defaults
        """
        result = 1000000

        for i in range(0, len(self.notes)):
            firstNoteLength = self.notes[i].getLength()

            for j in range(i + 1, len(self.notes)):
                secondNoteLength = self.notes[j].getLength()
                gcd = self.greatestCommonDivisor(firstNoteLength, secondNoteLength)
                if gcd < result:
                    result = gcd


        self.shortestLength = result

    def greatestCommonDivisor(self, x, y):
        """
        Calculates the greatest common divisor of two integers
        :param x: Integer
        :param y: Integer
        :return: The greatest common divisor of x and y
        """
        result = 1
        smallerValue = min(x,y)
        for i in range(2, smallerValue + 1):
            if (x % i == 0) and (y % i == 0):
                result = i

        return result

    def addNote(self, note):
        self.notes.append(note)

    def getFeature(self):
        """
        Estimate an array with the features of each note in the bar
        :return:
            Numpy array with the features of each note in the bar
        """
        result = []
        for i, note in enumerate(self.notes):
            result.append(note.getFeature())

        result = np.array(result)
        return result