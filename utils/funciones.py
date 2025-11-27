import numpy as np
import plotly.graph_objs as go
from scipy.integrate import odeint

# Definimos la ecuación diferencial fuera para que odeint la use
def modelo_cosecha_edo(P, t, r, K, h):
    # Ecuación: Crecimiento logístico MENOS la cosecha constante h
    dPdt = r * P * (1 - P/K) - h
    return dPdt

def funcion_grafica_cosecha(n_clicks, P0, r, K, t_max, h):
    # 1. Generar vector de tiempo (más puntos para que la curva sea suave)
    t = np.linspace(0, t_max, 200)

    # 2. Resolver la ecuación diferencial numéricamente
    # Pasamos los argumentos r, K, h a la función
    P = odeint(modelo_cosecha_edo, P0, t, args=(r, K, h))
    P = P.flatten() # Convertimos matriz a vector simple

    # 3. Lógica de Extinción:
    # Si la población baja de 0, matemáticamente sigue, pero biológicamente es 0.
    P[P < 0] = 0
    
    # Detectar si se extinguió para cambiar el color de la línea
    se_extingue = np.any(P == 0)
    color_linea = 'red' if se_extingue else '#10b981' # Rojo si muere, Verde si vive

    # --- CREAR LA FIGURA ---
    fig = go.Figure()

    # Traza 1: Población
    fig.add_trace(go.Scatter(
        x=t,
        y=P,
        mode='lines', # Quitamos markers para que se vea más limpio
        name='Población P(t)',
        line=dict(color=color_linea, width=4),
        hovertemplate='Día: %{x:.1f}<br>Población: %{y:.1f}<extra></extra>'
    ))

    # Traza 2: Capacidad de Carga
    fig.add_trace(go.Scatter(
        x=[0, t_max],
        y=[K, K],
        mode='lines',
        name='Capacidad (K)',
        line=dict(color='gray', width=2, dash='dash'),
        hovertemplate='K: %{y}<extra></extra>'
    ))

    # Traza 3: Umbral de Extinción (Línea en 0)
    fig.add_trace(go.Scatter(
        x=[0, t_max],
        y=[0, 0],
        mode='lines',
        name='Extinción',
        line=dict(color='black', width=1),
        showlegend=False
    ))

    # --- DISEÑO (LAYOUT) MEJORADO ---
    fig.update_layout(
        title=dict(
            text=f'<b>Modelo con Cosecha (h={h})</b>',
            y=0.95,
            x=0.5,
            xanchor='center',
            font=dict(size=20, color='#064e3b')
        ),
        xaxis_title="Tiempo (t)",
        yaxis_title="Población P(t)",
        hovermode='x unified', # Muestra toda la info en una línea vertical
        template='plotly_white', # Fondo blanco limpio
        
        # MÁRGENES: Aquí arreglamos que las letras no se junten
        margin=dict(l=40, r=40, t=80, b=80), 
        
        legend=dict(
            orientation="h",     # Horizontal
            yanchor="top",
            y=-0.2,              # Abajo del gráfico
            xanchor="center",
            x=0.5
        )
    )

    return fig