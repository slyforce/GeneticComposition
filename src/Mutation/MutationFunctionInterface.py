class MutationFunction:
    def __init__(self):
        # The probability that the mutation will be applied a melody
        self.trigger_probability = 1.

    def mutate(self, melody):
        raise NotImplemented