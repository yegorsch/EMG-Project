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

    def predict(self, emg):
        """
        Takes X_test matrix and performs LDA predict on it.
        :param X_test:
        :return: Most common class value.
        """
        if len(emg) == 0:
            return
        emg = np.array([x[1] for x in emg]).T
        b, a = sp.butter(4, 0.2, 'low')
        filtered_channels = []
        for i in range(8):
            channel_data = emg[:, i]
            filtered_channel = sp.filtfilt(b, a, channel_data)
            filtered_channels.append(filtered_channel)
        for i in range(8):
            emg[:, i] = filtered_channels[i]

        ys = self.model.predict(emg)
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
