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
    
    def __init__(self, df, year):
        # CONSTRUCTOR
        global agent_idx
        agent_idx = 0
        # Year
        self.year = str(year)
        # Read data from dataframe (I do not really like this)
        self.main_dataframe = df
        # List of population centres (nucleos de poblacion) if the universe
        population_centres = self.PopulationCentreBuilder()
        self.population_centres  = population_centres[0]
        self.cols_update = population_centres[1]
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
        self.year = str(int(self.year) + 1)
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
            #### ¿Y si no hay tantan gente infeliz como gente que se tiene que ir?
            ### Solo hay male ya que los he metido primero en la lista
            ### shuffe of inhabitants list ??????
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
                        # I could assumethey leave the universe but not
                        #self.remove_person_from_universe(person)
                        saldo -= 1
                        person.population_centre = random.choice(self.large_cities)
                        person.add_agent()
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
                    the_agent = Agents(agent_idx,
                                       random.choice(["M", "F"]),
                                       random.randrange(18, 101),
                                       population)
                    self.add_person_to_universe(the_agent)
                    the_agent.add_agent()
                    new_guys += 1
            
            ### UPDATE AGES ###
            for person in self.universe_persons:
                person.age += 1
                
            ### UODATE MORTALITY, NATALITY, .... ###
            d_args_update = {}
            for column in self.cols_update:
                d_args_update[column.lower()] = self.main_dataframe.query('CODMUN == ' + str(population.population_id))[column+self.year]
            population.uppdate_population(**d_args_update)
                
            
            
            
            
                                

            
    def remove_person_from_universe(self, agent):
        # METHOD TO REMOVE PEOPLE FROM UNIVERSE (those who die mainly)
        # Remove from the universe
        self.universe_persons.remove(agent)
        
    def add_person_to_universe(self, agent):
        # METHOD TO ADD PEOPLE TO THE UNIVERSE (newborn babies mainly)
        self.universe_persons.append(agent)    
        
    def Print(self):
        print('###################################################')
        print('#    POPULATION CENTRES IN THE UNIVERSE. ' + self.year +'     #')
        print('###################################################')
        print("Universe population: %s persons" % len(self.universe_persons))
        print("\n")
        for elem in self.population_centres:
            elem.Print()
        for elem in self.large_cities:
            elem.Print()
            

if __name__ == "__main__":
    # Toy dataframe, Just able to perform 3 updates
    my_df = pd.read_csv("data.csv")
    
    year = 2018
    
    my_universe = Universe(my_df, year)
    my_universe.Print()
    time.sleep(5)
    
    my_universe.update()
    my_universe.Print()
    time.sleep(5)
    
    my_universe.update()
    my_universe.Print()
    time.sleep(5)
    
    
    
