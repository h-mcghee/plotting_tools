import sys
import argparse
import numpy as np
from PyQt5.QtWidgets import QApplication
from plotter import MainWindow

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="2D Array Plotter")
    parser.add_argument(
        "filename",
        type=str,
        nargs="?",
        default="test_data/zmatrix.txt",
        help="Path to the input file containing the 2D matrix data (default: test_data/zmatrix.txt)."
    )
    args = parser.parse_args()

    # Load the data file
    try:
        file = np.genfromtxt(args.filename)
        x = file[0, 1:]
        y = file[1:, 0]
        matrix = file[1:, 1:]
    except Exception as e:
        print(f"Error loading file '{args.filename}': {e}")
        sys.exit(1)

    # Launch the PyQt5 application
    app = QApplication([])  
    window = MainWindow(x, y, matrix)
    window.show()
    window.setFocus()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
