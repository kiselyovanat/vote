#! /usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
import base64
from collections import Counter


class CIK(object):

    def __init__(self):
        #allElectors = None
        self.voters = None
        self.bulletins = {}
        self.votersIdAndPk = {}
        self.decryptedBulletins = {}
        self.results = None

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
        print "List of eligible voters:\n"
        for name in self.voters:
            print name
        print "-------------"

    def publishVoters(self):            # 3. ЦИК публикует список избирателей, участвующих в выборах
        print "List of voters participating in the elections:\n"
        for name in self.voters:
            print name
        print "-------------"

    def getBulletinFromVoter(self,filename):     # 6.1 ЦИК получает бюллетень
        file = open(filename, 'r')
        text = file.read()
        file.close()
        text = text[:len(text)-1]       # символ конца файла убираем

        Id, bul = text.split(' ')
        self.bulletins[Id] = bul

        #print self.bulletins
        #print "----"

    def publishBulletin(self):          # 6.2 ЦИК подтверждает получение бюллетеня, публикуя : Ek(I, v)
        #print len(self.bulletins)
        print "Publish bulletins:\n"
        for key in self.bulletins:
            print self.bulletins[key] + '\n'
        print "-------------"

    def getIdAndPkFromVoter(self,filename):      # 8.1 ЦИК получает идентификатор и закрытый ключ от избирателя
        file = open(filename, 'r')
        text = file.read()
        file.close()
        text = text[:len(text)-1]
             # символ конца файла убираем
        Id, Pk = text.split(',')
        self.votersIdAndPk[Id] = Pk
        #print self.votersIdAndPk
        #print Id
        #print Pk

    def decryptBulletin(self):          # 8.2 ЦИК расшифровывает бюллетени
        for key in self.votersIdAndPk:
            rsa_private_key = RSA.importKey(self.votersIdAndPk[key])
            rsa_private_key = PKCS1_OAEP.new(rsa_private_key)
            decrypted_text = base64.b64decode(self.bulletins[key])
            decrypted_text = rsa_private_key.decrypt(decrypted_text)
            self.decryptedBulletins[key] = decrypted_text, self.bulletins[key]
            #print decrypted_text
        #print self.decryptedBulletins

    def getResult(self):                # 8.3 ЦИК подсчитывает результат
        #for key in self.decryptedBulletins:
        self.results = Counter(self.decryptedBulletins[key][0] for key in self.decryptedBulletins)

    def publishResult(self):            # 8.4 В конце выборов она публикует их результаты и, для каждого варианта выбора, список соответствующий значений Ek(I, v).
        print "Results:\n"
        for key,value in sorted(self.results.iteritems()):
                print key, value
        print "-------------"
        print "Bulletins:\n"
        for key in self.decryptedBulletins:
            print self.decryptedBulletins[key][0], self.decryptedBulletins[key][1] + '\n'
        print "-------------"

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
        key = RSA.generate(2048)
        self.privateKey = key.export_key('PEM')
        self.publicKey = key.publickey().exportKey('PEM')

        #print self.privateKey
        #print self.publicKey

    def encryptBulletin(self):          # 5.3 избиратель создает Ek(I, v)
        rsa_public_key = RSA.importKey(self.publicKey)
        rsa_public_key = PKCS1_OAEP.new(rsa_public_key)
        encrypted = rsa_public_key.encrypt(self.bulletin)
        encrypted = base64.b64encode(encrypted)
        self.encryptedBulletin = encrypted
        #print encrypted

    def sentBulletin(self,filename):             # 5.4 избиратель посылает в ЦИК следующее сообщение : I,Ek(I, v)
        file = open(filename, 'w')
        file.write(str(self.id) + ' ' + self.encryptedBulletin + '\n')
        file.close()

    def sentIdAndPk(self,filename):              # 7. Каждый избиратель посылает ЦИК: I, d
        file = open(filename, 'w')
        file.write(str(self.id) + ',' + self.privateKey + '\n')
        file.close()

    def protest(self):                  # 9. Если избиратель обнаруживает, что его бюллетень подсчитан неправильно, он протестует, посылая ЦИК : I, Ek(I, v), d
        pass

C = CIK()

E = Elector(1,"Ian Jesse Ward")
E2 = Elector(2,"Erin Destiny Watson")

C.getElectors("electors.txt")
C.publishElectors()

E.willVote("voters.txt")
E2.willVote("voters.txt")

C.getVoters("voters.txt")
C.publishVoters()

E.vote("Jackson Blake Robinson")
E2.vote("Jeremiah Jeremiah Flores")

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
C.getIdAndPkFromVoter("a.txt")
E2.sentIdAndPk("b.txt")
C.getIdAndPkFromVoter("b.txt")
C.decryptBulletin()
C.getResult()
C.publishResult()
