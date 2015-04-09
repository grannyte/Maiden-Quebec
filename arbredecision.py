import csv

from worldtest.enemy import *
import os.path
import librpg.util

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
        self.actual = 1
        self.status = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
        self.enemy = enemy
        self.tick =0
    def loadfromcsv(self, csvn):
        if os.path.isfile(csvn):
            pfile = open(csvn, 'rb')
            read = csv.reader(pfile)
            darrayfaitmoichier = []
            for row in read:
                darrayfaitmoichier.append(row)
            self.racine.loadfromarray(darrayfaitmoichier)
            pfile.close()

    def savetocsv(self, csvn):
        pfile = open(csvn, 'wb')
        wtr = csv.writer(pfile, delimiter=',', lineterminator='\n')
        self.racine.savetocsv(wtr)
        pfile.close()

    def update(self):
        self.tick += 1
        minpos = librpg.util.Position(8, 8)
        mindist =8
        for obj in self.map.objects:
            pos = obj.position-self.position
            dist = abs(pos.x)+abs(pos.y)
            if dist < mindist:
                mindist = dist
                minpos = pos
        valeures = [self.position.x, self.position.y, self.hp, self.enemy.position.x, self.enemy.position.y, self.enemy.hp, minpos.x, minpos.y]
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
            self.schedule_movement(Defence((self, self.position), (self.enemy, self.enemy.position)), True)
        else:
            self.schedule_movement(Attack((self, self.position), (self.enemy, self.enemy.position)), True)
        BayesMonster.update(self)
        if self.hp <= 1:
            print ("l'arbre de decision est mort")
            self.algogenetique()

        if self.hero.hp <= 1:
            print("Le monstre est mort")
            self.algogenetique()

        if self.tick >= 250:
            print("Le monstre est un trouillard")
            self.algogenetique()

    def algogenetique(self):
        self.tick = 0
        name = "Monster"
        name += str(self.actual)
        name += ".M"
        #self.savetocsv(name)
        self.status[self.actual] = self.hp-self.enemy.hp*2
        if self.enemy.hp == 100:
            self.status[self.actual] -= 100
        if self.actual == 9:
            ostatus = list(self.status)
            ostatus.sort()
            maxval = ostatus[1]
            ostatus = ostatus[-len(self.status)/2:]
            self.actual = 0
            minval = ostatus[:-1]
            i = 0
            for v in self.status:
                i += 1
                if ostatus.__contains__(v):
                    name = "Monster"
                    name += str(i)
                    name += ".M"
                    if os.path.isfile(name):
                        pfile = open(name, 'rb')
                        read = csv.reader(pfile)
                        csvarray = []
                        for row in read:
                            linearray = []
                            for nb in row:
                                linearray.append(nb)
                            csvarray.append(linearray)
                        pfile.close()
                        if v != minval:
                            for i in range(20):
                                r = random.randrange(len(csvarray))
                                b = csvarray[r]
                                rb = random.randrange(len(b))
                                csvarray[r][rb] = random.randrange(8)
                            self.racine.loadfromarray(csvarray)
                            self.savetocsv(name)
                        elif v == minval:
                            best = self.status.index(maxval)
                            randresult = random.randrange(1)
                            name = "Monster"
                            name += str(best)
                            name += ".M"
                            pfile = open(name, 'rb')
                            read = csv.reader(pfile)
                            csvarrayb = []
                            for row in read:
                                linearray = []
                                for nb in row:
                                    linearray.append(nb)
                                csvarrayb.append(linearray)
                            pfile.close()
                            csvarrayc = []
                            if randresult == 1:
                                csvarrayc = csvarray[:-len(csvarray)/2]+csvarrayb[-len(csvarrayb)/2:]
                            else:
                                csvarrayc = csvarray[-len(csvarrayb)/2:]+csvarrayb[:-len(csvarray)/2]
                            self.racine.loadfromarray(csvarrayc)
                            name = "Monster"
                            name += str(i)
                            name += ".M"
                            self.savetocsv(name)
                    else:
                        name = "Monster"
                        name += str(i)
                        name += ".M"
                        self.savetocsv(name)
        else:
            self.actual += 1
        self.hp = 100
        self.emousser = 1.0
        self.enemy.hp = 100
        self.enemy.emousser = 1.0
        print(type(self.position))
        self.map.teleport_object(self, librpg.util.Position(7, 7))
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


