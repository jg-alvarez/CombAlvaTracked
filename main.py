# pyuic5 CT_gui.ui -o CT_gui.py
# pyrcc5 resource.qrc -o resource_rc.py
# pyinstaller --onefile --noupx --windowed --icon=gui\CT_icon.ico -n CombAlvaTracked  main.py

import sys
from PyQt5.QtWidgets import QApplication
from appcontroller import AppController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ctrl = AppController()
    ctrl.show()
    app.exec_()