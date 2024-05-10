import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,QSlider, QWidget, QGridLayout,QSizePolicy
from PyQt5.QtCore import Qt

from functions import MainWindow,idx

if __name__ == '__main__':

    app = QApplication([])  
    #eventually add load function like for fitting
    #add flip axis
    file = np.genfromtxt('test_data/305.txt')
    x = file[0,1:]
    y = file[1:,0]
    matrix = file[1:,1:]


    window = MainWindow(x,y,matrix)
    window.show()
    window.setFocus()

    sys.exit(app.exec_())