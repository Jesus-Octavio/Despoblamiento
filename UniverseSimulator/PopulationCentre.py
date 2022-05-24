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

from Family_version_3 import Family
from Family_version_3 import Fam_one_person
from Family_version_3 import Fam_kids



class PopulationCentre():
    # POPULATION CENTRES CONSTRUCTOE
    
    def __init__(self, year, identifier, name,
                 num_men, num_women,
                 hom, muj, nat, mor, saldott, features):
        
        self.year = year
        self.population_id = identifier
        self.population_name = name
        #self.num_men_init = hom
        self.num_men = num_men
        #self.num_women_init = muj
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
        
        
        
        ##################### TRYING TO BUILD UP FAMILES #####################
        # Goal: families as a dictionary.
        # I consider several types of family:
        #    * fam_one_person: single member family -lives alone-
        #    * fam_kids: family with kids: mother + father`+ kids
        # I pretend to create a dictionary whose keys are family types and
        # his values are families
        self.families = {"fam_one_person" : [],
                         "fam_kids"       : []}
        # Store families evolution
        self.families_hist = {}
        ######################################################################
        
    
        
    def update_population(self, nat, mor, saldott):
        self.natality = int(nat)
        self.mortality = int(mor)
        self.saldo_migratorio_total = int(saldott)
        
        
    def update_population_hist(self):
        self.natality_hist.append(int(self.natality))
        self.mortality_hist.append(int(self.mortality))
        self.men_hist.append(int(self.num_men))
        self.women_hist.append(int(self.num_women))
        self.saldo_hist.append(int(self.saldo_migratorio_total))
        self.year_hist.append(int(self.year))
        
    ####################### TRYING TO BUILD UP FAMILES ########################
    def update_families_hist(self):
        self.families_hist[self.year] = {"num_fam_one_person" : len(self.families["fam_one_person"]),
                                         "num_fam_kids" : len(self.families["fam_kids"])}
    ###########################################################################
            
    
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
    
    
    ####################### TRYING TO BUILD UP FAMILES #######################
    #def update_families_hist(self):
    #    self.families_hist[self.year] = {}
        
    ###########################################################################    
    
        
    def Print(self):
        print('---------------------------------------------------')
        print('|           Population centre ' + str(self.population_id) +'               |')
        print('---------------------------------------------------')
        print("Population Centre  : %s." % self.population_name)
        print("Total  inhabitants : %s." % (self.num_men + self.num_women))
        print("Male   inhabitants : %s." % self.num_men)
        print("Female inhabitants : %s." % self.num_women)
        
        
        print("\n")
        
        
    def Print_families(self):
        
        kids = 0
        adults = 0
        for agent in self.inhabitants:
            if (agent.is_kid and (not agent.family)):
                kids += 1
            elif (agent.is_kid != None) and (agent.maybe_parent != None) and (not agent.family):
                adults += 1
        print("KIDS   WITHOUT FAMILY: %s" % kids)
        print("ADULTS WITHOUT FAMILY: %s" % adults)
        print("\n")
        for key in self.families.keys():
            print("FAMILY: "  + key + " -> " + str(len(self.families[key])))
        print("\n")
        
        
        for family in self.families["fam_kids"]:
            if (not family.father) and (family.kids) and (not family.mother):
                print("FAMILY WITHOUT PARENTS")
            elif (not family.father) and (family.kids):
                print("FAMILY WITHOUT FATHER")
            elif (not family.mother) and (family.kids):
                print("FAMILY WITHOUT MOTHER")
            elif (family.mother) and (family.father) and (not family.kids):
                print("FAMILY WITHOUT KIDS BUT WITH PARENTS")

        """
        for family in self.families["fam_kids"]:
            print("--- NEW FAM ---")
            mmax = 0
            for elem  in family.kids:
                if elem.age > mmax:
                    mmax = elem.age
            for member in family.members:
                print("AGE %s" % member.age)
            if family.mother.age < mmax + 25 or family.father.age < mmax + 25:
                print("\n")
            if family.mother.age < mmax + 25:
                print("MOMMY %s, KID %s" % (family.mother.age, mmax))
            if family.father.age < mmax + 25:
                print("DADDY %s, KID %s" % (family.father.age, mmax))
        """
            
        print("\n")
    