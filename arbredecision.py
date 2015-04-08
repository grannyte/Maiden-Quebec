import csv

from worldtest.enemy import *


class base_noeud():
    def __init__(self, type_noeud, valeure_a, valeure_b):
        self.type_noeud = type_noeud
        self.valeure_a = valeure_a
        self.valeure_b = valeure_b

    def evaluer(self, valeures):
        return self.type_noeud

    def loadfromarray(self, csvf):
        current = csvf.pop(0)
        self.type_noeud = int(current[0])
        self.valeure_a = int(current[1])
        self.valeure_b = int(current[2])

    def savetocsv(self, csvf):
        csvf.writerow([self.type_noeud, self.valeure_a, self.valeure_b])


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

    def loadfromarray(self, csvf):
        current = csvf.pop(0)
        self.type_noeud = int(current[0])
        self.valeure_a = int(current[1])
        self.valeure_b = int(current[2])
        self.gauche.loadfromarray(csvf)
        self.droite.loadfromarray(csvf)

    def savetocsv(self, csvf):
        csvf.writerow([self.type_noeud, self.valeure_a, self.valeure_b])
        self.gauche.savetocsv(csvf)
        self.droite.savetocsv(csvf)

    def evaluer(self, valeures):
        if self.operation(valeures):
            return self.gauche.evaluer(valeures)
        else:
            return self.droite.evaluer(valeures)


class ArbreMonster(BayesMonster):
    def __init__(self, map, enemy):
        BayesMonster.__init__(self, map, enemy)
        self.racine = noeud_decision(0, 0, 0,
                                     noeud_decision(0, 0, 0,
                                                    noeud_decision(0, 0, 0,
                                                                   noeud_decision(0, 0, 0,
                                                                                  base_noeud(0, 0, 0),
                                                                                  base_noeud(0, 0, 0)),
                                                                   noeud_decision(0, 0, 0,
                                                                                  base_noeud(0, 0, 0),
                                                                                  base_noeud(0, 0, 0))),
                                                    noeud_decision(0, 0, 0,
                                                                   noeud_decision(0, 0, 0,
                                                                                  base_noeud(0, 0, 0),
                                                                                  base_noeud(0, 0, 0)),
                                                                   noeud_decision(0, 0, 0,
                                                                                  base_noeud(0, 0, 0),
                                                                                  base_noeud(0, 0, 0)))),
                                     noeud_decision(0, 0, 0,
                                                    noeud_decision(0, 0, 0,
                                                                   noeud_decision(0, 0, 0,
                                                                                  base_noeud(0, 0, 0),
                                                                                  base_noeud(0, 0, 0)),
                                                                   noeud_decision(0, 0, 0,
                                                                                  base_noeud(0, 0, 0),
                                                                                  base_noeud(0, 0, 0))),
                                                    noeud_decision(0, 0, 0,
                                                                   noeud_decision(0, 0, 0,
                                                                                  base_noeud(0, 0, 0),
                                                                                  base_noeud(0, 0, 0)),
                                                                   noeud_decision(0, 0, 0,
                                                                                  base_noeud(0, 0, 0),
                                                                                  base_noeud(0, 0, 0)))))
        self.loadfromcsv("Monster1.M")
        self.savetocsv("Monster1.M")

    def loadfromcsv(self, csvn):
        read = csv.reader(open(csvn, 'r'))
        darrayfaitmoichier = []
        for row in read:
            darrayfaitmoichier.append(row)
        self.racine.loadfromarray(darrayfaitmoichier)

    def savetocsv(self, csvn):
        wtr = csv.writer(open(csvn, 'w'), delimiter=',', lineterminator='\n')
        self.racine.savetocsv(wtr)

    def update(self):
        valeures = [self.position.x, self.position.y, self.hp, self.hero.position.x, self.hero.position.y, self.hero.hp]
        retour = self.racine.evaluer(valeures)
        if retour == 1:
            self.schedule_movement(ForcedStep(UP), True)
        elif retour == 2:
            self.schedule_movement(ForcedStep(DOWN), True)
        elif retour == 3:
            self.schedule_movement(ForcedStep(RIGHT), True)
        elif retour == 4:
            self.schedule_movement(ForcedStep(LEFT), True)
        elif retour == 5:
            self.schedule_movement(Attack((self, self.position), (self.hero, self.hero.map_object.position)), True)
        elif retour == 6:
            self.schedule_movement(Defence((self, self.position), (self.hero, self.hero.map_object.position)), True)
        print("HERO:" + str(round(self.hero.hp)) + " MONSTER:" + str(round(self.hp, 0)))
        print("HERO EMOUSSER: " + str(self.hero.emousser) + " MONSTER EMOUSSER: " + str(self.emousser))
        if self.hp <= 1:
            print (u'Le monstre est mort.')
            self.destroy()
        if self.hero.hp <= 1:
            print("Vous etes mort")
            self.map.gameover()
        BayesMonster.update(self)

