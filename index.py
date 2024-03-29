#IMPORTS
import dash
import plotly.plotly as py
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import numpy as np
import pandas as pd

#MAP AND PIECHART API
py.sign_in(username='Pasangdimdung', api_key= '8guPFK8ijphU3LjmCEJu')

# DATA
by_month_df = pd.read_csv('data/by_month_year')
by_year = pd.read_csv('data/modified_visitors_by_month', index_col = [0])
by_purpose = pd.read_csv('data/by_purpose_cleaned_new')
by_nationality = pd.read_csv('data/by_major_nationality_2013')
by_sex_age = pd.read_csv('data/by_sex_age')

app = dash.Dash()


#MAIN APP
app.layout = html.Div([

                html.H4(' Dash Board'),
                html.P(),
                 dcc.Dropdown(
                    id= 'options-dropdown',
                    options=[
                        {'label': 'By Purpose','value': 'BP'},
                        {'label': 'By Gender And Age','value': 'BGA'},
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
                            ),

                 html.P(),

                 dcc.Graph(
                    id= 'chloropleth-map',
                    figure = dict(
                         data=[ dict(
                                type = 'choropleth',
                                locations = by_nationality['CODE'],
                                z = by_nationality['No. of Tourist Days'],
                                text = by_nationality['Nationality'],
                                colorscale = [[0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
                                    [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
                                autocolorscale = False,
                                reversescale = True,
                                marker = dict(
                                    line = dict (
                                        color = 'rgb(180,180,180)',
                                        width = 0.5
                                    ) ),
                                colorbar = dict(
                                    autotick = False,
                                    title= 'Number of Tourists'),
                              ) ],
                          layout=dict(
                                  title = 'By Major Nationality (2013)',
                                  geo = dict(
                                          showframe = False,
                                          showcoastlines = False,
                                          projection = dict(
                                              type = 'Mercator'
                                                            )
                                          )
                                     )
                               )
                           )

                     ])

#DECORATOR
@app.callback(Output('graph-with-slider', 'figure'),
             [Input('year-slider', 'value'), Input('options-dropdown', 'value')])

def update_figure(selected_year, selected_option):
    #BY MONTH BLOCK
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

    #BY PURPOSE BLOCK
    elif selected_option == 'BP':
        # create a new dataframe for selected year
        dff = by_purpose[by_purpose.Year == selected_year ]
        return {'data' : [go.Bar(
                                 x=dff['Purpose of Visit'].values,
                                 y=dff['No of Tourists'].values,
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
   #BY YEAR BLOCK
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
    #BY GENDER BLOCK
    elif selected_option == 'BGA':
        filteredsexage_df = by_sex_age[by_sex_age.Years == selected_year]
        return {
                'data': [{
                      'values': [int(filteredsexage_df['Male'].values),int(filteredsexage_df['Female'].values)],
                      'labels': ['Male', 'Female'],
                      'domain': {"x": [0, .48]},
                      'name': 'Gender',
                      'hoverinfo':'label+value+name',
                      'textinfo':'label+percent',
                      'hole': .4,
                      'type': 'pie'
                         },

                         {
                      'values': [int(filteredsexage_df['15-below'].values),
                                 int(filteredsexage_df['16-30'].values),
                                 int(filteredsexage_df['31-45'].values),
                                 int(filteredsexage_df['46-60'].values),
                                 int(filteredsexage_df['61-over'].values),
                                 int(filteredsexage_df['Not_specified'].values),],
                      'labels': ['Below 15 yrs', '16-30 yrs', '31-45 yrs', '46-60 yrs', '61 and over', 'Not specified'],
                      'textposition':'inside',
                      'domain': {'x': [.52, 1]},
                      'name': 'Age Group',
                      'hoverinfo':'label+value+name',
                      'hole': .4,
                      'type': 'pie'
                      #'marker':{'colors':['#fac1b7', '#a9bb95', '#92d8d8']},
                    }],

              'layout': {
                    'title':"Tourists Arrival By Sex and Age 2003-2014",
                    'annotations': [{
                            "font": {"size": 20},
                            "showarrow": False,
                            "text": "GENDER",
                            "x": 0.20,
                            "y": 0.5
                                    },
                             {
                            "font": {"size": 20},
                            "showarrow": False,
                            "text": "AGE GRP",
                            "x": 0.8,
                            "y": 0.5
                                    }]
                         }
            }



if __name__ == '__main__':
    app.run_server()
