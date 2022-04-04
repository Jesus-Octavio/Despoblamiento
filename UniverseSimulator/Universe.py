#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 09:43:03 2022

@author: jesus
"""
import pandas as pd
import numpy as np

from PopulationCentre import PopulationCentre
from LargeCity import LargeCity
from Agents import Agents

"""
from SeaofBTCapp import SeaofBTCapp
from SeaofBTCapp import StartPage
from SeaofBTCapp import PageOne
from SeaofBTCapp import PopulationCentrePage
from SeaofBTCapp import PlotPage
from SeaofBTCapp import temp
"""





import random, time, math, sys
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
from plotly.subplots import make_subplots
import plotly.offline as py

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
            
                    
    def update(self):
        global agent_idx
        # Update year for Universe
        self.year = str(int(self.year) + 1)
        # Consider each population centre
        for population in self.population_centres:
            # Intialize dictoinary with age ranges to previous year
            population.ages_hist[self.year + "M"] = population.ages_hist[str(int(self.year) - 1) + "M"].copy()
            population.ages_hist[self.year + "F"] = population.ages_hist[str(int(self.year) - 1) + "F"].copy()
            
            print("INICIO ACTUALIZACION")
            print("HOMBRES")
            print(population.ages_hist[self.year + "M"])
            print("\n")
            print("MUJERES")
            print(population.ages_hist[self.year + "F"])
            print("\n")

            
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
                
                
            print("\n")    
            print("ESTADO TRAS MUERTES")
            print("HOMBRES")
            print(population.ages_hist[self.year + "M"])
            print("\n")
            print("MUJERES")
            print(population.ages_hist[self.year + "F"])
            print("\n")
            
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
            population.update_hist()
            
            print("\n")
            print("FINAL ACTUALIZACION")
            print("HOMBRES")
            print(population.ages_hist[self.year + "M"])
            print("\n")
            print("MUJERES")
            print(population.ages_hist[self.year + "F"])
            print("\n")


            
            # Update year for the population centre
            population.year = int(population.year) + 1
            
               
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
        
        
    def Print(self):
        print('###################################################')
        print('#    POPULATION CENTRES IN THE UNIVERSE. ' + self.year +'     #')
        print('###################################################')
        print("Universe population: %s persons" % len(self.universe_persons))
        print("\n")
        for population in self.population_centres:
            population.Print()
        for city in self.large_cities:
            city.Print()
            
    def Plot(self):
        for population in self.population_centres:
            population.plot_hist().show()

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