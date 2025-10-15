import dash
from dash import html, dcc , Input, Output, State, callback
import numpy as np
import plotly.graph_objs as go

### Layout de la pagina ###

dash.register_page(__name__, path='/pagina3', name='Pagina 3')  
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
    Output("grafica-poblacion", "figure"),
    Input("simulate-button", "n_clicks"),  # <-- este es el ID correcto del botón
    State("input-p0", "value"),
    State("input-r", "value"),
    State("input-k", "value"),             # <-- minúscula
    State("input-t", "value"),
    prevent_initial_call=False
)
def actualizar_grafica(n_clicks, P0, r, K, t_max):
    #Generar datos de la grafica
    t = np.linspace(0, t_max, 20)

    #Ecuacion logistica
    P = (P0 * K * np.exp(r * t)) / (K + P0 * (np.exp(r * t) - 1) )

    #Crear la figura
    trace_poblacion = go.Scatter(
        x=t,
        y=P,
        mode='lines+markers',
        name='Poblacion P(t)',
        line=dict(
            color='black',
            width=2,
            ),
        marker=dict(
            size=6,
            color='red',
            symbol='circle' 
        ),
        hovertemplate='t=%{x:.2f}<br>P(t)=%{y:.2f}<extra></extra>'

    )

    ##Crear grafico de la capacidad de carga
    trace_capacidad = go.Scatter(
        x=[0,t_max],
        y=[K,K],
        mode='lines',
        name='Capacidad de carga (K)',
        line=dict(
            color='red',
            width=2,
            dash='dot' 
        ),
        hovertemplate='K: %{y:.2f}<extra></extra>'
    )
    fig = go.Figure(data=[trace_poblacion, trace_capacidad])
   
    fig.update_layout(
    title=dict(
        text='<b> Modelo Logistico de crecimiento poblacional</b>',
        font= dict(
            size=20,
            color='black',
            ),
            x=0.5,
            y=0.95,
        ),
    xaxis_title="Tiempo (t)",
    yaxis_title="Población P(t)",
    hovermode='closest',
    margin = dict(l=40, r=40, t=70, b=40),
    paper_bgcolor='lightblue',
    font = dict(
        family="Outfit",
        size=12,
        color="black"
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom", 
        y=1.02,
    )
)

    fig.update_xaxes(
    showgrid=True,gridwidth=1,gridcolor='LightGray',
    zeroline=True, zerolinewidth=2, zerolinecolor='Gray',
    showline=True, linewidth=2, linecolor='Black', mirror=True,
    range = [0, t_max]
    )

    fig.update_yaxes(
    showgrid=True,gridwidth=1,gridcolor='LightGray',
    zeroline=True, zerolinewidth=2, zerolinecolor='Gray',
    showline=True, linewidth=2, linecolor='Black', mirror=True,
    range = [0, K + K*0.1]
    )

    
    return fig
