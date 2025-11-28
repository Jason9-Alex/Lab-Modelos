import dash
from dash import html, dcc, Input, Output, callback
import plotly.graph_objs as go
import numpy as np
from scipy.integrate import odeint
from dash import html, dcc, Input, Output, State, callback

dash.register_page(__name__, path='/caso_epidemia', name='Caso 1: Epidemia Estudiantil',order =9)

layout = html.Div([
    # --- ENCABEZADO CON TEXTO DEL PDF ---
    html.Div([
        html.H3("Caso de Estudio: Brote en Estudiantes (Q4)", className="title"),
        dcc.Markdown(r'''
        **Planteamiento del Problema:**
        Se simula un brote en una población cerrada de estudiantes.
        
        * **Población (N):** 7138 estudiantes[cite: 61].
        * **Paciente Cero:** 1 infectado inicial[cite: 64].
        * **Parámetros:** $\beta = 1/7138$ y $k = 0.40$[cite: 67, 69].
        ''', mathjax=True, style={'color': '#444'})
    ], style={'marginBottom': '20px'}),

    html.Div([
        # --- PANEL IZQUIERDO: CONTROLES ---
        html.Div([
            html.H4("Parámetros (Q4)", className="title"),
            
            html.Label("Población Total (N):"),
            dcc.Input(id="epi-N", type="number", value=7138, className="input-field"),
            
            html.Label("Tasa de Transmisión (beta):"),
            # El valor por defecto es 1/7138 approx 0.0001401
            dcc.Input(id="epi-beta", type="number", value=0.0001401, step=0.0000001, className="input-field"),
            html.Div("Nota: El PDF define beta como 1/N", style={'fontSize': '11px', 'color': 'gray'}),
            
            html.Label("Tasa de Recuperación (k):"),
            dcc.Input(id="epi-k", type="number", value=0.40, step=0.01, className="input-field"),

            html.Label("Infectados Iniciales (I0):"),
            dcc.Input(id="epi-I0", type="number", value=1, className="input-field"),
            
            html.Label("Días a simular:"),
            dcc.Input(id="epi-tmax", type="number", value=40, className="input-field"),
            
            html.Br(),
            html.Button("Simular Brote", id='btn-epi', className='btn-generar')

        ], className="content left", style={'width': '30%'}),

        # --- PANEL DERECHO: GRÁFICA Y RESPUESTAS ---
        html.Div([
# TARJETAS DE RESULTADOS (KPIs)
            html.Div([
                html.Div([
                    html.H5("R0 (Reprod. Básico)"),
                    html.H3(id='res-r0', style={'color': '#d97706'})
                ], style={'flex': 1, 'textAlign': 'center', 'backgroundColor': '#fffbeb', 'padding': '15px', 'borderRadius': '12px'}),
                
                html.Div([
                    html.H5("Día del Pico"),
                    html.H3(id='res-dia', style={'color': '#ef4444'})
                ], style={'flex': 1, 'textAlign': 'center', 'backgroundColor': '#fef2f2', 'padding': '15px', 'borderRadius': '12px'}),

                html.Div([
                    html.H5("Max. Infectados"),
                    html.H3(id='res-max', style={'color': '#b91c1c'})
                ], style={'flex': 1, 'textAlign': 'center', 'backgroundColor': '#fef2f2', 'padding': '15px', 'borderRadius': '12px'})
            
            # --- AQUÍ ESTÁ EL CAMBIO IMPORTANTE ---
            ], style={
                'display': 'flex', 
                'marginBottom': '100',  # <--- Antes era 15px. Súbelo a 40px para bajar la gráfica.
                'gap': '100'            # <--- Esto separa las tarjetas entre sí horizontalmente.
            }),

            # GRÁFICA
            dcc.Graph(id='grafica-epi', style={'height': '350px'}),
            
            # CONCLUSIÓN AUTOMÁTICA (Responde a la Q8 del PDF)
            html.Div(id='conclusion-texto', style={'marginTop': '15px', 'padding': '10px', 'borderLeft': '4px solid #10b981', 'backgroundColor': '#f0fdf4'})

        ], className="content right", style={'width': '70%'})

    ], className="page-container", style={'flexDirection': 'row', 'alignItems': 'flex-start'})
])


# --- LÓGICA MATEMÁTICA ---
def sistema_sir(y, t, beta, k):
    S, I, R = y
    dSdt = -beta * S * I
    dIdt = beta * S * I - k * I
    dRdt = k * I
    return [dSdt, dIdt, dRdt]

@callback(
    [Output('grafica-epi', 'figure'),
     Output('res-r0', 'children'),
     Output('res-dia', 'children'),
     Output('res-max', 'children'),
     Output('conclusion-texto', 'children')],
    [Input('btn-epi', 'n_clicks')],
    [State('epi-N', 'value'),
     State('epi-beta', 'value'),
     State('epi-k', 'value'),
     State('epi-I0', 'value'),
     State('epi-tmax', 'value')]
)
def simular_epidemia(n_clicks, N, beta, k, I0, t_max):
    # Conversión segura
    N, beta, k = float(N), float(beta), float(k)
    I0, t_max = float(I0), float(t_max)

    R0_init = 0
    S0 = N - I0 - R0_init
    y0 = [S0, I0, R0_init]
    t = np.linspace(0, t_max, 200)

    # 2. Resolver EDO
    sol = odeint(sistema_sir, y0, t, args=(beta, k))
    S, I, R = sol.T

    r0_val = (beta * S0) / k 
    
    # Pico
    idx_max = np.argmax(I)
    max_infectados = I[idx_max]
    dia_pico = t[idx_max]
    
    susceptibles_finales = S[-1]

    # 4. Gráfica
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=S, mode='lines', name='Susceptibles', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=t, y=I, mode='lines', name='Infectados', line=dict(color='red', width=3)))
    fig.add_trace(go.Scatter(x=t, y=R, mode='lines', name='Recuperados', line=dict(color='green')))

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

    # 5. Texto de Conclusión (Basado en Q8 del PDF [cite: 124-128])
    conclusion = [
        html.H5("Conclusión del Modelo (Q8):"),
        dcc.Markdown(f'''
        **¿Se infectó toda la población?** No.
        
        Al final de la epidemia, quedaron aproximadamente **{int(susceptibles_finales)} estudiantes sanos** (Susceptibles).
        La epidemia se detuvo porque la población susceptible cayó por debajo del umbral crítico.
        ''')
    ]

    return fig, f"{r0_val:.2f}", f"Día {dia_pico:.1f}", f"{int(max_infectados)}", conclusion