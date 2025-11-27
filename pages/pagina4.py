import dash
from dash import html, dcc, Input, Output, State, callback
# Importamos la nueva función desde tu archivo utils
from utils.funciones import funcion_grafica_cosecha 

dash.register_page(__name__, path='/pagina4', name='Modelo Cosecha')

layout = html.Div([
    # --- ENCABEZADO ---
    html.Div([
        html.H3("Modelo Logístico con Cosecha", className="title"),
        dcc.Markdown(
            r'''
            Este modelo simula qué pasa si extraemos recursos constantemente.
            Ecuación: $\frac{dP}{dt} = rP(1 - \frac{P}{K}) - h$
            ''', mathjax=True, style={'textAlign': 'center', 'color': '#555'}
        )
    ], style={'marginBottom': '20px'}),

    html.Div([
        # --- PANEL IZQUIERDO: PARAMETROS ---
        html.Div([
            html.H4("Controles", className="title", style={'fontSize':'18px'}),

            # SLIDER NUEVO: Cosecha
            html.Label("Tasa de Cosecha (h):"),
            html.Div([
                dcc.Slider(min=0, max=100, step=5, value=0, id='slider-h',
                           marks={0:'0', 50:'50', 100:'100'},
                           tooltip={"placement": "bottom", "always_visible": True})
            ], style={'marginBottom': '20px'}),

            html.Div([
                html.Label("Población Inicial P(0):"),
                dcc.Input(id="input-p0", type="number", value=200, className="input-field")
            ], className="input-group"),

            html.Div([
                html.Label("Tasa de Crecimiento (r):"),
                dcc.Input(id="input-r", type="number", value=0.1, step=0.01, className="input-field")
            ], className="input-group"),

            html.Div([
                html.Label("Capacidad de carga (K):"),
                dcc.Input(id="input-k", type="number", value=1000, className="input-field")
            ], className="input-group"),

            html.Div([
                html.Label("Tiempo máximo (t):"),
                dcc.Input(id="input-t", type="number", value=100, className="input-field")
            ], className="input-group"),

            html.Button("Actualizar Gráfica", id="btn-cosecha", className="btn-generar")

        ], className="content left", style={'width':'35%'}),

        # --- PANEL DERECHO: GRAFICA ---
        html.Div([
            html.H3("Simulación", className="title"),
            dcc.Graph(
                id='grafica-poblacion-cosecha',
                style={'height': '450px', 'width': '100%'}
            ),
            # Mensaje explicativo
            html.P("Si la línea se vuelve ROJA, significa que la cosecha es excesiva y la población se extingue.", 
                   style={'textAlign':'center', 'fontSize':'14px', 'marginTop':'10px', 'color':'gray'})

        ], className="content right", style={'width':'65%'})
        
    ], className="page-container", style={'flexDirection': 'row', 'alignItems': 'flex-start'})
])

@callback(
    Output("grafica-poblacion-cosecha", "figure"),
    Input("btn-cosecha", "n_clicks"), 
    # Escuchamos también el slider para que se actualice al moverlo (opcional)
    Input("slider-h", "value"),       
    State("input-p0", "value"),
    State("input-r", "value"),
    State("input-k", "value"),
    State("input-t", "value"),
    prevent_initial_call=False
)
def actualizar_grafica_cosecha(n_clicks, h, P0, r, K, t_max):
    # Convertimos a float por seguridad
    h = float(h) if h else 0
    P0 = float(P0)
    r = float(r)
    K = float(K)
    t_max = float(t_max)

    # Llamamos a la función que está en utils/funciones.py
    fig = funcion_grafica_cosecha(n_clicks, P0, r, K, t_max, h)
    
    return fig