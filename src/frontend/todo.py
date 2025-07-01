from PyQt5 import QtWidgets, QtCore, QtGui
import sys

from frontend.constant import (
    STYLE_TRANSPARENT,
    STYLE_HOVER,
    STYLE_PANE_TRANSPARENT,
    STYLE_PANE_HOVER,
    STYLE_BUTTON,
    STYLE_EXTRA_PANEL
)

class TransparentTimer(QtWidgets.QWidget):
    WORK_DURATION = 25 * 60  # 25分钟
    BREAK_DURATION = 5 * 60  # 5分钟

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self._drag_pos = None

        self.paused = False
        self.time_left = 25 * 60
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.pane = QtWidgets.QWidget(self)
        self.pane.setStyleSheet(STYLE_PANE_TRANSPARENT)

        # 增加状态标签，显示“工作中”或“休息中”
        # self.status_label = QtWidgets.QLabel("工作中", self.pane)
        # self.status_label.setStyleSheet(STYLE_TRANSPARENT)
        # self.status_label.setAlignment(QtCore.Qt.AlignCenter)

        self.label = QtWidgets.QLabel("25:00", self.pane)
        self.label.setStyleSheet(STYLE_TRANSPARENT)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.close_btn = QtWidgets.QPushButton("✖", self.pane)
        self.setup_button(self.close_btn)
        self.close_btn.clicked.connect(self.close)

        # 暂停/继续按钮
        self.pause_btn = QtWidgets.QPushButton("⏸", self.pane)
        self.setup_button(self.pause_btn)
        self.pause_btn.clicked.connect(self.toggle_pause)

        # 停止按钮
        self.stop_btn = QtWidgets.QPushButton("■", self.pane)
        self.setup_button(self.stop_btn)
        self.stop_btn.clicked.connect(self.stop_timer)

        pane_layout = QtWidgets.QVBoxLayout(self.pane)

        top_buttons = QtWidgets.QHBoxLayout()
        top_buttons.addStretch()
        top_buttons.addWidget(self.close_btn)

        button_row = QtWidgets.QHBoxLayout()
        button_row.addStretch()
        button_row.addWidget(self.pause_btn)
        button_row.addWidget(self.stop_btn)
        button_row.addStretch()# center

        pane_layout.addLayout(top_buttons)
        # pane_layout.addWidget(self.status_label, alignment=QtCore.Qt.AlignCenter)
        pane_layout.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)
        # pane_layout.addWidget(self.stop_btn, alignment=QtCore.Qt.AlignCenter)
        pane_layout.addLayout(button_row)
        pane_layout.setContentsMargins(10, 10, 10, 10)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.pane)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

      
        # ▼ / ▲ 按钮
        self.expand_btn = QtWidgets.QPushButton("▼", self.pane)
        self.expand_btn.setFixedSize(26, 26)
        self.expand_btn.setStyleSheet(STYLE_BUTTON)
        self.expand_btn.clicked.connect(self.toggle_panel)

        # 把按钮放到一个横向布局并靠右
        expand_layout = QtWidgets.QHBoxLayout()
        expand_layout.addStretch()
        expand_layout.addWidget(self.expand_btn)

        # 添加到主 pane 布局
        pane_layout.addLayout(expand_layout)

        self.extra_panel = QtWidgets.QFrame(self.pane)
        self.extra_panel.setMaximumHeight(0)
        self.extra_panel.setStyleSheet(STYLE_EXTRA_PANEL)
        self.extra_panel.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)

        extra_layout = QtWidgets.QVBoxLayout(self.extra_panel)
        extra_layout.setContentsMargins(5, 5, 5, 5)
        extra_layout.addWidget(QtWidgets.QLabel("Item 1"))
        extra_layout.addWidget(QtWidgets.QLabel("Item 2"))

        pane_layout.addWidget(self.extra_panel)
   
        # self.close_btn.hide()
        # self.pause_btn.hide()
        # self.stop_btn.hide()
        # self.expand_btn.hide()
        self.btns = []
        self.btns.append(self.close_btn)
        self.btns.append(self.pause_btn)
        self.btns.append(self.stop_btn)
        self.btns.append(self.expand_btn)

        for btn in self.btns:
            btn.hide()

        # 状态机：True=工作，False=休息
        self.is_working = True
        self.time_left = self.WORK_DURATION

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)


    def update_time(self):
        if self.paused: 
            return
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.label.setText(f"{minutes:02d}:{seconds:02d}")

        self.time_left -= 1
        if self.time_left < 0:
            # 时间结束，切换状态
            self.is_working = not self.is_working

            if self.is_working:
                self.time_left = self.WORK_DURATION
                # self.status_label.setText("工作中")
            else:
                self.time_left = self.BREAK_DURATION
                # self.status_label.setText("休息中")

    def stop_timer(self):
        self.timer.stop()
        self.time_left = 0
        self.update_time()
        self.pause_btn.setText("▶")
        self.paused = True

    def enterEvent(self, event):
        self.pane.setStyleSheet(STYLE_PANE_HOVER)
        for btn in self.btns:
            btn.show() 
        # self.close_btn.show()
        # self.pause_btn.show()
        # self.stop_btn.show()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.pane.setStyleSheet(STYLE_PANE_TRANSPARENT)
        for btn in self.btns:
            btn.hide() 
        # self.close_btn.hide()
        # self.pause_btn.hide()
        # self.stop_btn.hide()
        super().leaveEvent(event)

    def setup_button(self, btn):
        btn.setFixedSize(26, 26)
        btn.setStyleSheet(STYLE_BUTTON)

    def toggle_pause(self):
        if self.paused:
            self.timer.start(1000)
            self.pause_btn.setText("⏸")
            self.paused = False
        else:
            self.timer.stop()
            self.pause_btn.setText("▶")
            self.paused = True

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

    def keyPressEvent(self, event):
        # Ctrl+D 加速调试时间
        if event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_D:
            self.time_left -= 290
            if self.time_left < 0:
                self.time_left = 0  # 避免负数
            print(f"[DEBUG] Time fast-forwarded by 4m50s, new time_left = {self.time_left} seconds")
            self.update_time()  # 立即刷新显示
            event.accept()
        else:
            super().keyPressEvent(event)

    def toggle_panel(self):
        # if self.extra_panel.maximumHeight() == 0:
        #     new_height = 100  # 展开高度
        #     self.expand_btn.setText("▲")
        # else:
        #     new_height = 0
        #     self.expand_btn.setText("▼")
        is_collapsed = self.extra_panel.maximumHeight() == 0
        target_height = self.extra_panel.sizeHint().height() if is_collapsed else 0
        self.expand_btn.setText("▲" if is_collapsed else "▼")

        self.anim = QtCore.QPropertyAnimation(self.extra_panel, b"maximumHeight")
        self.anim.setDuration(200)
        self.anim.setStartValue(self.extra_panel.maximumHeight())
        self.anim.setEndValue(target_height)
        self.anim.finished.connect(self.adjustSize)  # 动画后自动调整窗口高度
        # self.anim.setEndValue(new_height)
        self.anim.start()

