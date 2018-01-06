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
######## check if possible
    def isAlive(p1):
        p1.__health>0
        return true

    def strike(self,opponent):
        opponent.__health -= self.__power

    def to_s(self):
        return "{name}: Health:{health}, Power:{power}"

    ######## check if possible
    def fight(p1,p2):
        print("Let the games begin")
        while p1.isAlive()and p2.isAlive():
            p1.strike(p2)
            p2.strike(p1)
            show_info(p1,p2)
        if p1.isAlive():
            print("{} WON!"(p1.__name))
        elif p2.isAlive():
            print("{} WON!"(p2.__name))
        else:
            print("TIE!!")

    def show_info():
        print("{}'s health:{} ||{}'s health:{}".format(p1.__name,p1.get_health(),p2.__name,p1.get_health()))

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
         def alive(self,health):
             if self.get_health <=0:
                 print()



p1=Hero('Superman', 5, 70)
p2=Hero('Spiderman',5,40)
p3=Vilin('Green goblin', 7, 30, "water")
print("\n"*2)
print("Show info():\n",p1.toString()+"\n",p2.toString())
print()
print("\n"*2)

Hero.fight(p1,p2)
'''
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
'''                                                                     # %C can replace a string










