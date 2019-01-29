#Imports
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import numpy as np
import pandas as pd

# Code to generate data values for our plot
df = pd.read_csv('data/modified_visitors_by_month', index_col = [0])
df1 = pd.read_csv('data/mpg.csv')
date = df['date'].values
visitors = df['Visitors'].values


app = dash.Dash()

app.layout= html.Div(
    [
        html.Div(
            [
                dcc.Dropdown(
                    id='dropdown',
                    options=[
                        {'label': 'By Purpose', 'value': 'BP'},
                        {'label': 'By Gender', 'value': 'BG'},
                        {'label': 'By Month', 'value': 'BM'},
                        {'label': 'By number of Trekkers', 'value': 'BNT'}
                            ],
                    value = 'BM'
                             ),

                dcc.RangeSlider(
                                count=1,
                                min=-5,
                                max=10,
                                step=0.5,
                                value=[-3, 7]
                               ),

                dcc.Graph(
                    id='Linechart',
                    figure= {'data':[go.Scatter(
                                         x=date,
                                         y=visitors,
                                         mode='lines+markers',
                                         name='LM'
                                                )
                                     ],
                              'layout':go.Layout(
                                           title='Tourist arrival by month from 1992-2013',
                                           xaxis= {'title': 'Months'},
                                           yaxis= {'title': 'No of Tourist'}
                                                 )
                            }
                         ),

                dcc.Graph(
                    id='histogram',
                    figure={
                        'data': [go.Histogram(
                                    x=df1['mpg'],
                                    xbins=dict(start=8,end=50,size=6),
                                )]
                                ,
                        'layout': go.Layout(
                                     title="Miles per Gallon Frequencies of<br>\
                                            1970's Era Vehicles"
                                            )
                            }
                           )


            ])
    ])


if __name__ == '__main__':
    app.run_server()
