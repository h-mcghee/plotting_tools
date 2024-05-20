import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,QSlider, QWidget, QGridLayout,QSizePolicy, QCheckBox, QLineEdit, QPushButton, QSpinBox,QFileDialog, QMessageBox
from PyQt5.QtCore import Qt


def idx(x, value):
    return np.argmin(np.abs(x - value))

def tof2energy(x, hv, s, t0, E0):
    """
    function for converting from TOF to energy
    requires:
    t the time of flight
    parameters:
        hv - photon energy
        s - source to detector distance
        t0 - start time
        E0 - potential offset in source
    """
    Me = 9.1093897e-31  # mass electron in kg
    ES = 6.242e18  # electrons per s

    eKE = (ES * 0.5 * Me) * ((1e9 * s / (x - t0))**2)  - E0

    BE = hv - eKE
    return BE

class MainWindow(QMainWindow):
    def __init__(self,x,y,matrix,parent = None):
        super(MainWindow,self).__init__(parent)
        self.og_x = self.x = x
        self.og_y = self.y = y
        self.og_matrix = self.matrix = matrix

        self.scale = 'linear'

        self.is_checked = False

        self.error = []

        self.setWindowTitle("2D Array Plotter")
        self.setGeometry(200, 200, 1000, 1500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QGridLayout(self.central_widget)

        self.xlims = [min(x),max(x)]
        self.xmin_lineedit = QLineEdit()
        self.xmax_lineedit = QLineEdit()
        self.apply_button = QPushButton("Apply x limits")
        self.apply_button.clicked.connect(self.apply_x_limits)
        layout.addWidget(self.xmin_lineedit,0,1)
        layout.addWidget(self.xmax_lineedit,0,2)
        layout.addWidget(self.apply_button,0,3)

        self.calib_checkbox = QCheckBox("TOF calibration")
        self.calib_checkbox.stateChanged.connect(self.tof_calib)
        layout.addWidget(self.calib_checkbox,0,4)

        self.bkg_sub_checkbox = QCheckBox("Bkg sub")
        self.bkg_sub_checkbox.stateChanged.connect(self.bkg_sub)
        layout.addWidget(self.bkg_sub_checkbox,1,3)

        self.average_checkbox = QCheckBox("Average")
        self.average_checkbox.stateChanged.connect(self.set_state)
        layout.addWidget(self.average_checkbox,1,4)

        self.spin_box = QSpinBox()
        self.spin_box.setMinimum(1)
        self.spin_box.setMaximum(20)
        self.spin_box.valueChanged.connect(self.update_xplot)
        layout.addWidget(self.spin_box,1,5)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save)
        layout.addWidget(self.save_button,2,1)

        self.selected_values = []

        # self.log_checkbox = QCheckBox("Log scale")
        # self.log_checkbox.stateChanged.connect(self.log_scale)
        # layout.addWidget(self.log_checkbox,1,4)


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
        self.ax_original.clear()
        if self.is_checked == True:
            self.selected_values = np.sum(self.matrix[:, x_index:x_index+self.spin_box.value()],axis=1)
            self.error = np.sqrt(2) * np.sqrt(np.sum(self.og_matrix[:, x_index:x_index+self.spin_box.value()],axis=1))
            self.ax_original.axvline(self.x[x_index], color='red')
            self.ax_original.axvline(self.x[x_index+self.spin_box.value()-1], color='red')

        else:
            self.selected_values = self.matrix[:, x_index]
            self.error = np.sqrt(2) * np.sqrt(self.og_matrix[:, x_index])
            self.ax_original.axvline(self.x[x_index], color='red')



        
        # Update original matrix plot
        
        self.ax_original.pcolormesh(self.x,self.y,self.matrix, cmap='viridis')
        # self.ax_original.set_yscale(self.scale)
        self.ax_original.set_xlim(self.xlims)

        self.ax_original.set_title("Original Matrix")
        
        # Update selected Y values plot
        self.ax_selected.clear()
        self.ax_selected.plot(self.y,self.selected_values)
        
        self.ax_selected.fill_between(self.y,self.selected_values - self.error, self.selected_values + self.error,alpha=0.5)
        if self.is_checked == True:
            self.ax_selected.set_title(f"Sum of Y values for X={self.x[x_index]:.3f} to {self.x[x_index+self.spin_box.value()-1]:.3f}")
        else:
            self.ax_selected.set_title(f"Selected Y values for X={self.x[x_index]}")
        self.ax_selected.set_xlabel("Y index")
        self.ax_selected.set_ylabel("Value")
        self.ax_selected.set_xscale('symlog',linthresh = 1000)
        
        
        
        self.fig_original.canvas.draw()
        self.fig_selected.canvas.draw()
        self.setFocus()

        

    def update_yplot(self):

        y_index = self.y_slider.value()
        print(y_index)
        selected_y_values = self.matrix[y_index, :]
        
        # Update original matrix plot
        self.ax_original.clear()
        self.ax_original.pcolormesh(self.x,self.y,self.matrix, cmap='viridis')
        # self.ax_original.set_yscale(self.scale)
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

    def bkg_sub(self,state):
        bkg = np.mean(self.matrix[0:3,:],axis=0)
        try:
            if state == Qt.Checked:
                self.matrix = self.matrix - bkg
                self.update_xplot()
                self.update_yplot()
            else:
                self.matrix = self.og_matrix
                self.update_xplot()
                self.update_yplot()
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e), QMessageBox.Ok)

    def apply_x_limits(self):
        self.xlims = [float(self.xmin_lineedit.text()),float(self.xmax_lineedit.text())]
        self.update_xplot()
        self.update_yplot()
        

    def tof_calib(self,state):
        try:
            self.x_slider.setValue(0)
            if state == Qt.Checked:
                
                self.x = tof2energy(self.x,2.164476933102369571e+01,3.278435274171569436e-01,3.444852703175022270e+03,0.000000000000000000e+00)    
                min_index = np.argmin(self.x)
                mask = (np.arange(self.x.shape[0]) >= min_index) & (self.x > 0)
                self.x = self.x[mask]
                self.matrix = self.matrix[:,mask]
                self.xlims = [min(self.x),max(self.x)]

                self.update_xplot()
                self.update_yplot()
            else:
                self.x = self.og_x
                self.matrix = self.og_matrix
                self.xlims = [min(self.x),max(self.x)]
                self.update_xplot()
                self.update_yplot()

        except Exception as e:
            QMessageBox.critical(None, "Error", str(e), QMessageBox.Ok)

    def set_state(self,state):
        if state == Qt.Checked:
            self.is_checked = True
        else:
            self.is_checked = False
        self.update_xplot()

    def save(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()", "","All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            with open(file_name, 'w') as f:
                for x, y in zip(self.y, self.selected_values):
                    f.write(f"{x}\t{y}\n")



    # def log_scale(self,state):
    #     if state == Qt.Checked:
    #         self.scale = ['symlog']
    #         self.update_xplot()
    #         self.update_yplot()
    #     else:
    #         self.scale = 'linear'
    #         self.update_xplot()
    #         self.update_yplot()

    



