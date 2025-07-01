from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import logging

logger = logging.getLogger(__name__) 

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

from frontend.todo import TransparentTimer

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TransparentTimer()

     # 连接关闭信号，执行清理回调
    def on_window_closed():
        # clean
        logger.info("Received window closed signal in main, cleaning up resources...")

    window.closed.connect(on_window_closed)

    window.resize(200, 130)
    window.move(1000, 50)
    window.show()
    sys.exit(app.exec_())
