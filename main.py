import csv
import sys
import numpy as np
from numpy import size
from os.path import expanduser,abspath
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame, QStackedWidget, QWidget, QPushButton, QLineEdit,\
    QFileDialog,QLabel,QTextEdit,QVBoxLayout,QScrollArea,QRadioButton
from PyQt5.uic import loadUi
from PyQt5.QtGui import QDoubleValidator, QValidator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class ScorepochsApp(QMainWindow):
    def __init__(self):
        super(ScorepochsApp, self).__init__()
        loadUi('qt_tesi.ui', self)
        self.data_proc = Data_Processing()
        self.Windows = self.findChild(QFrame, 'windows_frame')
        self.Menu_frame = self.findChild(QFrame, 'menu_frame')
        self.windows_StackedWidget = self.findChild(QStackedWidget, 'windows_StackedWidget')
        self.data_page = self.Windows.findChild(QWidget, 'data_page')
        self.plot_page = self.Windows.findChild(QWidget, 'plot_result_page')
        self.start_page = self.Windows.findChild(QWidget, 'start_page')
        self.example_page = self.Windows.findChild(QWidget, 'example_page')
        self.data_frame = self.data_page.findChild(QFrame, 'data_frame')
        self.browse = self.data_frame.findChild(QPushButton, 'browse_button')
        self.filename = self.data_frame.findChild(QLabel, 'filename')
        self.frequency = self.data_frame.findChild(QLineEdit, 'frequency')
        self.error_message_filename = self.data_frame.findChild(QLabel, 'error_message_file')
        self.error_message_frequency = self.data_frame.findChild(QLabel, 'error_message_frequency')
        self.error_message = self.data_frame.findChild(QTextEdit, 'error_message')
        self.add_plot = self.Menu_frame.findChild(QPushButton, 'plot_button')
        self.add_file = self.Menu_frame.findChild(QPushButton, 'addfile_button')
        self.example_button = self.Menu_frame.findChild(QPushButton, 'example_button')
        self.plot_scrollArea = self.Windows.findChild(QScrollArea, 'plot_scrollArea')
        self.widget_scrollArea = self.Windows.findChild(QWidget, 'scrollAreaWidget')
        self.frequency_example = self.Windows.findChild(QLineEdit, 'frequency_example')
        self.time_example = self.Windows.findChild(QLineEdit, 'time_example')
        self.number_channels_example = self.Windows.findChild(QLineEdit, 'number_channels_example')
        self.error_message_channels_example = self.Windows.findChild(QLabel, 'error_message_channels_example')
        self.error_message_frequency_example = self.Windows.findChild(QLabel, 'error_message_frequency_example')
        self.error_message_example = self.Windows.findChild(QLabel, 'error_message_example')
        self.error_message_time_example = self.Windows.findChild(QLabel, 'error_message_time_example')
        self.create_file_button = self.Windows.findChild(QPushButton, 'create_file_button')
        self.browse.clicked.connect(self.browseFile)
        self.add_plot.clicked.connect(self.get_List)
        self.add_file.clicked.connect(self.changepage_addfile)
        self.example_button.clicked.connect(self.changepage_createExample)
        self.create_file_button.clicked.connect(self.create_example)
        self.windows_StackedWidget.setCurrentWidget(self.start_page)
        self.plot_scrollArea.setWidgetResizable(True)
        self.scroll_layout = QVBoxLayout(self.widget_scrollArea)
        self.frequency.editingFinished.connect(self.validating_frequency)
        self.frequency_example.editingFinished.connect(self.validating_frequency_example)
        self.number_channels_example.editingFinished.connect(self.validating_number_channels_example)
        self.time_example.editingFinished.connect(self.validating_time_example)

    def browseFile(self):
        global fname
        home_directory = expanduser('~')
        fname, _ = QFileDialog.getOpenFileNames(self, 'Open file', home_directory, 'CSV Files (*.csv)')
        if fname == []:
            self.error_message_filename.setText('No File Selected')
        else:
            self.error_message.clear()
            self.error_message_filename.clear()
            self.filename.setText(str(fname[0]))
            self.fileselected = str(fname[0])

    def validating_frequency(self):
        self.error_message.clear()
        self.error_message_frequency.clear()
        rule = QDoubleValidator(1, 1000, 0)
        list = rule.validate(self.frequency.text(), 0)
        if list[0] != 2:
            self.error_message_frequency.setText('The frequency can have a value from 1 to 1000 [Hz]')

    def validating_frequency_example(self):
        self.error_message_frequency_example.clear()
        rule = QDoubleValidator(1, 1000, 0)
        list = rule.validate(self.frequency_example.text(), 0)
        if list[0] != 2:
            self.error_message_frequency_example.setText('The frequency can have a value from 1 to 1000 [Hz]\n')

    def validating_number_channels_example(self):
        self.error_message_channels_example.clear()
        rule = QDoubleValidator(1, 64, 0)
        list = rule.validate(self.number_channels_example.text(), 0)
        if list[0] != 2:
            self.error_message_channels_example.setText('The number of channels can have a value from 1 to 64\n')

    def validating_time_example(self):
        self.error_message_time_example.clear()
        rule = QDoubleValidator(1, 100, 0)
        list = rule.validate(self.time_example.text(), 0)
        if list[0] != 2:
            self.error_message_time_example.setText(
                'The sampling duration can have a value from 1 to 100 [s]\n')

    def get_List(self):
        self.error_message.clear()
        if str(self.error_message_filename.text()) != '' or str(self.error_message_frequency.text()) != '' or \
                    str(self.frequency.text()) == '' or str(self.filename.text()) == '':
            self.windows_StackedWidget.setCurrentWidget(self.data_page)
            self.error_message.setText('Enter the data correctly')
        else:
            Yarray, Xarray = self.data_proc.csv_File(self.fileselected, int(self.frequency.text()))
            self.plot(Yarray,Xarray)

    def changepage_addfile(self):
        self.windows_StackedWidget.setCurrentWidget(self.data_page)

    def changepage_createExample(self):
        self.windows_StackedWidget.setCurrentWidget(self.example_page)

    def plot(self, y, x):
        self.clear_layout()
        self.canvas = FigureCanvas(Figure())
        toolbar = NavigationToolbar(self.canvas, self)
        container = QWidget()
        lay = QVBoxLayout(container)
        lay.addWidget(toolbar)
        for i in range(len(y)):
            ax = self.canvas.figure.add_subplot(len(y), 1, (i + 1))
            ax.plot(x,y[i])
            ax.title.set_text('channel'+str(i+1))
            ax.title.set_size(8)
            self.canvas.figure.subplots_adjust(0.15, 0.02, 0.82, 0.98, 0, 0.35)
            lay.addWidget(self.canvas)
        self.scroll_layout.addWidget(container)
        container.setMinimumHeight(200 * len(y))
        self.windows_StackedWidget.setCurrentWidget(self.plot_page)

    def clear_layout(self):
        if self.scroll_layout is not None:
            while self.scroll_layout.count():
                item = self.scroll_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    @QtCore.pyqtSlot()
    def create_example(self, signal_frequency=2):
        self.error_message_example.clear()
        if str(self.error_message_frequency_example.text()) == '' and str(self.error_message_time_example.text()) == ''\
                and str(self.error_message_channels_example.text()) == '':
            with open('new.csv', 'w', newline='') as f:
                compile_csv = csv.writer(f)
                for i in range(int(self.number_channels_example.text())):
                    signal_frequency = signal_frequency + (i * 0.2)
                    time_steps = np.arange(0, int(self.time_example.text()), (1 / int(self.frequency_example.text())))
                    y = ((i + 1) * 0.2) * np.sin(2 * np.pi * signal_frequency * time_steps)
                    compile_csv.writerow(y)
        else:
            self.error_message_example.setText('Enter the data correctly')


class Data_Processing:

    def csv_File(self, file_name, frequency):
        Yarray = np.loadtxt(file_name, delimiter = ',')
        Xarray = np.arange(0, size(Yarray[0])/frequency, 1/frequency)
        return Yarray, Xarray

app= QApplication(sys.argv)
scorepochs = ScorepochsApp()
scorepochs.show()
sys.exit(app.exec_())