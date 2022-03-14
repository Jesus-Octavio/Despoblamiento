#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 09:43:03 2022

@author: jesus
"""
import pandas as pd
from PopulationCentre import PopulationCentre
from LargeCity import LargeCity
from Agents import Agents
import random, time, math
        

class Universe():
    # MAIN CLASS
    
    def __init__(self, df):
        # CONSTRUCTOR
        global agent_idx
        agent_idx = 0
        # Read data from dataframe (I do not really like this)
        self.main_dataframe = df
        # List of population centres (nucleos de poblacion) if the universe
        self.population_centres  = self.PopulationCentreBuilder()
        # List of persons in the universe
        self.universe_persons = self.AgentsBuilder()
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
            df_temp = self.main_dataframe.iloc[population]
            
            # Select some features about the population centre
            # Trying to compute a fits "happiness coefficient" to be able to
            # make decisions about migrations explained later)
            features = {"population_height_sea"  : df_temp["ALTITUD_M"],
                       "population_dist_pop"     : df_temp["DISTNUC10KM_M"],
                       "populaiton_dist_highway" : df_temp["DISTAUTOPAUTOV_M"],
                       "population_dist_train"   : df_temp["DISTESTACFERROC_M"]}
            
            
            # Invoke Population Center constructor
            the_population = PopulationCentre(
                    # IDENTIFICADOR NUCLEO.
                    identifier = df_temp["CODMUN"],
                    # NOMBRE NUCLEO.
                    name = df_temp["Nombre"],
                    # POBLACION MASCULINA.
                    num_men_init = df_temp["HOM2018"],
                    num_men = 0,
                    # POBLACION FEMENINA.
                    num_women_init = df_temp["MUJ2018"],
                    num_women = 0,
                    # NATALIDAD.
                    natality = df_temp["NAT2018"],
                    # MORTALIDAD.
                    mortality = df_temp["MOR2018"],
                    # CARACTERISTICAS (SELECCION QUE HE QUERID0)
                    features = features,
                    # TASA BRUTA DE NATALIDAD
                    gross_bith_rate = df_temp["TBNAT2018"],
                    # TASA BRUTA DE MORTALIDAD
                    gross_mortality_rate = df_temp["TBMOR2018"],
                    # TASA DE CRECIMIENTO VEGETATIVO
                    vegetative_growth =  df_temp["TCVEG2018"],
                    # SALDO VEGETATIVO
                    vegetative_balance = df_temp["SVEG2018"],
                    # ALTAS TOTALES
                    altas_totales = df_temp["ALTASTT2018"],
                    # ALTAS INTERIORES
                    altas_interiores = df_temp["ALTASINT2018"],
                    # ALTAS EXTERIORES
                    altas_exteriores = df_temp["ALTASEXT2018"],
                    # BAJAS TOTALES
                    bajas_totales = df_temp["BAJASTT2018"],
                    # BAJAS INTERIORES
                    bajas_interiores = df_temp["BAJASINT2018"],
                    # BAJAS EXTERIORES
                    bajas_exteriores = df_temp["BAJASEXT2018"],
                    # SALDO MIGRATORIO TOTAL
                    saldo_migratorio_total = df_temp["SALDOTT2018"],
                    # SALDO MIGRATORIO INTERNO
                    saldo_migratorio_interno = df_temp["SALDOINT2018"],
                    # SALDO MIGRATORIO EXTERNO
                    saldo_migratorio_externo = df_temp["SALDOEXT2018"])
                                              
            # Add specific population to the universe
            population_centres.append(the_population)
            
        return population_centres    
    
    
    def LargeCityBuilder(self):
        city_1 = LargeCity("CITY1", "Madrid",     0, 0, {})
        city_2 = LargeCity("CITY2", "Barcelona",  0, 0, {})
        return [city_1, city_2]

    
    def AgentsBuilder(self):
        # METHOD TO BUILD UP PERSONS (AGENTS) 
        # JUST TO INITIALIZE OUR MODEL !!
        global agent_idx # I want this variable to be global
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
        return agents
                
                
    def update(self):
        global agent_idx
        # Consider each population centre
        for population in self.population_centres:
            
            ### PEOPLE WHO LEAVE THE POPULATION CENTRE ###
            
            ## THOSE WHO DIE
            # Who is going to die?
            # I guess the oldest people (85% of total deaths)...
            deaths = 0
            while deaths < math.floor(0.85*population.mortality):
                max_age = 0
                person_to_die = None
                for person in population.inhabitants:
                    if person.age > max_age:
                        max_age = person.age
                        person_to_die = person
                person_to_die.remove_agent()
                self.remove_person_from_universe(person_to_die)
                deaths += 1
            # and some random people
            while deaths <= population.mortality:
                person_to_die = random.choice(population.inhabitants)
                person_to_die.remove_agent()
                self.remove_person_from_universe(person_to_die)
                deaths += 1
            
            ## SALDO MIGRATORIO (?):
            ## THOSE WHO ARE UNHAPPY ARE GOING TO LEAVE
            if population.saldo_migratorio_total < 0:
                saldo = 0
                # Consider each inhabitant
                for person in population.inhabitants:
                    # Is the person unhappy? If so -> remove
                    # But, where is the person going?
                    # (BY NOW) I ASSUME THE PERSON GOES TO A LARGE CITY
                    b = person.migrate()
                    if b:
                        # I could assumethey leave the universe but not
                        #self.remove_person_from_universe(person)
                        saldo -= 1
                        person.population_centre = random.choice(self.large_cities)
                        person.add_agent(new = False)
                    if saldo == population.saldo_migratorio_total:
                        break
        
            ### PEOPLE WHO ARRIVE IN THE POPULATION CENTRE ### 
            
            ## THOSE WHO ARE NEWBORN BABIES
            # Natality: new people with age 0 ¿Male or Female?
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
                new_borns += 1
                
            ## SALDO MIGRATORIO
            ## New guys on the town ! Where are they coming from? 
            ## Dont know, just create new people
            if population.saldo_migratorio_total > 0:
                new_guys = 0
                while new_guys < population.saldo_migratorio_total:
                    agent_idx = agent_idx + 1
                    # random.choice(["M", "F"]) same as the dice
                    the_agent = Agents(agent_idx, random.choice(["M", "F"]),
                                       random.randrange(18, 101),
                                       population)
                    self.add_person_to_universe(the_agent)
                    the_agent.add_agent()
                    new_guys += 1
            
            ### UPDATE AGES ###
            #for person in self.universe_persons:
            #    person.age += 1
                                

            
    def remove_person_from_universe(self, agent):
        # METHOD TO REMOVE PEOPLE FROM UNIVERSE (those who die mainly)
        # Remove from the universe
        self.universe_persons.remove(agent)
        
    def add_person_to_universe(self, agent):
        # METHOD TO ADD PEOPLE TO THE UNIVERSE (newborn babies mainly)
        self.universe_persons.append(agent)    
        
    def Print(self):
        print('###################################################')
        print('#        POPULATION CENTRES IN THE UNIVERSE       #')
        print('###################################################')
        print("Universe population: %s persons" % len(self.universe_persons))
        print("\n")
        for elem in self.population_centres:
            elem.Print()
            #for person in elem.inhabitants:
                #person.Print()
        for elem in self.large_cities:
            elem.Print()
            

if __name__ == "__main__":
    my_df = pd.read_csv("data.csv")
    my_universe = Universe(my_df)
    my_universe.Print()
    time.sleep(10)
    my_universe.update()
    my_universe.Print()
