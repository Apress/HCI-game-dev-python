# Import stuff
import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QLabel
from PyQt5.QtWidgets import QBoxLayout, QWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('QPushButton { font-size: 48pt; }')

    # Create a main window, a placeholder widget, and a layout.
    window = QMainWindow()
    widget = QWidget()
    layout = QBoxLayout(QBoxLayout.TopToBottom)

    # Set the layout for our widget to the vbox.
    widget.setLayout(layout)
    window.setCentralWidget(widget)

    # Add some buttons.
    buttons = [QPushButton('Button {}'.format(i)) for i in range(5)]
    for b in buttons:
        layout.addWidget(b)

    window.show()
    app.exec_()

