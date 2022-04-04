#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 14:01:22 2022

@author: jesus
"""

import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import pandas as pd
import numpy as np


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
        
        # Mean happiness for inhabitants
        self.mean_happiness = self.update_mean_happiness()
        
        ## PLOT. MULILINE CHART: POPULATION DYNAMICS
        self.natality_hist  = []
        self.mortality_hist = []
        self.men_hist       = []
        self.women_hist     = []
        self.saldo_hist     = []
        self.year_hist      = []
        
        ## PLOT. POPULATION PYRAMID
        self.ages_hist = {}
        
        
    def update_population(self, nat, mor, saldott):
        self.natality = int(nat)
        self.mortality = int(mor)
        self.saldo_migratorio_total = int(saldott)
        
    def update_hist(self):
        self.natality_hist.append(int(self.natality))
        self.mortality_hist.append(int(self.mortality))
        self.men_hist.append(int(self.num_men))
        self.women_hist.append(int(self.num_women))
        self.saldo_hist.append(int(self.saldo_migratorio_total))
        self.year_hist.append(int(self.year))
    
    def update_mean_happiness(self):
        """
        Method to compute mean happiness for the population centre.
        The mean happiness for a population centre is the result 
        of averaging inhabitants's happiness
        """
        mean_happiness = 0
        # Both must be the same !!! Are they? 
        # Problemns with initialization by ages
        num_inhabitants = self.num_men + self.num_women
        #num_inhabitants_2 = len(self.inhabitants)
        for agent in self.inhabitants:
            mean_happiness = mean_happiness + (agent.happiness  / num_inhabitants)
        return mean_happiness
        
        
    def Print(self):
        print('---------------------------------------------------')
        print('|           Population centre ' + str(self.population_id) +'               |')
        print('---------------------------------------------------')
        print("Population Centre : %s." % self.population_name)
        print("Total inhabitants : %s." % (self.num_men + self.num_women))
        print("Male  inhabitants : %s." % self.num_men)
        print("Women inhabitants : %s." % self.num_women)
        #print("HIATORIAS : %s." % self.ages_hist)
        
        print("\n")
        
    