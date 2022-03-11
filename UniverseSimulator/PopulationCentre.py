#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 14:01:22 2022

@author: jesus
"""

class PopulationCentre():
    # POPULATION CENTRES CONSTRUCTOE
    
    def __init__(self, identifier, name, men, women, natality, mortality, features):
        self.population_id = identifier
        self.population_name = name
        self.num_men = men
        self.num_women = women
        self.features = features
        self.natality = natality
        self.mortality = mortality
        self.inhabitants = []
        #self.inhabitant = inhabitants
        
    def Print(self):
        print('---------------------------------------------------')
        print('|                Population centre                |')
        print('---------------------------------------------------')
        print("Population: %s. Code %s." 
              % (self.population_name, self.population_id))
        print("Total inhabitants: %s." % (self.num_men + self.num_women))
        print("Male inhabitants: %s."% self.num_men)
        print("Women inhabitants: %s." % self.num_women)
        print("\n")
        
    