import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import numpy as np
import pandas as pd

by_month_df = pd.read_csv('data/by_month_year')
app = dash.Dash()

app.layout= html.Div([
            dcc.Dropdown(

                        id= 'my-dropdown',
                        options=[
                        {'label': 'By Purpose','value': 'BP'},
                        {'label': 'By Gender','value': 'BG'},
                        {'label': 'By Month','value': 'BM'},
                        {'label': 'By number of Trekkers','value': 'BNT'}
                        ],
                        value = 'BM')
                        ,

            dcc.Graph(id='scatterplot',
                    figure= { 'data'  : [go.Scatter(x=by_month_df.Month,
                     y= by_month_df.Visitors, mode='lines+markers', name='LM')],
                              'layout': go.Layout(title='Tourist arrival by month from 1992-2013',
                                                  xaxis= {'title': 'Months'},
                                                  yaxis= {'title': 'No of Tourist'})
                            })
                     ])
                     
if __name__ == '__main__':
    app.run_server()
