#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 15:44:44 2022

@author: jesus
"""

import numpy as np
import numpy.random

from PopulationCentre import PopulationCentre

class Agents():
    def __init__(self, identifier, sex, age, population_centre):
        # AGENTS/PEOPLE CONSTRUCTOR
        self.person_id = identifier
        self.sex = sex
        self.age = age
        self.population_centre = population_centre
        # Features about the place each person is living in
        self.features = population_centre.features
        # Happiness coefficient (I know this coefficient has no much sense
        # but I was trying to create a criterion to decide is s person wants to 
        # migrate or not)
        if self.features: # non-empty dict
            self.happiness = float(np.inner(np.random.dirichlet(np.ones(len(self.features)), size = 1),
                             list(self.features.values())) / np.sum(list(self.features.values())))
        else: # empty dict -> default = 1
            self.happiness = 1
        
        # Dont knowhow to use this yet...
        self.migration = 0
        self.new_migration = 0
        self.alive = 1
        
    ### SHOULD BE IN CLASS UNIVERSE ?
    ## SHOULD BE REMOVED?
    def add_agent(self, new = True):
        # Add agent to population centre
        self.population_centre.inhabitants.append(self)
        if new:
            if self.sex == "M":
                self.population_centre.num_men += 1
            else:
                self.population_centre.num_women += 1
            
    def remove_agent(self):
        # Remove agent from population centre
        self.population_centre.inhabitants.remove(self)
        if self.sex == "M":
            self.population_centre.num_men -= 1
        else: # sex = "F"
            self.population_centre.num_women -= 1
    
    ### SHOULD BE IN CLASS UNIVERSE ?
    ## SHOULD BE REMOVED?    
    def die(self):
        self.remove_agent()
        
    
    ### SHOULD BE IN CLASS UNIVERSE ?
    ## SHOULD BE REMOVED?        
    def migrate(self):
        # If a person want to migrate
        # If the peson is "unhappy" (?)
        if self.happiness <= 0.15:
            # If the person is old enough (just trying to model what we said about families..)
            # I think we will are able to "create" famillies but i have 
            # doubts about some of variables (i will try later)
            if self.age > 18:
                self.new_migration = 1
                self.migration = self.new_migration
                # That person is leaving the population centre 
                # but is the person leaving the universe ???????????
                #self.remove_agent()
                b = True
            else:
                b = False
        else:
            b = False
        return b
    
        
    def Print(self):
        print('- - - - - - - - - - - - - - - - - - - - - - - - - -')
        print('|                      AGENT                      |')
        print('- - - - - - - - - - - - - - - - - - - - - - - - - -')
        print("Lives in %s" % self.population_centre.population_name)
        print("Agent id: %s" % self.person_id)
        print("Age: %s" % self.age)
        print("Sex: %s" % self.sex)
        print("Happiness: %s" % self.happiness)
        print("\n")
        
        