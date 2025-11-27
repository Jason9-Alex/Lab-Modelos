import dash
from dash import html, dcc, Input, Output, callback
import plotly.graph_objs as go
import numpy as np

dash.register_page(__name__, path='/pagina1', name='Modelo Exponencial')

layout = html.Div([
    # --- CONTENEDOR IZQUIERDO: TEORÍA Y CONTROLES ---
    html.Div([
        html.H3("Crecimiento Exponencial", className="title"),
        
        # Tarjeta de Teoría (MathJax)
        html.Div([
            dcc.Markdown(r'''
            El modelo de Malthus asume que la tasa de crecimiento es proporcional a la población actual.
            
            $$ P(t) = P_0 e^{rt} $$
            
            Donde:
            * $P_0$: Población inicial.
            * $r$: Tasa de crecimiento intrínseca.
            ''', mathjax=True, style={'fontSize': '14px', 'color': '#555'})
        ], style={'backgroundColor': '#f9fafb', 'padding': '10px', 'borderRadius': '8px', 'marginBottom': '20px'}),

        html.H4("Parámetros", className="title", style={'fontSize':'18px'}),

        # Inputs Interactivos
        html.Div([
            html.Label("Población Inicial (P0):"),
            dcc.Slider(min=10, max=500, step=10, value=100, id='exp-p0',
                       marks={10:'10', 500:'500'}, 
                       tooltip={"placement": "bottom", "always_visible": True})
        ], style={'marginBottom': '15px'}),

        html.Div([
            html.Label("Tasa de Crecimiento (r):"),
            dcc.Slider(min=0.01, max=0.1, step=0.005, value=0.03, id='exp-r',
                       marks={0.01:'1%', 0.05:'5%', 0.1:'10%'}, 
                       tooltip={"placement": "bottom", "always_visible": True})
        ], style={'marginBottom': '15px'}),

        html.Div([
            html.Label("Tiempo de proyección (t):"),
            dcc.Slider(min=10, max=200, step=10, value=100, id='exp-t',
                       marks={10:'10', 200:'200'}, 
                       tooltip={"placement": "bottom", "always_visible": True})
        ]),

    ], className="content left", style={'width': '35%'}),

    # --- CONTENEDOR DERECHO: GRÁFICA Y KPI ---
    html.Div([
        # KPI: Tiempo de Duplicación
        html.Div([
            html.H5("Tiempo de Duplicación", style={'margin': '0', 'color': '#064e3b'}),
            html.H2(id='kpi-doubling-time', children="0 años", style={'margin': '0', 'color': '#10b981'}),
            html.P("Tiempo necesario para que la población se multiplique por 2.", style={'fontSize': '12px', 'color': 'gray'})
        ], style={'backgroundColor': '#ecfdf5', 'padding': '15px', 'borderRadius': '10px', 'marginBottom': '20px', 'textAlign': 'center', 'border': '1px solid #a7f3d0'}),

        # Gráfica
        html.H3("Proyección Visual", className="title"),
        dcc.Graph(id='graph-exponential', style={'height': '400px'})
        
    ], className="content right", style={'width': '65%'})

], className="page-container", style={'flexDirection': 'row', 'alignItems': 'flex-start'})


@callback(
    [Output("graph-exponential", "figure"),
     Output("kpi-doubling-time", "children")],
    [Input("exp-p0", "value"),
     Input("exp-r", "value"),
     Input("exp-t", "value")]
)
def actualizar_exponencial(P0, r, t_max):
    # 1. Cálculos matemáticos
    t = np.linspace(0, t_max, 100)
    
    # Modelo Exponencial
    P_exp = P0 * np.exp(r * t)
    
    # Modelo Lineal (para comparar y mostrar por qué el exp es "explosivo")
    # Asumimos crecimiento constante basado en la tasa inicial
    P_lin = P0 + (P0 * r) * t 

    # Cálculo del Tiempo de Duplicación: Td = ln(2) / r
    if r > 0:
        td = np.log(2) / r
        kpi_text = f"{td:.1f} unidades de tiempo"
    else:
        kpi_text = "Infinito (r=0)"

    # 2. Crear la Gráfica
    fig = go.Figure()

    # Traza Exponencial (La principal)
    fig.add_trace(go.Scatter(
        x=t, y=P_exp, mode='lines', name='Crecimiento Exponencial',
        line=dict(color='#2563eb', width=4),
        fill='tozeroy', # Relleno suave debajo
        fillcolor='rgba(37, 99, 235, 0.1)' 
    ))

    # Traza Lineal (Comparación)
    fig.add_trace(go.Scatter(
        x=t, y=P_lin, mode='lines', name='Comparación Lineal',
        line=dict(color='gray', width=2, dash='dot'),
        hovertemplate='Si fuera lineal: %{y:.1f}<extra></extra>'
    ))

    # Layout limpio
    fig.update_layout(
        title=dict(text="<b>Curva Exponencial vs Lineal</b>", x=0.5, y=0.95, xanchor='center'),
        xaxis_title="Tiempo (t)",
        yaxis_title="Población P(t)",
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=40, r=40, t=60, b=80), # Márgenes corregidos
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )

    return fig, kpi_text