import dash
from dash import html, dcc, Input, Output, callback
from dash import html, dcc, Input, Output, State, callback
import plotly.graph_objs as go
import numpy as np
from scipy.integrate import odeint

dash.register_page(__name__, path='/caso_rumor', name='Caso 2: Rumor Social', order =10)

layout = html.Div([
    # --- ENCABEZADO ---
    html.Div([
        html.H3("Caso de Estudio: El Rumor en la Facultad (Q1-Q6)", className="title"),
        dcc.Markdown(r'''
        **Contexto Social:** Un rumor se esparce en una clase de Derecho Penal.
        
        * **Susceptibles (S):** Alumnos que no saben el rumor.
        * **Propagadores (I):** Alumnos difundiendo el chisme.
        * **Racionales (R):** Docentes o alumnos escépticos que cortan la cadena.
        
        **Ecuaciones:** $\frac{dS}{dt} = -bSI$, $\frac{dI}{dt} = bSI - kI$, $\frac{dR}{dt} = kI$
        ''', mathjax=True, style={'color': '#444'})
    ], style={'marginBottom': '20px'}),

    html.Div([
        # --- PANEL IZQUIERDO: CONTROLES ---
        html.Div([
            html.H4("Condiciones del Rumor", className="title"),
            
            html.Label("Población Total (N):"),
            dcc.Input(id="rum-N", type="number", value=275, className="input-field"),
            
            html.Label("Tasa de Propagación 'b' (beta):"),
            dcc.Input(id="rum-b", type="number", value=0.004, step=0.001, className="input-field"),
            
            html.Label("Nivel de Racionalidad 'k' (Recuperación):"),
            dcc.Slider(
                id='rum-k-slider',
                min=0.01, max=0.05, step=0.01,
                value=0.01,
                marks={0.01: '0.01 (Crédulos)', 0.02: '0.02 (Escépticos)', 0.05: '0.05 (Racionales)'},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            html.P("A mayor 'k', más rápido la gente deja de creer el rumor.", style={'fontSize':'11px', 'color':'gray'}),

            html.Label("Propagadores Iniciales (I0):"),
            dcc.Input(id="rum-I0", type="number", value=1, className="input-field"),
            
            html.Label("Racionales Iniciales (R0):"),
            dcc.Input(id="rum-R0", type="number", value=8, className="input-field"),
            
            html.Label("Días a simular:"),
            dcc.Input(id="rum-tmax", type="number", value=15, className="input-field"),
            
            html.Br(), html.Br(),
            html.Button("Analizar Rumor", id='btn-rum', className='btn-generar')

        ], className="content left", style={'width': '35%'}),

        # --- PANEL DERECHO: GRÁFICA Y ANÁLISIS ---
        html.Div([
            # KPI Cards
            html.Div([
                html.Div([
                    html.H6("Pico de Propagadores (Q3a)"),
                    html.H3(id='rum-pico', style={'color': '#f59e0b'})
                ], style={'flex': 1, 'textAlign': 'center', 'backgroundColor': '#fffbeb', 'padding': '10px', 'borderRadius': '8px', 'marginRight': '5px'}),
                
                html.Div([
                    html.H6("Alcance Total (Q3b)"),
                    html.H3(id='rum-alcance', style={'color': '#6366f1'})
                ], style={'flex': 1, 'textAlign': 'center', 'backgroundColor': '#eef2ff', 'padding': '10px', 'borderRadius': '8px'})
            ], style={'display': 'flex', 'marginBottom': '15px'}),

            # GRÁFICA
            dcc.Graph(id='grafica-rumor', style={'height': '350px'}),
            
            # ANÁLISIS DE SENSIBILIDAD
            html.Div([
                html.H5("Análisis de Escenario (Q4, Q5 y Q6)"),
                html.P(id='texto-analisis-rumor', style={'fontSize': '14px'})
            ], style={'marginTop': '15px', 'padding': '15px', 'borderLeft': '4px solid #6366f1', 'backgroundColor': '#f8fafc'})

        ], className="content right", style={'width': '65%'})

    ], className="page-container", style={'flexDirection': 'row', 'alignItems': 'flex-start'})
])


# --- LÓGICA MATEMÁTICA ---
def sistema_rumor(y, t, b, k):
    S, I, R = y
    # Ecuaciones del PDF [cite: 150]
    dSdt = -b * S * I
    dIdt = b * S * I - k * I
    dRdt = k * I
    return [dSdt, dIdt, dRdt]

@callback(
    [Output('grafica-rumor', 'figure'),
     Output('rum-pico', 'children'),
     Output('rum-alcance', 'children'),
     Output('texto-analisis-rumor', 'children')],
    [Input('btn-rum', 'n_clicks'),
     Input('rum-k-slider', 'value')], # Se actualiza al mover el slider también
    [State('rum-N', 'value'),
     State('rum-b', 'value'),
     State('rum-I0', 'value'),
     State('rum-R0', 'value'),
     State('rum-tmax', 'value')]
)
def simular_rumor(n_clicks, k, N, b, I0, R0, t_max):
    # Conversión
    N, b, k = float(N), float(b), float(k)
    I0, R0, t_max = float(I0), float(R0), float(t_max)


    S0 = N - I0 - R0
    y0 = [S0, I0, R0]
    t = np.linspace(0, t_max, 200)


    sol = odeint(sistema_rumor, y0, t, args=(b, k))
    S, I, R = sol.T

    max_propagadores = np.max(I)
    dia_pico = t[np.argmax(I)]
    
    total_creyeron = S0 - S[-1]
    porcentaje_creyeron = (total_creyeron / S0) * 100

    # 4. Gráfica
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=S, mode='lines', name='Ignorantes (S)', line=dict(color='#6366f1'))) # Indigo
    fig.add_trace(go.Scatter(x=t, y=I, mode='lines', name='Propagadores (I)', line=dict(color='#f59e0b', width=3))) # Ambar
    fig.add_trace(go.Scatter(x=t, y=R, mode='lines', name='Racionales (R)', line=dict(color='#64748b'))) # Slate

    fig.update_layout(
        title={
            'text': "Dinámica SIR (Estudiantes)",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        template="plotly_white",
        hovermode="x unified",
        # MÁRGENES AJUSTADOS: Menos espacio a los lados, más espacio abajo para la leyenda
        margin=dict(l=10, r=10, t=50, b=100),
        # LEYENDA ABAJO HORIZONTAL (Esto libera el ancho)
        legend=dict(
            orientation="h", 
            yanchor="top", 
            y=-0.2, 
            xanchor="center", 
            x=0.5
        )
    )

    # 5. Texto Dinámico
    # El PDF menciona que si I0 aumenta, es más rápido (Q4) [cite: 206]
    # Y si R0 baja, dura más (Q5) [cite: 211]
    analisis = f"""
    En este escenario, el pico máximo de difusión ocurre el día {dia_pico:.1f}. 
    El {porcentaje_creyeron:.1f}% de los alumnos susceptibles terminaron escuchando el rumor.
    
    Observación (Q4/Q5): Si aumentas los propagadores iniciales (I0), verás que la curva naranja se dispara antes.
    Si aumentas la racionalidad (k), notarás que el pico baja drásticamente.
    """

    return fig, f"{int(max_propagadores)} alumnos", f"{porcentaje_creyeron:.1f}%", analisis