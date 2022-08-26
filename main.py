import csv
import os.path
import sys
import numpy as np
import pandas as pd
import copy
from numpy import size
from os.path import expanduser, abspath
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame, QStackedWidget, QWidget, QPushButton, QLineEdit,\
    QFileDialog, QLabel, QTextEdit, QVBoxLayout, QScrollArea, QCheckBox, QHBoxLayout, QSpinBox, QComboBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QDoubleValidator, QValidator
import plotly.io as pio
from plotly.graph_objs import Layout, Scatter, Figure, Marker, Heatmap,Histogram
from plotly.graph_objs.layout import YAxis, Annotation,Shape
from plotly.graph_objs.layout.annotation import Font
from plotly.subplots import make_subplots
from scipy import signal as sig
from scipy import stats as st
from scorepochs import _spectrum_parameters,scorEpochs

class ScorepochsApp(QMainWindow):
    def __init__(self):
        super(ScorepochsApp, self).__init__()
        loadUi('qt_tesi.ui', self)
        self.data_proc = Data_Processing()
        self.write_html = Write_html()
        self.fig = None
        self.f_len = 0
        self.Windows = self.findChild(QFrame, 'windows_frame')
        self.Menu_frame = self.findChild(QFrame, 'menu_frame')
        self.windows_StackedWidget = self.findChild(QStackedWidget, 'windows_StackedWidget')
        self.data_page = self.Windows.findChild(QWidget, 'data_page')
        self.plot_page = self.Windows.findChild(QWidget, 'plot_result_page')
        self.start_page = self.Windows.findChild(QWidget, 'start_page')
        self.file_created_page = self.Windows.findChild(QWidget, 'file_created_page')
        self.example_page = self.Windows.findChild(QWidget, 'example_page')
        self.plot_settings_page = self.Windows.findChild(QWidget, 'plot_settings_page')
        self.data_frame = self.data_page.findChild(QFrame, 'data_frame')
        self.browse = self.data_frame.findChild(QPushButton, 'browse_button')
        self.fileselected_combobox = self.Windows.findChild(QComboBox, 'fileselected_combobox')
        self.frequency = self.data_frame.findChild(QLineEdit, 'frequency')
        self.error_message_filename = self.data_frame.findChild(QLabel, 'error_message_file')
        self.error_message_frequency = self.data_frame.findChild(QLabel, 'error_message_frequency')
        self.error_message = self.data_frame.findChild(QTextEdit, 'error_message')
        self.plot_results_button = self.Menu_frame.findChild(QPushButton, 'plot_results_button')
        self.add_file = self.Menu_frame.findChild(QPushButton, 'addfile_button')
        self.example_button = self.Menu_frame.findChild(QPushButton, 'example_button')
        self.scorepochs_functions_button = self.Menu_frame.findChild(QPushButton, 'scorepochs_functions_button')
        self.plot_scrollArea = self.Windows.findChild(QScrollArea, 'plot_scrollArea')
        self.widget_scrollArea = self.Windows.findChild(QWidget, 'scrollAreaWidget')
        self.frequency_example = self.Windows.findChild(QLineEdit, 'frequency_example')
        self.time_example = self.Windows.findChild(QLineEdit, 'time_example')
        self.number_channels_example = self.Windows.findChild(QLineEdit, 'number_channels_example')
        self.error_message_channels_example = self.Windows.findChild(QLabel, 'error_message_channels_example')
        self.error_message_frequency_example = self.Windows.findChild(QLabel, 'error_message_frequency_example')
        self.error_message_example = self.Windows.findChild(QLabel, 'error_message_example')
        self.error_message_time_example = self.Windows.findChild(QLabel, 'error_message_time_example')
        self.message_create_file = self.Windows.findChild(QLabel, 'message_create_file')
        self.message_data_processing = self.Windows.findChild(QLabel, 'message_data_processing')
        self.create_file_button = self.Windows.findChild(QPushButton, 'create_file_button')
        self.add_plot = self.Windows.findChild(QPushButton, 'plot_button')
        self.time_dimension_epochs = self.Windows.findChild(QLineEdit, 'time_dimension_epochs')
        self.update_plot_button = self.Windows.findChild(QPushButton, 'update_plot_button')
        self.dimension_epochs_error_message = self.Windows.findChild(QLabel, 'dimension_epochs_error_message')
        self.compute_PSD_button = self.Windows.findChild(QPushButton, 'compute_PSD_button')
        self.compute_corr_matrix_button = self.Windows.findChild(QPushButton, 'compute_corr_matrix_button')
        self.compute_score_vector_button = self.Windows.findChild(QPushButton, 'compute_score_vector_button')
        self.compute_scorepochs_button = self.Windows.findChild(QPushButton, 'compute_scorepochs_button')
        self.min_freqRange = self.Windows.findChild(QLineEdit, 'min_freqRange')
        self.max_freqRange = self.Windows.findChild(QLineEdit, 'max_freqRange')
        self.scorepochs_error_message = self.Windows.findChild(QLabel, 'scorepochs_error_message')
        self.maxfreqRange_error_message = self.Windows.findChild(QLabel, 'maxfreqRange_error_message')
        self.minfreqRange_error_message = self.Windows.findChild(QLabel, 'minfreqRange_error_message')
        self.channels_box = self.Windows.findChild(QSpinBox, 'channels_box')
        self.epochs_box = self.Windows.findChild(QSpinBox, 'epochs_box')
        self.button_freqRange = self.Windows.findChild(QCheckBox, 'button_freqRange')
        self.psd_selection_frame = self.Menu_frame.findChild(QFrame, 'psd_selection_frame')
        self.channel_spinbox = self.Menu_frame.findChild(QSpinBox, 'channel_spinbox')
        self.epoch_spinbox = self.Menu_frame.findChild(QSpinBox, 'epoch_spinbox')
        self.feedback_files = self.Windows.findChild(QLabel, 'feedback_files')
        self.feedback_freq = self.Windows.findChild(QLabel, 'feedback_freq')
        self.epochs_box.setMaximum(0)
        self.epoch_spinbox.setMaximum(0)
        self.browse.clicked.connect(self.browseFile)
        self.add_plot.clicked.connect(self.eeg_plots)
        self.plot_results_button.clicked.connect(self.changepage_PlotResults)
        self.scorepochs_functions_button.clicked.connect(self.changepage_Scorepochs_Functions)
        self.add_file.clicked.connect(self.changepage_addfile)
        self.example_button.clicked.connect(self.changepage_createExample)
        self.create_file_button.clicked.connect(self.create_example)
        self.update_plot_button.clicked.connect(self.update_Plot)
        self.compute_PSD_button.clicked.connect(self.compute_Power_spectrum)
        self.compute_corr_matrix_button.clicked.connect(self.compute_Corr_matrix)
        self.compute_score_vector_button.clicked.connect(self.compute_scoreVector)
        self.compute_scorepochs_button.clicked.connect(self.compute_scorepochs)
        self.windows_StackedWidget.setCurrentWidget(self.start_page)
        self.plot_scrollArea.setWidgetResizable(True)
        self.scroll_layout = QVBoxLayout(self.widget_scrollArea)
        self.frequency.editingFinished.connect(self.validating_frequency)
        self.frequency_example.editingFinished.connect(self.validating_frequency_example)
        self.number_channels_example.editingFinished.connect(self.validating_number_channels_example)
        self.time_example.editingFinished.connect(self.validating_time_example)
        self.time_dimension_epochs.editingFinished.connect(self.validating_time_dimension_epochs)
        self.min_freqRange.editingFinished.connect(self.validating_min_freqRange)
        self.max_freqRange.editingFinished.connect(self.validating_max_freqRange)
        self.button_freqRange.stateChanged.connect(self.set_freqRange)
        self.fileselected_combobox.currentTextChanged.connect(self.new_file_selected)
        self.psd_selection_frame.setVisible(False)
        self.error_message.setReadOnly(True)

    def browseFile(self):
        self.feedback_files.clear()
        self.fileselected_combobox.clear()
        home_directory = expanduser('~')
        self.fname, _ = QFileDialog.getOpenFileNames(self, 'Open file', home_directory, 'CSV Files (*.csv)')
        if self.fname == []:
            if self.fileselected_combobox.currentIndex() == -1:
                self.error_message_filename.setText('No File Selected.')
            else:
                return
        else:
            self.error_message_filename.clear()
            self.feedback_files.setText('Files selected successfully')
            for i in range(len(self.fname)):
                self.fileselected_combobox.insertItem(i, str(self.fname[i]))

    def validating_frequency(self):
        self.error_message_frequency.clear()
        rule = QDoubleValidator(1, 1000, 0)
        list = rule.validate(self.frequency.text(), 0)
        self.feedback_freq.setText('Frequency selected successfully')
        if list[0] != 2:
            self.error_message_frequency.setText('The frequency can have a value from 1 to 1000 [Hz]')
            self.feedback_freq.clear()

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

    def validating_time_dimension_epochs(self):
        self.dimension_epochs_error_message.clear()
        self.scorepochs_error_message.clear()
        if self.fig is None:
            self.dimension_epochs_error_message.setText('First you have to create the plot.')
            self.time_dimension_epochs.clear()
        else:
            if self.time_dimension_epochs.text() != '':
                self.max = (1/int(self.frequency.text())) * (len(self.Yarray[0])-1)
                min = (1/int(self.frequency.text()))
                rule = QDoubleValidator(min, self.max , 10)
                list = rule.validate(self.time_dimension_epochs.text(), 0)
                self.epochs_box.setMinimum(1)
                self.epoch_spinbox.setMinimum(1)
                epLen = round(int(self.time_dimension_epochs.text())*int(self.frequency.text()))
                dataLen = len(self.Yarray[0])
                index = range(0, int(dataLen - epLen + 1), int(epLen + 1))
                self.epochs_box.setMaximum(len(index))
                self.epoch_spinbox.setMaximum(len(index))
                if list[0] != 2:
                    self.dimension_epochs_error_message.setText('Value out of range or incorrect format.[Format ex. "10,00"]')
                    self.epochs_box.setMinimum(0)
                    self.epochs_box.setMaximum(0)
                    self.epoch_spinbox.setMinimum(0)
                    self.epoch_spinbox.setMaximum(0)
            else:
                self.dimension_epochs_error_message.setText('Insert a value.')
                self.epochs_box.setMinimum(0)
                self.epochs_box.setMaximum(0)
                self.epoch_spinbox.setMinimum(0)
                self.epoch_spinbox.setMaximum(0)

    def validating_min_freqRange(self):
        self.minfreqRange_error_message.clear()
        self.scorepochs_error_message.clear()
        rule = QDoubleValidator(1, 40, 0)
        list = rule.validate(self.min_freqRange.text(), 0)
        if list[0] != 2:
            self.minfreqRange_error_message.setText('Min value: Range(1 : 40)')

    def validating_max_freqRange(self):
        self.maxfreqRange_error_message.clear()
        self.scorepochs_error_message.clear()
        rule = QDoubleValidator(1, 40, 0)
        list = rule.validate(self.max_freqRange.text(), 0)
        if list[0] != 2:
            self.maxfreqRange_error_message.setText('Max value: Range(1 : 40)')

    def new_file_selected(self):
        self.fig = None
        self.time_dimension_epochs.clear()
        self.epochs_box.setMinimum(0)
        self.epochs_box.setMaximum(0)
        self.epoch_spinbox.setMinimum(0)
        self.epoch_spinbox.setMaximum(0)
        self.channels_box.setMinimum(0)
        self.channels_box.setMaximum(0)
        self.channel_spinbox.setMinimum(0)
        self.channel_spinbox.setMaximum(0)

    def set_freqRange(self):
       if (self.button_freqRange.isChecked()):
            self.maxfreqRange_error_message.clear()
            self.minfreqRange_error_message.clear()
            self.scorepochs_error_message.clear()
            self.min_freqRange.setText('1')
            self.max_freqRange.setText('40')
            self.min_freqRange.setReadOnly(True)
            self.max_freqRange.setReadOnly(True)
       else:
           self.maxfreqRange_error_message.clear()
           self.minfreqRange_error_message.clear()
           self.scorepochs_error_message.clear()
           self.min_freqRange.setReadOnly(False)
           self.max_freqRange.setReadOnly(False)
           self.min_freqRange.clear()
           self.max_freqRange.clear()

    def eeg_plots(self):
        self.error_message.clear()
        if str(self.error_message_filename.text()) != '' or str(self.error_message_frequency.text()) != '' or \
                    str(self.frequency.text()) == '' or self.fileselected_combobox.currentIndex() == -1:
            self.windows_StackedWidget.setCurrentWidget(self.data_page)
            self.error_message.setText('Enter the data correctly')
        else:
            self.message_data_processing.setText('Data processing...')
            self.message_data_processing.repaint()
            self.Yarray, self.Xarray, self.ch_names= self.data_proc.csv_File(self.fileselected_combobox.currentText(),
                                                                             int(self.frequency.text()))
            self.channels_box.setMaximum(len(self.Yarray))
            self.channels_box.setMinimum(1)
            self.channel_spinbox.setMaximum(len(self.Yarray))
            self.channel_spinbox.setMinimum(1)
            self.epochs_box.setMinimum(0)
            self.epochs_box.setMaximum(0)
            self.epoch_spinbox.setMinimum(0)
            self.epoch_spinbox.setMaximum(0)
            self.fig = self.write_html.create_file_html(self.Yarray, self.Xarray, self.ch_names)
            self.plot()

    def changepage_addfile(self):
        self.windows_StackedWidget.setCurrentWidget(self.data_page)
        self.psd_selection_frame.setVisible(False)

    def changepage_createExample(self):
        self.windows_StackedWidget.setCurrentWidget(self.example_page)
        self.message_create_file.clear()
        self.psd_selection_frame.setVisible(False)

    def changepage_PlotResults(self):
        if self.fig is not None:
            self.error_message.clear()
            self.windows_StackedWidget.setCurrentWidget(self.plot_page)
        else:
            self.windows_StackedWidget.setCurrentWidget(self.data_page)
            self.error_message.setText('First create the figure that displays traces of the M / EEG channels.')

    def changepage_Scorepochs_Functions(self):
        self.message_data_processing.clear()
        self.error_message.clear()
        self.dimension_epochs_error_message.clear()
        self.windows_StackedWidget.setCurrentWidget(self.plot_settings_page)
        self.psd_selection_frame.setVisible(False)
        self.channels_box.setValue(self.channel_spinbox.value())
        self.epochs_box.setValue(self.epoch_spinbox.value())

    def update_Plot(self):
        if str(self.dimension_epochs_error_message.text()) != '':
            return
        else:
            if self.time_dimension_epochs.text() != '':
                    self.write_html.update_Plot(self.time_dimension_epochs.text(),self.frequency.text(),self.Yarray,self.fig)
                    self.psd_selection_frame.setVisible(True)
                    self.plot('update_figure.html')
            else:
                self.dimension_epochs_error_message.setText('First you have to insert the epochs dimension.')

    def compute_Power_spectrum(self):
        if str(self.dimension_epochs_error_message.text()) != '' or self.time_dimension_epochs.text() == '' \
                or self.epochs_box.value() == 0:
            self.scorepochs_error_message.setText('First you have to define the time dimension of each epoch.')
        else:
            self.scorepochs_error_message.clear()
            name_html_file = 'update_figure.html'
            self.write_html.Power_spectrum_html(float(self.time_dimension_epochs.text()),
                                                        int(self.frequency.text()), self.Yarray,
                                                        self.channels_box.value(), self.epochs_box.value())
            self.plot(name_html_file)

    def compute_Corr_matrix(self):
        if self.min_freqRange.text() != '' and self.max_freqRange.text() != '' \
                and int(self.min_freqRange.text()) >= int(self.max_freqRange.text()):
            self.scorepochs_error_message.setText('Min value in frequency is bigger than max value!')
        else:
            if self.scorepochs_error_message.text() == '' and self.minfreqRange_error_message.text() == '' \
                    and self.maxfreqRange_error_message.text() == '' and self.min_freqRange.text() != '' \
                    and self.max_freqRange.text() != '' and self.time_dimension_epochs.text() != ''\
                    and self.dimension_epochs_error_message.text() == '':
                name_html_file = 'update_figure.html'
                self.write_html.Corr_matrix_html(float(self.time_dimension_epochs.text()),
                                                 int(self.frequency.text()), self.Yarray,
                                                 int(self.min_freqRange.text()), int(self.max_freqRange.text()))
                self.plot(name_html_file)
            else:
                self.scorepochs_error_message.setText('Insert value correctly!')
                if self.time_dimension_epochs.text() == '':
                    self.dimension_epochs_error_message.setText('First you have to insert the epochs dimension.')

    def compute_scoreVector(self):
        if self.min_freqRange.text() != '' and self.max_freqRange.text() != '' \
                and int(self.min_freqRange.text()) >= int(self.max_freqRange.text()):
            self.scorepochs_error_message.setText('Min value in frequency is bigger than max value!')
        else:
            if self.scorepochs_error_message.text() == '' and self.minfreqRange_error_message.text() == '' \
                    and self.maxfreqRange_error_message.text()  == '' and self.min_freqRange.text() != '' \
                    and self.max_freqRange.text() != '':
                name_html_file = 'update_figure.html'
                idx_best, epoch, scores, scoreVector = scorEpochs(
                    {'freqRange': [int(self.min_freqRange.text()),int(self.max_freqRange.text())],
                     'fs': int(self.frequency.text()),
                     'windowL': int(self.time_dimension_epochs.text())}, self.Yarray)
                self.write_html.scoreVector_html(scoreVector, self.ch_names)
                self.plot(name_html_file)
            else:
                self.scorepochs_error_message.setText('Insert value correctly!')
                if self.time_dimension_epochs.text() == '':
                    self.dimension_epochs_error_message.setText('First you have to insert the epochs dimension.')

    def compute_scorepochs(self):
        if self.min_freqRange.text() != '' and self.max_freqRange.text() != '' \
                and int(self.min_freqRange.text()) >= int(self.max_freqRange.text()):
            self.scorepochs_error_message.setText('Min value in frequency is bigger than max value!')
        else:
            if self.scorepochs_error_message.text() == '' and self.minfreqRange_error_message.text() == '' \
                    and self.maxfreqRange_error_message.text()  == '' and self.min_freqRange.text() != '' \
                    and self.max_freqRange.text() != '':
                name_html_file = 'update_figure.html'
                idx_best, epoch, scores, scoreVector = scorEpochs(
                    {'freqRange': [int(self.min_freqRange.text()),int(self.max_freqRange.text())],
                     'fs': int(self.frequency.text()),
                     'windowL': int(self.time_dimension_epochs.text())}, self.Yarray)
                self.write_html.scorepochs_html(scores)
                self.plot(name_html_file)
            else:
                self.scorepochs_error_message.setText('Insert value correctly!')
                if self.time_dimension_epochs.text() == '':
                    self.dimension_epochs_error_message.setText('First you have to insert the epochs dimension.')


    @QtCore.pyqtSlot()
    def plot(self , name_html = 'figure.html'):
        self.clear_layout()
        container = QWidget()
        lay = QVBoxLayout(container)
        url = os.path.abspath(name_html)
        webView = QWebEngineView()
        html_map = QtCore.QUrl.fromLocalFile(url)
        webView.load(html_map)
        webView.setFixedWidth(1090)
        webView.setMinimumHeight(730)
        lay.addWidget(webView)
        self.scroll_layout.addWidget(container)
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
            self.message_create_file.setText('Creating the file...')
            self.message_create_file.repaint()
            with open('new.csv', 'w', newline='') as f:
                compile_csv = csv.writer(f)
                for i in range(int(self.number_channels_example.text())):
                    signal_frequency = signal_frequency + (i * 0.2)
                    time_steps = np.arange(0, int(self.time_example.text()), (1 / int(self.frequency_example.text())))
                    y = ((i + 1) * 0.2) * np.sin(2 * np.pi * signal_frequency * time_steps)
                    compile_csv.writerow(y)
            self.windows_StackedWidget.setCurrentWidget(self.file_created_page)
        else:
            self.error_message_example.setText('Enter the data correctly')

