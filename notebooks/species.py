import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy



class Species:

    def __init__(self,weights=[]):
        self.fitness = 0
        self.brain = self.create_neuralnetowork(weights)

    def create_neuralnetowork(self,weights):
        if weights == []:
            model = Sequential([
            Dense(units=10, input_shape=(11,), activation="relu", bias_initializer="RandomNormal" ), #first hidden layer
            Dense(units=5, activation="softmax", bias_initializer="RandomNormal") #output
            ])
        else:
            model = Sequential([
            Dense(units=10, input_shape=(11,), activation="relu"), #first hidden layer
            Dense(units=5, activation="softmax") #output
            ])
            model.set_weights(weights)
        return model

    #@tf.function(input_signature=(tf.TensorSpec(shape=[1,11], dtype=tf.int32),))
    def spit_output(self, input_params:list):
        #print(f"input params:{input_params}")
        command_dict = {0:"eat", 1:"move_up", 2:"move_down", 3: "move_right", 4:"move_left"}
        #run neural net and convert input to command
        decisions = self.brain(np.array(input_params).reshape(1,11), training=False)
        #print(f"decisions: {decisions}")
        command_int = decisions.numpy().argmax()
        return command_dict[command_int]

    def set_fitness (self, fitness):
        self.fitness = fitness
