import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import numpy as np

import geopandas as gpd

print('Loading data...')

gdf = gpd.read_file('nzmap.geojson')

gdf = gdf.to_crs(epsg=4326)

print('Done!')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

A1 = np.arange(2000,2020,1)
A2 = [str(x) for x in A1]

app.layout = html.Div([

    html.H1(
        children='NZ Road Cycling Fatalities',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
    ),

    html.Div([
                dcc.Dropdown(
                    id='dropdown_on',
                    options=[{'label': i, 'value': i} for i in A2],
                    value='2000'
                ),
    ],style={'width': '40%', 'display': 'inline-block',}),

html.Div([], style={'width':'100%'}),

    html.Div([
                dcc.Graph(id="fig")
    ],style={'width': '100%', 'display': 'inline-block', 'padding': '0 10',},),
]) 

@app.callback(
    Output("fig", "figure"), 
    [Input("dropdown_on", "value")])
def draw_choropleth(color_on):
    fig = px.choropleth_mapbox(gdf, 
                            geojson=gdf.geometry, 
                            locations=gdf.index, 
                            color=color_on,
                            color_continuous_scale="Viridis",
                            range_color=(0, 5),
                            mapbox_style="carto-positron",
                            zoom=4, 
                            center = {"lat":gdf.centroid.y.mean(), "lon":gdf.centroid.x.mean()},
                            opacity=0.5,
                            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                        height=700,
                        )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)