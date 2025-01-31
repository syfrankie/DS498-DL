"""Support Vector Machine (SVM) model."""

import numpy as np


class SVM:
    def __init__(self, n_class: int, lr: float, epochs: int, reg_const: float):
        """Initialize a new classifier.

        Parameters:
            n_class: the number of classes
            lr: the learning rate
            epochs: the number of epochs to train for
            reg_const: the regularization constant
        """
        self.w = None
        self.lr = lr
        self.epochs = epochs
        self.reg_const = reg_const
        self.n_class = n_class

    def calc_gradient(self, X_train: np.ndarray, y_train: np.ndarray) -> np.ndarray:
        """Calculate gradient of the svm hinge loss.

        Inputs have dimension D, there are C classes, and we operate on
        mini-batches of N examples.

        Parameters:
            X_train: a numpy array of shape (N, D) containing a mini-batch
                of data
            y_train: a numpy array of shape (N,) containing training labels;
                y[i] = c means that X[i] has label c, where 0 <= c < C

        Returns:
            the gradient with respect to weights w; an array of the same shape
                as w
        """
        dw = np.zeros((np.shape(X_train)[1], self.n_class))
        for i in range(X_train.shape[0]):
            pred = np.dot(X_train[i], self.w)
            for j in range(self.n_class):
                if j != y_train[i]:
                    temp = max(0, 1 - pred[y_train[i]] + pred[j])
                    if temp != 0:
                        dw[:, j] = np.add(dw[:, j], X_train[i])
                        dw[:, y_train[i]] = np.subtract(dw[:, y_train[i]], X_train[i])
        dw /= X_train.shape[0]
        return dw + self.w * self.reg_const

    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        """Train the classifier.

        Hint: operate on mini-batches of data for SGD.

        Parameters:
            X_train: a numpy array of shape (N, D) containing training data;
                N examples with D dimensions
            y_train: a numpy array of shape (N,) containing training labels
        """
        self.w = np.random.normal(0, .01, size=(np.shape(X_train)[1], self.n_class))
        batch_size = 200
        for _ in range(self.epochs):
            idx = np.sort(np.random.choice(X_train.shape[0],size=batch_size,replace=False))
            dw = self.calc_gradient(X_train[idx], y_train[idx])
            self.w -= self.lr * dw
        

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Use the trained weights to predict labels for test data points.

        Parameters:
            X_test: a numpy array of shape (N, D) containing testing data;
                N examples with D dimensions

        Returns:
            predicted labels for the data in X_test; a 1-dimensional array of
                length N, where each element is an integer giving the predicted
                class.
        """
        pred = np.argmax(np.dot(X_test, self.w), axis = 1)
        return pred
