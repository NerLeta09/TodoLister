from PyQt5 import QtWidgets, QtCore, QtGui
import sys

from frontend.todo import TransparentTimer

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TransparentTimer()
    window.resize(200, 130)
    window.move(1000, 50)
    window.show()
    sys.exit(app.exec_())
