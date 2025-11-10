import dash
from dash import html, dcc, Input, Output, State, callback
import numpy as np
import plotly.graph_objs as go
from scipy.integrate import odeint 

dash.register_page(__name__, path='/Pagina7', name='Modelo SEIR')

layout = html.Div([
    html.Div([
        html.H4("Modelo SEIR - Epidemiología", className="title"),

        html.Div([
            html.Label("Población total (N):"),
            dcc.Input(id="input-N-seir", type="number", value=1000, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Tasa de exposición (β):"),
            dcc.Input(id="input-beta-seir", type="number", value=0.5, step=0.01, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Tasa de incubación (σ):"),
            dcc.Input(id="input-sigma", type="number", value=0.2, step=0.01, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Tasa de recuperación (γ):"),
            dcc.Input(id="input-gamma-seir", type="number", value=0.1, step=0.01, className="input-field")
        ], className="input-group"),
     
        html.Div([
            html.Label("Expuestos iniciales (E0):"),
            dcc.Input(id="input-E0", type="number", value=5, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Infectados iniciales (I0):"),
            dcc.Input(id="input-I0-seir", type="number", value=2, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Tiempo de simulación (días):"),
            dcc.Input(id="input-tiempo-seir", type="number", value=160, className="input-field")
        ], className="input-group"),

        html.Button("Simular epidemia", id="btn-simular-seir", className="btn-generar"),
        
        
    ], className="content left"),

    html.Div([
        html.H3("Evolución de la epidemia", className="title"),
        dcc.Graph(id="graph-SEIR", style={'height': '450px', 'width': '100%'})
    ], className="content right"),
], className="page-container")


# Función del sistema de ecuaciones diferenciales SEIR
def ecuaciones_SEIR(y, t, N, beta, sigma, gamma):
    S, E, I, R = y
    dSdt = -beta * S * I / N
    dEdt = beta * S * I / N - sigma * E
    dIdt = sigma * E - gamma * I
    dRdt = gamma * I
    return dSdt, dEdt, dIdt, dRdt


@callback(
    Output("graph-SEIR", "figure"),
    Input("btn-simular-seir", "n_clicks"),
    State("input-N-seir", "value"),
    State("input-beta-seir", "value"),
    State("input-sigma", "value"),
    State("input-gamma-seir", "value"),
    State("input-E0", "value"),
    State("input-I0-seir", "value"),
    State("input-tiempo-seir", "value"),
    prevent_initial_call=False
)
def actualizar_grafica_SEIR(n_clicks, N, beta, sigma, gamma, E0, I0, tiempo_max):
    # Validar inputs
    if None in (N, beta, sigma, gamma, E0, I0, tiempo_max) or N <= 0 or E0 < 0 or I0 < 0:
        return go.Figure()
    
    # Convertir a números
    N = float(N)
    beta = float(beta)
    sigma = float(sigma)
    gamma = float(gamma)
    E0 = float(E0)
    I0 = float(I0)
    tiempo_max = float(tiempo_max)
    
    # Condiciones iniciales
    S0 = N - E0 - I0
    R0_inicial = 0
    y0 = [S0, E0, I0, R0_inicial]
    
    # Vector de tiempo
    t = np.linspace(0, tiempo_max, 300)
    
    try:
        # Resolver el sistema de ecuaciones diferenciales
        solucion = odeint(ecuaciones_SEIR, y0, t, args=(N, beta, sigma, gamma))
        S, E, I, R = solucion.T
    except Exception as e:
        S = np.full_like(t, S0)
        E = np.full_like(t, E0)
        I = np.full_like(t, I0)
        R = np.full_like(t, R0_inicial)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t, y=S, mode='lines', name='Susceptibles (S)', 
        line=dict(color='blue', width=2), 
        hovertemplate='Día: %{x:.1f}<br>Susceptibles: %{y:.0f}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=t, y=E, mode='lines', name='Expuestos (E)', 
        line=dict(color='orange', width=2),
        hovertemplate='Día: %{x:.1f}<br>Expuestos: %{y:.0f}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=t, y=I, mode='lines', name='Infectados (I)', 
        line=dict(color='red', width=2),
        hovertemplate='Día: %{x:.1f}<br>Infectados: %{y:.0f}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=t, y=R, mode='lines', name='Recuperados (R)', 
        line=dict(color='green', width=2),
        hovertemplate='Día: %{x:.1f}<br>Recuperados: %{y:.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='<b>Evolución del Modelo SEIR</b>',
            x=0.5,
            font=dict(size=16, color='darkblue')
        ),
        xaxis_title="Tiempo (días)",
        yaxis_title="Número de personas",
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=80, b=40),  
        paper_bgcolor='lightcyan',
        font=dict(
            family="Outfit",
            size=12,
            color='black'
        ),
        legend=dict(
            orientation="h",
            yanchor="top",      
            y=-0.15,            
            xanchor="center",   
            x=0.5               
        )
    )

    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='Lightgrey',
        zeroline=True, 
        zerolinewidth=2, 
        zerolinecolor='grey'
    )
    fig.update_xaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='Lightgrey',
        zeroline=True, 
        zerolinewidth=2, 
        zerolinecolor='grey'
    )   
    return fig