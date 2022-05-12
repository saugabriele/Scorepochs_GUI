import csv
import sys
import numpy as np
from numpy import size
from os.path import expanduser,abspath
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QDialog, QFileDialog, QApplication, QMainWindow,QVBoxLayout, QPushButton, QLabel,\
    QLineEdit, QDoubleSpinBox, QComboBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QDoubleValidator, QValidator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class MiApp(QMainWindow):
    def __init__(self):
        super(MiApp, self).__init__()
        loadUi('qt_tesi.ui', self)
        self.min = 0
        self.max = 0
        self.grafica = Canvas_grafica()
        self.data_proc = Data_Processing()
        self.grafica_uno = self.findChild(QVBoxLayout, 'grafica_uno')
        self.browse = self.findChild(QPushButton, 'browse')
        self.filename = self.findChild(QLineEdit, 'filename')
        self.startplot = self.findChild(QPushButton, 'startplot')
        self.number_channels = self.findChild(QLineEdit, 'number_channels')
        self.frequency = self.findChild(QLineEdit, 'frequency')
        self.simulation = self.findChild(QPushButton, 'simulation')
        self.min_time = self.findChild(QLineEdit, 'min_time')
        self.max_time = self.findChild(QLineEdit, 'max_time')
        self.browse.clicked.connect(self.browseFile)
        self.startplot.clicked.connect(self.get_List)
        self.simulation.clicked.connect(self.create_example)
        self.grafica_uno.addWidget(self.grafica)
        self.frequency.editingFinished.connect(self.validating_frequenza)
        self.number_channels.editingFinished.connect(self.validating_number_channels)
        self.min_time.editingFinished.connect(self.validating_min_time)
        self.max_time.editingFinished.connect(self.validating_max_time)

    def browseFile(self):
        global fname
        home_directory = expanduser('~')
        fname, _ = QFileDialog.getOpenFileNames(self, 'Open file', home_directory, 'CSV Files (*.csv)')
        self.filename.setText(str(fname[0]))
        self.fileselected = str(fname[0])

    def validating_frequenza(self):
        rule = QDoubleValidator(1,1000,0)
        list = rule.validate(self.frequency.text(),0)
        if list[0] != 2:
            sys.exit(app.exec_())

    def validating_number_channels(self):
        rule = QDoubleValidator(1, 64, 0)
        list = rule.validate(self.number_channels.text(), 0)
        if list[0] != 2:
            sys.exit(app.exec_())

    def validating_min_time(self):
        rule = QDoubleValidator(-100000, 100000, 5)
        list = rule.validate(self.min_time.text(), 0)
        if list[0] != 2:
            sys.exit(app.exec_())
        string_value = self.min_time.text()
        self.min = float(string_value.replace(',','.'))

    def validating_max_time(self):
        rule = QDoubleValidator(-100000, 100000, 5)
        list = rule.validate(self.max_time.text(), 0)
        if list[0] != 2:
            sys.exit(app.exec_())
        string_value = self.max_time.text()
        self.max = float(string_value.replace(',','.'))

    def get_List(self):
        Yarray , Xarray = self.data_proc.csv_File(self.fileselected, int(self.frequency.text()),
                                                  int(self.number_channels.text()))
        if self.max>=self.min:
            self.grafica.plot(Yarray, Xarray, self.min,self.max)
        else:
            sys.exit(app.exec_())

    def create_example(self):
        with open('new.csv', 'w', newline='') as f:
            compile_csv = csv.writer(f)
            for i in range(int(self.number_channels.text())):
                signal_freq = 2
                time_steps = np.arange(0, 10.01, (1/int(self.frequency.text())))
                y = ((i + 1) * 0.2) * np.sin(2 * np.pi * signal_freq * time_steps)
                compile_csv.writerow(y)
        self.fileselected = str(abspath('new.csv'))
        self.get_List()



class Canvas_grafica(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        FigureCanvas.__init__(self,self.fig)


    def plot(self,array, x, min, max):
        self.fig.clear()
        labels = []
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel('Time')
        for i in range(len(array)):
            self.ax.plot(x,array[i])
            labels.append('channel ' + str(i+1))
        if max!=0:
                self.ax.set_xlim([min, max])
        self.fig.legend(labels)
        self.fig.tight_layout()
        self.draw()

class Data_Processing:

    def csv_File(self, file_name, frequency, number_ch):
        with open(file_name) as f:
            Yarray = []
            Xarray = []
            for j in range(number_ch):
                line = next(f)
                Yarray.append([float(x) for x in line.split(',')])
            for i in range(size(Yarray[0])):
                Xarray.append((1/frequency) * (i + 1))
        return Yarray, Xarray
"""
    def plot_example(self, s_freq):
        signal_freq= 1
        increment = float(signal_freq/s_freq)
        time_steps= np.arange(0, 10.01, increment)
        y = np.sin(2 * np.pi * signal_freq * time_steps)
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel('Time')
        self.ax.set_xlim([0,10.01])
        self.ax.plot(time_steps, y)
        self.fig.tight_layout()
        self.draw()
"""


app= QApplication(sys.argv)
mi_app = MiApp()
mi_app.show()
sys.exit(app.exec_())