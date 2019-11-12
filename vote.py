#! /usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

class CIK(object):

    def __init__(self):
        #allElectors = None
        self.voters = None
        self.bulletins = []
        self.votersIdAndPk = None

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

    def getBulletinFromVoter(self,filename):     # 6.1 ЦИК получает бюллетень
        file = open(filename, 'r')
        text = file.read()
        file.close()
        text = text[:len(text)-1]       # символ конца файла убираем

        self.bulletins.append(text.split(' '))

        #print self.bulletins
        #print "----"

    def publishBulletin(self):          # 6.2 ЦИК подтверждает получение бюллетеня, публикуя : Ek(I, v)
        #print len(self.bulletins)
        for i in range(0, len(self.bulletins)):
            print self.bulletins[i][1]

    def getIdAndPkFromVoter(self):      # 8.1 ЦИК получает идентификатор и закрытый ключ от избирателя
        file = open(filename, 'r')
        text = file.read()
        file.close()
        text = text[:len(text)-1]
             # символ конца файла убираем
        self.votersIdAndPk.append(text.split(' '))


    def decryptBulletin(self):          # 8.2 ЦИК расшифровывает бюллетени
        for i in self.bulletins:
            #ciphertext = i
            print "--"
            print i
            #ciphertext_decoded = base64.b64decode(ciphertext)

    def getResult(self):                # 8.3 ЦИК подсчитывает результат
        pass

    def publishResult(self):            # 8.4 В конце выборов она публикует их результаты и, для каждого варианта выбора, список соответствующий значений Ek(I, v).
        pass

class Elector(object):

    def __init__(self,id,name):
         self.id = id                   # 4. Каждый избиратель получает идентификационный номер
         self.name = name
         self.isVoter = False
         self.publicKey = None
         self.privateKey = None
         self.bulletin = None
         self.encryptedBulletin = None

    def willVote(self,filename):        # 2. В течение определенного срока каждый избиратель сообщает в ЦИК, собирается ли он голосовать
        file = open(filename, 'a')
        file.write(self.name + '\n')
        file.close()
        self.isVoter = True

    def vote(self, chosenOne):          # бюллетень - ФИО того, за кого голосует избиратель
        self.bulletin = chosenOne

    def generateKeys(self):               # 5.1 Каждый избиратель генерирует открытый ключ и 5.2 закрытый ключ
        self.privateKey = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
        self.publicKey = self.privateKey.public_key()

        #print self.privateKey
        #print self.publicKey

    def encryptBulletin(self):          # 5.3 избиратель создает Ek(I, v)
        ciphertext = self.publicKey.encrypt(
          self.bulletin,
          padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
              )
        )
        ciphertext  = str(base64.b64encode(ciphertext))
        self.encryptedBulletin = ciphertext
        #print ciphertext

    def sentBulletin(self,filename):             # 5.4 избиратель посылает в ЦИК следующее сообщение : I,Ek(I, v)
        file = open(filename, 'w')
        file.write(str(self.id) + ' ' + self.encryptedBulletin + '\n')
        file.close()

    def sentIdAndPk(self,filename):              # 7. Каждый избиратель посылает ЦИК: I, d
        file = open(filename, 'w')
        file.write(str(self.id) + ' ' + str(self.privateKey) + '\n')
        file.close()

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

E.generateKeys()
E.encryptBulletin()
E.sentBulletin("bul.txt")
C.getBulletinFromVoter("bul.txt")

E2.generateKeys()
E2.encryptBulletin()
E2.sentBulletin("bul2.txt")
C.getBulletinFromVoter("bul2.txt")

C.publishBulletin()

E.sentIdAndPk("a.txt")
C.decryptBulletin()
