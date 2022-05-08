#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  7 10:35:29 2022

@author: jesus
"""


import warnings
warnings.simplefilter("always")

class Family():
    
    def __init__(self):
        pass
        
        
    def add_family(self):
        if isinstance(self, Fam_one_person):
            self.population_centre.families["fam_one_person"].append(self)
        elif isinstance(self, Fam_kids):
            self.population_centre.families["fam_kids"].append(self)
        else:
            warnings.warn("FAMILY CLASS UNDEFINED")
            
    
    def remove_family(self):
        if isinstance(self, Fam_one_person):
            self.population_centre.families["fam_one_person"].remove(self)
        elif isinstance(self, Fam_kids):
            self.population_centre.families["fam_kids"].remove(self)
        else:
            warnings.warn("FAMILY CLASS UNDEFINED")
            
        
        
        
class Fam_one_person(Family):
    
    def __init__(self, population_centre):
        self.members = None
        self.population_centre = population_centre
        
    def update(self, agent):
        if agent.family:
            warnings.warn("THIS AGENT  ALREADY HAS A FAMILY!")
        if self.members:
            warnings.warn("THIS FAMILY IS COMPLETE")
        else:
            self.members = agent
            #agent.family = True
            agent.family = self
            
class Fam_kids(Family):
    
    def __init__(self, population_centre, kids_limit):
        self.population_centre = population_centre
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
                #agent.family = True
                agent.family = self
        elif role == "mother":
            if self.mother:
                warnings.warn("THIS FAMILY ALREADY HAS A MOTHER")
            else:
                self.mother = agent
                self.members.append(agent)
                #agent.family = True
                agent.family = self
        elif role == "kid":
            if len(self.kids) >= self.kids_limit:
                warnings.warn("ENOUGH KIDS")
            else:
                self.kids.append(agent)
                self.members.append(agent)
                #agent.family = True
                agent.family = self
                
    
      
    # Break up of a family when all of the kids are older then 25 yars old
    def disband(self):
        # Comnsider each kid
        for kid in self.kids:
            if self.kid.age >= 25:
                self.kids.remove(kid)
                my_family = Fam_one_person(kid.population_centre)
                my_family.update(kid)
                self.population_centre.families["fam_one_person"].append(my_family)
            
        # no more kids in the family -> free agents
        if not self.kids: 
            
            # new one person family for the father
            my_family = Fam_one_person(self.father.population_centre)
            my_family.update(self.father)
            # add fmaily to population centre
            self.population_centre.families["fam_one_person"].append(my_family)
            
            # new one persone fmaily for the mother
            my_family = Fam_one_person(self.mother.population_centre)
            my_family.update(self.mother)
            # add family to population centre
            self.population_centre.families["fam_one_person"].append(my_family)
            
            # remove family
            self.population_centre.families["fam_kids"].remove(self)
            
            return True
            
        # the family still has kids
        # do not remove family
        else:
            pass
            return False
            
                
                
                
                
                    
                    
            
        
            
    
            
            
