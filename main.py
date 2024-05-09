import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,QSlider, QWidget, QGridLayout,QSizePolicy
from PyQt5.QtCore import Qt



def idx(x, value):
    return np.argmin(np.abs(x - value))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("2D Array Plotter")
        self.setGeometry(200, 200, 1000, 1200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QGridLayout(self.central_widget)

        # Create Matplotlib figure for the original matrix
        self.fig_original, self.ax_original = plt.subplots(figsize = (6,6))
        self.canvas_original = FigureCanvas(self.fig_original)
        layout.addWidget(self.canvas_original,0,0)

        # Add slider for selecting X value
        

        self.x_slider = QSlider()
        self.x_slider.setOrientation(1)  # Vertical orientation
        self.x_slider.setMinimum(x[0])
        self.x_slider.setMaximum(1000*x[-1])
        self.x_slider.setValue(0)
        self.x_slider.setSingleStep(1)
        self.x_slider.setTickPosition(QSlider.TicksRight)
        self.x_slider.valueChanged.connect(self.update_xplot)
        layout.addWidget(self.x_slider,1,0)



        self.y_slider = QSlider()
        self.y_slider.setOrientation(0)
        self.y_slider.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)  # horizontal orientation
        self.y_slider.setMinimum(y[0])
        self.y_slider.setMaximum(y[-1])
        self.y_slider.setValue(0)
        self.y_slider.setSingleStep(1)
        self.y_slider.setTickInterval(1000)
        self.y_slider.setTickPosition(QSlider.TicksLeft)
        self.y_slider.valueChanged.connect(self.update_yplot)
        layout.addWidget(self.y_slider,0,1)

        # Create Matplotlib figure for selected Y values
        self.fig_selected, self.ax_selected = plt.subplots()
        self.canvas_selected = FigureCanvas(self.fig_selected)
        layout.addWidget(self.canvas_selected,2,0)
        self.update_xplot()

        self.fig_y_selected, self.ax_y_selected = plt.subplots()
        self.canvas_y_selected = FigureCanvas(self.fig_y_selected)
        layout.addWidget(self.canvas_y_selected,3,0)
        self.update_yplot()

        

    def update_xplot(self):

        x_index = idx(x,self.x_slider.value()/1000)
        selected_values = matrix[:, x_index]
        
        # Update original matrix plot
        self.ax_original.clear()
        self.ax_original.pcolormesh(x,y,matrix, cmap='viridis')
        self.ax_original.set_yscale('symlog',linthresh = 1000)
        self.ax_original.set_title("Original Matrix")
        
        # Update selected Y values plot
        self.ax_selected.clear()
        self.ax_selected.plot(y,selected_values)
        self.ax_selected.set_title(f"Selected Y values for X={x[x_index]}")
        self.ax_selected.set_xlabel("Y index")
        self.ax_selected.set_ylabel("Value")
        self.ax_original.axvline(x=x[x_index], color='red')
        
        self.fig_original.canvas.draw()
        self.fig_selected.canvas.draw()

    def update_yplot(self):

        y_index = idx(y,self.y_slider.value())
        selected_y_values = matrix[y_index, :]
        
        # Update original matrix plot
        self.ax_original.clear()
        self.ax_original.pcolormesh(x,y,matrix, cmap='viridis')
        self.ax_original.set_yscale('symlog',linthresh = 1000)

        self.ax_original.set_title("Original Matrix")
        
        # Update selected Y values plot
        self.ax_y_selected.clear()
        self.ax_y_selected.plot(x,selected_y_values)
        self.ax_y_selected.set_title(f"Selected Y values for X={y[y_index]}")
        self.ax_y_selected.set_xlabel("X index")
        self.ax_y_selected.set_ylabel("Value")
        self.ax_original.axhline(y=y[y_index], color='red')
        
        self.fig_original.canvas.draw()
        self.fig_y_selected.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Generate sample 2D matrix
    

    #eventually add load function like for fitting
    #add flip axis
    file = np.genfromtxt('/Users/harrymcghee/PIP Dropbox/PIPGROUP/3_USERS/2_HMG/Artemis2023/zmatrix.txt')
    x = file[0,1:]
    y = file[1:,0]
    matrix = file[1:,1:]
    matrix_size = len(y)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

y