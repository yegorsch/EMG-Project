import pickle
from collections import Counter

import numpy as np


class Model:

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
        #print("NARUZHU" if data_counter.most_common(1)[0][0] == 2 else "VNUTR")
        return data_counter.most_common(1)[0][0]

class Classifier:

    def __init__(self, model_name):
        self.model = Model(model_name)

    def predict(self, X_test):
        return self.model.predict(X_test)
