from worldtest.enemy import *


class base_noeud():
    def __init__(self, type_noeud, valeure_a, valeure_b):
        self.type_noeud = type_noeud
        self.valeure_a = valeure_a
        self.valeure_b = valeure_b

    def evaluer(self, valeures):
        return self.type_noeud


class noeud_decision(base_noeud):
    def __init__(self, type_noeud, valeure_a, valeure_b, droite, gauche):
        base_noeud.__init__(self, type_noeud, valeure_a, valeure_b)
        self.droite = droite
        self.gauche = gauche

    def operation(self, tableau):
        if self.operation == 1:
            return tableau[self.valeure_a] > tableau[self.valeure_b]
        elif self.operation == 2:
            return tableau[self.valeure_a] >= tableau[self.valeure_b]
        elif self.operation == 3:
            return tableau[self.valeure_a] == tableau[self.valeure_b]
        elif self.operation == 4:
            return tableau[self.valeure_a] <= tableau[self.valeure_b]
        elif self.operation == 5:
            return tableau[self.valeure_a] < tableau[self.valeure_b]
        else:
            return tableau[self.valeure_a] != tableau[self.valeure_b]

    def evaluer(self, valeures):
        if self.operation(valeures):
            return self.gauche.evaluer(valeures)
        else:
            return self.droite.evaluer(valeures)



class Monster(BayesMonster):
    def __init__(self, map, hero):
        BayesMonster.__init__(self, map, hero)
        self.hp = HP_INITIAL

    def activate(self, party_avatar, direction):
        self.hp -= 10
        print(u'Attaque du monstre (-10) [' + str(self.hp) + '/' + str(HP_INITIAL) + ']')
        if (self.hp <= 0):
            print(u'Le monstre est mort.')
            self.destroy()

    def collide_with_party(self, party_avatar, direction):
        pass

    def update(self):
        pass