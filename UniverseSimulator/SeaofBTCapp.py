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

import pandas as pd
import numpy as np


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

        self.frames = {}

        for F in (StartPage, PageOne, PopulationCentrePage, PlotPage, temp):

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
        welcome_pic_label = tk.Label(self, image=welcome_pic)
        
        self.configure(background='black')
        
        button = tk.Button(self, text = "ENTER", command=lambda: controller.show_frame(PageOne))
        
        welcome_pic_label.pack()
        button.pack()
        
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        
        global comein_pic
        
        tk.Frame.__init__(self, parent)
        
        #comein_pic = ImageTk.PhotoImage(Image.open("/home/jesus/Escritorio/come.jpg"))
        #comein_pic_label = tk.Label(self, image=comein_pic)
        
        button0 = tk.Button(self, text = "ANTERIOR",
                            command=lambda: controller.show_frame(StartPage))
        
        button1 = tk.Button(self, text = "CONSULTA", 
                            command=lambda: controller.show_frame(PopulationCentrePage))
        
        #button2 = tk.Button(self, text='BACK', command=lambda: controller.show_frame(StartPage))
        
        #comein_pic_label.pack()
        button0.pack()
        button1.pack()
        #button2.pack()
        
"""        
class PopulationCentrePage(tk.Frame):
    
    def __init__(self, parent, controller):
        
        global comein_pic
        
        tk.Frame.__init__(self, parent)
        
        self.label = tk.Label(self, text = "SELECCIONE MUNICIPIO").pack()
        
        muni = ["ALCAZAR DE SAN JUAMN", "CAMPO DE CRIPTANA", "TOMELLOSO"]
        ids = ["1", "2", "3"]
        
        for i in range(3):
            button = tk.Button(self, text = str(i),
                               command = lambda : controller.show_frame_set_population(PlotPage, muni[i], ids[i])).pack()
#            controller.set_population(muni[i], ids[i]
"""

class PopulationCentrePage(Pages, tk.Frame,):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        var = tk.StringVar()

        def selection():
            countries = []
            cname = lb.curselection()
            for i in cname:
                op = lb.get(i)
                countries.append(op)
            return countries
        
        
        def showSelected():
            countries = selection()
            for val in countries:
                print(val)
            
            
        show = tk.Label(self, text = "SELECCIONE UN MUNICIPIO", font = ("Times", 14), padx = 10, pady = 10)
        show.pack() 
        lb = tk.Listbox(self, selectmode = "multiple")
        lb.pack(padx = 10, pady = 10, fill = "both") 

        x =["Tomelloso", "Alcazar de San Juan", "Campo de Criptana"]

        for item in range(len(x)): 
            lb.insert("end", x[item]) 
            lb.itemconfig(item, bg="#bdc1d6") 

        tk.Button(self, text = "CONFIRMAR CONSULTA", command=showSelected).pack()
        
        tk.Button(self, text = "SIGUIENTE",
                  command= lambda : controller.show_frame_set_population(PlotPage, name = selection()[0], _id = "2")).pack()
    

    

class PlotPage(tk.Frame, Pages):
    
    def __init__(self, parent, controller):
        
        
        global comein_pic
        
        tk.Frame.__init__(self, parent)
        
        button3 = tk.Button(self, text="CONSULTA ACUTAL", command=self.pp)
        button3.pack()
        #button3.bind("<Button-1>", self.pp())
        
        
        self.label = tk.Label(self, text = "SELECCIONE TIPO DE GRÁFICO").pack()
        
        button1 = tk.Button(self, text="GRÁFICO MULTILINEA: EVOLUCIÓN TEMPORAL",
                            command = lambda: controller.show_frame(temp))
        button1.pack()
        
        button2 = tk.Button(self, text="PIRÁMIDE POBLACIONAL: EVOLUCIÓN TEMPORAL",
                            command = lambda: controller.show_frame(temp))
        button2.pack()
        
    
    def pp(self):
        text = str("HA ESCOGIDO EL MUNICIPIO %s CON CÓDIGO %s" % (Pages.name, Pages._id))
        self.label = tk.Label(self, text = text).pack()
        
          
import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from  matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import sys

class temp(tk.Frame):

    def __init__(self, parent, controller):
        
        def createWidgets():

            t = np.arange(0, 3, .01)

            f0 = tk.Frame()
            
            fig = plt.figure(figsize=(8, 8))
        
            fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

            canvas = FigureCanvasTkAgg(fig, f0)
            toolbar = NavigationToolbar2Tk(canvas, f0)
            toolbar.update()
            canvas._tkcanvas.pack(fill=tk.BOTH, expand=1)
        
        
            f0.pack(fill=tk.BOTH, expand=1)

    
        tk.Frame.__init__(self, parent)
        #uper().__init__()
        button1 = tk.Button(self, text="GRÁFICO MULTILINEA: EVOLUCIÓN TEMPORAL",
                            command = createWidgets)
        button1.pack()
        

        
     
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
    app = SeaofBTCapp(universe = my_universe)
    app.mainloop()
   
#app = SeaofBTCapp()
#app.mainloop()