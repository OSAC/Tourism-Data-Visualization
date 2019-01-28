import dash
import dash_core_components as dcc
import dash_core_components 
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import numpy as np
import pandas as pd

by_month_df = pd.read_csv('data/by_month_year')
app = dash.Dash()

app.layout = html.Div([
    dash_core_components.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=by_month_df['Year'].min(),
        max=by_month_df['Year'].max(),
        value=by_month_df['Year'].min(),
        marks={str(year): str(year) for year in by_month_df['Year'].unique()}
    )
])

#app.config['suppress_callback_exceptions']=True                    
@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])

def update_figure(selected_year):
    filtered_df = by_month_df[by_month_df.Year == selected_year]
    traces = []
    
    traces.append(go.Scatter(
        x = filtered_df['Month'],
        y = filtered_df['Visitors'],
        mode='markers',
        opacity=0.7,
        marker={
            'size': 15,
            'line': {'width': 0.5, 'color': 'white'}
        }
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={ 'title': 'Months'},
            yaxis={'title': 'No of visitors'},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()
