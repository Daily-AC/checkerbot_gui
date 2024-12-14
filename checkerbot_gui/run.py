from checkerbot_gui.ui import CheckerBotApp
import sys
from PyQt5.QtWidgets import QApplication

def run():
    app = QApplication(sys.argv)
    window = CheckerBotApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
