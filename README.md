# Scorepochs - GUI

This project aims to create a GUI (Graphical User Iterface) for the [Scorepochs](https://github.com/Scorepochs-tools/scorepochs_py) tool already created in another work by Simone Maurizio La Cava.

Scorepochs aims to represent a simple tool for automatic scoring of resting-state M/EEG epochs to provide an accurate yet objective method to aid M/EEG experts during epoch selection procedure.

This graphical interface allows the user to implement the Scorepochs algorithm and obtain a graphical representation of the results, in such a way as to facilitate the choice.

## Project Description

Description | Screenshot
---|---
This simple GUI is written entirely in Python with PyQt5 - PyQt is a Python binding for Qt, which is a set of C++ libraries and development tools. | <img src="https://user-images.githubusercontent.com/103278076/176162207-11988211-f6fa-4c5e-a6cc-fe80d7021e54.png" width = "300">
Graphic representation of a set of M/EEG recordings made using the plotly Python library - The M/EEG recordings are supplied by the user by loading a .csv or .edf file. | <img src="https://user-images.githubusercontent.com/103278076/176219411-ba7cbf06-f7d1-4d50-a676-a116654f29ba.png" width = "300">
Graphic representation of the PSD calculation result - After defining the time dimension of the epochs, the algorithm calculates for each epoch of each PSD channel using the Welch method in a given frequency range | <img src="https://user-images.githubusercontent.com/103278076/176227886-ead87c3b-19e4-4f75-a401-a3ade57ed846.png" width = "300">
Graphical representation of the correlation matrices - At the channel level, a similarity score, computed by using the Spearman correlation coefficient, is evaluated between the PSD values ​​extracted from all the epochs, thereby providing a correlation matrix. | <img src="https://user-images.githubusercontent.com/103278076/200137480-00ebc797-ddad-4204-9b1d-382ff90a2af4.png" width = "300">
Graphical representation of the score vectors - The average is computed over the columns of the symmetric matrix to obtain a score vector with a length equal to the number of epochs, where the entries represent the mean similarity score of the corresponding epoch. | <img src="https://user-images.githubusercontent.com/103278076/200137627-db0f0fa6-9b3a-41ba-91dd-3adac8ea1aa0.png" width = "300">
Graphical representation of the scores provided by Scorepochs for each single epoch and their distribution - These scores are obtained by calculating the average of the score vectors across the channels. | <img src="https://user-images.githubusercontent.com/103278076/200137693-34d35867-2b64-4189-b59d-0f700909c67a.png" width = "300">

## Required libraries
 - Numpy
 - Scipy
 - PyQt5
 - Plotly
