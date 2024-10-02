from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QColor
import json
from copy import deepcopy
from gui.CT_gui import Ui_CT_gui
from dicerollcontroller import DiceRollController
from character import Char

class AppController(QMainWindow, Ui_CT_gui):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # In-program
        self.MaxHPEdit.textChanged.connect(self.MaxHPEdited)
        self.CharDataTable.cellChanged.connect(self.EditCharDataTable)
        self.AddCharButton.clicked.connect(self.AddCharacterButtonPushed)
        self.UndoCharButton.clicked.connect(self.RemoveCharacterButtonPushed)
        self.StartCombButton.clicked.connect(self.StartCombatButtonPushed)
        self.DealActionButton.clicked.connect(self.DealActionButtonPushed)
        self.NextTurnButton.clicked.connect(self.NextTurnButtonPushed)
        self.EndCombatButton.clicked.connect(self.EndCombatButtonPushed)
        # Home menu
        self.actionNew.triggered.connect(self.NewButtonPushed)
        self.actionSave.triggered.connect(self.writeSaveFile)
        self.actionSave_as.triggered.connect(self.writeSaveAsFile)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionDice.triggered.connect(self.DiceRollWindowOpen)
        
        self.turn = 0           # Index of active character
        self.round = 0          # Current round number
        self.charList = []      # List of characters
        self.charListOG = []    # List of characters Unordered
        self.i = 0              # Total number of characters

        self.saved = False
        self.saveFile = None

        self.diceRoll = DiceRollController()

    def MaxHPEdited(self):
        if self.CurrentHPEdit.text() == self.MaxHPEdit.text()[:-1]:
            self.CurrentHPEdit.setText(self.MaxHPEdit.text())
        
    def AddCharacterButtonPushed(self):
        if not self.CombatCheckBox.checkState() and self.CharEdit.text() and self.MaxHPEdit.text() and self.CurrentHPEdit.text() and self.ACEdit.text() and self.InitiativeEdit.text() and self.CondComboBox.currentText():
            self.i += 1

            self.charList.append(Char(self.CharEdit.text(), int(self.MaxHPEdit.text()), int(self.CurrentHPEdit.text()), int(self.ACEdit.text()), int(self.InitiativeEdit.text()), self.CondComboBox.currentText()))
            
            self.CharDataTable.insertRow(self.i - 1)
            self.CharDataTable.setItem(self.i - 1, 0, QTableWidgetItem(self.charList[self.i - 1].name))
            self.CharDataTable.setItem(self.i - 1, 1, QTableWidgetItem(str(self.charList[self.i - 1].MaxHP)))
            self.CharDataTable.setItem(self.i - 1, 2, QTableWidgetItem(str(self.charList[self.i - 1].HP)))
            self.CharDataTable.setItem(self.i - 1, 3, QTableWidgetItem(str(self.charList[self.i - 1].AC)))
            self.CharDataTable.setItem(self.i - 1, 4, QTableWidgetItem(str(self.charList[self.i - 1].init)))
            self.CharDataTable.setItem(self.i - 1, 5, QTableWidgetItem(self.charList[self.i - 1].cond))

            # self.DmgDealtEdit.setText(self.charList[self.i - 1].name)

        self.CharEdit.setText("")
        self.MaxHPEdit.setText("")
        self.CurrentHPEdit.setText("")
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

    def RemoveCharacterButtonPushed(self):
        if not self.CombatCheckBox.checkState():
            self.i -= 1
            if (self.i >= 0) and (self.CharDataTable.currentRow() >= 0):
                removedChar = self.charList.pop(self.CharDataTable.currentRow())

                self.CharDataTable.removeRow(self.CharDataTable.currentRow())
            elif self.i >= 0:
                removedChar = self.charList.pop()

                self.CharDataTable.removeRow(self.i)
            else:
                self.i = 0

    def EditCharDataTable(self, row, column):
        if not self.CombatCheckBox.checkState() and self.i:
            if column == 0:
                self.charList[row].name = self.CharDataTable.item(row, column).text()
            elif column == 1:
                self.charList[row].MaxHP = int(self.CharDataTable.item(row, column).text())
            elif column == 2:
                self.charList[row].HP = int(self.CharDataTable.item(row, column).text())
            elif column == 3:
                self.charList[row].AC = int(self.CharDataTable.item(row, column).text())
            elif column == 4:
                self.charList[row].init = int(self.CharDataTable.item(row, column).text())
            elif column == 5:
                if self.CharDataTable.item(row, column).text() in self.charList[row].condList:
                    self.charList[row].cond = self.CharDataTable.item(row, column).text()
                else:
                    self.CharDataTable.item(row, column).setText(self.charList[row].cond)
        elif self.CombatCheckBox.checkState():
            self.CharDataTable.item(row, 0).setText(self.charListOG[row].name)
            self.CharDataTable.item(row, 1).setText(str(self.charListOG[row].MaxHP))
            self.CharDataTable.item(row, 2).setText(str(self.charListOG[row].HP))
            self.CharDataTable.item(row, 3).setText(str(self.charListOG[row].AC))
            self.CharDataTable.item(row, 4).setText(str(self.charListOG[row].init))
            self.CharDataTable.item(row, 5).setText(self.charListOG[row].cond)

    def SortingKeyInit(self, _e):
        return _e.init
    
    def StartCombatButtonPushed(self):
        if self.round == 0 and self.i > 0:
            self.CombatCheckBox.setCheckState(True)

            self.round = 1
            self.RoundNumber.setText(str(self.round))

            self.charListOG.clear()
            self.charListOG = deepcopy(self.charList)
            # self.charListOG = self.charList.copy()
            self.charList.sort(reverse = True, key = self.SortingKeyInit)
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
                    else:
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
        if self.CombatCheckBox.checkState():
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
        if self.CombatCheckBox.checkState():
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

    def EndCombatButtonPushed(self):
        if self.CombatCheckBox.checkState():
            self.CombatCheckBox.setCheckState(False)
            
            for n in range((self.i)- 1, -1, -1):
                self.CharDataTable.removeRow(n)
                self.CharOrderTable.removeRow(n)
                self.DmgTargetComboBox.removeItem(n)
                self.CondTargetComboBox.removeItem(n)
                self.DmgHealedComboBox.removeItem(n)

            charListTemp1 = []
            charListTemp2 = []
            charListTemp3 = []
            for char in self.charListOG:
                charListTemp1.append(char.name)
            for char in self.charList:
                charListTemp2.append(charListTemp1.index(char.name))
            for index in charListTemp2:
                charListTemp3.append(self.charList[index])

            self.charList = charListTemp3

            for n, char in enumerate(self.charList):
                self.CharDataTable.insertRow(n)
                self.CharDataTable.setItem(n, 0, QTableWidgetItem(char.name))
                self.CharDataTable.setItem(n, 1, QTableWidgetItem(str(char.MaxHP)))
                self.CharDataTable.setItem(n, 2, QTableWidgetItem(str(char.HP)))
                self.CharDataTable.setItem(n, 3, QTableWidgetItem(str(char.AC)))
                self.CharDataTable.setItem(n, 4, QTableWidgetItem(str(char.init)))
                self.CharDataTable.setItem(n, 5, QTableWidgetItem(char.cond))

            self.round = 0
            self.turn = 0

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

    def DiceRollWindowOpen(self):
        self.diceRoll.show()

    def writeSaveFile(self):
        Combat = {
            "turn": self.turn,
            "round": self.round,
            "combStarted": self.CombatCheckBox.checkState()
        }
        sL = [Combat]
        
        if self.charListOG:
            charListTemp1 = []
            charListTemp2 = []
            charListTemp3 = []
            for char in self.charListOG:
                charListTemp1.append(char.name)
            for char in self.charList:
                charListTemp2.append(charListTemp1.index(char.name))
            for index in charListTemp2:
                charListTemp3.append(self.charList[index])

            self.charList = charListTemp3
        
        for char in self.charList:
            dicChar = {
                'Name':char.name,
                'MaxHP':char.MaxHP,
                'HP':char.HP,
                'AC':char.AC,
                'init':char.init,
                'cond':char.cond,
                'permaDead':char.permaDead
            }

            sL.append(dicChar)

        if not self.saved:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(None, "Save File", "", "Json Files (*.json);;All Files (*)", options=options)
            if file_name:
                try:
                    with open(file_name, 'w', encoding='utf-8') as file:
                        json.dump(sL, file, indent=4)
                    self.saved = True
                    self.saveFile = file_name
                    print("File saved successfully.")
                except Exception as e:
                    print(f"Error saving file: {e}")
        else:
            with open(self.saveFile, 'w', encoding='utf-8') as file:
                json.dump(sL, file, indent=4)
            print("File saved successfully.")

    def writeSaveAsFile(self):
        Combat = {
            "turn": self.turn,
            "round": self.round,
            "combStarted": self.CombatCheckBox.checkState()
        }
        sL = [Combat]
        
        if self.charListOG:
            charListTemp1 = []
            charListTemp2 = []
            charListTemp3 = []
            for char in self.charListOG:
                charListTemp1.append(char.name)
            for char in self.charList:
                charListTemp2.append(charListTemp1.index(char.name))
            for index in charListTemp2:
                charListTemp3.append(self.charList[index])

            self.charList = charListTemp3
        
        for char in self.charList:
            dicChar = {
                'Name':char.name,
                'MaxHP':char.MaxHP,
                'HP':char.HP,
                'AC':char.AC,
                'init':char.init,
                'cond':char.cond,
                'permaDead':char.permaDead
            }

            sL.append(dicChar)

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(None, "Save File", "", "Json Files (*.json);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as file:
                    json.dump(sL, file, indent=4)
                self.saved = True
                self.saveFile = file_name
                print("File saved successfully.")
            except Exception as e:
                print(f"Error saving file: {e}")
        
    def openFile(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Open File", "", "Json Files (*.json);;All files (*)")
        if file_path:
            self.NewButtonPushed()

            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

                # ---------------------------------------------------------------------
                # Mudar forma como adiciono pra usando as funções já existentes
                for n in range(1, len(data)):
                    charOpen = Char(data[n]["Name"], data[n]["MaxHP"], data[n]["HP"], data[n]["AC"], data[n]["init"],data[n]["cond"])
                    charOpen.permaDead = data[n]["permaDead"]
                    self.charList.append(charOpen)

                    self.CharDataTable.insertRow(n - 1)
                    self.CharDataTable.setItem(n - 1, 0, QTableWidgetItem(charOpen.name))
                    self.CharDataTable.setItem(n - 1, 1, QTableWidgetItem(str(charOpen.MaxHP)))
                    self.CharDataTable.setItem(n - 1, 2, QTableWidgetItem(str(charOpen.HP)))
                    self.CharDataTable.setItem(n - 1, 3, QTableWidgetItem(str(charOpen.AC)))
                    self.CharDataTable.setItem(n - 1, 4, QTableWidgetItem(str(charOpen.init)))
                    self.CharDataTable.setItem(n - 1, 5, QTableWidgetItem(charOpen.cond))

                self.i = len(self.charList)

                # ---------------------------------------------------------------------
                if data[0]["combStarted"]:
                    self.StartCombatButtonPushed()
                    
                    while self.turn != data[0]["turn"]:
                        self.NextTurnButtonPushed()

                    self.round = data[0]["round"]
                    self.RoundNumber.setText(str(self.round))
                    
                # ---------------------------------------------------------------------
                self.saved = True
                self.saveFile = file_path
                
            print("file opened")
        else:
            print("No file selected")

    def closeEvent(self, _event):
        self.diceRoll.close()
        _event.accept()
