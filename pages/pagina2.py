import dash    
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np

P0 = 900000
K = 1072764
r = 0.2311
t = np.linspace(0, 12, 100)  # Tiempo en años
P_logistico = (P0 * K * np.exp(r * t)) / ((K - P0) + P0 * np.exp(r * t))
P_exponencial = P0 * np.exp(r * t)
#SCATTER PLOT
trace_exponencial = go.Scatter(
    x=t,
    y=P_exponencial,
    mode='lines',
    line=dict(color='green', width=3, dash='solid'),
    name='Crecimiento Exponencial',
    hovertemplate='t: %{x:.1f}<br>P(t): %{y:.0f}<extra></extra>'
)
trace_logistico = go.Scatter(
    x=t,
    y=P_logistico,
    mode='lines',
    line=dict(color='blue', width=3),
    name='Crecimiento Logístico',
    hovertemplate='t: %{x:.1f}<br>P(t): %{y:.0f}<extra></extra>'
)
trace_capacidad = go.Scatter(
    x=t,
    y=[K] * len(t),
    mode='lines',
    line=dict(color='red', width=2, dash='dash'),
    name=f'Capacidad de Carga (K={K})',
    hovertemplate='Capacidad de Carga: ' + str(K) + '<extra></extra>'
)
trace_inicial = go.Scatter(
    x=[0],
    y=[P0],
    mode='markers+text',
    marker=dict(color='black', size=10),
    text=[f'P₀={P0}'],
    textposition='top right',
    name='Población Inicial',
    hovertemplate='Población Inicial: ' + str(P0) + '<extra></extra>'
)

# Crear la figura con todas las trazas
fig = go.Figure(data= [trace_exponencial, trace_logistico, trace_capacidad, trace_inicial])
fig.update_layout(
    title=dict(
        text='<b>Comparación: Crecimiento Exponencial vs Logístico</b>',
        font=dict(size=20, color='black'),
        x=0.5,
        y=0.95,
    ),
    xaxis_title="Tiempo (t)",
    yaxis_title="Población P(t)",
    hovermode='closest',
    margin=dict(l=40, r=40, t=80, b=40),
    paper_bgcolor='lightblue',
    font=dict(
        family="Outfit",
        size=12,
        color="black"
    ),
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
        bgcolor='rgba(255,255,255,0.8)'
    )
)
fig.update_xaxes(
    showgrid=True, gridwidth=1, gridcolor='LightGray',
    zeroline=True, zerolinewidth=2, zerolinecolor='Gray',
    showline=True, linewidth=2, linecolor='Black', mirror=True,
)

fig.update_yaxes(
    showgrid=True, gridwidth=1, gridcolor='LightGray',
    zeroline=True, zerolinewidth=2, zerolinecolor='Gray',
    showline=True, linewidth=2, linecolor='Black', mirror=True,
)

dash.register_page(__name__, path='/b', name='Pagina2')

layout = html.Div(children=[ 
    
    #contenedor izquierdo
        html.Div(children=[
            html.H3("Crecimiento de la Población y Capacidad de Carga", className="title"),
    
        dcc.Markdown("""
Modelo Logístico con Capacidad de Carga  
Consideremos la ecuación diferencial logística sujeta a una población inicial de $P_0$  
con capacidad de carga $K$ y tasa de crecimiento $r$.  
Solución del Problema de Valor Inicial  
La solución del correspondiente problema de valor inicial viene dada por:

$$
P(t) = \\frac{P_0 K e^{rt}}{(K - P_0) + P_0 e^{rt}}
$$
""", mathjax=True),

dcc.Markdown("""
Caso de Estudio Específico

Utilizamos los valores:
- Población inicial: $P_0 = 900000$ ciervos
- Tasa de crecimiento: $r = 0.2311$
- Capacidad de carga: $K = 1072764$

Desarrollo Matemático

$$
P(t) = \\frac{900000 \cdot 1072764 \cdot e^{0.2311t}}{(1072764 - 900000) + 900000 \cdot e^{0.2311t}} = \\frac{900000 \cdot 1072764 \cdot e^{0.2311t}}{172764 + 900000 \cdot e^{0.2311t}}
$$
Dividiendo la parte superior e inferior entre $900000$ obtenemos:

$$
P(t) = \\frac{1072764 \cdot e^{0.2311t}}{0.19196 + e^{0.2311t}}
$$
""", mathjax=True),
    
    dcc.Markdown("""
    #### Interpretación

    La gráfica muestra cómo el modelo logístico (azul) se estabiliza en la capacidad de carga, 
    mientras que el modelo exponencial (verde) crece sin límite, demostrando la importancia 
    de incluir límites ambientales en los modelos poblacionales.
    """),
    
], className="content left"),
    
    #contenedor derecho
    html.Div(children=[
        html.H3("Grafica", className="title"),
        dcc.Graph( 
            figure=fig,
            style={"height":"350px",'width':"100%"},
        )
    ],className="content right")
],className="page-container" )