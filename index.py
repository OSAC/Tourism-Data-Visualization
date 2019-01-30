#IMPORTS
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

# DATA
by_month_df = pd.read_csv('data/by_month_year')
by_year = pd.read_csv('data/modified_visitors_by_month', index_col = [0])
by_purpose = pd.read_csv('data/by_purpose_cleaned')


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


#MAIN APP
app.layout = html.Div([

                html.H4(' Dash Board'),
                html.P(),
                 dcc.Dropdown(
                    id= 'options-dropdown',
                    options=[
                        {'label': 'By Purpose','value': 'BP'},
                        #{'label': 'By Gender','value': 'BG'},
                        {'label': 'By Month','value': 'BM'},
                        {'label': 'By Year','value': 'BY'},
                        #{'label': 'By number of Trekkers','value': 'BNT'}
                            ],
                    value = 'BM'
                               ),

                 dcc.Graph(
                    id='graph-with-slider'),

                 html.Label('Data Range'),
                 html.P(),

                 dcc.Slider(
                    id='year-slider',
                    min=by_month_df['Year'].min(),
                    max=by_month_df['Year'].max(),
                    value=by_month_df['Year'].min(),
                    marks={str(year): str(year) for year in by_month_df['Year'].unique()}
                            )
                     ])

#DECORATOR
@app.callback(Output('graph-with-slider', 'figure'),
             [Input('year-slider', 'value'), Input('options-dropdown', 'value')])

def update_figure(selected_year, selected_option):
    if selected_option == 'BM':
        filtered_df = by_month_df[by_month_df.Year == selected_year]

        traces = []

        traces.append( go.Scatter(
                         x = filtered_df['Month'].values,
                         y = filtered_df['Visitors'].values,
                         mode='markers',
                         opacity=0.7,
                         marker={
                            'size': 15,
                            'line': {'width': 0.5, 'color': 'white'}
                                }
                                    )
                      )

        return {
            'data': traces,
            'layout': go.Layout(
                        title='Tourists Arrival By Months',
                        xaxis={ 'title': 'Months'},
                        yaxis={'title': 'No of visitors'},
                        hovermode='closest'
                                )
                }

    # by purpose block
    elif selected_option == 'BP':
        # create a new dataframe for selected year
        dff = by_purpose[by_purpose.Year == selected_year ]
        return {'data' : [go.Bar(
                                 x=dff['Purpose of visit'].values,
                                 y=dff['No of tourists'].values,
                                 name = "Histogram "
                                )
                         ],
                'layout': go.Layout(
                             title= 'Tourist Arrival By Purpose',
                             xaxis={ 'title': 'Purpose of Visit in: {}'.format(selected_year)},
                             yaxis={'title': 'Total No of visitors'},
                             hovermode='closest'
                 )


               }

    elif selected_option == 'BY':
            return {
                'data' : [go.Scatter(
                            x = by_year.date.values,
                            y = by_year.Visitors.values,
                            mode = 'lines+markers'
                                    )
                         ],
                 'layout': go.Layout(
                             title= 'Tourist Arrival By Year',
                             xaxis={ 'title': 'Years (1992-2013)'},
                             yaxis={'title': 'No of visitors'},
                             hovermode='closest'
                 )
                    }
                    

if __name__ == '__main__':
    app.run_server()
