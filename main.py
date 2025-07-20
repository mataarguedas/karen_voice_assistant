import sys
import traceback
from PyQt5.QtWidgets import QApplication

from ui.main_window import MainWindow

def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(f"[UNHANDLED EXCEPTION]\n{tb}")
    if 'window' in globals() and hasattr(window, 'console_output'):
        window.console_output.append(f"[CRITICAL ERROR]\n{tb}")

sys.excepthook = excepthook

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
