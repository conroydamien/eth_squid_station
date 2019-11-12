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
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import requests

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
                            src=app.get_asset_url("squid-logo-1.png"),
                            id="plotly-image",
                            style={
                                "height": "100px",
                                "width": "auto",
                                "margin-bottom": "0px",
                                'margin-top':'0px'
                            },
                        )
                    ],
                    className="one-third column",
                    style={"margin-bottom": "0px","margin-top": "0px"},
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "",
                                    style={"margin-bottom": "0px","margin-top": "0px"},
                                ),
                                html.H5(
                                    "", style={"margin-bottom": "0px","margin-top": "0px"},
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    style={"margin-bottom": "0px","margin-top": "0px"},
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
                    style={"margin-bottom": "0px","margin-top": "0px"},
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "0px","margin-top": "0px"},
        ),
                    html.Div(
                            [
                                html.Div(
                                    [dcc.Interval(id='interval1', interval=3 * 1000, n_intervals=0),
                                    html.H4(id="Block Number"), html.H6("Block Number")],
                                    id="dangerously",
                                    className="mini_container",
                                    style={"width": "300px",'text-align':'center','font-size':'large','margin-top':'0px','margin-bottom':'0px'},
                                ),
                                html.Div(
                                    [dcc.Interval(id='interval2', interval=3 * 1000, n_intervals=0),
                                    html.H4(id="Safe"), html.H6("Safe < 30 min")],
                                    id="safe",
                                    className="mini_container",
                                    style={"width": "300px",'text-align':'center','font-size':'large','margin-top':'0px','margin-bottom':'0px'},
                                ),
                                html.Div(
                                    [dcc.Interval(id='interval3', interval=3 * 1000, n_intervals=0),
                                    html.H4(id="Standard"), html.H6("Standard < 5 min")],
                                    id="standard",
                                    className="mini_container",
                                    style={"width": "300px",'text-align':'center','font-size':'large','margin-top':'0px','margin-bottom':'0px'},
                                ),
                                html.Div(
                                    [dcc.Interval(id='interval4', interval=3 * 1000, n_intervals=0),
                                    html.H4(id="Fast"), html.H6("Fast < 2 min")],
                                    id="fast",
                                    className="mini_container",
                                    style={"width": "300px",'text-align':'center','font-size':'large','margin-top':'0px','margin-bottom':'0px'},
                                ),
                                html.Div(
                                    [dcc.Interval(id='interval5', interval=3 * 1000, n_intervals=0),
                                    html.H4(id="Fastest"), html.H6("Fastest ~ 1 Block")],
                                    id="fastest",
                                    className="mini_container",
                                    style={"width": "300px",'text-align':'center','font-size':'large','margin-top':'0px','margin-bottom':'0px'},
                                ),

                            ],
                            id="",
                            className="row container-display",
                            style={'position':'center'}
                        ),



        html.Div(
            [
                html.Div(

                    [
                    html.H4('Comparison of Gas Price Recommendations', style={"display": "flex", "flex-direction": "column",'margin-top':'0px'}),
                    dcc.Graph(id="main-graph"),
                    dcc.Interval(id='graph-update',interval=3 * 1000, n_intervals=0)],
                    className=" pretty_container",
                    style={'text-align':'center'},
                ),
            ],
            style={'margin-top':'0px'}
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column",'margin-top':'0px'},
)

@app.callback(dash.dependencies.Output('Block Number', 'children'),
    [dash.dependencies.Input('interval1', 'n_intervals')])
def update(n_intervals):
    with open('ethgasAPI.json') as f:
        api = json.load(f)
    return api['blockNum']

@app.callback(dash.dependencies.Output('Safe', 'children'),
    [dash.dependencies.Input('interval2', 'n_intervals')])
def update(n_intervals):
    with open('ethgasAPI.json') as f:
        api = json.load(f)
    return api['safeLow']


@app.callback(dash.dependencies.Output('Standard', 'children'),
    [dash.dependencies.Input('interval3', 'n_intervals')])
def update(n_intervals):
    with open('ethgasAPI.json') as f:
        api = json.load(f)
    return api['standard']

@app.callback(dash.dependencies.Output('Fast', 'children'),
    [dash.dependencies.Input('interval4', 'n_intervals')])
def update(n_intervals):
    with open('ethgasAPI.json') as f:
        api = json.load(f)
    return api['fast']

@app.callback(dash.dependencies.Output('Fastest', 'children'),
    [dash.dependencies.Input('interval5', 'n_intervals')])
def update(n_intervals):
    with open('ethgasAPI.json') as f:
        api = json.load(f)
    return api['fastest']

@app.callback(dash.dependencies.Output('main-graph', 'figure'),
    [dash.dependencies.Input('graph-update', 'n_intervals')])
def update(n_intervals):
    layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',showlegend=True,xaxis={'title':'Transaction Gas Budgets'},yaxis={'title':'Current Recommended Gas Price'})
    with open('ethgasAPI.json') as f:
        api = json.load(f)

        print(list(api.keys()))
    r = requests.get("https://ethgasstation.info/json/ethgasAPI.json")
    ethgasStation_dict = dict((k, r.json()[k]) for k in ('safeLow', 'average', 'fast', 'fastest','block_time'))

    ethgasStation_dict['standard'] = ethgasStation_dict['average']
    del ethgasStation_dict['average']
    print(ethgasStation_dict)
    del api["blockNum"]
    ethgasStation = [x / 10 for x in list(ethgasStation_dict.values())]
    print(ethgasStation)
    ethgasStation[-2] = ethgasStation[-2]*10
    trace1 = go.Bar(x=list(api.keys()),
                y=list(api.values()),
                name='Squid Predict',
                )
    trace2 = go.Bar(x=list(ethgasStation_dict.keys()),
            y=ethgasStation,
            name='Eth Gas Predict',
            )
    data = [trace1,trace2]
    return go.Figure(data=data, layout=layout)

# Main
if __name__ == "__main__":
    app.run_server(debug=False)
