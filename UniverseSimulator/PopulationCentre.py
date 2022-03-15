#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 14:01:22 2022

@author: jesus
"""

class PopulationCentre():
    # POPULATION CENTRES CONSTRUCTOE
    
    def __init__(self, year, identifier, name,
                 num_men, num_women,
                 hom, muj, nat, mor, saldott, features):
        
        self.year = year
        self.population_id = identifier
        self.population_name = name
        self.num_men_init = hom
        self.num_men = num_men
        self.num_women_init = muj
        self.num_women = num_women
        self.natality = nat
        self.mortality = mor
        self.saldo_migratorio_total = saldott
        self.features = features
        self.inhabitants = []
        #self.inhabitant = inhabitants
        
    def uppdate_population(self, nat, mor, saldott):
        self.natality = int(nat)
        self.mortality = int(mor)
        self.saldo_migratorio_total = int(saldott)
        
        
    def Print(self):
        print('---------------------------------------------------')
        print('|           Population centre ' + str(self.population_id) +'               |')
        print('---------------------------------------------------')
        print("Population Centre : %s." % self.population_name)
        print("Total inhabitants : %s." % (self.num_men + self.num_women))
        print("Male  inhabitants : %s." % self.num_men)
        print("Women inhabitants : %s." % self.num_women)
        
        print("\n")
        
    