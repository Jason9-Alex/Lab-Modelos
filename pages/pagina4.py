import dash
from dash import html, dcc , Input, Output, State, callback
import numpy as np
import plotly.graph_objs as go
from utils.funciones import funcion_graficas_ecu_log

### Layout de la pagina ###

dash.register_page(__name__, path='/pagina4', name='Pagina 4')  
layout = html.Div([
    #contenedor izquierdo
    html.Div([
        html.H3("Parametros del modelo", className="title"),

        html.Div([
            html.Label("Poblacion Inicial P(0):"),
            dcc.Input(id="input-p0", type="number", value=200,className="input-field")
            
        ],className="input-group"),
        html.Div([
            html.Label("Tasa de Crecimiento (r):"),
            dcc.Input(id="input-r", type="number", value=0.04,className="input-field")
        ],className="input-group"),
        html.Div([
            html.Label("capacidad de carga(K):"),
            dcc.Input(id="input-k", type="number", value=750 ,className="input-field")
        ],className="input-group"),
        html.Div([
            html.Label("Tiempo maximo(t):"),
            dcc.Input(id="input-t", type="number", value=100,className="input-field")
        ],className="input-group"),
        html.Button("Generar Grafica", id="simulate-button", className="simulate-button")
    ],className="content left"),

#contenedor derecho 
    html.Div([
        html.H3("Grafica", className="title"),
        dcc.Graph(
              id = 'grafica-poblacion',
              style={'height': '350px' ,'width':'100%'},
            )
      
    ],className="content right")
          
],className="page-container")



###CALLBACKS###

@callback(
    Output("grafica-poblacion-4", "figure"),
    Input("simulate-button", "n_clicks"),  # <-- este es el ID correcto del botón
    State("input-p0", "value"),
    State("input-r", "value"),
    State("input-k", "value"),             # <-- minúscula
    State("input-t", "value"),
    prevent_initial_call=False
)
def actualizar_grafica(n_clicks, P0, r, K, t_max):
    fig = funcion_graficas_ecu_log(n_clicks, P0, r, K, t_max)
    return fig

