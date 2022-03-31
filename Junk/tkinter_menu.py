#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 09:27:54 2022

@author: jesus
"""

import tkinter as tk

class Window:
    def __init__(self, master):
        self.master = root
        
        #Frame
        self.frame = tk.Frame(self.master, width = 200, height = 250)
        self.frame.pack()
        
        #MenuButton
        self.mbutton = tk.Menubutton(self.frame, text = "My Menu Button")
        self.menu = tk.Menu(self.mbutton, tearoff = 0)
        self.menu.add_command(label = "Load", command = self.command1)
        self.menu.add_command(label = "Save", command = self.command1)
        self.mbutton["menu"] = self.menu
        
        self.mbutton.place(x = 50, y = 50)
        
    def command1(self):
        print("hola")

if __name__ == "__main__":
    root = tk.Tk()
    window = Window(root)
    root.mainloop()
        
        
    

