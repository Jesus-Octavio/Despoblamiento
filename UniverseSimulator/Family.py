#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 12:09:49 2022

@author: jesus
"""


class Family():
    
    def __init__(self, population_centre):
        self.population_centre = population_centre


class Fam_unipersonal(Family):
    
    def __init__(self, population_centre, agent):
        self.members = [agent]
        agent.family = True
        
        
class Fam_grupo(Family):
    
    def __init__(self, agent):
        self.members = [agent]
    
    def update(self, population_centre, agent):
        self.membres.append(agent)
        agent.family = True
        
        
        
class Fam_hijos(Family):
    
    def __init__(self, population_centre, agent_mother, agent_father):
        self.mother = agent_mother
        self.father = agent_father
        self.kids = []
        self.members = [self.mother, self.father]
        
        
        agent_mother.family = True
        agent_father.family = True
    
    def update(self, agent_kid):
        self.kids.append(agent_kid)
        self.members.append(agent_kid)
        agent_kid.family = True

"""
class Fam_otros(Family):
    del __init__(self, population_centre):
"""
        
    


        
        
    
        