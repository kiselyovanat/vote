#! /usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from Crypto.Cipher import AES

class CIK(object):

    def __init__(self):
        #allElectors = None
        self.voters = None
        self.bulletins = None

    def getElectors(self, filename):    # все избиратели хранятся в файле
        file = open(filename, 'r')
        text = file.read()
        text = text[:len(text)-1]       # символ конца файла убираем
        self.voters = set(text.split('\n'))    # каждая строка - ФИО избирателя
        file.close()

    def getVoters(self, filename):      #все желающие голосовать отмечаются в файле
        file = open(filename, 'r')
        text = file.read()
        text = text[:len(text)-1]       # символ конца файла убираем
        voters = set(text.split('\n'))     # каждая строка - ФИО избирателя
        file.close()

        self.voters = self.voters & voters

    def publishElectors(self):          # 1. ЦИК публикует список всех правомочных избирателей
        print "Список правомочных избирателей:"
        for name in self.voters:
            print name

    def publishVoters(self):            # 3. ЦИК публикует список избирателей, участвующих в выборах
        print "Список избирателей, участвующих в выборах:"
        for name in self.voters:
            print name

    def getBulletinFromVoter(self):     # 6.1 ЦИК получает бюллетень
        pass

    def publishBulletin(self):          # 6.2 ЦИК подтверждает получение бюллетеня, публикуя : Ek(I, v)
        pass

    def getIdAndPkFromVoter(self):      # 8.1 ЦИК получает идентификатор и закрытый ключ от избирателя
        pass

    def decryptBulletin(self):          # 8.2 ЦИК расшифровывает бюллетени
        pass

    def getResult(self):                # 8.3 ЦИК подсчитывает результат
        pass

    def publishResult(self):            # 8.4 В конце выборов она публикует их результаты и, для каждого варианта выбора, список соответствующий значений Ek(I, v).
        pass

class Elector(object):

    def __init__(self,id,name):
         self.id = id                   # 4. Каждый избиратель получает идентификационный номер
         self.name = name
         self.isVoter = False
         self.openKey = None
         self.privateKey = None
         self.bulletin = None

    def willVote(self,filename):        # 2. В течение определенного срока каждый избиратель сообщает в ЦИК, собирается ли он голосовать
        file = open(filename, 'a')
        file.write(self.name + '\n')
        file.close()
        self.isVoter = True

    def vote(self, chosenOne):          # бюллетень - ФИО того, за кого голосует избиратель
        self.bulletin = chosenOne

    def generateKeys(self):               # 5.1 Каждый избиратель генерирует открытый ключ и 5.2 закрытый ключ
        pass

    def encryptBulletin(self):          # 5.3 избиратель создает Ek(I, v)
        pass

    def sentBulletin(self):             # 5.4 избиратель посылает в ЦИК следующее сообщение : I,Ek(I, v)
        pass

    def sentIdAndPk(self):              # 7. Каждый избиратель посылает ЦИК: I, d
        pass

    def protest(self):                  # 9. Если избиратель обнаруживает, что его бюллетень подсчитан неправильно, он протестует, посылая ЦИК : I, Ek(I, v), d
        pass

C = CIK()

E = Elector(1,"AAA")
E2 = Elector(2,"dddd")

C.getElectors("electors.txt")
C.publishElectors()

E.willVote("voters.txt")
E2.willVote("voters.txt")

C.getVoters("voters.txt")
C.publishVoters()


E.vote("ттт")
E2.vote("иии")
