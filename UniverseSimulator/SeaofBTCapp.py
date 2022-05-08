#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 09:37:41 2022

@author: jesus
"""



import tkinter as tk
from tkinter import messagebox
import sys
from PIL import ImageTk, Image
from paho.mqtt.client import Client 
from time import sleep

from Universe import Universe
from PopulationCentre import PopulationCentre
from LargeCity import LargeCity
from Agents import Agents
from Family_version_3 import Fam_one_person
from Family_version_3 import Fam_kids

import pandas as pd
import numpy as np
  
          
import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from  matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import plotly.offline as py
import sys


LARGE_FONT= ("Verdana", 12)


class Pages:
    name = None
    _id = None
    

class SeaofBTCapp(Pages, tk.Tk):

    def __init__(self, universe, *args, **kwargs):
               
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.universe = universe
        self.frames = {}

        for F in (StartPage, PageOne, PopulationCentrePage, PlotPage):

            frame = F(container, self)

            self.frames[F] = frame
            
            
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
        
        
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()
        
    def show_frame_set_population(self, cont, name, _id):
        
        frame = self.frames[cont]
        frame.tkraise()
        
        Pages.name = name
        Pages._id = _id
        
        

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        
        global welcome_pic 
        
        tk.Frame.__init__(self,parent)
        
        welcome_pic = ImageTk.PhotoImage(Image.open("/home/jesus/Escritorio/welcome.jpg"))
        tk.Label(self,
                 image = welcome_pic).pack()
        
        self.configure(background='black')
        
        tk.Button(self,
                  text = "ENTER",
                  command = lambda: controller.show_frame(PageOne)).pack()
        
        
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        
        global comein_pic
        
        tk.Frame.__init__(self, parent)
        
        #comein_pic = ImageTk.PhotoImage(Image.open("/home/jesus/Escritorio/come.jpg"))
        #comein_pic_label = tk.Label(self, image=comein_pic)
        
        
        tk.Button(self,
                  text = "CONSULTA", 
                  command = lambda: controller.show_frame(PopulationCentrePage)).pack()
        
        tk.Button(self,
                  text = "ATRÁS",
                  command = lambda: controller.show_frame(StartPage)).pack()
        
        
      
class PopulationCentrePage(Pages, tk.Frame,):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        var = tk.StringVar()

        def selection():
            towns_names = []
            cname = lb.curselection()
            for i in cname:
                op = lb.get(i)
                towns_names.append(op)
            
            towns_object = []
            for town in towns_names:
                for population in controller.universe.population_centres:
                    if town == population.population_name:
                        towns_object.append(population)
            
            return [towns_names, towns_object]
        
        
        def showSelected():
            towns = selection()
            for item in towns:
                print(item)
            
            
        show = tk.Label(self, text = "SELECCIONE UN MUNICIPIO", font = ("Times", 14), padx = 10, pady = 10)
        show.pack() 
        lb = tk.Listbox(self, selectmode = "multiple")
        lb.pack(padx = 10, pady = 10, fill = "both") 
        
        
        for item in range(len(controller.universe.population_centres)): 
            lb.insert("end", controller.universe.population_centres[item].population_name) 
            lb.itemconfig(item, bg="#bdc1d6") 

        tk.Button(self,
                  text = "CONFIRMAR CONSULTA",
                  command = showSelected).pack()
        
        tk.Button(self,
                  text = "SIGUIENTE",
                  command= lambda : controller.show_frame_set_population(PlotPage, name = selection()[0][0], _id = str(selection()[1][0].population_id))).pack()
        
        tk.Button(self,
                  text = "ATRÁS",
                  command = lambda : controller.show_frame(PageOne)).pack()
    

#from tkinterweb import HtmlFrame
    

class PlotPage(tk.Frame, Pages):
    
    def __init__(self, parent, controller):
        
        
        def button_1_plot():
            fig = controller.universe.plot_population_hist(int(Pages._id))    
            py.plot(fig, filename = "multiline.html", auto_open = True)
            #frame = HtmlFrame(self)
            #frame.pack(fill = "both", expand = True)
            #frame.load_url(url = 'file:///home/jesus/Escritorio/Despoblamiento/UniverseSimulator/primer.html')
            
        def button_2_plot():
            fig = controller.universe.plot_population_pyramid(int(Pages._id))    
            py.plot(fig, filename = "piramide.html", auto_open = True)
            #frame = HtmlFrame(self)
            #frame.pack(fill = "both", expand = True)
            #frame.load_url(url = 'file:///home/jesus/Escritorio/Despoblamiento/UniverseSimulator/primer.html')
            
        
        global comein_pic
        
        tk.Frame.__init__(self, parent)
        
        tk.Button(self,
                  text = "CONSULTA ACUTAL",
                  command = self.confirm_query).pack()
        #button3.pack()
        #button3.bind("<Button-1>", self.pp())
        
        
        self.label = tk.Label(self, text = "SELECCIONE TIPO DE GRÁFICO").pack()
        
        tk.Button(self,
                  text = "GRÁFICO MULTILINEA: EVOLUCIÓN TEMPORAL",
                  command = button_1_plot).pack()
        
        tk.Button(self,
                  text="PIRÁMIDE POBLACIONAL: EVOLUCIÓN TEMPORAL",
                  command = button_2_plot).pack()
        
        tk.Button(self,
                  text = "ATRÁS",
                  command = lambda: controller.show_frame(PopulationCentrePage)).pack()
        
        button_destroy = tk.Button(self,
                                   text = "CERRAR",
                                   command = lambda: controller.destroy())
        button_destroy.pack(side = "bottom")
        
     
    def confirm_query(self):
        text = str("HA ESCOGIDO EL MUNICIPIO %s CON CÓDIGO %s" % (Pages.name, Pages._id))
        self.label = tk.Label(self, text = text).pack()

        
     
if __name__ == "__main__":
    # Toy dataframe
    my_df = pd.read_csv("data_aumentada_years.csv")
    my_families_df = pd.read_csv("families.csv")
    my_df = my_df[my_df["CODMUN"].isin([39085])]
    my_families_df = my_families_df[my_families_df["CODMUN"].isin([39085])]
    #my_df = my_df[my_df["CODMUN"]]
    
    year = 2012
    
    my_universe = Universe(my_df, my_families_df, year)
    my_universe.Print()

    
        
    for i in range(1, 2):
        my_universe.update()
        my_universe.Print()
    
    
    #my_universe.regression_metrics()
    #app = SeaofBTCapp(universe = my_universe)
    #app.mainloop()
       
#app = SeaofBTCapp()
#app.mainloop()