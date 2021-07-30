import copy
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
import scipy.optimize as opt


class Lab:
    def __init__(self, filename, start_light_time, time_light_on, whole_time):
        self.start = start_light_time
        self.time_light_on = time_light_on
        self.whole_time = whole_time
        self.x_data, self.y_data = self.extract_data_from_txt()\
        self.filename = filename

    def extract_data_from_txt(self):
        time_array = []
        pH_array = []
        with open(self.filename) as f:
            lines = f.readlines()
            for line in lines:
                curr_line = line.split()
                if int(lines[0]) > self.start and int(lines[0]) % 2 != 0:
                    time_array.append(int(lines[0]) - 50)
                    pH_array.append(int((lines[19])[:-2]))

        return time_array, pH_array

    def make_plot(self):
        fig, ax = plt.subplots()
        ax.plot(self.x_data, self.y_data)
        plt.xlabel("Time")
        plt.ylabel("pH")
        plt.title("pH test")
        plt.show()


