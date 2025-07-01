from PyQt5 import QtWidgets, QtCore, QtGui
import sys

from constant import (
    STYLE_TRANSPARENT,
    STYLE_HOVER,
    STYLE_PANE_TRANSPARENT,
    STYLE_PANE_HOVER,
    STYLE_BUTTON
)

class TransparentTimer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self._drag_pos = None  # 用于拖动窗口

        self.pane = QtWidgets.QWidget(self)
        self.pane.setStyleSheet(STYLE_PANE_TRANSPARENT)

        self.label = QtWidgets.QLabel("25:00", self.pane)
        self.label.setStyleSheet(STYLE_TRANSPARENT)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        # 关闭按钮
        self.close_btn = QtWidgets.QPushButton("✖", self.pane)
        self.setup_button(self.close_btn)
        self.close_btn.clicked.connect(self.close)

        # 停止按钮，放在计时数字下方
        self.stop_btn = QtWidgets.QPushButton("■", self.pane)  # ■ 表示停止
        self.setup_button(self.stop_btn)
        self.stop_btn.clicked.connect(self.stop_timer)

        # 布局
        pane_layout = QtWidgets.QVBoxLayout(self.pane)

        # 顶部右侧关闭按钮
        top_buttons = QtWidgets.QHBoxLayout()
        top_buttons.addStretch()
        top_buttons.addWidget(self.close_btn)

        pane_layout.addLayout(top_buttons)
        pane_layout.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)
        pane_layout.addWidget(self.stop_btn, alignment=QtCore.Qt.AlignCenter)
        pane_layout.setContentsMargins(10, 10, 10, 10)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.pane)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        self.close_btn.hide()
        self.stop_btn.hide()

        self.time_left = 25 * 60
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.label.setText(f"{minutes:02d}:{seconds:02d}")
        self.time_left -= 1
        if self.time_left < 0:
            self.timer.stop()

    def stop_timer(self):
        self.timer.stop()

    def enterEvent(self, event):
        self.pane.setStyleSheet(STYLE_PANE_HOVER)
        self.close_btn.show()
        self.stop_btn.show()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.pane.setStyleSheet(STYLE_PANE_TRANSPARENT)
        self.close_btn.hide()
        self.stop_btn.hide()
        super().leaveEvent(event)

    def setup_button(self, btn):
        btn.setFixedSize(26, 26)
        btn.setStyleSheet(STYLE_BUTTON)

    # 恢复拖动功能
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TransparentTimer()
    window.resize(200, 100)
    window.move(1000, 50)
    window.show()
    sys.exit(app.exec_())
