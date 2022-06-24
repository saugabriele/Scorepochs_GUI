import csv
import os.path
import sys
import numpy as np
import pandas as pd
from numpy import size
from os.path import expanduser,abspath
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame, QStackedWidget, QWidget, QPushButton, QLineEdit,\
    QFileDialog,QLabel,QTextEdit,QVBoxLayout,QScrollArea,QRadioButton
from PyQt5.uic import loadUi
from PyQt5.QtGui import QDoubleValidator, QValidator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import plotly.io as pio
from plotly.graph_objs import Layout,Scatter, Figure, Marker, Heatmap
from plotly.graph_objs.layout import YAxis, Annotation,Shape
from plotly.graph_objs.layout.annotation import Font
from plotly.subplots import make_subplots
import plotly.offline as plt
from scipy import signal as sig
from scipy import stats as st
from scorepochs_py import _spectrum_parameters,scorEpochs

class ScorepochsApp(QMainWindow):
    def __init__(self):
        super(ScorepochsApp, self).__init__()
        loadUi('qt_tesi.ui', self)
        self.data_proc = Data_Processing()
        self.fileselected = ''
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
        self.filename = self.data_frame.findChild(QLabel, 'filename')
        self.frequency = self.data_frame.findChild(QLineEdit, 'frequency')
        self.error_message_filename = self.data_frame.findChild(QLabel, 'error_message_file')
        self.error_message_frequency = self.data_frame.findChild(QLabel, 'error_message_frequency')
        self.error_message = self.data_frame.findChild(QTextEdit, 'error_message')
        self.plot_results_button = self.Menu_frame.findChild(QPushButton, 'plot_results_button')
        self.add_file = self.Menu_frame.findChild(QPushButton, 'addfile_button')
        self.example_button = self.Menu_frame.findChild(QPushButton, 'example_button')
        self.plot_settings_button = self.Menu_frame.findChild(QPushButton, 'plot_settings_button')
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
        self.error_message_compute_PSD = self.Windows.findChild(QLabel, 'error_message_compute_PSD')
        self.compute_corr_matrix_button = self.Windows.findChild(QPushButton, 'compute_corr_matrix_button')
        self.compute_score_vector_button = self.Windows.findChild(QPushButton, 'compute_score_vector_button')
        self.compute_scorepochs_button = self.Windows.findChild(QPushButton, 'compute_scorepochs_button')
        self.min_freqRange = self.Windows.findChild(QLineEdit, 'min_freqRange')
        self.max_freqRange = self.Windows.findChild(QLineEdit, 'max_freqRange')
        self.scorepochs_error_message = self.Windows.findChild(QLabel, 'scorepochs_error_message')
        self.maxfreqRange_error_message = self.Windows.findChild(QLabel, 'maxfreqRange_error_message')
        self.minfreqRange_error_message = self.Windows.findChild(QLabel, 'minfreqRange_error_message')
        self.browse.clicked.connect(self.browseFile)
        self.add_plot.clicked.connect(self.get_List)
        self.plot_results_button.clicked.connect(self.changepage_PlotResults)
        self.plot_settings_button.clicked.connect(self.changepage_PlotSettings)
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

    def browseFile(self):
        global fname
        home_directory = expanduser('~')
        fname, _ = QFileDialog.getOpenFileNames(self, 'Open file', home_directory, 'CSV Files (*.csv)')
        if fname == []:
            if self.fileselected == '':
                    self.error_message_filename.setText('No File Selected')
            else:
                return
        else:
            self.error_message_filename.clear()
            self.filename.setText(str(fname[0]))
            self.fileselected = str(fname[0])

    def validating_frequency(self):
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

    def validating_time_dimension_epochs(self):
        self.error_message_compute_PSD.clear()
        self.dimension_epochs_error_message.clear()
        self.max = (1/int(self.frequency.text())) * (len(self.Yarray[0])-1)
        min = (1/int(self.frequency.text()))
        rule = QDoubleValidator(min, self.max , 10)
        list = rule.validate(self.time_dimension_epochs.text(), 0)
        if list[0] != 2:
            self.dimension_epochs_error_message.setText(
                'Value out of range or incorrect format.[Format ex. "10,00"]')

    def validating_min_freqRange(self):
        self.minfreqRange_error_message.clear()
        self.scorepochs_error_message.clear()
        if self.f_len != 0:
            rule = QDoubleValidator(0, int(((self.f_len-1) * 1.6) - 1), 0)
            list = rule.validate(self.min_freqRange.text(), 0)
            if list[0] != 2:
                self.minfreqRange_error_message.setText('Min value: Range(0 : %d)' % int(((self.f_len-1) * 1.6) - 1))
        else:
            self.scorepochs_error_message.setText('First compute the Power Spectrum')

    def validating_max_freqRange(self):
        self.maxfreqRange_error_message.clear()
        self.scorepochs_error_message.clear()
        if self.f_len != 0:
            rule = QDoubleValidator(0, int((self.f_len-1) * 1.6), 0)
            list = rule.validate(self.max_freqRange.text(), 0)
            if list[0] != 2:
                self.maxfreqRange_error_message.setText('Max value: Range(0 : %d)' % int(((self.f_len-1) * 1.6)))
        else:
            self.scorepochs_error_message.setText('First compute the Power Spectrum')


    def get_List(self):
        self.error_message.clear()
        if str(self.error_message_filename.text()) != '' or str(self.error_message_frequency.text()) != '' or \
                    str(self.frequency.text()) == '' or str(self.filename.text()) == '':
            self.windows_StackedWidget.setCurrentWidget(self.data_page)
            self.error_message.setText('Enter the data correctly')
        else:
            self.message_data_processing.setText('Data processing...')
            self.message_data_processing.repaint()
            self.Yarray, self.Xarray, self.ch_names= self.data_proc.csv_File(self.fileselected, int(self.frequency.text()))
            self.plot()

    def changepage_addfile(self):
        self.windows_StackedWidget.setCurrentWidget(self.data_page)
        self.message_data_processing.clear()

    def changepage_createExample(self):
        self.windows_StackedWidget.setCurrentWidget(self.example_page)
        self.message_create_file.clear()

    def changepage_PlotResults(self):
        self.windows_StackedWidget.setCurrentWidget(self.plot_page)

    def changepage_PlotSettings(self):
        if self.fig is not None:
            self.windows_StackedWidget.setCurrentWidget(self.plot_settings_page)
        else:
            self.windows_StackedWidget.setCurrentWidget(self.data_page)

    def createFile_html(self):
        pio.templates.default = "plotly_white"
        step = 1. / len(self.Yarray)
        kwargs = dict(domain=[1 - step, 1], showticklabels=False, zeroline=False, showgrid=False)
        layout = Layout(yaxis=YAxis(kwargs), showlegend=False)
        self.traces = [Scatter(x=self.Xarray, y=self.Yarray[0], line=dict(color="#335BFF", width=0.8))]
        for ii in range(1, len(self.Yarray)):
            kwargs.update(domain=[1 - (ii + 1) * step, 1 - ii * step])
            layout.update({'yaxis%d' % (ii + 1): YAxis(kwargs), 'showlegend': False ,
                           'xaxis%d' % (ii + 1) : dict(showticklabels=False)})
            self.traces.append(Scatter(x=self.Xarray, y=self.Yarray[ii],
                                       yaxis='y%d' % (ii + 1), line=dict(color="#335BFF", width=0.8)))

        self.annotations = [Annotation(x=-0.06, y=0, xref='paper', yref='y%d' % (i + 1),
                                       text=ch_name, font=Font(size=9), showarrow=False)
                            for i, ch_name in enumerate(self.ch_names)]
        layout.update(annotations=self.annotations)
        layout.update(autosize=False, width= 1080, height = 565, margin=dict(l=70, r=30, t=35, b=30))
        self.fig = Figure(data=self.traces, layout=layout)
        self.fig.update_layout(xaxis1_showticklabels=True, xaxis1_side= "top")
        self.fig.write_html('figure.html')

    def update_Plot(self):
        if str(self.dimension_epochs_error_message.text()) != '':
            return
        else:
            i= 0
            x = float(self.time_dimension_epochs.text())
            offset = (1/int(self.frequency.text()))
            self.max = (1 / int(self.frequency.text())) * (len(self.Yarray[0]) - 1)
            fig = self.fig
            name_html_file = 'update_figure.html'

            while i <= ((self.max/x)-1):
                fig.add_shape(Shape(type='rect', xref='x', yref='paper',x0=(x*i)+(offset*i), x1=x*(i+1)+(offset*i), y0 = -0.02, y1 = 1.003))
                fig.layout.shapes[i]['yref'] = 'paper'
                fig.add_annotation(Annotation(x=(x*i + x*(i+1))/2, y=-0.055, yref='paper',
                                                   text=('e'+str(i+1)), font=Font(size=12), showarrow=False))
                i = i+1
            fig.write_html('update_figure.html')
            self.plot(name_html_file)

    def compute_Power_spectrum(self):
        if str(self.dimension_epochs_error_message.text()) != '' or self.time_dimension_epochs.text() == '':
            self.error_message_compute_PSD.setText('First you have to define the time dimension of each epoch.')
        else:
            self.scorepochs_error_message.clear()
            epLen = round(float(self.time_dimension_epochs.text()) * int(self.frequency.text()))
            dataLen = len(self.Yarray[0])
            nCh = len(self.Yarray)
            idx_ep = range(0, int(dataLen - epLen + 1), int(epLen + 1))
            nEp = len(idx_ep)
            traces_update = []
            name_html_file = 'update_figure.html'
            pio.templates.default = "plotly_white"
            x_step = 1. / nEp
            y_step = 1. / nCh
            y_kwargs = dict(domain=[1 - y_step, 1], showticklabels=False, zeroline=False, showgrid=False)
            x_kwargs = dict(domain=[1 - x_step, 1], showticklabels=False)
            layout = Layout(yaxis=YAxis(y_kwargs), showlegend=False, xaxis= x_kwargs )

            for e in range(nEp):
                x_kwargs.update(domain=[0 + (e) * x_step, 0 + (e+1) * x_step -0.01])
                for c in range(nCh):
                    y_kwargs.update(domain=[1 - (c + 1) * y_step, 1 - c * y_step])
                    layout.update({'yaxis%d' % (c + 1): YAxis(y_kwargs), 'showlegend': False,
                                   'xaxis%d' % (e + 1): x_kwargs})
                    epoch = self.Yarray[c][idx_ep[e]:idx_ep[e] + epLen]
                    # compute power spectrum
                    f, aux_pxx = sig.welch(epoch.T, fs = int(self.frequency.text()), window='hamming', nperseg=round(epLen / 8),
                                           detrend=False)
                    self.f_len = len(f)
                    traces_update.append(Scatter(x=f, y=aux_pxx, yaxis='y%d' % (c + 1),
                                                 xaxis= 'x%d' % (e + 1), line=dict(color="#335BFF", width=0.8)))
            annotations = [Annotation(x=-0.06, y= 0, xref='paper', yref='y%d' % (i + 1),
                                           text=ch_name, font=Font(size=9), showarrow=False)
                                for i, ch_name in enumerate(self.ch_names)]
            layout.update(annotations=annotations)
            layout.update(autosize=False, width=1080, height=565, margin=dict(l=70, r=30, t=35, b=30))
            fig = Figure(data=traces_update, layout=layout)
            fig.update_xaxes(type = 'log')
            fig.write_html(name_html_file)
            self.plot(name_html_file)

    def compute_Corr_matrix(self):
        if self.min_freqRange.text() != '' and self.max_freqRange.text() != '' \
                and int(self.min_freqRange.text()) >= int(self.max_freqRange.text()):
            self.scorepochs_error_message.setText('Min value in frequency is bigger than max value!')
        else:
            if self.scorepochs_error_message.text() == '' and self.minfreqRange_error_message.text() == '' \
                    and self.maxfreqRange_error_message.text() == '' and self.min_freqRange.text() != '' \
                    and self.max_freqRange.text() != '':
                self.data = []
                name_html_file = 'update_figure.html'
                epLen = round(float(self.time_dimension_epochs.text()) * int(self.frequency.text()))
                dataLen = len(self.Yarray[0])
                nCh = len(self.Yarray)
                idx_ep = range(0, int(dataLen - epLen + 1), int(epLen + 1))
                nEp = len(idx_ep)
                epoch = np.zeros((nEp, nCh, epLen))
                freqRange = [int(self.min_freqRange.text()),int(self.max_freqRange.text())]
                for e in range(nEp):
                    for c in range(nCh):
                        epoch[e][c][0:epLen] = self.Yarray[c][idx_ep[e]:idx_ep[e] + epLen]
                        f, aux_pxx = sig.welch(epoch[e][c].T, fs = int(self.frequency.text()), window='hamming', nperseg=round(epLen / 8),
                                               detrend=False)
                        if c == 0 and e == 0:  # The various parameters are obtained in the first interation
                            pxx, idx_min, idx_max, nFreq = _spectrum_parameters(f, freqRange, aux_pxx, nEp, nCh)
                        pxx[e][c] = aux_pxx[idx_min:idx_max + 1]
                pxxXch = np.zeros((nEp, idx_max - idx_min + 1))
                for c in range(nCh):
                    for e in range(nEp):
                        pxxXch[e] = pxx[e][c]
                    score_ch, p = st.spearmanr(pxxXch, axis=1)
                    self.data.append(score_ch)
                fig = make_subplots(4, 16, subplot_titles=[ch_name for i, ch_name in enumerate(self.ch_names)])
                channel=0
                for i in range(4):
                    for j in range(16):
                        fig.add_trace(Heatmap(z=self.data[channel], showscale= True, zmin=0, zmax=1, colorscale = 'Viridis'), i+1, j+1)
                        channel =  channel + 1
                fig.update_annotations(font_size = 9)
                fig.update_layout(autosize = False, width= 1080, height = 565)
                fig.write_html(name_html_file)
                self.plot(name_html_file)
            else:
                self.scorepochs_error_message.setText('Insert value correctly!')

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
                fig = make_subplots(8, 8, subplot_titles=[ch_name for i, ch_name in enumerate(self.ch_names)])
                channel = 0
                for i in range(8):
                    for j in range(8):
                        fig.add_trace(Heatmap(z=[scoreVector[channel]], showscale=True, zmin=0, zmax=1, colorscale='Viridis'), i + 1,
                                      j + 1)
                        channel = channel + 1
                fig.update_annotations(font_size=9)
                fig.update_xaxes(showticklabels=False)
                fig.update_yaxes(showticklabels=False)
                fig.update_layout(autosize=False, width=1080, height=565)
                fig.write_html(name_html_file)
                self.plot(name_html_file)
            else:
                self.scorepochs_error_message.setText('Insert value correctly!')

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
                fig = Figure(data = [Heatmap(z=[scores], showscale=True, zmin=0, zmax=1, colorscale='Viridis')],
                             layout=Layout(title= 'Scorepochs results:'))
                fig.update_xaxes(showticklabels=False)
                fig.update_yaxes(showticklabels=False)
                fig.update_layout(autosize=False, width=1080, height=565)
                fig.write_html(name_html_file)
                self.plot(name_html_file)
            else:
                self.scorepochs_error_message.setText('Insert value correctly!')


    @QtCore.pyqtSlot()
    def plot(self , name_html = 'figure.html'):
        self.clear_layout()
        container = QWidget()
        lay = QVBoxLayout(container)
        self.createFile_html()
        url = os.path.abspath(name_html)
        webView = QWebEngineView()
        html_map = QtCore.QUrl.fromLocalFile(url)
        webView.load(html_map)
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

app= QApplication(sys.argv)
scorepochs = ScorepochsApp()
scorepochs.show()
sys.exit(app.exec_())