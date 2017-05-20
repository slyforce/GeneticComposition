from keras.models import model_from_json

class NeuralModelReader:
    def load_model(self, file):

        if file == '':
            print "Cannot read file", file
            return

        # load json and create model
        with open(file + '.json', 'r') as json_file:
            loaded_model_json = json_file.read()

        loaded_model = model_from_json(loaded_model_json)

        # load weights into new model
        loaded_model.load_weights(file + ".h5")

        return loaded_model

    def save_model(self, model, file):
        # serialize model to JSON
        model_json = model.to_json()
        with open(file + ".json", "w") as json_file:
            json_file.write(model_json)

        # serialize weights to HDF5
        model.save_weights(file + ".h5")