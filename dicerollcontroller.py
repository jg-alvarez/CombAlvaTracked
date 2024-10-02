from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from gui.CT_DiceRoll_gui import Ui_DiceRollWind
from numpy import random
import dSet_rc

class DiceRollController(QDialog, Ui_DiceRollWind):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # Remove the context help button from the title bar
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        rollButton = QPushButton(self.tr("&Roll"))
        rollButton.setDefault(True)

        self.buttonBox.addButton(rollButton, QDialogButtonBox.ActionRole)

        rollButton.clicked.connect(self.RollButtonPushed)
        self.buttonBox.rejected.connect(self.CloseButtonPushed)

    def Roll(self):
        result = 0
        d = 2
        if self.DiceTypeBox.currentText() == "d2":
            d = 2
        elif self.DiceTypeBox.currentText() == "d4":
            d = 4
        elif self.DiceTypeBox.currentText() == "d6":
            d = 6
        elif self.DiceTypeBox.currentText() == "d8":
            d = 8
        elif self.DiceTypeBox.currentText() == "d10":
            d = 10
        elif self.DiceTypeBox.currentText() == "d12":
            d = 12
        elif self.DiceTypeBox.currentText() == "d20":
            d = 20
        elif self.DiceTypeBox.currentText() == "d100":
            d = 100

        n = int(self.NumDiceEdit.text())
        mod = int(self.ModifierEdit.text())

        t = random.randint(1, (d + 1))
        
        for i in range(n):
            result += random.randint(1, (d + 1))
        result += mod

        # return result
        self.RollLabel.setText(str(result))

    def RollButtonPushed(self):
        pixmap = QPixmap(':/dSet/dice/' + self.DiceTypeBox.currentText() + '.png')
        self.RollLabel.setPixmap(pixmap)
        QTimer.singleShot(500, self.Roll)

        # r = self.Roll()

        # if r == 69:
        #     r = "Nice"
        # elif r == 420:
        #     r = "Blaze it"
        # else:
        #     r = str(r)

        # self.RollLabel.setText(str(r))        
        
    def CloseButtonPushed(self):
        self.DiceTypeBox.setCurrentText("d2")
        self.RollLabel.setText(str(0))
        self.NumDiceEdit.setText(str(1))