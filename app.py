# Import required libraries
import pickle
import copy
import pathlib
import dash
import math
import time
import json
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html

# Multi-dropdown options
from controls import COUNTIES, WELL_STATUSES, WELL_TYPES, WELL_COLORS

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

# Create controls


# Load data
df = pd.read_csv(DATA_PATH.joinpath("alltx.csv"), low_memory=False)



# Create app layout
app.layout = html.Div(
    [
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("squid-logo.png"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "ETH Squid Station",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Gas Prediction", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Learn More", id="learn-more-button"),
                            href="https://github.com/dmintercept/eth_squid_station",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),

                        html.Div(
                            [
                                html.Div(
                                    [dcc.Interval(id='interval1', interval=5 * 1000, n_intervals=5),
                                    html.H6(id="Block Number"), html.P("Block Number")],
                                    id="dangerously",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [dcc.Interval(id='interval2', interval=5 * 1000, n_intervals=5),
                                    html.H6(id="Safe"), html.P("Safe")],
                                    id="safe",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [dcc.Interval(id='interval3', interval=5 * 1000, n_intervals=5),
                                    html.H6(id="Standard"), html.P("Standard")],
                                    id="standard",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [dcc.Interval(id='interval4', interval=5 * 1000, n_intervals=5),
                                    html.H6(id="Fast"), html.P("Fast")],
                                    id="fast",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [dcc.Interval(id='interval5', interval=5 * 1000, n_intervals=5),
                                    html.H6(id="Fastest"), html.P("Fastest")],
                                    id="fastest",
                                    # className="mini_container",
                                ),
                                html.Div(
                                    [dcc.Interval(id='interval6', interval=5 * 1000, n_intervals=5),
                                    html.H6(id="Very Fast"), html.P("Very Fast")],
                                    id="very fast",
                                    # className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),


        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="main_graph")],
                    className="pretty_container",
                ),
            ],
            #className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

@app.callback(dash.dependencies.Output('Block Number', 'children'),
    [dash.dependencies.Input('interval1', 'n_intervals')])
def update(n_intervals):
    with open('ethgasAPI.json') as f:
        api = json.load(f)
        print(api)  
    return api['blockNum']

@app.callback(dash.dependencies.Output('Safe', 'children'),
    [dash.dependencies.Input('interval2', 'n_intervals')])
def update(n_intervals):
    with open('ethgasAPI.json') as f:
        api = json.load(f)
        print(api)  
    return api['safeLow']


@app.callback(dash.dependencies.Output('Standard', 'children'),
    [dash.dependencies.Input('interval3', 'n_intervals')])
def update(n_intervals):
    with open('ethgasAPI.json') as f:
        api = json.load(f)
        print(api)  
    return api['standard']

@app.callback(dash.dependencies.Output('Fast', 'children'),
    [dash.dependencies.Input('interval4', 'n_intervals')])
def update(n_intervals):
    with open('ethgasAPI.json') as f:
        api = json.load(f)
        print(api)  
    return api['fast']

@app.callback(dash.dependencies.Output('Fastest', 'children'),
    [dash.dependencies.Input('interval5', 'n_intervals')])
def update(n_intervals):
    with open('ethgasAPI.json') as f:
        api = json.load(f)
        print(api)  
    return api['fastest']


# Main
if __name__ == "__main__":
    app.run_server(debug=True)