class Data_Processing:

    def csv_File(self, file_name, frequency):
        #table=pd.read_csv(file_name ,sep=';',dtype=float,header=None).T
        #Yarray=table.values
        Yarray_pre = np.genfromtxt(file_name, delimiter=';', unpack=True)
        Yarray = np.nan_to_num(Yarray_pre)
        Xarray = np.arange(0, size(Yarray[0])/frequency, 1/frequency)
        Ch_names = []
        for i in range(len(Yarray)):
            ch_name = 'channel ' + str(i+1)
            Ch_names.append(ch_name)
        return Yarray, Xarray, Ch_names

class Write_html:

    def create_file_html(self , Yarray, Xarray, ch_names):
        pio.templates.default = "plotly_white"
        step = 1. / len(Yarray)
        kwargs = dict(domain=[1 - step, 1], showticklabels=False, zeroline=False, showgrid=False)
        layout = Layout(yaxis=YAxis(kwargs), showlegend=False)
        traces = [Scatter(x=Xarray, y=Yarray[0], line=dict(color="#335BFF", width=0.8))]
        for ii in range(1, len(Yarray)):
            kwargs.update(domain=[1 - (ii + 1) * step, 1 - ii * step])
            layout.update({'yaxis%d' % (ii + 1): YAxis(kwargs), 'showlegend': False,
                           'xaxis%d' % (ii + 1): dict(showticklabels=False)})
            traces.append(Scatter(x=Xarray, y=Yarray[ii],
                                       yaxis='y%d' % (ii + 1), line=dict(color="#335BFF", width=0.8)))

        annotations = [Annotation(x=-0.06, y=0, xref='paper', yref='y%d' % (i + 1),
                                       text=ch_name, font=Font(size=9), showarrow=False)
                            for i, ch_name in enumerate(ch_names)]
        layout.update(annotations=annotations)
        layout.update(autosize=False, width=1080, height=565, margin=dict(l=70, r=30, t=35, b=30))
        fig = Figure(data=traces, layout=layout)
        fig.update_layout(xaxis1_showticklabels=True, xaxis1_side="top")
        fig.write_html('figure.html')
        return fig

    def update_Plot(self,time_dimension_epochs, frequency, Yarray, figure):
            i= 0
            x = float(time_dimension_epochs)
            offset = (1/int(frequency))
            max = (1 / int(frequency)) * (len(Yarray[0]) - 1)
            fig = copy.deepcopy(figure)

            while i <= ((max/x)-1):
                fig.add_shape(Shape(type='rect', xref='x', yref='paper',x0=(x*i)+(offset*i), x1=x*(i+1)+(offset*i),
                                    y0 = -0.02, y1 = 1.003))
                fig.layout.shapes[i]['yref'] = 'paper'
                fig.add_annotation(Annotation(x=(x*i + x*(i+1))/2, y=-0.055, yref='paper',
                                                   text=('e'+str(i+1)), font=Font(size=12), showarrow=False))
                i = i+1
            fig.write_html('update_figure.html')


    def Power_spectrum_html(self, time_dimension_epochs, frequency, Yarray, channel, epoch_selected):
        epLen = round(time_dimension_epochs * frequency)
        dataLen = len(Yarray[0])
        idx_ep = range(0, int(dataLen - epLen + 1), int(epLen + 1))
        name_html_file = 'update_figure.html'

        epoch = Yarray[channel-1][idx_ep[epoch_selected-1]:idx_ep[epoch_selected-1] + epLen]
        # compute power spectrum
        f, aux_pxx = sig.welch(epoch.T, fs=frequency, window='hamming', nperseg=round(epLen / 8),
                               detrend=False)

        fig = Figure(data=[Scatter(x=f, y=aux_pxx, line=dict(color="#335BFF", width=0.8))],
                     layout=Layout(title='Channel {c}, epoch {e}:'.format(c =channel, e=epoch_selected),
                                   autosize=False, width=1080, height=540, margin=dict(l=70, r=30, t=35, b=30)))
        fig.update_xaxes(type='log')
        fig.write_html(name_html_file)

    def Corr_matrix_html(self, time_dimension_epochs, frequency, Yarray, min_freqRange, max_freqRange):
        data = []
        ep_name = []
        name_html_file = 'update_figure.html'
        epLen = round(time_dimension_epochs * frequency)
        dataLen = len(Yarray[0])
        nCh = len(Yarray)
        idx_ep = range(0, int(dataLen - epLen + 1), int(epLen + 1))
        nEp = len(idx_ep)
        epoch = np.zeros((nEp, nCh, epLen))
        freqRange = [min_freqRange, max_freqRange]
        for e in range(nEp):
            for c in range(nCh):
                epoch[e][c][0:epLen] = Yarray[c][idx_ep[e]:idx_ep[e] + epLen]
                f, aux_pxx = sig.welch(epoch[e][c].T, fs=frequency, window='hamming', nperseg=round(epLen / 8),
                                       detrend=False)
                if c == 0 and e == 0:  # The various parameters are obtained in the first interation
                    pxx, idx_min, idx_max, nFreq = _spectrum_parameters(f, freqRange, aux_pxx, nEp, nCh)
                pxx[e][c] = aux_pxx[idx_min:idx_max + 1]
            ep_name.append('E%d' % (e + 1))
        pxxXch = np.zeros((nEp, idx_max - idx_min + 1))
        for c in range(nCh):
            for e in range(nEp):
                pxxXch[e] = pxx[e][c]
            score_ch, p = st.spearmanr(pxxXch, axis=1)
            data.append(score_ch)
        fig = Figure()
        fig.add_trace(Heatmap(x=ep_name, y=ep_name[::-1], z=data[0][::-1], showscale=True, zmin=0,
                              zmax=1,colorscale='Viridis',
                              hovertemplate="<br>".join(["x: %{x}","y: %{y}","Score: %{z}<extra></extra>"])))
        fig.update_layout(autosize=False, width=1080, height=560, title = 'Correlation Matrix:', yaxis_scaleanchor="x")
        fig.update_layout(
            updatemenus=[
                {
                    "buttons": [
                        {
                            "label": "channel %d" % (c+1),
                            "method": "update",
                            "args": [{"z": [data[c][::-1]]}]
                        }
                        for c in range(len(data))
                    ],
                    "x": 0.28,
                    "y": 1.18,
                }
            ]
        )
        fig['layout']['xaxis']['constrain'] = 'domain'
        fig.write_html(name_html_file)

    def scoreVector_html(self, scoreVector, ch_names):
        name_html_file = 'update_figure.html'
        ep_name = []
        hover_text = []
        for i in range(len(scoreVector)):
            hover_text.append([])
            for j in range(len(scoreVector[0])):
                hover_text[-1].append('Epoch: {}<br />Score: {}<br />Max value: {}<br />Min value: {}'.format((j + 1),
                                                scoreVector[i][j],np.amax(scoreVector[i]), np.amin(scoreVector[i])))
                if i == 0:
                    ep_name.append('E%d' % (j + 1))
        fig = make_subplots(16, 4, subplot_titles=[ch_name for i, ch_name in enumerate(ch_names)])
        channel = 0
        for i in range(int(len(ch_names)/4)):
            for j in range(4):
                if (j+(i*4)) <= len(ch_names):
                    fig.add_trace(Heatmap(x= ep_name, z=[scoreVector[channel]], showscale=True, zmin=0, zmax=1,
                                          colorscale='Viridis', hoverinfo = 'text', text=[hover_text[j+(4*i)]], xgap = 2),
                                  i + 1, j + 1)
                channel = channel + 1
        fig.update_annotations(font_size=9)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        fig.update_layout(autosize=False, width=1080, height=700)
        fig.write_html(name_html_file)

    def scorepochs_html(self, scores):
        name_html_file = 'update_figure.html'
        ep_name = []
        for k in range(len(scores)):
            ep_name.append('E%d' % (k + 1))
        fig = make_subplots(3,4,specs=[[{'colspan':4}, None, None, None],
                                       [{},{'colspan':2, 'rowspan':2}, None, {}],
                                       [{},None,None,{}]],
                            subplot_titles=['Scorepochs result:',None, 'Score distribution graph:'])
        fig.add_trace(Heatmap(x=ep_name, z=[scores], showscale=True, zmin=0, zmax=1, colorscale='Viridis',xgap=3,
                              hovertemplate="<br>".join(["%{x}","Score: %{z}<extra></extra>"])))
        fig.add_trace(Histogram(x=scores, xbins=dict(size=0.005), hovertemplate="<br>".join([
            "Interval: %{x}",
            "Count: %{y}<extra></extra>",
        ])), 2, 2)
        fig.update_yaxes(showticklabels=False)
        fig.update_layout(autosize=False, width=1080, height=565)
        fig.write_html(name_html_file)



app= QApplication(sys.argv)
scorepochs = ScorepochsApp()
scorepochs.show()
sys.exit(app.exec_())
