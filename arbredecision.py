import csv
import os.path
import math

import librpg.util

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
        self.valeure_a = max(min(int(current[1]), 8), 0)
        self.valeure_b = max(min(int(current[2]), 8), 0)

    def savetocsv(self, csvf):
        csvf.writerow([self.type_noeud, self.valeure_a, self.valeure_b])


class noeud_decision(base_noeud):
    GREATER_THAN = 1
    GREATER_OR_EQUAL = 2
    EQUAL = 3
    LESSER_OR_EQUAL = 4
    LESSER = 5
    NOT_EQUAL = 6

    def __init__(self, type_noeud, valeure_a, valeure_b, droite, gauche):
        base_noeud.__init__(self, type_noeud, valeure_a, valeure_b)
        self.droite = droite
        self.gauche = gauche

    def operation(self, tableau):
        if self.type_noeud == 1:
            return tableau[self.valeure_a] > tableau[self.valeure_b]
        elif self.type_noeud == 2:
            return tableau[self.valeure_a] >= tableau[self.valeure_b]
        elif self.type_noeud == 3:
            return tableau[self.valeure_a] == tableau[self.valeure_b]
        elif self.type_noeud == 4:
            return tableau[self.valeure_a] <= tableau[self.valeure_b]
        elif self.type_noeud == 5:
            return tableau[self.valeure_a] < tableau[self.valeure_b]
        elif self.type_noeud == 6:
            return tableau[self.valeure_a] > (tableau[self.valeure_b]-1)
        elif self.type_noeud == 7:
            return tableau[self.valeure_a] >= (tableau[self.valeure_b]-1)
        elif self.type_noeud == 8:
            return tableau[self.valeure_a] <= (tableau[self.valeure_b]-1)
        elif self.type_noeud == 9:
            return tableau[self.valeure_a] < (tableau[self.valeure_b]-1)
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
        BayesMonster.__init__(self, map, enemy, 'Rhulk.png')
        self.initarbre()
        self.loadfromcsv("Monster0.M")
        self.actual = 0
        self.status = []
        self.enemy = enemy
        self.generation = 12
        self.harshness = 0.001
        self.bonus = 0.0
        pfile = open("Trace.t", 'rb')
        read = csv.reader(pfile)
        csvarray = []
        for row in read:
            linearray = []
            for nb in row:
                linearray.append(float(nb))
                self.generation = float(nb)
            csvarray.append(linearray)
        pfile.close()
        self.lpfile = open("Trace.t", 'w')
        self.lwtr = csv.writer(self.lpfile, delimiter=',', lineterminator='\n')
        for row in csvarray:
            self.lwtr.writerow(row)
            print(row)
        self.tick = 0
        self.lastpos = librpg.util.Position(8, 8)

    def initarbre(self):
        self.racine = noeud_decision(noeud_decision.LESSER, 0, 2,
                                     noeud_decision(noeud_decision.NOT_EQUAL, 1, 3,
                                                    noeud_decision(noeud_decision.LESSER, 1, 3,
                                                                   noeud_decision(0, 0, 0,
                                                                                  base_noeud(4, 0, 0),
                                                                                  base_noeud(4, 0, 0)),
                                                                   noeud_decision(0, 0, 0,
                                                                                  base_noeud(3, 0, 0),
                                                                                  base_noeud(3, 0, 0))),
                                                    noeud_decision(noeud_decision.LESSER, 1, 3,
                                                                   noeud_decision(0, 0, 0,
                                                                                  base_noeud(1, 0, 0),
                                                                                  base_noeud(1, 0, 0)),
                                                                   noeud_decision(0, 0, 0,
                                                                                  base_noeud(2, 0, 0),
                                                                                  base_noeud(2, 0, 0)))),
                                     noeud_decision(noeud_decision.GREATER_THAN, 1, 3,
                                                    noeud_decision(0, 0, 0,
                                                                   noeud_decision(0, 0, 0,
                                                                                  base_noeud(3, 0, 0),
                                                                                  base_noeud(5, 0, 0)),
                                                                   noeud_decision(5, 1, 3,
                                                                                  base_noeud(4, 0, 0),
                                                                                  base_noeud(3, 0, 0))),
                                                    noeud_decision(0, 0, 0,
                                                                   noeud_decision(0, 0, 2,
                                                                                  base_noeud(3, 0, 0),
                                                                                  base_noeud(3, 0, 0)),
                                                                   noeud_decision(0, 0, 2,
                                                                                  base_noeud(4, 0, 0),
                                                                                  base_noeud(3, 0, 0)))))

    def loadfromcsv(self, csvn):
        if os.path.isfile(csvn):
            pfile = open(csvn, 'rb')
            read = csv.reader(pfile)
            darrayfaitmoichier = []
            for row in read:
                darrayfaitmoichier.append(row)
            self.racine.loadfromarray(darrayfaitmoichier)
            pfile.close()
        else:
            self.initarbre()

    def savetocsv(self, csvn):
        pfile = open(csvn, 'wb')
        wtr = csv.writer(pfile, delimiter=',', lineterminator='\n')
        self.racine.savetocsv(wtr)
        pfile.close()

    def update(self):
        self.tick += 1
        minpos = librpg.util.Position(8, 8)
        mindist = 8
        for obj in self.map.objects:
            pos = obj.position - self.position
            dist = abs(pos.x) + abs(pos.y)
            if dist < mindist:
                mindist = dist
                minpos = pos
        valeures = [self.position.x, self.position.y, self.enemy.position.x, self.enemy.position.y, self.hp,
                    self.enemy.hp,
                    minpos.x, minpos.y]
        retour = self.racine.evaluer(valeures)
        if self.lastpos != self.position:
            self.bonus += 0.1
            self.lastpos = self.position
        elif math.sqrt(math.pow(abs(self.position.x-self.enemy.position.x), 2)+math.pow(abs(self.position.y-self.enemy.position.y), 2)) > 1:
            self.bonus -= 0.1
        if retour == 1:
            self.schedule_movement(ForcedStep(UP), True)
            self.bonus += 0.01
        elif retour == 2:
            self.schedule_movement(ForcedStep(DOWN), True)
            self.bonus += 0.01
        elif retour == 3:
            self.schedule_movement(ForcedStep(RIGHT), True)
            self.bonus += 0.01
        elif retour == 4:
            self.schedule_movement(ForcedStep(LEFT), True)
            self.bonus += 0.01
        elif retour == 5:
            self.schedule_movement(Defence((self, self.position), (self.enemy, self.enemy.position)), True)
        else:
            self.schedule_movement(Attack((self, self.position), (self.enemy, self.enemy.position)), True)
        BayesMonster.update(self)
        if self.simulation:
            if self.hp <= 1:
                print ("l'arbre de decision est mort")
                self.algogenetique()

            if self.hero.hp <= 1:
                print("Le monstre est mort")
                self.algogenetique()

            if self.tick >= 1050:
                print("Le monstre est un trouillard")
                self.algogenetique()

    def algogenetique(self):
        self.tick = 0
        name = "Monster"
        name += str(self.actual)
        name += ".M"
        if not (os.path.isfile(name)):
            self.savetocsv(name)
        self.status.append(self.hp - self.enemy.hp * 2 + self.bonus)
        self.bonus = 0.0
        if self.enemy.hp == 100:
            self.status[self.actual] -= 100
        if self.actual >= 20:
            self.generation += 1
            outgoing = list(self.status)
            outgoing.append(self.generation)
            self.lwtr.writerow(outgoing)
            ostatus = list(self.status)
            ostatus.sort()
            maxval = ostatus[len(ostatus) - 1]
            ostatus = ostatus[-len(self.status) / 2:]
            print(ostatus)
            time.sleep(10)
            self.actual = 0
            minval = ostatus[:-1]
            li = 0
            for v in self.status:
                li += 1
                if ostatus.__contains__(v):
                    name7 = "Monster"
                    name7 += str(li)
                    name7 += ".M"
                    if os.path.isfile(name7):
                        pfile = open(name7, 'rb')
                        read = csv.reader(pfile)
                        csvarray = []
                        for row in read:
                            linearray = []
                            for nb in row:
                                linearray.append(nb)
                            csvarray.append(linearray)
                        pfile.close()
                        best = self.status.index(maxval)
                        if v != minval:
                            name4 = "Monster"
                            name4 += str(best)
                            name4 += ".M"
                            pfile = open(name4, 'rb')
                            read = csv.reader(pfile)
                            csvarrayb = []
                            for row in read:
                                linearray = []
                                for nb in row:
                                    linearray.append(nb)
                                csvarrayb.append(linearray)
                            pfile.close()
                            randresult = random.randrange(1)
                            if randresult == 1:
                                csvarray = csvarray[len(csvarray) / 2:] + csvarrayb[-len(csvarrayb) / 2:]
                            else:
                                csvarray = csvarray[len(csvarrayb) / 2:] + csvarrayb[:-len(csvarray) / 2]
                            for i in range(3):
                                r = random.randrange(len(csvarray))
                                b = csvarray[r]
                                rb = random.randrange(len(b))
                                csvarray[r][rb] = random.randrange(9)
                            self.racine.loadfromarray(csvarray)
                            if name7 == "Monster20.M":
                                print("After Simple Modification")
                            self.savetocsv(name7)
                        elif v == minval:
                            randresult = random.randrange(1)
                            bostatus = list(self.status)
                            bostatus.sort()
                            bostatus = bostatus[:2]
                            name3 = "Monster"
                            name3 += str(best)
                            name3 += ".M"
                            pfile = open(name3, 'rb')
                            read = csv.reader(pfile)
                            csvarrayb = []
                            for row in read:
                                linearray = []
                                for nb in row:
                                    linearray.append(nb)
                                csvarrayb.append(linearray)
                            pfile.close()
                            name4 = "Monster"
                            name4 += str(bostatus[1])
                            name4 += ".M"
                            pfile = open(name4, 'rb')
                            read = csv.reader(pfile)
                            csvarray = []
                            for row in read:
                                linearray = []
                                for nb in row:
                                    linearray.append(nb)
                                csvarray.append(linearray)
                            pfile.close()
                            csvarrayc = []
                            if randresult == 1:
                                csvarrayc = csvarray[:-len(csvarray) / 2] + csvarrayb[-len(csvarrayb) / 2:]
                            else:
                                csvarrayc = csvarray[-len(csvarrayb) / 2:] + csvarrayb[:-len(csvarray) / 2]
                            self.racine.loadfromarray(csvarrayc)
                            name2 = "Monster"
                            name2 += str(li)
                            name2 += ".M"
                            if name2 == "Monster20.M":
                                print("After Modification")
                            self.savetocsv(name2)
                    else:
                        self.savetocsv(name7)
                        if name == "Monster20.M":
                            print("Not existent")
            self.status = []
        else:
            self.actual += 1
        self.hp = 100
        self.emousser = 1.0
        self.enemy.hp = 100
        self.enemy.emousser = 1.0
        print(type(self.position))
        self.map.teleport_object(self, librpg.util.Position(random.randrange(2, 7), random.randrange(2, 7)))
        self.map.teleport_object(self.enemy, librpg.util.Position(5, 4))
        self.schedule_movement(Wait(10), True)
        self.enemy.schedule_movement(Wait(10), True)
        self.enemy.state = SmartMonster.GUARD_WALK
        self.enemy.corner = (8, 1)
        self.enemy.last_time = time.time()
        name = "Monster"
        name += str(self.actual)
        name += ".M"
        self.loadfromcsv(name)


