import copy
import matplotlib.pyplot as plt


class Lab:
    def __init__(self, filename, plot_title, start_light_time, time_light_on, whole_time, start_num=0):
        self.start = start_light_time
        self.time_light_on = time_light_on
        self.whole_time = whole_time
        self.filename = filename
        self.start_num = 0
        if start_num % 2 == 0:
            self.start_num =1

        self.x_data, self.y_data = self.extract_data_from_txt()
        self.plot_title = plot_title

    def extract_data_from_txt(self):
        time_array = []
        pH_array = []
        with open(self.filename) as f:
            lines = f.readlines()
            for line in lines:
                curr_line = line.split()
                if int(curr_line[0]) > 0 and (int(curr_line[0]) + self.start_num) % 2 != 0 and \
                        int(curr_line[0]) < (self.start + self.whole_time*2) * 2:
                    time_array.append((int(curr_line[0])) / 2)
                    pH_array.append(float((curr_line[18])[:-2]))

        return time_array, pH_array

    def make_plot(self):
        fig, ax = plt.subplots()
        ax.plot(self.x_data, self.y_data)
        plt.xlabel("Time, s")
        plt.ylabel("pH")
        plt.title(self.plot_title)
        plt.axvspan(0, self.whole_time, facecolor="grey", alpha=0.5)
        plt.axvspan(self.start, self.start + self.time_light_on, facecolor="white", alpha=1)
        plt.text(self.start + self.time_light_on * 0.5, min(self.y_data) + (max(self.y_data) - min(self.y_data)) * 0.1,
                 "light on", size=10, bbox=dict(boxstyle="square"))
        plt.text(self.start + self.time_light_on + (self.whole_time - self.time_light_on - self.start) * 0.4,
                 min(self.y_data) + (max(self.y_data) - min(self.y_data)) * 0.1, "light off", size=10,
                 bbox=dict(boxstyle="square"))
        plt.show()

