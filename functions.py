import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,QSlider, QWidget, QGridLayout,QSizePolicy, QCheckBox, QLineEdit, QPushButton
from PyQt5.QtCore import Qt


def idx(x, value):
    return np.argmin(np.abs(x - value))

class MainWindow(QMainWindow):
    def __init__(self,x,y,matrix,parent = None):
        super(MainWindow,self).__init__(parent)
        self.x = x
        self.y = y
        self.matrix = matrix




        self.setWindowTitle("2D Array Plotter")
        self.setGeometry(200, 200, 800, 1500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QGridLayout(self.central_widget)

        self.xlims = [3500,4000]
        self.xmin_lineedit = QLineEdit()
        self.xmax_lineedit = QLineEdit()
        self.apply_button = QPushButton("Apply x limits")
        self.apply_button.clicked.connect(self.apply_x_limits)
        layout.addWidget(self.xmin_lineedit,0,1)
        layout.addWidget(self.xmax_lineedit,0,2)
        layout.addWidget(self.apply_button,0,3)

        # Create Matplotlib figure for the original matrix

        self.fig_original, self.ax_original = plt.subplots(figsize = (6,6))
        self.ax_original.set_xlim(self.xlims)
        self.canvas_original = FigureCanvas(self.fig_original)
        layout.addWidget(self.canvas_original,0,0)
        self.canvas_original.mpl_connect('button_press_event', self.on_mouse_press)

        #add checkbox for background subtraction
        # self.bkg = QCheckBox()
        # layout.addWidget(self.bkg,0,1)

        # Add slider for selecting X value
        
        self.x_slider = QSlider()
        self.x_slider.setOrientation(1)  # Vertical orientation
        self.x_slider.setMinimum(self.x[0])
        self.x_slider.setMaximum(len(self.x))
        self.x_slider.setValue(0)
        self.x_slider.setSingleStep(1)
        self.x_slider.setTickPosition(QSlider.TicksRight)
        self.x_slider.valueChanged.connect(self.update_xplot)
        self.x_slider.setFocusPolicy(Qt.NoFocus)  # Make sure the widget can receive focus

        # layout.addWidget(self.x_slider,1,0)



        self.y_slider = QSlider()
        self.y_slider.setOrientation(0)
        self.y_slider.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)  # horizontal orientation
        self.y_slider.setMinimum(self.y[0])
        self.y_slider.setMaximum(len(self.y))
        self.y_slider.setValue(0)
        self.y_slider.setSingleStep(1)
        self.y_slider.setTickInterval(1000)
        self.y_slider.setTickPosition(QSlider.TicksLeft)
        self.y_slider.valueChanged.connect(self.update_yplot)
        self.y_slider.setFocusPolicy(Qt.NoFocus)  # Make sure the widget can receive focus

        # layout.addWidget(self.y_slider,0,1)

        # Create Matplotlib figure for selected Y values
        self.fig_selected, self.ax_selected = plt.subplots()
        self.canvas_selected = FigureCanvas(self.fig_selected)
        layout.addWidget(self.canvas_selected,2,0)
        self.update_xplot()

        self.fig_y_selected, self.ax_y_selected = plt.subplots()
        self.canvas_y_selected = FigureCanvas(self.fig_y_selected)
        layout.addWidget(self.canvas_y_selected,3,0)
        self.update_yplot()

    def on_mouse_press(self, event):
        # Get the mouse position in data coordinates
        x = event.xdata
        y = event.ydata

        # Find the closest data point to the mouse position
        x_index = np.argmin(np.abs(self.x - x))
        y_index = np.argmin(np.abs(self.y - y))
        if event.dblclick:
            self.y_slider.setValue(y_index)
            self.update_yplot()
        else:
            self.x_slider.setValue(x_index)

        # Update the plot with the selected data point
            self.update_xplot()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.x_slider.setValue(self.x_slider.value() - 1)
            # self.update_xplot()
        elif event.key() == Qt.Key_Right:
            self.x_slider.setValue(self.x_slider.value() + 1)
            # self.update_xplot()

        elif event.key() == Qt.Key_Up:
            self.y_slider.setValue(self.y_slider.value() + 1)
            # self.update_yplot()

        elif event.key() == Qt.Key_Down:
            self.y_slider.setValue(self.y_slider.value() - 1)
            # self.update_yplot()
        else:
            super().keyPressEvent(event)

    def update_xplot(self):
        x_index = self.x_slider.value()
        selected_values = self.matrix[:, x_index]
        
        # Update original matrix plot
        self.ax_original.clear()
        self.ax_original.pcolormesh(self.x,self.y,self.matrix, cmap='viridis')
        self.ax_original.set_yscale('symlog',linthresh = 1000)
        self.ax_original.set_xlim(self.xlims)

        self.ax_original.set_title("Original Matrix")
        
        # Update selected Y values plot
        self.ax_selected.clear()
        self.ax_selected.plot(self.y,selected_values)
        self.ax_selected.set_title(f"Selected Y values for X={self.x[x_index]}")
        self.ax_selected.set_xlabel("Y index")
        self.ax_selected.set_ylabel("Value")
        self.ax_original.axvline(self.x[x_index], color='red')
        
        self.fig_original.canvas.draw()
        self.fig_selected.canvas.draw()

        

    def update_yplot(self):

        y_index = self.y_slider.value()
        print(y_index)
        selected_y_values = self.matrix[y_index, :]
        
        # Update original matrix plot
        self.ax_original.clear()
        self.ax_original.pcolormesh(self.x,self.y,self.matrix, cmap='viridis')
        self.ax_original.set_yscale('symlog',linthresh = 1000)
        self.ax_original.set_xlim(self.xlims)


        self.ax_original.set_title("Original Matrix")
        
        # Update selected Y values plot
        self.ax_y_selected.clear()
        self.ax_y_selected.plot(self.x,selected_y_values)
        self.ax_y_selected.set_title(f"Selected Y values for X={self.y[y_index]}")
        self.ax_y_selected.set_xlabel("X index")
        self.ax_y_selected.set_ylabel("Value")
        self.ax_y_selected.set_xlim(self.xlims)
        self.ax_original.axhline(self.y[y_index], color='red')
        
        self.fig_original.canvas.draw()
        self.fig_y_selected.canvas.draw()

    def bkg_sub(self):
        bkg = np.mean(self.matrix[0:3,:],axis=0)
        self.matrix = self.matrix - bkg

    def apply_x_limits(self):
        self.xlims = [float(self.xmin_lineedit.text()),float(self.xmax_lineedit.text())]
        self.update_xplot()
        self.update_yplot()


