#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 14:46:31 2022

@author: christopherdalmau
"""
import matplotlib.pyplot as plt

lista = list()
listb = list()
"""
gender = input("Enter your gender(M/W)")
age = int(input("Enter your age"))
"""
resthr = int(input("Enter your resting heart rate"))
maxhr = int(input("enter your max heart rate: "))
vo2max = (maxhr / resthr) * 15.3

lista.append(1)
listb.append(vo2max)

plt.plot(lista,listb)
plt.show()

i = 2

while resthr >= 0:
    resthr = int(input("Enter your resting heart rate"))
    maxhr = int(input("enter your max heart rate: "))
    vo2max = (maxhr / resthr) * 15.3
    lista.append(i)
    listb.append(vo2max)
    plt.plot(lista,listb)
    plt.show()
    i += 1
    
    """
    if(resthr >= -1):
        break
    if(gender == "M") and (age >= 18) and (age <= 25) and (vo2max >= 60):
        print("Your vo2max is excellent keep up the good work")
    """




    



