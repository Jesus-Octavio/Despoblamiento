#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 09:55:24 2022

@author: jesus
"""

import pandas as pd
df = pd.read_csv("data.csv")
for elem in df.columns:
    if "2018" in elem:
        print(elem)