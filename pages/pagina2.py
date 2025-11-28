import dash
from dash import html, dcc, Input, Output, State, callback
import plotly.graph_objs as go
import numpy as np
from scipy.integrate import odeint

dash.register_page(__name__, path='/pagina2', name='Modelo Logistico')

layout = html.Div([
    # --- ENCABEZADO ---
    html.Div([
        html.H3("Modelo Logistico de Crecimiento Poblacional", className="title"),
        dcc.Markdown(r'''
            
            Describe una población que necesita un número mínimo de individuos para sobrevivir.
            
            $$ \frac{dP}{dt} = rP \left( 1 - \frac{P}{K} \right) \left( \frac{P}{A} - 1 \right) $$
            
            * **$K$**: Capacidad de carga.
            * **$A$**: Umbral de extinción (Punto crítico).
            ''', mathjax=True, style={'textAlign': 'center', 'color': '#555'}
        )
    ], style={'marginBottom': '20px'}),

    html.Div([
        # --- CONTROLES ---
        html.Div([
            html.H4("Parámetros", className="title", style={'fontSize':'18px'}),
            
            html.Label("Población Inicial (P0) - ¡Prueba debajo de A!"),
            dcc.Slider(min=0, max=100, step=5, value=30, id='allee-p0',
                       marks={0:'0', 100:'100'}, 
                       tooltip={"placement": "bottom", "always_visible": True}),
            
            html.Br(),
            html.Label("Umbral de Extinción (A)"),
            dcc.Slider(min=0, max=50, step=5, value=20, id='allee-a',
                       marks={0:'0', 20:'20', 50:'50'}, 
                       tooltip={"placement": "bottom", "always_visible": True}),
            
            html.Br(),
            html.Label("Capacidad de Carga (K)"),
            dcc.Slider(min=100, max=500, step=50, value=300, id='allee-k',
                       marks={100:'100', 500:'500'}, 
                       tooltip={"placement": "bottom", "always_visible": True}),
            
            html.Br(),
            html.Label("Tasa de Crecimiento (r)"),
            dcc.Slider(min=0.1, max=1.0, step=0.1, value=0.5, id='allee-r',
                       marks={0.1:'0.1', 1.0:'1.0'}, 
                       tooltip={"placement": "bottom", "always_visible": True}),

        ], className="content left", style={'width': '30%'}),

        # --- GRÁFICA ---
        html.Div([
            html.H3("Dinámica Poblacional", className="title"),
            dcc.Graph(id='grafica-allee', style={'height': '400px'}),
            html.Div(id='mensaje-allee', style={'textAlign': 'center', 'marginTop': '10px', 'fontWeight': 'bold'})
        ], className="content right", style={'width': '70%'})

    ], className="page-container", style={'flexDirection': 'row', 'alignItems': 'flex-start'})
])

# Ecuación Diferencial del Efecto Allee
def modelo_allee(P, t, r, K, A):
    # dP/dt = r * P * (1 - P/K) * (P/A - 1)
    return r * P * (1 - P/K) * (P/A - 1)

@callback(
    [Output("grafica-allee", "figure"),
     Output("mensaje-allee", "children"),
     Output("mensaje-allee", "style")],
    [Input("allee-p0", "value"),
     Input("allee-a", "value"),
     Input("allee-k", "value"),
     Input("allee-r", "value")]
)
def actualizar_allee(P0, A, K, r):
    t = np.linspace(0, 50, 200)
    
    # Resolver EDO
    P = odeint(modelo_allee, P0, t, args=(r, K, A))
    P = P.flatten()
    
    # Análisis del resultado
    final_p = P[-1]
    
    # Lógica de colores y mensajes
    if final_p < 1: # Extinción
        color_linea = '#ef4444' # Rojo
        msg = " La población se extinguió (P0 < A). No hubo suficientes individuos para reproducirse."
        msg_style = {'color': '#ef4444', 'fontSize': '16px'}
    else: # Supervivencia
        color_linea = '#10b981' # Verde
        msg = " La población prosperó y alcanzó su capacidad de carga (P0 > A)."
        msg_style = {'color': '#10b981', 'fontSize': '16px'}

    # Graficar
    fig = go.Figure()

    # Curva de Población
    fig.add_trace(go.Scatter(x=t, y=P, mode='lines', name='Población', line=dict(color=color_linea, width=4)))
    
    # Línea de Capacidad (K)
    fig.add_trace(go.Scatter(x=[0, 50], y=[K, K], mode='lines', name='Capacidad (K)', 
                             line=dict(color='gray', dash='dash')))
    
    # Línea de Umbral (A) - ¡La parte importante!
    fig.add_trace(go.Scatter(x=[0, 50], y=[A, A], mode='lines', name='Umbral Crítico (A)', 
                             line=dict(color='orange', dash='dot', width=2)))

    # Área de peligro (Relleno rojo debajo de A)
    fig.add_hrect(y0=0, y1=A, line_width=0, fillcolor="red", opacity=0.1, annotation_text="Zona de Extinción")

    fig.update_layout(
        title=dict(text=f'<b>Población Inicial: {P0} vs Umbral: {A}</b>', x=0.5, xanchor='center'),
        xaxis_title="Tiempo",
        yaxis_title="Población",
        template="plotly_white",
        margin=dict(l=40, r=40, t=60, b=80),
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor='center')
    )

    return fig, msg, msg_style