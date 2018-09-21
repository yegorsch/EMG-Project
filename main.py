from Tkinter import *
from collections import deque
from threading import Lock

import myo
import numpy as np
import scipy.signal as sp
from matplotlib import pyplot as plt

from classifier import Classifier
from window import TextWindow


class EmgCollector(myo.DeviceListener):

    def __init__(self, n):
        self.n = n
        self.lock = Lock()
        self.emg_data_queue = deque(maxlen=n)

    def get_emg_data(self):
        with self.lock:
            return list(self.emg_data_queue)

    # myo.DeviceListener

    def on_connected(self, event):
        event.device.stream_emg(True)

    def on_emg(self, event):
        with self.lock:
            self.emg_data_queue.append((event.timestamp, event.emg))


class App(object):

    def __init__(self, listener, classifier=None):
        self.n = listener.n
        self.listener = listener
        self.fig = plt.figure()
        self.axes = [self.fig.add_subplot('81' + str(i)) for i in range(1, 9)]
        [(ax.set_ylim([-100, 100])) for ax in self.axes]
        self.graphs = [ax.plot(np.arange(self.n), np.zeros(self.n))[0] for ax in self.axes]
        plt.ion()

        self.classifier = classifier
        self.classes = {1: "INSIDE", 2: "OUTSIDE", 3:"REST"}


    def update_plot(self):
        emg_data = self.listener.get_emg_data()
        emg_data = np.array([x[1] for x in emg_data]).T
        for g, data in zip(self.graphs, emg_data):
            if len(data) < self.n:
                # Fill the left side with zeroes.
                data = np.concatenate([np.zeros(self.n - len(data)), data])
            data = self.process_data(data)
            g.set_ydata(data)
        plt.draw()

    def process_data(self, data):
        # Rectify
        data = np.absolute(data)
        # Remove mean
        data = data - np.mean(data)
        # Apply fitering
        b, a = sp.butter(4, 0.5, 'low')
        output_signal = sp.filtfilt(b, a, data)
        return output_signal

    def make_prediction(self):
        emg_data = self.listener.get_emg_data()
        emg_data = np.array([x[1] for x in emg_data])
        return self.classifier.predict(emg_data)

    def main(self, root, tw):
        while True:
            self.update_plot()
            plt.pause(1.0 / 30)
            # Update text view
            root.update()
            root.update_idletasks()
            res = self.make_prediction()
            tw.set_text(self.classes[res])


def main():
    myo.init(sdk_path='/Users/egor/Documents/University/myo_sdk')
    hub = myo.Hub()
    listener = EmgCollector(128)
    root = Tk()
    text_window = TextWindow(root)
    with hub.run_in_background(listener.on_event):
        App(listener, Classifier("model_3.sav")).main(root, text_window)


if __name__ == '__main__':
    main()
