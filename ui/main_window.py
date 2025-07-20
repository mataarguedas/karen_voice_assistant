import sys
import threading
import traceback
import re

from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QTextEdit, QSystemTrayIcon, QMenu, QAction)
from PyQt5.QtGui import (QPixmap, QPainter, QBrush, QColor, QFont, QPainterPath, QIcon, QFontDatabase, QPen, QTextCursor, QTextCharFormat)
from PyQt5.QtCore import Qt, QTimer

from backend.voice_assistant import VoiceAssistant
from utils.helpers import resource_path
import config

class CircleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(150, 150)
        self.active = False
        self.image_path = resource_path(config.KAREN_PIC_FILE)
        self.pixmap = QPixmap(self.image_path)
        
    def set_active(self, active):
        self.active = active
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, self.width(), self.height())
        painter.setClipPath(path)
        scaled_pixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        x = (self.width() - scaled_pixmap.width()) / 2
        y = (self.height() - scaled_pixmap.height()) / 2
        painter.drawPixmap(int(x), int(y), scaled_pixmap)
        if self.active:
            pen_width = 4
            painter.setPen(QPen(QColor(0, 150, 255, 180), pen_width))
            painter.drawEllipse(int(pen_width / 2), int(pen_width / 2), int(self.width() - pen_width), int(self.height() - pen_width))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Karen")
        self.setFixedSize(300, 600)
        self.setWindowIcon(QIcon(resource_path(config.KAREN_CIRCLE_PIC_FILE)))
        self._setup_tray_icon()
        self._setup_ui()
        self.start_initial_animation()

    def _setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        self.initial_full_text = "Karen"
        self.initial_current_text = ""
        self.initial_char_index = 0
        self.initial_message = QLabel(self.initial_current_text, self)
        self.set_font(self.initial_message, size=16, bold=True)
        self.initial_message.setAlignment(Qt.AlignCenter)
        self.initial_message.setWordWrap(True)
        self.initial_message.setStyleSheet("color: #7691ac;")
        self.initial_message.setGeometry(20, 250, self.width() - 40, 100)
        
        self.listening_full_text = "Listening for 'Hey Karen', 'Ey Karen', or '你好, 美丽'..."
        self.listening_current_text = ""
        self.listening_char_index = 0

        self.voice_indicator = CircleWidget()
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setLineWrapMode(QTextEdit.WidgetWidth)
        self.set_font(self.console_output, size=10)
        self.console_output.setStyleSheet(f"QTextEdit {{ background-color: {self.palette().window().color().name()}; color: #7792ad; border: none; }}")

        sys.stdout = self
        sys.stderr = self

    def _setup_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.windowIcon())
        self.tray_icon.setToolTip("Karen is running")
        tray_menu = QMenu()
        show_action = tray_menu.addAction("Show")
        show_action.triggered.connect(self.show_window)
        quit_action = tray_menu.addAction("Exit")
        quit_action.triggered.connect(self.quit_app)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.restore_window)

    def set_font(self, widget, size=10, bold=False, is_chinese=False):
        font_name = "Roboto"
        if is_chinese:
            font_name = "Source Han Sans CN Light"
        
        font_path = resource_path(config.ROBOTO_FONT_FILE)
        font_id = QFontDatabase.addApplicationFont(font_path)
        
        font = QFont(font_name, size)
        
        if font.family() != font_name:
            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                font = QFont(families[0], size)
            else:
                font = QFont("Arial", size)

        if bold: font.setBold(True)
        widget.setFont(font)

    def _contains_chinese(self, text):
        return re.search("[\u4e00-\u9fff]", text)

    def start_initial_animation(self):
        self.initial_message.show()
        self.initial_timer = QTimer(self)
        self.initial_timer.timeout.connect(self.update_initial_text)
        self.initial_timer.start(100)

    def update_initial_text(self):
        if self.initial_char_index < len(self.initial_full_text):
            self.initial_current_text += self.initial_full_text[self.initial_char_index]
            self.initial_message.setText(self.initial_current_text)
            self.initial_char_index += 1
        else:
            self.initial_timer.stop()
            QTimer.singleShot(2000, self.show_main_ui_and_start_second_animation)

    def show_main_ui_and_start_second_animation(self):
        self.initial_message.hide()
        self.main_layout.addWidget(self.voice_indicator, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.console_output)
        self.main_layout.addStretch()
        self.start_listening_animation()

    def start_listening_animation(self):
        self.listening_timer = QTimer(self)
        self.listening_timer.timeout.connect(self.update_listening_text)
        self.listening_timer.start(20)

    def update_listening_text(self):
        if self.listening_char_index < len(self.listening_full_text):
            self.listening_current_text += self.listening_full_text[self.listening_char_index]
            self.update_console_from_backend(self.listening_full_text, clear_before_add=True)
            self.listening_char_index += 1
        else:
            self.listening_timer.stop()
            self.start_backend()

    def write(self, text):
        self.console_output.moveCursor(self.console_output.textCursor().End)
        self.console_output.insertPlainText(text)

    def flush(self): pass

    def start_backend(self):
        self.backend = VoiceAssistant()
        self.backend.update_text.connect(self.update_console_from_backend)
        self.backend.voice_activity.connect(self.voice_indicator.set_active)
        self.backend.wake_word_detected.connect(self.show_window)
        self.backend.command_finished.connect(self.demote_window)
        
        self.backend_thread = threading.Thread(target=self.backend.run, daemon=True)
        self.backend_thread.start()

    def show_window(self):
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.show()
        self.raise_()
        self.activateWindow()

    def demote_window(self):
        if self.windowFlags() & Qt.WindowStaysOnTopHint:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.show()

    def update_console_from_backend(self, text, clear_before_add=False):

        if clear_before_add:
            self.console_output.clear()

        cursor = self.console_output.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        default_format = QTextCharFormat()
        default_font = QFont("Roboto", 10)
        default_format.setFont(default_font)
        
        chinese_format = QTextCharFormat()
        chinese_font = QFont("Source Han Sans CN Light", 10)
        chinese_format.setFont(chinese_font)

        for line in text.splitlines(True):
            if self._contains_chinese(line):
                cursor.insertText(line, chinese_format)
            else:
                cursor.insertText(line, default_format)

        self.console_output.setTextCursor(cursor)
        self.console_output.ensureCursorVisible()
        
    def restore_window(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_window()

    def quit_app(self):
        if hasattr(self, 'backend'): self.backend.stop()
        self.tray_icon.hide()
        QApplication.instance().quit()

    def closeEvent(self, event):
        self.demote_window()
        event.ignore()
        self.hide()
        self.tray_icon.showMessage("Karen", "Application was minimized to tray.", QSystemTrayIcon.Information, 2000)

