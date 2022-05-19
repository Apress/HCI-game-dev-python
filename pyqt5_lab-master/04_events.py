import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow
from PyQt5.QtWidgets import QBoxLayout, QWidget

# This is the *slot* we will connect to button presses.
def clicky():
    print('Clicky clicky!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('QPushButton { font-size: 48pt; }')
    window = QMainWindow()
    widget = QWidget()
    layout = QBoxLayout(QBoxLayout.TopToBottom)
    widget.setLayout(layout)
    window.setCentralWidget(widget)

    # Add some buttons.
    buttons = [QPushButton('Button {}'.format(i)) for i in range(5)]
    for b in buttons:
        b.clicked.connect(clicky)  # Connect the clicked signal to clicky()
        layout.addWidget(b)

    # Show the main window and call main loop.
    window.show()
    app.exec_()

