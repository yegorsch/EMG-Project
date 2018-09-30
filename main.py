from Tkinter import *
from collections import deque
from threading import Lock

import myo
import numpy as np
import scipy.signal as sp
from matplotlib import pyplot as plt

from classifier import Classifier, Regressor
from window import TextWindow

import pyautogui

import json

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

    # def on_orientation(self, event):
    #     with self.lock:
    #         print(event.acceleration)


class App(object):

    def __init__(self, listener, classifier=None, regressor=None, plot=False):

        self.n = listener.n
        self.listener = listener
        self.plot_enable = plot

        if plot:
            self.setup_plot()

        self.classifier = classifier
        self.regressor = regressor

        with open('classes.json') as f:
            data = json.load(f)
            self.bindings = {int(k): v for k,v in data["bindings"].items()}
            self.classes = {int(k): v for k,v in data["classes"].items()}
            self.prev_key = "left"

    def setup_plot(self):
        self.fig = plt.figure()
        self.axes = [self.fig.add_subplot('81' + str(i)) for i in range(1, 9)]
        [(ax.set_ylim([-100, 100])) for ax in self.axes]
        self.graphs = [ax.plot(np.arange(self.n), np.zeros(self.n))[0] for ax in self.axes]
        plt.ion()

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
        plt.pause(1/30.0)

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

    def get_cont_data(self):
        emg_data = self.listener.get_emg_data()
        emg_data = np.array([x[1] for x in emg_data])
        return self.regressor.predict(emg_data)
        

    def main(self, root, tw):
        while True:
            if self.plot_enable:
                self.update_plot()
            cont_data = self.get_cont_data()
            # Update text view
            self.update_tk(root)
            res = self.make_prediction()
            tw.set_text(str(cont_data))
            self.handle_direction(res)

    def update_tk(self, root):
        root.update()
        root.update_idletasks()

    def handle_direction(self, value):
        if value == 3:
            pyautogui.keyUp(self.prev_key)
            self.prev_key = ""
        elif self.bindings[value] != self.prev_key:
            pyautogui.keyUp(self.prev_key)  # Release previous key
            self.prev_key = self.bindings[value]  # Update prev key to new key
            pyautogui.keyDown(self.bindings[value])  # Press new key


def main():
    myo.init(sdk_path='/Users/egor/Documents/University/myo_sdk')
    hub = myo.Hub()
    listener = EmgCollector(48)
    root = Tk()
    text_window = TextWindow(root)
    with hub.run_in_background(listener.on_event):
        App(listener, classifier=Classifier("Models/model_3.sav"), regressor=Regressor("Models/krr2.sav"), plot=False).main(root, text_window)

if __name__ == '__main__':
    main()
