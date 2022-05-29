#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 29 17:02:38 2022

@author: jesus
"""

import pandas as pd 
import folium
import webbrowser

df_merged = pd.read_csv("df_estructura_completo.csv")
Mad = folium.Map(location = [42.3442315,-3.7649043], zoom_start=7)
for x in range(df_merged.shape[0]):
    
    temp = pd.DataFrame(df_merged.iloc[x,:]).transpose()
    lat = float(temp["LATITUD_ET"])
    lon = float(temp["LONGITUD_E"])
    loc = [lat, lon]
    
    mystr = "<h1> Nombre del municipio </h1><br>"
    for col in temp.columns[:3]:
        mystr = mystr + "<p style=\"width:2px;height:10px;\">"  + col.upper() + ": " + str(temp[col].values[0]) + "</p><br>"
    
  

    
    html="""
    <h1> Nombre del municipio </h1><br>
    <p style="width:2px;height:10px;"> ldgfs </p>
    <p style="width:2px;height:10px;"> aldhv </p>
    <p style="width:2px;height:10px;"> aldv </p>
    <p style="width:2px;height:10px;"> asldkvb </p>
    <p style="width:2px;height:10px;"> aksdhvf </p>
    <p style="width:2px;height:10px;"> dkshfva </p>
    <p style="width:2px;height:10px;"> qkwevf </p>

    """
    iframe = folium.IFrame(html=html, width=500, height=300)
    popup = folium.Popup(iframe, max_width=2650)
    
    folium.Marker(location = loc,
                  popup = mystr,
                  tooltip = temp["CODMUN"].values[0],
                  icon = folium.Icon(icon = "fa-bicycle",
                                     prefix = 'fa',
                                     color = "white",
                                     icon_color = "lightgreen")).add_to(Mad)

Mad    
webbrowser.open(Mad, new=2)