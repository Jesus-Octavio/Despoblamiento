#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 18:21:46 2022

@author: jesus
"""

import webbrowser
from threading import Timer
from dash import Dash, html
import dash_cytoscape as cyto

app = Dash(__name__)

app.layout = html.Div([
    html.P("Dash Cytoscape:"),
    cyto.Cytoscape(
        id='cytoscape',
        elements=[
            {'data': {'id': 'ca', 'label': 'Canada'}}, 
            {'data': {'id': 'on', 'label': 'Ontario'}}, 
            {'data': {'id': 'qc', 'label': 'Quebec'}},
            {'data': {'source': 'ca', 'target': 'on'}}, 
            {'data': {'source': 'ca', 'target': 'qc'}}
        ],
        layout={'name': 'breadthfirst'},
        style={'width': '400px', 'height': '500px'}
    )
])

def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")
    

if __name__ == "__main__":
        
    Timer(1, open_browser).start()
    app.run_server(#debug=True,
                   host = "127.0.0.1",
                   port = "8050")