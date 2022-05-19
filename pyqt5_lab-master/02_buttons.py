# Import stuff
import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow

# Use a __main__ guard, you never know.
if __name__ == '__main__':
    # Create our application -- MUST be done first.
    app = QApplication(sys.argv)

    # Create a main window with a single QLabel.
    window = QMainWindow()
    button = QPushButton('Hello PyQT5!')
    window.setCentralWidget(button)

    # Show the main window and call main loop.
    window.show()
    app.exec_()


