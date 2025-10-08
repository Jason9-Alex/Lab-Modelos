import dash    
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np


PO=100  # Población inicial
r=0.03  # Tasa de crecimiento  
t = np.linspace(0, 100, 30)  # Tiempo
P = PO * np.exp(r * t)  # Función de crecimiento exponencial

#SCATTER PLOT
trace = go.Scatter(
    x=t,
    y=P,
    mode='lines+markers',
    marker=dict(color='blue', size=4),
    name='Datos de Población'
)
name = 'P(t) = P0*e^(rt)',
hovertemplate ='t : %{x}<br>P(t) : %{y}<extra></extra>'

#crear la figura
fig=go.Figure(data=trace)
fig.update_layout(
    title=dict(
        text='<b> Crecimiento Exponencial de la Población </b>',
        font= dict(
            size=20,
            color='black',
            ),
            x=0.5,
            y=0.9,
        ),
    xaxis_title="Tiempo (t)",
    yaxis_title="Población P(t)",
    hovermode='closest',
    margin = dict(l=40, r=40, t=60, b=40),
    paper_bgcolor='lightblue',
    font = dict(
        family="Outfit",
        size=12,
        color="black"
    )
)
fig.update_xaxes(
    showgrid=True,gridwidth=1,gridcolor='LightGray',
    zeroline=True, zerolinewidth=2, zerolinecolor='Gray',
    showline=True, linewidth=2, linecolor='Black', mirror=True,
)
fig.update_yaxes(
    showgrid=True,gridwidth=1,gridcolor='LightGray',
    zeroline=True, zerolinewidth=2, zerolinecolor='Gray',
    showline=True, linewidth=2, linecolor='Black', mirror=True,
)

dash.register_page(__name__, path='/a', name='Pagina1')

layout = html.Div(children= [ 
    
    #contenedor izquierdo
    html.Div(children = [
        html.H2("Crecimineto de la poblacion y capacidad de carga",className="title"),
        
        dcc.Markdown(""" 
        Para modelar el crecimiento de la población mediante una ecuación 
        diferencial, primero tenemos que introducir algunas variables y 
        términos relevantes. La variable $t$ representará el tiempo. Las 
        unidades de tiempo pueden ser horas, días, semanas,meses o incluso 
        años. Cualquier problema dado debe especificar las unidades utilizadas 
        en ese problema en particular. La variable  $P$ representará a la 
        población. Como la población varía con el tiempo, se entiende que 
        es una función del tiempo. Por lo tanto, utilizamos la notación $P(t)$ 
        para la población en función del tiempo. Si  $P(t)$ es una función 
        diferenciable, entonces la primera derivada  $\\frac{dP}{dt}$ representa
        la tasa instantánea de cambio de la población en función del tiempo.
        """,mathjax=True ),
        
            dcc.Markdown(""" 
        Un ejemplo de función de crecimiento exponencial es  $P(t)=P_0^ert$.
        En esta función,  $P(t)$
        representa la población en el momento  $t$,$P_0$
        representa la población inicial (población en el tiempo  $t=0$),
        y la constante  r>0
        se denomina tasa de crecimiento. La Figura 4.18 muestra un gráfico de  P(t)=100e0,03t.
        Aquí  $P_0=100$  y  $r=0,03$.
        """,mathjax=True ),
        ],className="content left"),
    


    #contenedor derecho
    html.Div(children=[
        html.H2("Grafica", className="title"),
        dcc.Graph( 
            figure=fig,
            style={"height":"350px",'width':"100%"},
        )
    ],className="content right")
],className="page-container" )
