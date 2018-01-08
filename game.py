import random
import sys
import os
import math

class Hero:
    __name = ""    #using __ will make the variable changable only from the class
    __power = 0
    __health = 0

    def __init__(self, name, power, health):   #constractors
        self.__name = name
        self.__power = power
        self.__health = health

    def set_name(self, name):
        self.__name = name

    def set_power(self, power):
        self.__power = power

    def set_health(self, health):
        self.__health = health

    def get_power(self):
        return self.__power

    def get_health(self):
        return self.__health

    def get_name(self):
        return self.__name

    def get_type(self):
        print("Hero")

    def toString(self):
        return "{} has power strength of {} points and {} health points".format(self.__name,
                                                                                self.__power,
                                                                                self.__health)
    def isAlive(self):
        return self.__health>0

    def show_info(self):
        return("{}'s health points:{}".format(self.__name,self.get_health()))

    @staticmethod
    def strike(p1,p2):
        p1.__health -= p2.__power

    def to_s(self):
        return "{name}: Health:{health}, Power:{power}"

    @staticmethod
    def fight(p1,p2):
        print("Let the games begin")
        while p1.isAlive()and p2.isAlive():
            Hero.strike(p1,p2)
            Hero.strike(p2,p1)
            print(p1.show_info()+"\n"+p2.show_info())
        if p1.isAlive():
            print("{} WON!".format(p1.__name))
        elif p2.isAlive():
            print("{} WON!".format(p2.__name))
        else:
            print("TIE!!")



class Vilin(Hero):
     __weakness= ""

     def __init__(self, name, power, health, weakness):
         self.__weakness = weakness
         super(Vilin,self).__init__(name,power,health)

         def set_weakness(self, weakness):
             self.__weakness = weakness

         def get_weakness(self):
             return self.__weakness

         def get_type(self):
             print("Vilin")

         def toString(self):
             return "{} has power strength of {} points, {} health points and his secret weakness is {}".format(self.__name,
                                                                                                            self.__power,
                                                                                                             self.__health,
                                                                                                                self.__weakness)

p1 = Hero('Superman', 5, 70)
p2 = Hero('WonderWomen',4,95)
Hero.fight(p1,p2)


'''
p3 = Vilin('Green goblin', 7, 30, "water")
print("\n"*2)
print("Show info():\n",p1.to_s()+"\n",p2.to_s())
print("\n"*2)

<<<<<<< HEAD
=======
Hero.fight(p1,p2)
'''
>>>>>>> 2ecc016b67618b9c4bf0c7dccbd0d38e488d37b7
print(a.toString())
print(f.toString())

a = Hero('Superman', 5, 70)
b = Hero('Spiderman', 7, 60)
c = Hero('Wonderwomen', 5, 75)
d = Hero('Flash', 4, 90)
f = Vilin('Green goblin', 7, 30, "water")
g = Vilin('The Joker', 5, 40, "daylight")
h = Vilin('Lex luthor', 6, 50, "human")


print ('Choose your Superhero')
#name =sys.stdin.readline()
#print ('Get ready', name ,end='!!')
'''
