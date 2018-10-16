import pickle
from collections import Counter
import scipy.signal as sp
import numpy as np


class ClassifierModel:

    def __init__(self, file_name):
        self.model = pickle.load(open(file_name, 'rb'))

    def predict(self, X_test):
        """
        Takes X_test matrix and performs LDA predict on it.
        :param X_test:
        :return: Most common class value.
        """
        if len(X_test) == 0:
            return 3
        y_test = self.model.predict(np.abs(X_test))
        data_counter = Counter(y_test)
        return data_counter.most_common(1)[0][0]

class RegressorModel:

    def __init__(self, file_name):
        self.model = pickle.load(open(file_name, 'rb'))
        self.wind_size = 60

    def filter(self, emg):
        N = len(emg)
        i_start = range(1, N - self.wind_size)
        i_stop = range(self.wind_size, N)
        EMG_av = np.zeros((N - self.wind_size, 8))
        for i in range(N - 5 - self.wind_size):
            sample = np.mean(emg[i_start[i]:i_stop[i], :], axis=0)
            EMG_av[i, :] = sample
        return EMG_av

    def predict(self, emg):
        """
        Takes X_test matrix and performs LDA predict on it.
        :param X_test:
        :return: Most common class value.
        """
        if len(emg) < 16:
            return None
        emg = np.abs(emg)
        if len(emg) < self.wind_size:
            return None
        emg = self.filter(emg)
        ys = self.model.predict(emg)
        # avg = np.mean(ys)
        return ys

class Classifier:

    def __init__(self, model_name):
        self.model = ClassifierModel(model_name)

    def predict(self, X_test):
        return self.model.predict(X_test)

class Regressor:

    def __init__(self, model_name):
        self.model = RegressorModel(model_name)

    def predict(self, X_test):
        return self.model.predict(X_test)
