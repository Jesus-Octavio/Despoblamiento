#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 09:43:03 2022

@author: jesus
"""

from PopulationCentre import PopulationCentre
from LargeCity import LargeCity
from Agents import Agents

from Family import Family
from Family import Fam_unipersonal
from Family import Fam_monoparental
from Family import Fam_pareja_no_ninios
from Family import Fam_ninios
from Family import Fam_centros
from Family import Fam_otros


# load regression metrics
from sklearn.metrics import explained_variance_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
                            


# plots and more
import pandas as pd
import random
import numpy as np
import random, time, math, sys
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
from plotly.subplots import make_subplots
import plotly.offline as py
import warnings
import re
from varname import nameof
from itertools import chain



def myround(x, base=5):     
    """
    Auxiliary function. Given an age, returns its range according to
    the discretization in the read data
        
    Examples
    ------
    >>> myround(1)
    0-4        
    >>> myround(23)
    20-24        
    >>> myround(106)
    >100
    """
    init = base * math.floor(float(x) / base)    
    if init >= 100:
        return '>' + str(100)     
    end =  base * math.ceil(float(x) / base)
    if init == end:
        end = end + 5
    return str(init) + '-' + str(end - 1)


        

class Universe():
    # MAIN CLASS
    
    def __init__(self, df, df_families, year):
        # CONSTRUCTOR
        global agent_idx
        agent_idx = 0
        # Year
        self.year = str(year)
        # Read data from dataframe (population,......)
        self.main_dataframe = df
        
        
        ##################### TRYING TO BUILD UP FAMILES #####################
        # Read data from dataframe (FAMILIES)
        self.families_dataframe = df_families
        # Do we need a list of families in the complete universe????
        ######################################################################
        

        # List of population centres (nucleos de poblacion) if the universe
        population_centres = self.PopulationCentreBuilder()
        self.population_centres  = population_centres[0]
        self.cols_update = population_centres[1]
        # List of persons in the universe
        self.universe_persons = self.AgentsBuilder()
        
        
        
        ##################### TRYING TO BUILD UP FAMILES #####################
        self.FamilyBuilder()
        ######################################################################
        
        
        
        
        
        # (Out-of-the (?)) universe city. Trying to model a large city.
        # E.g. Madrid or Barcelona. These cities are out of the universe
        # as they are part of other CCAA. But this large city does not need
        # to be out of our Universe
        self.large_cities = self.LargeCityBuilder()
        
        
        
        

    def PopulationCentreBuilder(self):
        # METHOD TO BUILD UP POPULATION CENTRES
        # List to store population centres
        population_centres = [] 
        # As we are reading from a datafrase (assume each population centre 
        # appears just once in the dataframe), consider each row:
        for population in range(self.main_dataframe.shape[0]):
            # Select specific row
            columns_list = self.main_dataframe.columns
            df_temp = self.main_dataframe.iloc[population]
            
            # Select some features about the population centre
            # Trying to compute a fits "happiness coefficient" to be able to
            # make decisions about migrations explained later)
            features = {"population_height_sea"  : df_temp["ALTITUD_M"],
                       "population_dist_pop"     : df_temp["DISTNUC10KM_M"],
                       "populaiton_dist_highway" : df_temp["DISTAUTOPAUTOV_M"],
                       "population_dist_train"   : df_temp["DISTESTACFERROC_M"]}
            
            my_cols = ["HOM" + self.year, "MUJ" + self.year,
                       "NAT" + self.year, "MOR" + self.year, 
                       "SALDOTT" + self.year]
            
            my_cols_update = ["NAT", "MOR", "SALDOTT"]
            
            d_args = {}
            d_args["features"] = features
            for column in columns_list:
                if column in my_cols:
                    d_args[column[:len(column)-4].lower()] = df_temp[column]
            
            # Invoke Population Center constructor
            the_population = PopulationCentre(
                    # year
                    year = self.year,
                    # identifier for population centre
                    identifier = df_temp["CODMUN"],
                    # name for population centre
                    name = df_temp["Nombre"],
                    # male population
                    num_men = 0,
                    # female population
                    num_women = 0,
                    # rest of arguments
                    **d_args)

            # Add specific population to the universe
            population_centres.append(the_population)
        
        return  [population_centres, my_cols_update]
    
    
    def LargeCityBuilder(self):
        city_1 = LargeCity("CITY1", "Madrid",     0, 0, {})
        city_2 = LargeCity("CITY2", "Barcelona",  0, 0, {})
        return [city_1, city_2]

    """     
    PARA INICIALIZAR SI NO TENEMOS DATOS DESGLOSADOS SEGÚN FRANJAS
    DE EDAD:
       
    def AgentsBuilder(self):
        # METHOD TO BUILD UP PERSONS (AGENTS) 
        # JUST TO INITIALIZE OUR MODEL !!
        global agent_idx # I want this variable to be global ## gloabal en universo?
        # Empty list to store agents
        agents = []
        # Identifier for agents
        # Consider each population centre
        for population in self.population_centres:
            # CREATE PEOPLE
            # Consider male population
            for i in range(population.num_men_init):
                # Invoke Agents constructor
                the_agent = Agents(identifier = agent_idx,
                                   sex = "M",
                                   age = random.randint(0, 101),
                                   population_centre = population)
                # Add agent to population centre
                the_agent.add_agent()
                # Add agent to global list
                agents.append(the_agent)
                # Update identifier
                agent_idx += 1
            # Same as previous but for female population
            for i in range(population.num_women_init):
                the_agent = Agents(identifier = agent_idx,
                                   sex = "F",
                                   age = random.randint(0, 101),
                                   population_centre = population)
                the_agent.add_agent()                   
                agents.append(the_agent)
                agent_idx += 1
                
               
            # Update historial
            population.update_hist()
        return agents
    
    """
    
    def AgentsBuilder(self):
        global agent_idx
        agents = []
        age_cols = [col for col in self.main_dataframe.columns if col.startswith('Edad_')]
        #age_cols = self.main_dataframe.filter(regex = r'^Edad_.*?$', axis = 1)
        #male_cols =  self.main_dataframe.filter(regex = r'^Edad_M.*?$', axis = 1)
        #female_ cols = self.main_dataframe.filter(regex = r'^Edad_F.*?$', axis = 1)
        for population in self.population_centres:
            # Dictionary for age ranges
            age_range = {self.year + "M" : {}, self.year + "F" : {}}
            # SElect subdataframe
            df_temp = self.main_dataframe.\
                query('CODMUN == ' + str(population.population_id))[age_cols]
            for col in df_temp.columns:
                sex = col.split(":")[0][-1]
                if "-" in col:
                    init = int(col.split(":")[1].split("-")[0])
                    end = int(col.split(":")[1].split("-")[1])
                    key = str(init) + '-' + str(end)
                else:
                    init = int(col.split(":")[1].split(">")[1])
                    end = 110
                    key = ">" + str(init)
                    
                # Update distionay for age ranges
                if key not in age_range[self.year + sex].keys():
                    age_range[self.year + sex].update({key : int(df_temp[col])})
                else: 
                    age_range[self.year + sex][key] += int(df_temp[col])
                        
                for i in range(int(df_temp[col])):
                    # Create agent
                    the_agent = Agents(identifier = agent_idx,
                                   sex = sex,
                                   age = random.randint(init, end),
                                   population_centre = population)
                    # Add agent to population centre
                    the_agent.add_agent()
                    # Add agent to global list
                    agents.append(the_agent)
                    # Update identifier
                    agent_idx += 1
            
            # Update dictionary with age ranges and historial
            population.ages_hist = age_range
            #print(population.ages_hist)
            population.update_hist()
        return agents
            
    
    ####################### TRYING TO BUILD UP FAMILIES #######################
    
    
    def FamilyBuilder(self):
        # Consider each population centre
        for population in self.population_centres:
            
            # Given a population centre, select specific row in df
            df_temp = self.families_dataframe.\
                query('CODMUN == ' + str(population.population_id))
            
            ##### 1 people families #####
            fam1pe = df_temp["1PER"].values[0]
            
            msme65 = df_temp["MSME65"].values[0]
            hsme65 = df_temp["HSME65"].values[0]
            ms65ma = df_temp["MS65MA"].values[0]
            hs65ma = df_temp["HS65MA"].values[0]
                 
            msme65_init = df_temp["MSME65"].values[0]
            hsme65_init = df_temp["HSME65"].values[0]
            ms65ma_init = df_temp["MS65MA"].values[0]
            hs65ma_init = df_temp["HS65MA"].values[0]
            
            
            while (msme65 > 0) and (fam1pe > 0):
                my_family = Fam_unipersonal(population)
                population.families["fam_unipersonal"].append(my_family)
                msme65 -= 1
                fam1pe-= 1
            
            while (hsme65 > 0) and (fam1pe > 0):
                my_family = Fam_unipersonal(population)
                population.families["fam_unipersonal"].append(my_family)
                hsme65 -= 1
                fam1pe-= 1
                
            while (ms65ma > 0) and (fam1pe > 0):
                my_family = Fam_unipersonal(population)
                population.families["fam_unipersonal"].append(my_family)
                ms65ma -= 1
                fam1pe-= 1
                
            while (hs65ma > 0) and (fam1pe > 0):
                my_family = Fam_unipersonal(population)
                population.families["fam_unipersonal"].append(my_family)
                hs65ma -= 1
                fam1pe-= 1
                
            while (fam1pe > 0):
                my_family = Fam_unipersonal(population)
                population.families["fam_unipersonal"].append(my_family)
                fam1pe -= 1
                
            #print("Familias restantes de 1 persona: %s" % fam1pe)
            
            
            ##### 2 people families #####
            fam2pe = df_temp["2PER"].values[0]
            
            pmhj25  = df_temp["PMHJ25"].values[0]
            pmthi25 = df_temp["PMTHI25"].values[0]
            pjnohj  = df_temp["PJNOHJ"].values[0]
            
            pmhj25_init  = df_temp["PMHJ25"].values[0]
            pmthi25_init = df_temp["PMTHI25"].values[0]
            pjnohj_init  = df_temp["PJNOHJ"].values[0]
            
                        
            
            while (pjnohj > 0) and (fam2pe > 0):
                my_family = Fam_pareja_no_ninios(population)
                population.families["fam_no_ninios"].append(my_family)
                pjnohj -= 1
                fam2pe -= 1
            
            while (pmthi25 > 0) and (fam2pe > 0):
                my_family = Fam_monoparental(population, kids_limit = 2)
                population.families["fam_monoparental"].append(my_family)
                pmthi25 -= 1
                fam2pe -= 1
                
            while (pmhj25 > 0) and (fam2pe > 0):
                my_family = Fam_monoparental(population, kids_limit = 2)
                population.families["fam_monoparental"].append(my_family)
                pmhj25 -= 1
                fam2pe -= 1
                
                
            while (fam2pe > 0):
                my_family = Fam_otros(population, limit = 2)
                population.families["fam_otros"].append(my_family)
                fam2pe -= 1
            
            #print("Familias restantes de 2 persona: %s" % fam2pe)
            

            
            ##### 3-4-5-6>= people families#####
            fam3pe = df_temp["3PER"].values[0]
            fam4pe = df_temp["4PER"].values[0]
            fam5pe = df_temp["5PER"].values[0]
            fam5pe = df_temp["5PER"].values[0]
            fam6pe = df_temp["6OMASP"].values[0]
            
            pjhja25      = df_temp["PJHJA25"].values[0]
            pjthj25      = df_temp["PJTHJ25"].values[0]
            pjhj25       = pjthj25 + pjhja25
            #pjhj25_init  = pjthj25 + pjhja25
            
            # thiking about shared flats for students...
            mpnofam = df_temp["MPNOFAM"].values[0]
            
            # otro tipo de hogar ---? elderly houses ? students residences ? 
            # health centers, ej, San Juan de Dios en cienpozuelos xd ? 
            # hostels ? 
            othg = df_temp["OTHG"].values[0]
            
            
            
            while (pjhj25 > 0) and ((fam3pe > 0) or (fam4pe > 0) or (fam5pe > 0) or (fam6pe > 0)):
                
                # my_people = random.randint(3,8)
                available = []
                if (fam3pe > 0): 
                    available.append(int(re.findall(r'\d+', nameof(fam3pe))[0]))
                if (fam4pe > 0): 
                    available.append(int(re.findall(r'\d+', nameof(fam4pe))[0]))
                if (fam5pe > 0): 
                    available.append(int(re.findall(r'\d+', nameof(fam5pe))[0]))
                if (fam6pe > 0): 
                    available = available + list((int(re.findall(r'\d+', nameof(fam6pe))[0]), 7, 8))
                
                my_people = random.choice(available)
                
                if my_people == 3:
                    fam3pe -= 1
                elif my_people == 4:
                    fam4pe -= 1
                elif my_people == 5:
                    fam5pe -= 1
                else:
                    fam6pe -= 1
                
                kids_limit = my_people - 2
                my_family = Fam_ninios(population, kids_limit)
                population.families["fam_ninios"].append(my_family)
                
                pjhj25 -= 1
                
                
            while (mpnofam > 0) and ((fam3pe > 0) or (fam4pe > 0) or (fam5pe > 0) or (fam6pe > 0)):
                
                # my_people = random.randint(3,8)
                available = []
                if (fam3pe > 0): 
                    available.append(int(re.findall(r'\d+', nameof(fam3pe))[0]))
                if (fam4pe > 0): 
                    available.append(int(re.findall(r'\d+', nameof(fam4pe))[0]))
                if (fam5pe > 0): 
                    available.append(int(re.findall(r'\d+', nameof(fam5pe))[0]))
                if (fam6pe > 0): 
                    available = available + list((int(re.findall(r'\d+', nameof(fam6pe))[0]), 7, 8))
                
                my_people = random.choice(available)
                
                if my_people == 3:
                    fam3pe -= 1
                elif my_people == 4:
                    fam4pe -= 1
                elif my_people == 5:
                    fam5pe -= 1
                else:
                    fam6pe -= 1
                
                
                my_family = Fam_otros(population, limit = my_people)
                population.families["fam_otros"].append(my_family)
                
                mpnofam -= 1
            
        
            while (fam3pe > 0):
                my_family = Fam_otros(population, limit = 3)
                population.families["fam_otros"].append(my_family)
                fam3pe -= 1
                
            #print("Familias restantes de 3 persona: %s" % fam3pe)
            
            ##### 4 people families #####
                        
            while (fam4pe > 0):
                my_family = Fam_otros(population, limit = 4)
                population.families["fam_otros"].append(my_family)
                fam4pe -= 1
            
            #print("Familias restantes de 4 persona: %s" % fam4pe)
            
            ##### 5 people families #####
            
            
            while (fam5pe > 0):
                my_family = Fam_otros(population, limit = 5)
                population.families["fam_otros"].append(my_family)
                fam5pe -= 1
        
            #print("Familias restantes de 5 persona: %s" % fam5pe)
            
            ##### 6 or more people families #####
            
            
            while (fam6pe > 0):
                my_family = Fam_otros(population, limit = 6)
                population.families["fam_otros"].append(my_family)
                fam6pe -= 1
            
            #print("Familias restantes de 6 persona: %s" % fam6pe)   
            #print("\n")
                
                
            
            random.shuffle(population.inhabitants)
            
            oldies = []
            youngsters = []
            kids = []
            male_parent_susceptible = []
            female_parent_susceptible = []

            
            
            for agent in population.inhabitants:
                
                if agent.age >= 90:
                    oldies.append(agent)
                
                elif 65 < agent.age < 90:
    
                    # Male agents
                    if (agent.sex == "M"):
                        if (hs65ma_init > 0):
                            for family in population.families["fam_unipersonal"]:
                                if len(family.members) < 1:
                                    family.update(agent)
                                    hs65ma_init -= 1
                                    break
                        if agent.family == False:
                            oldies.append(agent)
                    
                    # female agents       
                    elif (agent.sex == "F"):
                        if (ms65ma_init > 0):
                            for family in population.families["fam_unipersonal"]:
                                if len(family.members) < 1:
                                    family.update(agent)
                                    ms65ma_init -= 1
                                    break
                                
                        if agent.family == False:
                            oldies.append(agent)
                       
                            
                elif 25 < agent.age <= 65:
                    
                    # Male agents
                    if (agent.sex == "M"): 
                        if (hsme65_init > 0):
                            for family in population.families["fam_unipersonal"]:
                                if len(family.members) < 1:
                                    family.update(agent)
                                    hsme65_init -= 1
                                    break
                                
                        if agent.family == False:
                            male_parent_susceptible.append(agent)
                        
                                
                    
                    # female agents        
                    else: #(agent.sex == "F"):
                        if (msme65_init > 0):
                            for family in population.families["fam_unipersonal"]:
                                if len(family.members) < 1:
                                    family.update(agent)
                                    msme65_init -= 1
                                    break
                        
                        if agent.family == False:
                            female_parent_susceptible.append(agent)
                                
                  
                elif 18 <= agent.age <= 25:
                    youngsters.append(agent)
                    
                else: # 0<= agent.age <18
                    for family in population.families["fam_ninios"]:
                        if len(family.kids) < family.kids_limit:
                            family.update(agent = agent, rol = "kid")
                            break
                    if agent.family == False:
                        kids.append(agent)
                            
            
            
            # assign youngsters
            # Iterate over the same list we are removing elements.... bad idea
            #  copy is needed
            youngsters_copy = youngsters.copy()
            for young in youngsters_copy:                
                for family in population.families["fam_ninios"]:
                    if len(family.kids) < family.kids_limit:
                        family.update(agent = young, rol = "kid")
                        youngsters.remove(young)
                        break
                else:
                    continue
            
            youngsters_copy = youngsters.copy()
            for young in youngsters_copy:                
                for family in population.families["fam_otros"]:
                    if family.limit > len(family.members):
                        family.update(young)
                        youngsters.remove(young)
                        break
                else:
                    continue
            
            
            
            # padres de familia
            male_parent_susceptible_copy = male_parent_susceptible.copy()
            for male in male_parent_susceptible_copy:
                for family in population.families["fam_ninios"]:
                    if not family.father:
                        my_bool = True
                        for elem in family.kids:
                                my_bool = my_bool and (male.age > elem.age + 20)
                        if my_bool:
                            family.update(male, rol = "father")
                            male_parent_susceptible.remove(male)
                            break
                    
 
            # madres de familia
            female_parent_susceptible_copy = female_parent_susceptible.copy()
            for female in female_parent_susceptible_copy:
                for family in population.families["fam_ninios"]:
                    if not family.mother:
                        # if theres a father... age difference
                        if family.father:
                            if ((female.age - 5 <= family.father[0].age <= female.age + 5) 
                             or (family.father[0].age - 5 <= female.age <= family.father[0].age + 5)): 
                                family.update(female, rol = "mother")
                                female_parent_susceptible.remove(female)
                                break
                        else:
                            family.update(female, rol = "mother")
                            female_parent_susceptible.remove(female)
                            break
            
            
            # parejas sin hijos
            male_no_parent_susceptible_copy = male_parent_susceptible.copy()
            for male in male_no_parent_susceptible_copy:
                for family in population.families["fam_no_ninios"]:
                    if (not family.boy):
                        family.update(male)
                        male_parent_susceptible.remove(male)
                        break
            
            female_no_parent_susceptible_copy = female_parent_susceptible.copy()
            for female in female_no_parent_susceptible_copy:
                for family in population.families["fam_no_ninios"]:
                    if (not family.girl):
                        if family.boy:
                            if ((female.age - 5 <= family.boy[0].age <= female.age + 5) 
                                 or (family.boy[0].age - 5 <= female.age <= family.boy[0].age + 5)): 
                                family.update(female)
                                female_parent_susceptible.remove(female)
                                break
                        else:
                            family.update(female)
                            female_parent_susceptible.remove(female)
                            break
            
            
   
            print("RESTANTES")    
            fam = 0
            nofam = 0
            for agent in population.inhabitants:
                if agent.family:
                    fam += 1
                else:
                    if agent.age < 25:
                        print("Edad %s. Sexo %s" % (agent.age, agent.sex))
                    nofam += 1
            
            for item in list(chain(*list(population.families.values()))):
                if len(item.members) == 0:
                    pass
                    #print(type(item))
            print("People do have a family: %s" % fam)
            print("People do not have a family yet: %s" % nofam)
            
            
            rest = kids+youngsters+male_parent_susceptible+female_parent_susceptible+oldies
            rest_copy = rest.copy()
            print("RESTO %s" % len(rest))
            print("\n")
            

            
            for agent in rest_copy:
                for family in population.families["fam_otros"]:
                    if len(family.members) < family.limit:
                            family.update(agent)
                            rest.remove(agent)
                            break
            
            
            
            print("\n")    
            print("RESTANTES")    
            fam = 0
            nofam = 0
            for agent in population.inhabitants:
                if agent.family:
                    fam += 1
                else:
                    if agent.age < 25:
                        print("Edad %s. Sexo %s" % (agent.age, agent.sex))
                    nofam += 1
            
            for item in list(chain(*list(population.families.values()))):
                if len(item.members) == 0:
                    pass
                    #print(type(item))
            print("People do have a family: %s" % fam)
            print("People do not have a family yet: %s" % nofam)
            print("RESTO %s" % len(rest))   
            print("\n")
            
        
            # otro tipo hogar
            
            temp = 0
            for i in range(math.floor(othg*0.25)):
                capacity = random.randint(50, 100)
                temp += capacity
                centre = Fam_centros(population, capacity)
                population.families["fam_centros"].append(centre)
                
            print("capacidad %s" % temp)
            rest_copy = rest.copy()
            
            for centre in population.families["fam_centros"]:
                for agent in rest_copy:
                    if not agent.family:
                        if len(centre.members) < centre.capacity:
                            centre.update(agent)
                            rest.remove(agent)
                        else:
                            break
                            rest_copy = rest.copy()
                        
                        
            
            
               
            
            print("\n")    
            print("RESTANTES")    
            print("RESTO %s" % len(rest))
            fam = 0
            nofam = 0
            for agent in population.inhabitants:
                if agent.family:
                    fam += 1
                else:
                    
                    print("Edad %s. Sexo %s" % (agent.age, agent.sex))
                    #print(elem in oldies)
                    nofam += 1
            
            for item in list(chain(*list(population.families.values()))):
                if len(item.members) == 0:
                    pass
                    #print(type(fam))
            print("People do have a family: %s" % fam)
            print("People do not have a family yet: %s" % nofam)
            print("\n")
            
            
        
                
            
            
    ###########################################################################
            
        
                    
    def update(self):
        global agent_idx
        # Update year for Universe
        self.year = str(int(self.year) + 1)
        # Consider each population centre
        for population in self.population_centres:
            # Intialize dictoinary with age ranges to previous year
            population.ages_hist[self.year + "M"] = population.ages_hist[str(int(self.year) - 1) + "M"].copy()
            population.ages_hist[self.year + "F"] = population.ages_hist[str(int(self.year) - 1) + "F"].copy()
            
            #print("INICIO ACTUALIZACION")
            #print("HOMBRES")
            #print(population.ages_hist[self.year + "M"])
            #print("\n")
            #print("MUJERES")
            #print(population.ages_hist[self.year + "F"])
            #print("\n")

            
            ### PEOPLE WHO LEAVE THE POPULATION CENTRE ###
            
            ## THOSE WHO DIE
            # Who is going to die?
            # I guess the oldest people (85% of total deaths)...
            
            l = []
            
            deaths = 0
            while deaths < math.floor(0.85*population.mortality):
                max_age = 0
                person_to_die = None
                for person in population.inhabitants:
                    if person.age > max_age:
                        max_age = person.age
                        person_to_die = person
                        
                # Update dictionary with ages by range:
                # Al menos no está muriando gente repetida.
                #print(str(person_to_die.person_id) + " - " + person_to_die.sex + " - " + str(person_to_die.age) + " - " + str(myround(person_to_die.age)))
                if person.person_id in l:
                    raise Exception("OYE!")
                l.append(person_to_die.person_id)
                
                interval = myround(person_to_die.age)
                population.ages_hist[self.year + person_to_die.sex][interval] -= 1
                # Remove person
                person_to_die.remove_agent()
                self.remove_person_from_universe(person_to_die)
                deaths += 1
            # and some random people
            while deaths <= population.mortality:
                person_to_die = random.choice(population.inhabitants)
                #print(str(person_to_die.person_id) + " - " + person_to_die.sex + " - " + str(person_to_die.age) + " - " + str(myround(person_to_die.age)))
                # Update dictionary with ages by range:
                interval = myround(person_to_die.age)
                population.ages_hist[self.year + person_to_die.sex][interval] -= 1
                # Remove person
                person_to_die.remove_agent()
                self.remove_person_from_universe(person_to_die)
                deaths += 1
                
                
            #print("\n")    
            #print("ESTADO TRAS MUERTES")
            #print("HOMBRES")
            #print(population.ages_hist[self.year + "M"])
            #print("\n")
            #print("MUJERES")
            #print(population.ages_hist[self.year + "F"])
            #print("\n")
            
            ## SALDO MIGRATORIO (?):
            ## THOSE WHO ARE UNHAPPY ARE GOING TO LEAVE
            #### ¿Y si no hay tantan gente infeliz como gente que se tiene que ir?
            ### Solo hay male ya que los he metido primero en la lista
            ### shuffle of inhabitants list ??????
            if population.saldo_migratorio_total < 0:
                saldo = 0
                # Consider each inhabitant
                for person in population.inhabitants:
                    ### THE MOST UNHAPPUY PEOPLEMUST LEAVE !
                    
                    # Is the person unhappy? If so -> remove
                    # But, where is the person going?
                    # (BY NOW) I ASSUME THE PERSON GOES TO A LARGE CITY
                    b = person.migrate()
                    if b:
                        # I could assume they leave the universe but not
                        #  self.remove_person_from_universe(person)
                        saldo -= 1
                        # Update dictionary with ages by range:
                        interval = myround(person.age)
                        population.ages_hist[self.year + person.sex][interval] -= 1
                        person.remove_agent() # ya esta en person.migrate()
                        
                    
                        person.population_centre = random.choice(self.large_cities)
                
                        # Update dictionary with ages by range:
                        #interval = myround(person.age)
                        #population.ages_hist[self.year + person.sex][interval] -= 1
                        
                        person.add_agent() # necesito añadirlo a la ciudad destino
                        
                        
                    if saldo == population.saldo_migratorio_total:
                        break
                
        
            ### PEOPLE WHO ARRIVE IN THE POPULATION CENTRE ### 
            
            ## SALDO MIGRATORIO
            ## New guys on the town ! Where are they coming from? 
            ## Dont know, just create new people
            if population.saldo_migratorio_total > 0:
                new_guys = 0
                while new_guys < population.saldo_migratorio_total:
                    agent_idx = agent_idx + 1
                    # random.choice(["M", "F"]) same as the dice
                    the_agent = Agents(agent_idx,
                                       random.choice(["M", "F"]),
                                       random.randrange(18, 101),
                                       population)
                    self.add_person_to_universe(the_agent)
                    the_agent.add_agent()
                    new_guys += 1
                   
                    # Update dictionary with ages by range:
                    interval = myround(the_agent.age)
                    population.ages_hist[self.year + the_agent.sex][interval] += 1
            
            
            
            
            ### UPDATE AGES ###
            # HAY QUE ACTUALIZAR EN EL MOMENTO ADECUADO. RECIEN NACIDOS CON 1 AÑO !?
            # EL PROBLEMA EN LA PIRÁMIDE POBLACIONAL ESTÁ EN ESTA LINEA!!!
            # No estoy actualizando en la pirámide....
            ## FIXED ERRO !!!
            #for person in self.universe_persons:
             #   person.age += 1
              #  interval = myround(person.age)
              #  person.population_centre.ages_hist[self.year + person.sex][interval] += 1
                
            for person in population.inhabitants:
                #if person.population_centre.population_name not in ["Madrid", "Barcelona"]:
                interval_1 = myround(person.age)
                person.age += 1
                interval_2 = myround(person.age)
                if interval_1 != interval_2:
                    person.population_centre.ages_hist[self.year + person.sex][interval_1] -= 1
                    person.population_centre.ages_hist[self.year + person.sex][interval_2] += 1
                else:
                    pass
                #else:
                #    person.age += 1
                    
                    
            ## THOSE WHO ARE NEWBORN BABIES
            # Natality: new people with age -1 ¿Male or Female?
            new_borns = 0
            while new_borns <= population.natality:
                dice =  random.random()
                agent_idx = agent_idx + 1
                if dice < 0.5:
                    the_agent = Agents(agent_idx, "M", 0, population)
                else:
                    the_agent = Agents(agent_idx, "F", 0, population)
                ## Add agent to the universe
                self.add_person_to_universe(the_agent)
                # Add agent to population centre
                the_agent.add_agent()
                # Update counter
                new_borns += 1
                # Update dictionary with ages by range:
                interval = myround(the_agent.age)
                population.ages_hist[self.year + the_agent.sex][interval] += 1
                
                
            ### UPDATE MORTALITY, NATALITY, .... ###
            d_args_update = {}
            for column in self.cols_update:
                d_args_update[column.lower()] = self.main_dataframe.\
                    query('CODMUN == ' + str(population.population_id))[column+self.year]
            
            population.update_population(**d_args_update)            
                        
            #print("\n")
            #print("FINAL ACTUALIZACION")
            #print("HOMBRES")
            #print(population.ages_hist[self.year + "M"])
            #print("\n")
            #print("MUJERES")
            #print(population.ages_hist[self.year + "F"])
            #print("\n")
            
            # Update year for the population centre
            population.year = int(population.year) + 1
            population.update_hist()
            #print(population.year_hist)
            
            
            
            
            
            
            
            
            
            
               
    def remove_person_from_universe(self, agent):
        # METHOD TO REMOVE PEOPLE FROM UNIVERSE (those who die mainly)
        # Remove from the universe
        self.universe_persons.remove(agent)
        
        
    def add_person_to_universe(self, agent):
        # METHOD TO ADD PEOPLE TO THE UNIVERSE (newborn babies mainly)
        self.universe_persons.append(agent)    
        
        
    def plot_population_hist(self, population_code):
        # METHOD FOR PLOTTING POPULATION HISTORIAL IN A
        # SPECIFIED POPULATION CENTRE.

        #population_code = int(input("Please, enter a population code: "))
        
        my_population = False
        for population in self.population_centres:
            if population.population_id == population_code:
                my_population = population
        
        if my_population == False:
            raise Exception("Population centre not found")
        
        
        data  = {"NAT" : my_population.natality_hist,
                 "MOR" : my_population.mortality_hist,
                 "HOM" : my_population.men_hist,
                 "MUJ" : my_population.women_hist,
                  #"SALDOMIG" : my_population.saldo_hist,
                 "YEAR" : my_population.year_hist}
        
        df = pd.DataFrame.from_dict(data)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x = df["YEAR"], y = np.log(df["HOM"]),
                      mode = "lines",
                      name = "Hombres"))
        
        fig.add_trace(go.Scatter(x = df["YEAR"], y = np.log(df["MUJ"]),
                      mode = "lines",
                      name = "Mujeres"))
        
        fig.add_trace(go.Scatter(x = df["YEAR"], y = np.log(df["NAT"]),
                      mode = "lines",
                      name = "Natalidad"))
        
        fig.add_trace(go.Scatter(x = df["YEAR"], y = np.log(df["MOR"]),
                      mode = "lines",
                      name = "Mortalidad"))
        
        # SALDO MIGRATORIO NEGATIVO -> ERROR !!!
        #fig.add_trace(go.Scatter(x = df["YEAR"], y = np.log(df["SALDOMIG"]),
        #              mode = "lines",
        #              name = "Saldo migratorio"))
        
        fig.update_layout(title = "Evolución de variables en %s" % my_population.population_name,
                    xaxis_title = "Año",
                    yaxis_title = "Total personas (log-scale)")
  
        
        #fig.show()
        return fig
        
    def plot_population_pyramid(self, population_code):
        # METHOD FOR PLOTTING POPULATION HISTORIAL IN A
        # SPECIFIED POPULATION CENTRE. ALDO PLOTS POPULATIUON PYRAMID

        #population_code = int(input("Please, enter a population code: "))
        
        my_population = False
        for population in self.population_centres:
            if population.population_id == population_code:
                my_population = population
        
        if my_population == False:
            raise Exception("Population centre not found")
        
        
        df = pd.DataFrame.from_dict(my_population.ages_hist)
        
        
        fig = make_subplots(rows = int(len(df.columns) / 2), cols = 1,
                 subplot_titles = np.unique([x[:-1] for x in df.columns]))
        
        
        # Function 2Z -> Z ... i guess not
        row = 1
        for i in range(0, len(df.columns), 2):
            if i == 0:
                show = True
            else:
                show = False
        

            fig.add_trace(go.Bar(
                          y = df.index.values.tolist(),
                          x = df.iloc[:, i],
                          name  = "Hombres",
                          marker_color = "blue",
                          orientation = "h",
                          showlegend = show),
                          row = row, col = 1)
            
            fig.add_trace(go.Bar(
                          y = df.index.values.tolist(),
                          x = - df.iloc[:, i + 1],
                          name  = "Mujeres",
                          marker_color = "orange",
                          orientation = "h",
                          showlegend = show),
                          row = row, col = 1)
            
            fig.update_layout(barmode = 'relative',
                               bargap = 0.0, bargroupgap = 0)
            fig.update_xaxes(tickangle=90)


            #for t in fig2.data:
             #   fig.append_trace(t , row = row, col = 1)
                
            row += 1
            
        
        fig.update_layout(
                    title_text="Evolución de la pirámide poblacional en %s" 
                        % my_population.population_name,
                    bargap = 0.0, bargroupgap = 0,)
        #fig.show()
        return fig
    
    def regression_metrics(self):
        print("--- REGRESSION METRICS ---")
        for population in self.population_centres:
            years = population.year_hist
            total_pred = [sum(x) for x in zip(population.men_hist, population.women_hist)]
            total_obs = []
            for year in years:
                temp = self.main_dataframe.\
                    query('CODMUN == ' + str(population.population_id))["POB"+ str(year)].\
                    values
                temp = int(temp)
                total_obs.append(temp)
        
            
            print("- " + population.population_name.upper() + " -")
            print(total_pred)
            print(total_obs)
            print("Explained variance:  %s" % explained_variance_score(total_pred, total_obs))
            print("MAE:  %s" % mean_absolute_error(total_pred, total_obs))
            print("MSE:  %s" % mean_squared_error(total_pred, total_obs))
            print("R2:  %s" % r2_score(total_pred, total_obs))
            print("\n")
        
        
        
    def Print(self):
        print('###################################################')
        print('#    POPULATION CENTRES IN THE UNIVERSE. ' + self.year +'     #')
        print('###################################################')
        print("Universe population: %s persons" % len(self.universe_persons))
        print("\n")
        for population in self.population_centres:
            population.Print()
            ################### TRYING TO BUILD UP FAMILIES ###################
            population.Print_families()
            ###################################################################
        for city in self.large_cities:
            city.Print()
            
    """
    # Not useful anymore
    # But leave it here just in case
    def Plot(self):
        for population in self.population_centres:
            population.plot_hist().show()
    """    

"""

if __name__ == "__main__":
    # Toy dataframe
    my_df = pd.read_csv("data_aumentada_years.csv")
    my_df = my_df[my_df["CODMUN"].isin([39085, 39035])]
    #my_df = my_df[my_df["CODMUN"]]
    
    year = 2012
    
    my_universe = Universe(my_df, year)
    my_universe.Print()
    for i in range(1,2):
        my_universe.update()
        my_universe.Print()
        
    
    #my_universe.plot_population_pyramid()
    app = SeaofBTCapp()
    app.mainloop()
    
""" 