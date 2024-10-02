class Char:
    def __init__(self, _name, _MaxHP, _HP, _AC, _init, _cond):
        self.name = _name
        self.MaxHP = _MaxHP
        self.HP = _HP
        self.AC = _AC
        self.init = _init
        self.cond = _cond
        self.permaDead = False

        self.condList = ["Normal", "Prone", "Hiden", "Grappled", "Charmed", "Frightened", "Poisoned", "Blind", "Incapacited", "Paralised", "Petrified", "Restrained", "Stunned", "Unconscious", "Invisible", "Deafened", "Stable", "Revived", "Downed", "Perma Dead"]

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