#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  7 10:35:29 2022

@author: jesus
"""


import warnings
warnings.simplefilter("always")

class Family():
    
    def __init__(self, population_centre):
        self.population_centre = population_centre
        
class Fam_one_person(Family):
    
    def __init__(self, population_centre):
        self.members = None
        
    def update(self, agent):
        if agent.family:
            warnings.warn("THIS AGENT  ALREADY HAS A FAMILY!")
        if self.members:
            warnings.warn("THIS FAMILY IS COMPLETE")
        else:
            self.members = agent
            agent.family = True
            
class Fam_kids(Family):
    
    def __init__(self, population_centre, kids_limit):
        self.kids_limit = kids_limit
        self.members = []
        self.father = None
        self.mother = None
        self.kids = []
        
    def update(self, agent, role):
        if agent.family:
            warnings.warn("THIS AGENT  ALREADY HAS A FAMILY!")
        if role == "father":
            if self.father:
                warnings.warn("THIS FAMILY ALREADY HAS A FATHER")
            else:
                self.father = agent
                self.members.append(agent)
                agent.family = True
        elif role == "mother":
            if self.mother:
                warnings.warn("THIS FAMILY ALREADY HAS A MOTHER")
            else:
                self.mother = agent
                self.members.append(agent)
                agent.family = True
        elif role == "kid":
            if len(self.kids) >= self.kids_limit:
                warnings.warn("ENOUGH KIDS")
            else:
                self.kids.append(agent)
                self.members.append(agent)
                agent.family = True
                #warnings.warn("KID NUMBER %s OF %s" % (len(self.kids), self.kids_limit))
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        
            
            
    