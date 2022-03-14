#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 14:01:22 2022

@author: jesus
"""

class PopulationCentre():
    # POPULATION CENTRES CONSTRUCTOE
    
    def __init__(self, identifier, name, num_men_init, num_men,
                 num_women_init, num_women,
                 natality, mortality, features,
                 gross_bith_rate, gross_mortality_rate,
                 vegetative_growth, vegetative_balance,
                 altas_totales, altas_interiores, altas_exteriores, 
                 bajas_totales, bajas_interiores, bajas_exteriores, 
                 saldo_migratorio_total, saldo_migratorio_interno,
                 saldo_migratorio_externo):
        
        self.population_id = identifier
        self.population_name = name
        self.num_men_init = num_men_init
        self.num_men = num_men
        self.num_women_init = num_women_init
        self.num_women = num_women
        self.natality = natality
        self.mortality = mortality
        self.features = features
        self.gross_bith_rate = gross_bith_rate
        self.gross_mortality_rate = gross_mortality_rate
        self.vegetative_growth = vegetative_growth
        self.vegetative_balance = vegetative_balance
        self.altas_totales = altas_totales
        self.altas_interiores = altas_interiores
        self.altas_exteriores = altas_exteriores
        self.bajas_totales = bajas_totales
        self.bajas_interiores = bajas_interiores
        self.bajas_exteriores = bajas_exteriores
        self.saldo_migratorio_total = saldo_migratorio_total
        self.saldo_migratorio_interno = saldo_migratorio_interno
        self.saldo_migratorio_externo = saldo_migratorio_externo
        self.inhabitants = []
        #self.inhabitant = inhabitants
        
    def Print(self):
        print('---------------------------------------------------')
        print('|                Population centre                |')
        print('---------------------------------------------------')
        print("Population Centre: %s. Code: %s." % (self.population_name, self.population_id))
        print("Total inhabitants: %s." % (self.num_men + self.num_women))
        print("Male inhabitants : %s." % self.num_men)
        print("Women inhabitants: %s." % self.num_women)
        print("\n")
        
    