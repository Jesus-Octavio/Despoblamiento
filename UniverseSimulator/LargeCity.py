#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 10:39:38 2022

@author: jesus
"""

class LargeCity():
    
    # LARGE CITY CONSTRUCTOR
    def __init__(self, identifier, name, num_men, num_women, features):
        self.population_id = identifier
        self.population_name = name
        self.num_men = num_men
        self.num_women = num_women
        self.features = {}
        self.inhabitants = []
        
        
    def Print(self):
        print('---------------------------------------------------')
        print('|        Large City (Out-of-the-universe?)        |')
        print('---------------------------------------------------')
        print("LARGE CITY: %s. Code: %s." 
              % (self.population_name, self.population_id))
        print("Total inhabitants: %s." % (self.num_men + self.num_women))
        print("Male inhabitants : %s."% self.num_men)
        print("Women inhabitants: %s." % self.num_women)
        print("\n")

        