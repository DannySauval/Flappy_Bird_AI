import numpy as np
import random

class NeuralNetwork:
    """
        Class to generate a NeuralNetwork.
        One hidden layer.
    """
    calibration = 0.58

    def __init__(self, weights_list):
        self.weights = weights_list
        self.output = 0

    def feedforward(self, x_input):
        """
            Process the feedforward of the NeuralNetwork.
        """
        layer1 = self.sigmoid(np.dot(x_input, self.weights[0]))
        layer2 = self.sigmoid(np.dot(layer1, self.weights[1]))
        # (0.99896684/2) is substracted from layer2 to get a probability of 0.5.
        # I am not really sure about this part and I need to dig a little bit more.
        # self.output = self.sigmoid(layer2-(0.99896684/2))
        self.output = self.sigmoid(layer2-self.calibration)

    def make_decision(self, x_input):
        """
            Make a decision based on the output of the Neural Network.
        """
        self.feedforward(x_input)
        if self.output > 0.5:
            return True
        return False

    def __str__(self):
        return f'{self.output}'

    @staticmethod
    def clsinit():
        mean = 0
        N = 1000

        for i in range(0, N):
            x = np.random.randn(1,4)
            weights = [np.random.rand(4, 7), np.random.rand(7, 1)]
            nn = NeuralNetwork(weights)
            nn.make_decision(x)
            mean += nn.output

        NeuralNetwork.calibration = mean / N

    @staticmethod
    def sigmoid(x_input):
        """
            Sigmoid activation function.
            Mathematical definition of the sigmoid function.
        """
        return 1/(1+np.exp(-x_input))

if __name__ == '__main__':
    mean = 0
    N = 1000

    for i in range(0, N):
        x = np.random.randn(1,4)
        weights = [np.random.rand(4, 7), np.random.rand(7, 1)]
        nn = NeuralNetwork(weights)
        nn.make_decision(x)
        mean += nn.output

    mean /= N

    print(mean)
