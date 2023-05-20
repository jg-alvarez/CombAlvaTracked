from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QColor
from gui.CT_gui import Ui_CT_gui
from character import Char

class AppController(QMainWindow, Ui_CT_gui):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        self.AddCharButton.clicked.connect(self.AddCharacterButtonPushed)
        self.UndoCharButton.clicked.connect(self.UndoCharacterButtonPushed)
        self.StartCombButton.clicked.connect(self.StartCombatButtonPushed)
        self.DealActionButton.clicked.connect(self.DealActionButtonPushed)
        self.NextTurnButton.clicked.connect(self.NextTurnButtonPushed)
        self.actionNew.triggered.connect(self.NewButtonPushed)
        
        self.turn = 0           # Index of active character
        self.round = 0          # Current round number
        self.charList = []      # List of characters
        self.i = 0              # Total number of characters
        
    def AddCharacterButtonPushed(self):
        if not self.CombatCheckBox.checkState() and self.CharEdit.text() and self.HPEdit.text() and self.ACEdit.text() and self.InitiativeEdit.text() and self.CondComboBox.currentText():
            self.i += 1

            self.charList.append(Char(self.CharEdit.text(), int(self.HPEdit.text()), int(self.ACEdit.text()), int(self.InitiativeEdit.text()), self.CondComboBox.currentText()))
            
            self.CharDataTable.insertRow(self.i - 1)
            self.CharDataTable.setItem(self.i - 1, 0, QTableWidgetItem(self.charList[self.i - 1].name))
            self.CharDataTable.setItem(self.i - 1, 1, QTableWidgetItem(str(self.charList[self.i - 1].MaxHP)))
            self.CharDataTable.setItem(self.i - 1, 2, QTableWidgetItem(str(self.charList[self.i - 1].AC)))
            self.CharDataTable.setItem(self.i - 1, 3, QTableWidgetItem(str(self.charList[self.i - 1].init)))
            self.CharDataTable.setItem(self.i - 1, 4, QTableWidgetItem(self.charList[self.i - 1].cond))

            # self.DmgDealtEdit.setText(self.charList[self.i - 1].name)

        self.CharEdit.setText("")
        self.HPEdit.setText("")
        self.ACEdit.setText("")
        self.InitiativeEdit.setText("")
        self.CondComboBox.setCurrentText("Normal")

    def UndoCharacterButtonPushed(self):
        if not self.CombatCheckBox.checkState():
            self.i -= 1
            if self.i >= 0:
                removedChar = self.charList.pop()

                self.CharDataTable.removeRow(self.i)
            else:
                self.i = 0

    def SortingKey(self, _e):
        return _e.init
    
    def StartCombatButtonPushed(self):
        if self.round == 0 and self.i > 0:
            self.CombatCheckBox.setCheckState(True)

            self.round = 1
            self.RoundNumber.setText(str(self.round))

            self.charList.sort(reverse = True, key = self.SortingKey)
            t = 0

            for n in self.charList:
                self.DmgTargetComboBox.addItem(n.name)
                self.CondTargetComboBox.addItem(n.name)
                self.DmgHealedComboBox.addItem(n.name)

                self.CharOrderTable.insertRow(t)

                name = QTableWidgetItem(n.name)
                HP = QTableWidgetItem(str(n.HP))
                AC = QTableWidgetItem(str(n.AC))
                init = QTableWidgetItem(str(n.init))
                cond = QTableWidgetItem(n.cond)

                if t == 0:
                    name.setBackground(QColor.fromRgbF(0,0,255, 0.5))
                    HP.setBackground(QColor.fromRgbF(0,0,255, 0.5))
                    AC.setBackground(QColor.fromRgbF(0,0,255, 0.5))
                    init.setBackground(QColor.fromRgbF(0,0,255, 0.5))
                    cond.setBackground(QColor.fromRgbF(0,0,255, 0.5))
                    self.CondDealtComboBox.setCurrentText(n.cond)
                if n.cond != "Normal":
                    name.setForeground(QColor.fromRgb(121,255,0))
                    HP.setForeground(QColor.fromRgb(121,255,0))
                    AC.setForeground(QColor.fromRgb(121,255,0))
                    init.setForeground(QColor.fromRgb(121,255,0))
                    cond.setForeground(QColor.fromRgb(121,255,0))

                self.CharOrderTable.setItem(t, 0, name)
                self.CharOrderTable.setItem(t, 1, HP)
                self.CharOrderTable.setItem(t, 2, AC)
                self.CharOrderTable.setItem(t, 3, init)
                self.CharOrderTable.setItem(t, 4, cond)

                t +=1

    def DealActionButtonPushed(self):
        if not self.charList[self.turn].permaDead:
            t = 0
            # Deals conditions
            for n in self.charList:
                # self.CondTargetComboBox.textActivated
                if n.name == self.CondTargetComboBox.currentText() and n.cond != self.CondDealtComboBox.currentText():
                    n.CondChanged(self.CondDealtComboBox.currentText())
                    
                    name = QTableWidgetItem(n.name)
                    HP = QTableWidgetItem(str(n.HP))
                    AC = QTableWidgetItem(str(n.AC))
                    init = QTableWidgetItem(str(n.init))
                    cond = QTableWidgetItem(n.cond)

                    if n.cond != "Normal" and n.cond != "Stable":
                        name.setForeground(QColor.fromRgb(121,255,0))
                        HP.setForeground(QColor.fromRgb(121,255,0))
                        AC.setForeground(QColor.fromRgb(121,255,0))
                        init.setForeground(QColor.fromRgb(121,255,0))
                        cond.setForeground(QColor.fromRgb(121,255,0))
                    elif n.cond == "Normal":
                        name.setForeground(QColor.fromRgb(0,0,0))
                        HP.setForeground(QColor.fromRgb(0,0,0))
                        AC.setForeground(QColor.fromRgb(0,0,0))
                        init.setForeground(QColor.fromRgb(0,0,0))
                        cond.setForeground(QColor.fromRgb(0,0,0))
                    elif n.cond == "Stable":
                        name.setForeground(QColor.fromRgb(0,0,255))
                        HP.setForeground(QColor.fromRgb(0,0,255))
                        AC.setForeground(QColor.fromRgb(0,0,255))
                        init.setForeground(QColor.fromRgb(0,0,255))
                        cond.setForeground(QColor.fromRgb(0,0,255))

                    if self.CondTargetComboBox.currentText() == self.charList[self.turn].name:
                        name.setBackground(QColor.fromRgbF(0,0,255, 0.5))
                        HP.setBackground(QColor.fromRgbF(0,0,255, 0.5))
                        AC.setBackground(QColor.fromRgbF(0,0,255, 0.5))
                        init.setBackground(QColor.fromRgbF(0,0,255, 0.5))
                        cond.setBackground(QColor.fromRgbF(0,0,255, 0.5))

                    self.CharOrderTable.setItem(t, 0, name)
                    self.CharOrderTable.setItem(t, 1, HP)
                    self.CharOrderTable.setItem(t, 2, AC)
                    self.CharOrderTable.setItem(t, 3, init)
                    self.CharOrderTable.setItem(t, 4, cond)

                t +=1

            # Deals damage
            t = 0
            for n in self.charList:
                if int(self.DmgDealtEdit.text()) and n.name == self.DmgTargetComboBox.currentText() and n.cond != "Perma Dead":
                    n.DmgReceived(int(self.DmgDealtEdit.text()))
                    
                    name = QTableWidgetItem(n.name)
                    HP = QTableWidgetItem(str(n.HP))
                    AC = QTableWidgetItem(str(n.AC))
                    init = QTableWidgetItem(str(n.init))
                    cond = QTableWidgetItem(n.cond)

                    if n.cond == "Perma Dead" or n.cond == "Downed":
                        name.setForeground(QColor.fromRgb(255,0,0))
                        HP.setForeground(QColor.fromRgb(255,0,0))
                        AC.setForeground(QColor.fromRgb(255,0,0))
                        init.setForeground(QColor.fromRgb(255,0,0))
                        cond.setForeground(QColor.fromRgb(255,0,0))
                    elif n.cond == "Stable":
                        name.setForeground(QColor.fromRgb(0,0,255))
                        HP.setForeground(QColor.fromRgb(0,0,255))
                        AC.setForeground(QColor.fromRgb(0,0,255))
                        init.setForeground(QColor.fromRgb(0,0,255))
                        cond.setForeground(QColor.fromRgb(0,0,255))
                    elif n.cond != "Normal":
                        name.setForeground(QColor.fromRgb(121,255,0))
                        HP.setForeground(QColor.fromRgb(121,255,0))
                        AC.setForeground(QColor.fromRgb(121,255,0))
                        init.setForeground(QColor.fromRgb(121,255,0))
                        cond.setForeground(QColor.fromRgb(121,255,0))

                    if self.DmgTargetComboBox.currentText() == self.charList[self.turn].name:
                        name.setBackground(QColor.fromRgbF(0,0,255, 0.5))
                        HP.setBackground(QColor.fromRgbF(0,0,255, 0.5))
                        AC.setBackground(QColor.fromRgbF(0,0,255, 0.5))
                        init.setBackground(QColor.fromRgbF(0,0,255, 0.5))
                        cond.setBackground(QColor.fromRgbF(0,0,255, 0.5))

                    self.CharOrderTable.setItem(t, 0, name)
                    self.CharOrderTable.setItem(t, 1, HP)
                    self.CharOrderTable.setItem(t, 2, AC)
                    self.CharOrderTable.setItem(t, 3, init)
                    self.CharOrderTable.setItem(t, 4, cond)

                t +=1

            # Deals healing
            # flagActionReceived = 0
            t = 0
            for n in self.charList:
                if int(self.DmgHealedEdit.text()) and n.name == self.DmgHealedComboBox.currentText() and n.cond != "Perma Dead":
                    n.DmgHealed(int(self.DmgHealedEdit.text()))
                #     flagActionReceived = 1

                # if flagActionReceived:
                    name = QTableWidgetItem(n.name)
                    HP = QTableWidgetItem(str(n.HP))
                    AC = QTableWidgetItem(str(n.AC))
                    init = QTableWidgetItem(str(n.init))
                    cond = QTableWidgetItem(n.cond)

                    if n.cond == "Normal":
                        name.setForeground(QColor.fromRgb(0,0,0))
                        HP.setForeground(QColor.fromRgb(0,0,0))
                        AC.setForeground(QColor.fromRgb(0,0,0))
                        init.setForeground(QColor.fromRgb(0,0,0))
                        cond.setForeground(QColor.fromRgb(0,0,0))
                    elif n.cond == "Stable":
                        name.setForeground(QColor.fromRgb(0,0,255))
                        HP.setForeground(QColor.fromRgb(0,0,255))
                        AC.setForeground(QColor.fromRgb(0,0,255))
                        init.setForeground(QColor.fromRgb(0,0,255))
                        cond.setForeground(QColor.fromRgb(0,0,255))
                    elif n.cond == "Downed":
                        name.setForeground(QColor.fromRgb(255,0,0))
                        HP.setForeground(QColor.fromRgb(255,0,0))
                        AC.setForeground(QColor.fromRgb(255,0,0))
                        init.setForeground(QColor.fromRgb(255,0,0))
                        cond.setForeground(QColor.fromRgb(255,0,0))
                    else:
                        name.setForeground(QColor.fromRgb(121,255,0))
                        HP.setForeground(QColor.fromRgb(121,255,0))
                        AC.setForeground(QColor.fromRgb(121,255,0))
                        init.setForeground(QColor.fromRgb(121,255,0))
                        cond.setForeground(QColor.fromRgb(121,255,0))

                    if self.DmgHealedComboBox.currentText() == self.charList[self.turn].name:
                        name.setBackground(QColor.fromRgbF(0,0,255, 0.5))
                        HP.setBackground(QColor.fromRgbF(0,0,255, 0.5))
                        AC.setBackground(QColor.fromRgbF(0,0,255, 0.5))
                        init.setBackground(QColor.fromRgbF(0,0,255, 0.5))
                        cond.setBackground(QColor.fromRgbF(0,0,255, 0.5))

                    self.CharOrderTable.setItem(t, 0, name)
                    self.CharOrderTable.setItem(t, 1, HP)
                    self.CharOrderTable.setItem(t, 2, AC)
                    self.CharOrderTable.setItem(t, 3, init)
                    self.CharOrderTable.setItem(t, 4, cond)

                t +=1

            self.CondDealtComboBox.setCurrentText(self.charList[self.turn].cond)
            self.CondTargetComboBox.setCurrentText(self.charList[self.turn].name)
            self.DmgDealtEdit.setText("0")
            self.DmgTargetComboBox.setCurrentText(self.charList[self.turn].name)
            self.DmgHealedEdit.setText("0")
            self.DmgHealedComboBox.setCurrentText(self.charList[self.turn].name)

    def NextTurnButtonPushed(self):
        if self.turn < (self.i - 1):
            self.turn += 1
        else:
            self.turn = 0
            self.round += 1
            self.RoundNumber.setText(str(self.round))

        if self.turn == 0:
            t = self.i - 1
        else:
            t = self.turn - 1

        nameB = QTableWidgetItem(self.charList[t].name)
        HPB = QTableWidgetItem(str(self.charList[t].HP))
        ACB = QTableWidgetItem(str(self.charList[t].AC))
        initB = QTableWidgetItem(str(self.charList[t].init))
        condB = QTableWidgetItem(self.charList[t].cond)
        
        if (int(t) % 2) != 0:
            nameB.setBackground(QColor.fromRgb(245,245,245))
            HPB.setBackground(QColor.fromRgb(245,245,245))
            ACB.setBackground(QColor.fromRgb(245,245,245))
            initB.setBackground(QColor.fromRgb(245,245,245))
            condB.setBackground(QColor.fromRgb(245,245,245))
        else:
            nameB.setBackground(QColor.fromRgb(255,255,255))
            HPB.setBackground(QColor.fromRgb(255,255,255))
            ACB.setBackground(QColor.fromRgb(255,255,255))
            initB.setBackground(QColor.fromRgb(255,255,255))
            condB.setBackground(QColor.fromRgb(255,255,255))

        if self.charList[t].cond == "Normal":
            nameB.setForeground(QColor.fromRgb(0,0,0))
            HPB.setForeground(QColor.fromRgb(0,0,0))
            ACB.setForeground(QColor.fromRgb(0,0,0))
            initB.setForeground(QColor.fromRgb(0,0,0))
            condB.setForeground(QColor.fromRgb(0,0,0))
        elif self.charList[t].cond == "Stable":
            nameB.setForeground(QColor.fromRgb(0,0,255))
            HPB.setForeground(QColor.fromRgb(0,0,255))
            ACB.setForeground(QColor.fromRgb(0,0,255))
            initB.setForeground(QColor.fromRgb(0,0,255))
            condB.setForeground(QColor.fromRgb(0,0,255))
        elif self.charList[t].cond == "Downed" or self.charList[t].cond == "Perma Dead":
            nameB.setForeground(QColor.fromRgb(255,0,0))
            HPB.setForeground(QColor.fromRgb(255,0,0))
            ACB.setForeground(QColor.fromRgb(255,0,0))
            initB.setForeground(QColor.fromRgb(255,0,0))
            condB.setForeground(QColor.fromRgb(255,0,0))
        else:
            nameB.setForeground(QColor.fromRgb(121,255,0))
            HPB.setForeground(QColor.fromRgb(121,255,0))
            ACB.setForeground(QColor.fromRgb(121,255,0))
            initB.setForeground(QColor.fromRgb(121,255,0))
            condB.setForeground(QColor.fromRgb(121,255,0))

        self.CharOrderTable.setItem(t, 0, nameB)
        self.CharOrderTable.setItem(t, 1, HPB)
        self.CharOrderTable.setItem(t, 2, ACB)
        self.CharOrderTable.setItem(t, 3, initB)
        self.CharOrderTable.setItem(t, 4, condB)

        if self.charList[self.turn].permaDead:
            self.NextTurnButtonPushed()
        else:
            name = QTableWidgetItem(self.charList[self.turn].name)
            HP = QTableWidgetItem(str(self.charList[self.turn].HP))
            AC = QTableWidgetItem(str(self.charList[self.turn].AC))
            init = QTableWidgetItem(str(self.charList[self.turn].init))
            cond = QTableWidgetItem(self.charList[self.turn].cond)
            
            name.setBackground(QColor.fromRgbF(0,0,255, 0.5))
            HP.setBackground(QColor.fromRgbF(0,0,255, 0.5))
            AC.setBackground(QColor.fromRgbF(0,0,255, 0.5))
            init.setBackground(QColor.fromRgbF(0,0,255, 0.5))
            cond.setBackground(QColor.fromRgbF(0,0,255, 0.5))

            if self.charList[self.turn].cond == "Normal":
                name.setForeground(QColor.fromRgb(0,0,0))
                HP.setForeground(QColor.fromRgb(0,0,0))
                AC.setForeground(QColor.fromRgb(0,0,0))
                init.setForeground(QColor.fromRgb(0,0,0))
                cond.setForeground(QColor.fromRgb(0,0,0))
            elif self.charList[self.turn].cond == "Stable":
                name.setForeground(QColor.fromRgb(0,0,255))
                HP.setForeground(QColor.fromRgb(0,0,255))
                AC.setForeground(QColor.fromRgb(0,0,255))
                init.setForeground(QColor.fromRgb(0,0,255))
                cond.setForeground(QColor.fromRgb(0,0,255))
            elif self.charList[self.turn].cond == "Downed":
                name.setForeground(QColor.fromRgb(255,0,0))
                HP.setForeground(QColor.fromRgb(255,0,0))
                AC.setForeground(QColor.fromRgb(255,0,0))
                init.setForeground(QColor.fromRgb(255,0,0))
                cond.setForeground(QColor.fromRgb(255,0,0))
            else:
                name.setForeground(QColor.fromRgb(121,255,0))
                HP.setForeground(QColor.fromRgb(121,255,0))
                AC.setForeground(QColor.fromRgb(121,255,0))
                init.setForeground(QColor.fromRgb(121,255,0))
                cond.setForeground(QColor.fromRgb(121,255,0))

            self.CharOrderTable.setItem(self.turn, 0, name)
            self.CharOrderTable.setItem(self.turn, 1, HP)
            self.CharOrderTable.setItem(self.turn, 2, AC)
            self.CharOrderTable.setItem(self.turn, 3, init)
            self.CharOrderTable.setItem(self.turn, 4, cond)

            self.CondDealtComboBox.setCurrentText(self.charList[self.turn].cond)
            self.CondTargetComboBox.setCurrentText(self.charList[self.turn].name)
            self.DmgDealtEdit.setText("0")
            self.DmgTargetComboBox.setCurrentText(self.charList[self.turn].name)
            self.DmgHealedEdit.setText("0")
            self.DmgHealedComboBox.setCurrentText(self.charList[self.turn].name)

    def NewButtonPushed(self):
        self.charList.clear()

        for n in range((self.i)- 1, -1, -1):
            self.CharDataTable.removeRow(n)
            self.CharOrderTable.removeRow(n)
            self.DmgTargetComboBox.removeItem(n)
            self.CondTargetComboBox.removeItem(n)
            self.DmgHealedComboBox.removeItem(n)
            
        self.i = 0
        self.round = 0
        self.turn = 0
        self.CombatCheckBox.setCheckState(False)
