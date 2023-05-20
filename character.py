class Char:
    def __init__(self, name, HP, AC, init, cond):
        self.name = name
        self.MaxHP = HP
        self.HP = HP
        self.AC = AC
        self.init = init
        self.cond = cond
        self.permaDead = False

    def DmgReceived(self, _dmg):
        self.HP -= _dmg

        if self.HP <= -self.MaxHP:
            self.CondChanged("Perma Dead")
            self.permaDead = True
        elif self.HP <= 0:
            self.CondChanged("Downed")

    def DmgHealed(self, _dmg):
        self.HP += _dmg

        if self.HP == 0:
            self.CondChanged("Stable")
        elif (self.HP > 0) and ((self.HP - _dmg) <= 0):
            self.CondChanged("Normal")

    def CondChanged(self, _cond):
        if  self.cond != "Perma Dead":
            if self.cond == "Downed" and _cond == "Stable":
                self.HP = 0
                
            self.cond = _cond
        elif  _cond == "Revived":
            self.cond = "Normal"
            self.HP = 1
            self.permaDead = False