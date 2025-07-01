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

        self.locked = False
        self._drag_pos = None

        # === 背景窗格（承载 label 和按钮） ===
        self.pane = QtWidgets.QWidget(self)
        self.pane.setStyleSheet(STYLE_PANE_TRANSPARENT)

        # === 倒计时标签 ===
        self.label = QtWidgets.QLabel("25:00", self.pane)
        self.label.setStyleSheet(STYLE_TRANSPARENT)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        # === 关闭 & 锁定按钮 ===
        self.close_btn = QtWidgets.QPushButton("✖", self.pane)
        self.lock_btn = QtWidgets.QPushButton("🔒", self.pane)

        self.setup_button(self.close_btn)
        self.setup_button(self.lock_btn)

        self.close_btn.clicked.connect(self.close)
        self.lock_btn.clicked.connect(self.toggle_lock)

        # === pane 内布局：按钮 + label ===
        pane_layout = QtWidgets.QVBoxLayout(self.pane)
        top_buttons = QtWidgets.QHBoxLayout()
        top_buttons.addStretch()
        top_buttons.addWidget(self.lock_btn)
        top_buttons.addWidget(self.close_btn)

        pane_layout.addLayout(top_buttons)
        pane_layout.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)
        pane_layout.setContentsMargins(10, 10, 10, 10)

        # === 主窗口布局 ===
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.pane)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        # 初始按钮隐藏
        self.close_btn.hide()
        self.lock_btn.hide()

        # 定时器
        self.time_left = 25 * 60
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def setup_button(self, btn):
        btn.setFixedSize(26, 26)
        btn.setStyleSheet(STYLE_BUTTON)

    def toggle_lock(self):
        self.locked = not self.locked
        if self.locked:
            self.setWindowFlag(QtCore.Qt.WindowTransparentForInput, True)  # 锁定鼠标输入
            self.lock_btn.setText("🔓")
        else:
            self.setWindowFlag(QtCore.Qt.WindowTransparentForInput, False)
            self.lock_btn.setText("🔒")
        self.show()

    def update_time(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.label.setText(f"{minutes:02d}:{seconds:02d}")
        self.time_left -= 1
        if self.time_left < 0:
            self.timer.stop()

    def enterEvent(self, event):
        self.pane.setStyleSheet(STYLE_PANE_HOVER)
        self.close_btn.show()
        self.lock_btn.show()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.pane.setStyleSheet(STYLE_PANE_TRANSPARENT)
        self.close_btn.hide()
        self.lock_btn.hide()
        super().leaveEvent(event)

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
