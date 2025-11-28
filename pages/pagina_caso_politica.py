import dash
from dash import html, dcc, Input, Output, State, callback
import plotly.graph_objs as go
import numpy as np
from scipy.integrate import odeint

dash.register_page(__name__, path='/caso_politica', name='Caso 3: Política Pública',order =11)

layout = html.Div([
    # --- ENCABEZADO ---
    html.Div([
        html.H3("Caso de Estudio: Política de Reciclaje (Q1-Q6)", className="title"),
        dcc.Markdown(r'''
        **Contexto Político:** Implementación de una norma de reciclaje en una ciudad.
        
        * **Susceptibles (S):** Ciudadanos que aún no adoptan la medida.
        * **Influyentes (I):** Promotores activos de la política (Adopción).
        * **Rechazadores (R):** Opositores que deciden no acatarla.
        
        **Ecuaciones:** $\frac{dS}{dt} = -bSI$, $\frac{dI}{dt} = bSI - kI$, $\frac{dR}{dt} = kI$
        ''', mathjax=True, style={'color': '#444'})
    ], style={'marginBottom': '20px'}),

    html.Div([
        # --- PANEL IZQUIERDO: CONTROLES ---
        html.Div([
            html.H4("Dinámica Social", className="title"),
            
            html.Label("Población Ciudadana (N):"),
            dcc.Input(id="pol-N", type="number", value=10050, className="input-field"),
            
            html.Label("Tasa de Adopción 'b' (Influencia):"),
            # OJO: Los valores son muy pequeños en este caso (5 ceros) [cite: 261]
            dcc.Input(id="pol-b", type="number", value=0.00005, step=0.00001, className="input-field"),
            html.Div("Si 'b' sube, el marketing es más efectivo.", style={'fontSize':'11px', 'color':'gray'}),

            html.Label("Tasa de Rechazo 'k' (Oposición):"),
            dcc.Input(id="pol-k", type="number", value=0.00002, step=0.00001, className="input-field"),

            html.Label("Influyentes Iniciales (I0):"),
            dcc.Input(id="pol-I0", type="number", value=50, className="input-field"),
            
            html.Label("Días a simular:"),
            dcc.Input(id="pol-tmax", type="number", value=100, className="input-field"),
            
            html.Br(), html.Br(),
            html.Button("Simular Política", id='btn-pol', className='btn-generar')

        ], className="content left", style={'width': '35%'}),

        # --- PANEL DERECHO: GRÁFICA Y ANÁLISIS ---
        html.Div([
            # KPI Cards
            html.Div([
                html.Div([
                    html.H6("Pico de Influencia"),
                    html.H3(id='pol-pico', style={'color': '#d946ef'}) # Magenta
                ], style={'flex': 1, 'textAlign': 'center', 'backgroundColor': '#fdf4ff', 'padding': '10px', 'borderRadius': '8px', 'marginRight': '5px'}),
                
                html.Div([
                    html.H6("Total Rechazos"),
                    html.H3(id='pol-rechazo', style={'color': '#059669'}) # Verde
                ], style={'flex': 1, 'textAlign': 'center', 'backgroundColor': '#ecfdf5', 'padding': '10px', 'borderRadius': '8px'})
            ], style={'display': 'flex', 'marginBottom': '15px'}),

            # GRÁFICA
            dcc.Graph(id='grafica-politica', style={'height': '350px'}),
            
            # ANÁLISIS ESTRATÉGICO (Basado en el PDF [cite: 304])
            html.Div([
                html.H5("Análisis para Planificadores"),
                dcc.Markdown(id='texto-analisis-pol')
            ], style={'marginTop': '15px', 'padding': '15px', 'borderLeft': '4px solid #0ea5e9', 'backgroundColor': '#f0f9ff'})

        ], className="content right", style={'width': '65%'})

    ], className="page-container", style={'flexDirection': 'row', 'alignItems': 'flex-start'})
])


# --- LÓGICA MATEMÁTICA ---
def sistema_politica(y, t, b, k):
    S, I, R = y
    # Mismas ecuaciones SIR [cite: 442]
    dSdt = -b * S * I
    dIdt = b * S * I - k * I
    dRdt = k * I
    return [dSdt, dIdt, dRdt]

@callback(
    [Output('grafica-politica', 'figure'),
     Output('pol-pico', 'children'),
     Output('pol-rechazo', 'children'),
     Output('texto-analisis-pol', 'children')],
    [Input('btn-pol', 'n_clicks')],
    [State('pol-N', 'value'),
     State('pol-b', 'value'),
     State('pol-k', 'value'),
     State('pol-I0', 'value'),
     State('pol-tmax', 'value')]
)
def simular_politica(n_clicks, N, b, k, I0, t_max):
    # Conversión
    N, b, k = float(N), float(b), float(k)
    I0, t_max = float(I0), float(t_max)

    R0 = 0
    S0 = N - I0 - R0
    y0 = [S0, I0, R0]
    t = np.linspace(0, t_max, 200)


    sol = odeint(sistema_politica, y0, t, args=(b, k))
    S, I, R = sol.T

    idx_max = np.argmax(I)
    max_influyentes = I[idx_max]
    dia_pico = t[idx_max]
    total_rechazadores = R[-1]

    # 4. Gráfica
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=S, mode='lines', name='Susceptibles (S)', line=dict(color='#0ea5e9'))) # Azul cielo
    fig.add_trace(go.Scatter(x=t, y=I, mode='lines', name='Influyentes (I)', line=dict(color='#d946ef', width=3))) # Magenta
    fig.add_trace(go.Scatter(x=t, y=R, mode='lines', name='Rechazadores (R)', line=dict(color='#059669'))) # Esmeralda

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

    # 5. Texto de Análisis
    analisis = f"""
    El momento de mayor debate público (Pico de Influencia) será alrededor del **día {dia_pico:.0f}**.
    
    Para el día {t_max:.0f}, se estima que **{int(total_rechazadores)} ciudadanos** rechazarán la medida definitivamente.
    
    **Recomendación:** Si aumentas la tasa 'b' (campañas de educación), el pico ocurrirá antes. Si aumentas 'k' (descontento social), el número de rechazadores crecerá [cite: 289-293].
    """

    return fig, f"{int(max_influyentes)} personas", f"{int(total_rechazadores)}", analisis