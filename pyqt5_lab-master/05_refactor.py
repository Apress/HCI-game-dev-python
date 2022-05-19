# Import stuff
import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow
from PyQt5.QtWidgets import QBoxLayout, QWidget

# Use a __main__ guard, you never know.
if __name__ == '__main__':
    # Create our application -- MUST be done first.
    app = QApplication(sys.argv)

    # BUILD THE INTERFACE...

    app.exec_()

