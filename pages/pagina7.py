import dash
from dash import html, dcc, Input, Output, State, callback
import numpy as np
import plotly.graph_objs as go
from scipy.integrate import odeint 

dash.register_page(__name__, path='/Pagina7', name='Modelo SEIR')

# --- Estilos inline para las pestañas (para que combinen con tu nuevo CSS) ---
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'borderRadius': '10px 10px 0px 0px',
    'backgroundColor': '#f9f9f9'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#10b981', # El color verde de tu tema
    'color': 'white',
    'padding': '6px',
    'borderRadius': '10px 10px 0px 0px',
}

layout = html.Div([
    # --- CONTENEDOR IZQUIERDO: PARÁMETROS ---
    html.Div([
        html.H4("Parámetros SEIR", className="title"),
        html.P("Ajusta las condiciones iniciales y tasas:", style={'fontSize': '14px'}),

        html.Div([
            html.Label("Población total (N):"),
            dcc.Input(id="input-N-seir", type="number", value=1000, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Tasa de transmisión (β):"),
            dcc.Input(id="input-beta-seir", type="number", value=0.5, step=0.01, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Tasa de incubación (σ):"),
            dcc.Input(id="input-sigma", type="number", value=0.2, step=0.01, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Tasa de recuperación (γ):"),
            dcc.Input(id="input-gamma-seir", type="number", value=0.1, step=0.01, className="input-field")
        ], className="input-group"),
     
        html.Div([
            html.Label("Expuestos iniciales (E0):"),
            dcc.Input(id="input-E0", type="number", value=5, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Infectados iniciales (I0):"),
            dcc.Input(id="input-I0-seir", type="number", value=2, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Días a simular:"),
            dcc.Input(id="input-tiempo-seir", type="number", value=160, className="input-field")
        ], className="input-group"),

        html.Button("Simular Escenarios", id="btn-simular-seir", className="btn-generar"),
        
    ], className="content left"),

    # --- CONTENEDOR DERECHO: VISUALIZACIÓN CON TABS ---
    html.Div([
        html.H3("Análisis de la Epidemia", className="title"),
        
        # Agregamos Tabs para tener dos vistas diferentes
        dcc.Tabs([
            dcc.Tab(label='Serie de Tiempo (2D)', children=[
                dcc.Graph(id="graph-SEIR-time", style={'height': '450px', 'width': '100%'})
            ], style=tab_style, selected_style=tab_selected_style),
            
            dcc.Tab(label='Espacio de Fase (3D)', children=[
                html.P("Trayectoria S-I-R: Visualiza cómo converge el sistema.", style={'textAlign':'center', 'fontSize':'12px', 'color':'gray'}),
                dcc.Graph(id="graph-SEIR-3d", style={'height': '450px', 'width': '100%'})
            ], style=tab_style, selected_style=tab_selected_style),
        ])
        
    ], className="content right"),
], className="page-container")


# Función del sistema de ecuaciones diferenciales SEIR
def ecuaciones_SEIR(y, t, N, beta, sigma, gamma):
    S, E, I, R = y
    dSdt = -beta * S * I / N
    dEdt = beta * S * I / N - sigma * E
    dIdt = sigma * E - gamma * I
    dRdt = gamma * I
    return dSdt, dEdt, dIdt, dRdt


@callback(
    [Output("graph-SEIR-time", "figure"),
     Output("graph-SEIR-3d", "figure")],
    Input("btn-simular-seir", "n_clicks"),
    State("input-N-seir", "value"),
    State("input-beta-seir", "value"),
    State("input-sigma", "value"),
    State("input-gamma-seir", "value"),
    State("input-E0", "value"),
    State("input-I0-seir", "value"),
    State("input-tiempo-seir", "value"),
    prevent_initial_call=False
)
def actualizar_graficas_SEIR(n_clicks, N, beta, sigma, gamma, E0, I0, tiempo_max):
    # Validar inputs básicos
    if None in (N, beta, sigma, gamma, E0, I0, tiempo_max):
        return go.Figure(), go.Figure()
    
    # Conversión segura
    N, beta, sigma, gamma = float(N), float(beta), float(sigma), float(gamma)
    E0, I0, tiempo_max = float(E0), float(I0), float(tiempo_max)
    
    # Condiciones iniciales
    S0 = N - E0 - I0
    R0_inicial = 0
    y0 = [S0, E0, I0, R0_inicial]
    
    t = np.linspace(0, tiempo_max, 300)
    
    try:
        solucion = odeint(ecuaciones_SEIR, y0, t, args=(N, beta, sigma, gamma))
        S, E, I, R = solucion.T
    except:
        return go.Figure(), go.Figure()

    # --- FIGURA 1: Serie de Tiempo (La clásica) ---
    fig_time = go.Figure()
    fig_time.add_trace(go.Scatter(x=t, y=S, mode='lines', name='Susceptibles', line=dict(color='#3b82f6')))
    fig_time.add_trace(go.Scatter(x=t, y=E, mode='lines', name='Expuestos', line=dict(color='#f59e0b', dash='dash')))
    fig_time.add_trace(go.Scatter(x=t, y=I, mode='lines', name='Infectados', line=dict(color='#ef4444', width=3)))
    fig_time.add_trace(go.Scatter(x=t, y=R, mode='lines', name='Recuperados', line=dict(color='#10b981')))
    
    fig_time.update_layout(
        title="Evolución en el Tiempo",
        xaxis_title="Días",
        yaxis_title="Población",
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", y=1.15,x=0.5,xanchor="center")
    )

    # --- FIGURA 2: Retrato de Fase 3D (LO NUEVO) ---
    # Mostramos Susceptibles vs Infectados vs Recuperados
    fig_3d = go.Figure(data=[go.Scatter3d(
        x=S,
        y=I,
        z=R,
        mode='lines',
        line=dict(
            color=t,        # El color varía según el tiempo
            colorscale='Viridis',
            width=5
        ),
        name='Trayectoria',
        hovertemplate='S: %{x:.0f}<br>I: %{y:.0f}<br>R: %{z:.0f}<extra></extra>'
    )])

    # Agregamos punto de inicio y final para referencia
    fig_3d.add_trace(go.Scatter3d(
        x=[S[0]], y=[I[0]], z=[R[0]], mode='markers', name='Inicio', marker=dict(size=5, color='green')
    ))
    fig_3d.add_trace(go.Scatter3d(
        x=[S[-1]], y=[I[-1]], z=[R[-1]], mode='markers', name='Final', marker=dict(size=5, color='red')
    ))

    fig_3d.update_layout(
        title="Espacio de Fase (S vs I vs R)",
        scene=dict(
            xaxis_title='Susceptibles',
            yaxis_title='Infectados',
            zaxis_title='Recuperados',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)) # Perspectiva inicial
        ),
        margin=dict(l=0, r=0, t=30, b=0)
    )

    return fig_time, fig_3d