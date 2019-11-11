#! /usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

class CIK(object):

    def __init__(self):
        allElectors[] = None
        voters[] = None
        bulletins[] = None

    def getElectors(self, filename):    #все избиратели хранятся в файле
        pass

    def getVoters(self, filename):      #все желающие голосовать отмечаются в файле
        pass

    def publishElectors(self):          # 1. ЦИК публикует список всех правомочных избирателей
        pass

    def publishVoters(self):            # 3. ЦИК публикует список избирателей, участвующих в выборах
        pass

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

    def __init__(self):
         id = None                      # 4. Каждый избиратель получает идентификационный номер
         name = None
         isVoter = None
         openKey = None
         privateKey = None
         bulletin = None

    def willVote(self,filename):        # 2. В течение определенного срока каждый избиратель сообщает в ЦИК, собирается ли он голосовать
        pass

    def generateOk(self):               # 5.1 Каждый избиратель генерирует открытый ключ
        pass

    def generatePk(self):               # 5.2 Каждый избиратель генерирует закрытый ключ
        pass

    def encryptBulletin(self):          # 5.3 избиратель создает Ek(I, v)
        pass

    def sentBulletin(self):             # 5.4 избиратель посылает в ЦИК следующее сообщение : I,Ek(I, v)
        pass

    def sentIdAndPk(self):              # 7. Каждый избиратель посылает ЦИК: I, d
        pass

    def protest(self):                  # 9. Если избиратель обнаруживает, что его бюллетень подсчитан неправильно, он протестует, посылая ЦИК : I, Ek(I, v), d
        pass
