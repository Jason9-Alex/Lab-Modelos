import numpy as np
import plotly.graph_objs as go

def funcion_graficas_ecu_log(n_clicks, P0, r, K, t_max):
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
