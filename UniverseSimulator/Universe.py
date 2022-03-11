#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 09:43:03 2022

@author: jesus
"""
import pandas as pd
from PopulationCentre import PopulationCentre
from Agents import Agents
import random
        

class Universe():
    # MAIN CLASS
    
    def __init__(self, df):
        # CONSTRUCTOR
        
        # Read data from dataframe (I do not really like this)
        self.main_dataframe = df
        # List of population centres (nucleos de poblacion) if the universe
        self.population_centres  = self.PopulationCentreBuilder()
        # List of persons in the universe
        self.universe_persons = self.AgentsBuilder()
        

    def PopulationCentreBuilder(self):
        # METHOD TO BUILD UP POPULATION CENTRES
        # List to store population centres
        population_centres = [] 
        # As we are reading from a datafrase (assume each population centre 
        # appears just once in the dataframe), consider each row:
        for population in range(self.main_dataframe.shape[0]):
            # Select specifir row
            df_temp = self.main_dataframe.iloc[population]
            # Select population centre identifier
            population_id = df_temp["CODMUN"]
            # Select population centre name
            population_name = df_temp["Nombre"]
            # Initialize male population
            men = df_temp["HOM2018"]
            # Initialize female population
            women = df_temp["MUJ2018"]
            # Total of births
            natality = df_temp["NAT2018"]
            # Total of deaths
            mortality = df_temp["MOR2018"]
            # Select some features about the population centre
            # Trying to compute a fits "happiness coefficient" to be able to
            # make decisions about migrations explained later)
            features= {"population_height_sea" : df_temp["ALTITUD_M"],
                       "population_dist_pop" : df_temp["DISTNUC10KM_M"],
                       "populaiton_dist_highway" : df_temp["DISTAUTOPAUTOV_M"],
                       "population_dist_train" : df_temp["DISTESTACFERROC_M"]}
            # Invoke Population Center constructor
            the_population = PopulationCentre(identifier = population_id, 
                                              name = population_name,
                                              men = men,
                                              women = women,
                                              natality = natality,
                                              mortality = mortality,
                                              features = features)
                                              
            # Add specific population to the universe
            population_centres.append(the_population)
            
        return population_centres    

    
    def AgentsBuilder(self):
        # METHOD TO BUILD UP PERSONS (AGENTS)
        global agent_idx # I want this variable to be global
        # Empty list to store agents
        agents = []
        # Identifier for agents
        agent_idx = 0
        # Consider each population centre
        for population in self.population_centres:
            # CREATE PEOPLE
            # Consider male population
            for i in range(population.num_men):
                # Invoke Agents constructor
                the_agent = Agents(identifier = agent_idx,
                                   sex = "M",
                                   age = random.randint(0, 100),
                                   population_centre = population)
                # Add agent to population centre
                the_agent.add_agent(the_agent)
                # Add agent to global list
                agents.append(the_agent)
                # Update identifier
                agent_idx += 1
            # Same as previous but for female population
            for i in range(population.num_women):
                the_agent = Agents(identifier = agent_idx,
                                   sex = "F",
                                   age = random.randint(0, 100),
                                   population_centre = population)
                the_agent.add_agent(the_agent)                   
                agents.append(the_agent)
                agent_idx += 1
        return agents
                
                
    def update(self):
        for population in self.population_centres:
            for person in population.inhabitants:
                b = person.migrate()
                if b:
                    self.remove_person(person)
            new_borns = 0
            while new_borns <= population.natality:
                dice =  random.random()
                if dice < 0.5:
                    Agents(agent_idx + 1, "M", 0, population)
                else:
                    Agents(agent_idx + 1, "F", 0, population)
                new_borns += 1
            
            deaths = 0
            
            kill_elderly_percent = round(0.85*population.mortality)
            while deaths <= round(0.7*population.mortality):
                max_age = 0
                person_to_die = None
                for person in population.inhabitants:
                    if person.age > max_age:
                        max_age = person.age
                        person_to_die = person
                person_to_die.die()
                self.remove_person(person_to_die)
                deaths += 1
            kill_random_people = population.mortality - kill_elderly_percent
            deaths = 0
            while deaths < kill_random_people:
                person_to_die = random.choice(population.inhabitants)
                person_to_die.die()
                self.remove_person(person_to_die)
                deaths += 1
                
                
                
    def remove_person(self, agent):
        # METHOD TO REMOVE PEOPLE
        # Remove from the universe
        self.universe_persons.remove(agent)
        
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
            

if __name__ == "__main__":
    my_df = pd.read_csv("data.csv")
    my_universe = Universe(my_df)
    my_universe.Print()
    my_universe.update()
    my_universe.Print()
