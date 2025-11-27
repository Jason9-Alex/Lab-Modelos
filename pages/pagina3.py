import dash
from dash import html, dcc, Input, Output, State, callback
import numpy as np
import plotly.graph_objs as go

dash.register_page(__name__, path='/pagina3', name='Modelo Logístico')

layout = html.Div([
    # --- ENCABEZADO CON ECUACIÓN (MathJax) ---
    html.Div([
        html.H3("Modelo de Crecimiento Logístico", className="title"),
        dcc.Markdown(
            r'''
            La ecuación diferencial es:  $\frac{dP}{dt} = rP(1 - \frac{P}{K})$
            ''', 
            mathjax=True,
            style={'textAlign': 'center', 'fontSize': '18px', 'color': '#064e3b'}
        )
    ], style={'marginBottom': '20px'}),

    html.Div([
        # --- PANEL IZQUIERDO: CONTROLES (SLIDERS) ---
        html.Div([
            html.H4("Parámetros", className="title", style={'fontSize':'18px'}),
            
            html.Label("Población Inicial (P0)"),
            dcc.Slider(min=0, max=500, step=10, value=50, id='slider-p0', 
                       marks={0:'0', 500:'500'}, tooltip={"placement": "bottom", "always_visible": True}),
            
            html.Br(),
            html.Label("Tasa de crecimiento (r)"),
            dcc.Slider(min=0, max=1, step=0.01, value=0.1, id='slider-r',
                       marks={0:'0', 1:'1'}, tooltip={"placement": "bottom", "always_visible": True}),

            html.Br(),
            html.Label("Capacidad de Carga (K)"),
            dcc.Slider(min=100, max=1000, step=50, value=800, id='slider-k',
                       marks={100:'100', 1000:'1K'}, tooltip={"placement": "bottom", "always_visible": True}),
            
            html.Br(),
            html.Label("Tiempo Máximo"),
            dcc.Slider(min=10, max=200, step=10, value=100, id='slider-t',
                       marks={10:'10', 200:'200'}, tooltip={"placement": "bottom", "always_visible": True}),

        ], className="content left", style={'width': '30%'}),

        # --- PANEL DERECHO: GRÁFICAS CON TABS ---
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='Población vs Tiempo', children=[
                    dcc.Graph(id='grafica-logistica-tiempo')
                ]),
                dcc.Tab(label='Velocidad de Crecimiento (dP/dt)', children=[
                     html.P("Esta parábola muestra que el crecimiento es máximo cuando P = K/2", 
                            style={'textAlign':'center', 'fontSize':'12px', 'color':'gray', 'marginTop':'10px'}),
                    dcc.Graph(id='grafica-logistica-fase')
                ]),
            ])
        ], className="content right", style={'width': '70%'})
        
    ], className="page-container", style={'flexDirection': 'row', 'alignItems': 'flex-start'})
])

@callback(
    [Output("grafica-logistica-tiempo", "figure"),
     Output("grafica-logistica-fase", "figure")],
    [Input("slider-p0", "value"),
     Input("slider-r", "value"),
     Input("slider-k", "value"),
     Input("slider-t", "value")]
)
def actualizar_logistica(P0, r, K, t_max):
    # Generar datos
    t = np.linspace(0, t_max, 200)
    # Solución exacta de la logística
    P = (K * P0 * np.exp(r * t)) / (K + P0 * (np.exp(r * t) - 1))
    
    # Calcular Derivada (dP/dt) para la segunda gráfica
    # dP/dt = r * P * (1 - P/K)
    P_fase = np.linspace(0, K * 1.1, 100) # Un rango de poblaciones posibles
    dP_dt = r * P_fase * (1 - P_fase / K)

    # --- GRAFICA 1: TIEMPO ---
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=t, y=P, mode='lines', name='Población', line=dict(color='#10b981', width=3)))
    # Línea de capacidad de carga
    fig1.add_trace(go.Scatter(x=[0, t_max], y=[K, K], mode='lines', name='Capacidad (K)', 
                             line=dict(color='red', dash='dash')))
    
    fig1.update_layout(
        title="Curva Sigmoidea (S)",
        xaxis_title="Tiempo", yaxis_title="Población",
        margin=dict(l=20, r=20, t=50, b=50),
        template="plotly_white",
        legend=dict(orientation="h", y=1.5 , x = 0.5, xanchor="center")
    )

    # --- GRAFICA 2: FASE (Parábola) ---
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=P_fase, y=dP_dt, mode='lines', name='Velocidad', 
                             fill='tozeroy', line=dict(color='#3b82f6')))
    
    # Marcamos el punto máximo (K/2)
    max_val = np.max(dP_dt)
    fig2.add_annotation(x=K/2, y=max_val, text="Máx Crecimiento (K/2)", showarrow=True, arrowhead=1)

    fig2.update_layout(
        title="Espacio de Fase: Velocidad vs Población",
        xaxis_title="Población (P)", yaxis_title="Velocidad (dP/dt)",
        margin=dict(l=20, r=20, t=50, b=50),
        template="plotly_white"
    )

    return fig1, fig2