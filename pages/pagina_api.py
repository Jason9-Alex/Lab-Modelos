import dash
from dash import html, dcc, Input, Output, callback
import plotly.graph_objs as go
import requests
import pandas as pd

dash.register_page(__name__, path='/api_clima', name='Mapa Climático Mundial',order = 8)

# --- DICCIONARIO AMPLIADO (Para llenar el mapa) ---
ciudades = {
    "Lima": {"lat": -12.0464, "lon": -77.0428},
    "Buenos Aires": {"lat": -34.6037, "lon": -58.3816},
    "Ciudad de México": {"lat": 19.4326, "lon": -99.1332},
    "Nueva York": {"lat": 40.7128, "lon": -74.0060},
    "Madrid": {"lat": 40.4168, "lon": -3.7038},
    "Londres": {"lat": 51.5074, "lon": -0.1278},
    "París": {"lat": 48.8566, "lon": 2.3522},
    "Moscú": {"lat": 55.7558, "lon": 37.6173},
    "Tokio": {"lat": 35.6762, "lon": 139.6503},
    "Sídney": {"lat": -33.8688, "lon": 151.2093},
    "Ciudad del Cabo": {"lat": -33.9249, "lon": 18.4241},
    "El Cairo": {"lat": 30.0444, "lon": 31.2357}
}

layout = html.Div([
    html.Div([
        html.H3("Monitor Climático Global", className="title"),
        html.P("Selecciona una ciudad para ver su ubicación y pronóstico en tiempo real.", className="text-muted"),
        
        # --- CONTROL PRINCIPAL ---
        html.Label("Selecciona Ciudad:"),
        dcc.Dropdown(
            id='dropdown-ciudad',
            options=[{'label': k, 'value': k} for k in ciudades.keys()],
            value='Lima',
            clearable=False,
            style={'marginBottom': '20px', 'color': 'black'}
        ),

        # --- KPI: DATOS ACTUALES ---
        html.Div([
            html.Div([
                html.H6("Temperatura"),
                html.H3(id='kpi-temp', children="--", style={'color': '#d97706'})
            ], style={'flex': 1, 'textAlign': 'center', 'borderRight': '1px solid #ddd'}),
            
            html.Div([
                html.H6("Viento"),
                html.H3(id='kpi-wind', children="--", style={'color': '#2563eb'})
            ], style={'flex': 1, 'textAlign': 'center'})
        ], style={'display': 'flex', 'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '10px', 'boxShadow': '0 2px 5px rgba(0,0,0,0.05)', 'marginBottom': '20px'}),

        html.Button("Actualizar API", id='btn-api', className='btn-generar')

    ], className="content left", style={'width': '30%'}),

    # --- PANEL DERECHO: MAPA + GRÁFICA ---
    html.Div([
        
        # 1. EL MAPA MUNDI
        html.H5("Ubicación Geográfica"),
        dcc.Graph(id='mapa-mundi', style={'height': '300px', 'marginBottom': '20px'}),

        # 2. LA GRÁFICA DE SERIE DE TIEMPO
        html.H5("Pronóstico 7 Días (Hora por Hora)"),
        dcc.Graph(id='grafica-clima', style={'height': '300px'}),
        
        html.P("Datos: Open-Meteo API", style={'fontSize': '11px', 'textAlign': 'right', 'color': 'gray'})

    ], className="content right", style={'width': '70%'})

], className="page-container", style={'flexDirection': 'row', 'alignItems': 'flex-start'})


@callback(
    [Output('kpi-temp', 'children'),
     Output('kpi-wind', 'children'),
     Output('mapa-mundi', 'figure'),
     Output('grafica-clima', 'figure')],
    [Input('dropdown-ciudad', 'value'),
     Input('btn-api', 'n_clicks')]
)
def actualizar_dashboard(ciudad_seleccionada, n_clicks):
    # --- 1. PREPARAR DATOS DEL MAPA ---
    lats = [v['lat'] for v in ciudades.values()]
    lons = [v['lon'] for v in ciudades.values()]
    nombres = list(ciudades.keys())
    
 
    colores = ['lightgray'] * len(ciudades)
    tamano = [8] * len(ciudades)
    

    idx = nombres.index(ciudad_seleccionada)
    colores[idx] = '#ef4444' # Rojo intenso
    tamano[idx] = 15         # Más grande

    fig_map = go.Figure(go.Scattergeo(
        lon = lons,
        lat = lats,
        text = nombres,
        mode = 'markers',
        marker = dict(
            size = tamano,
            color = colores,
            line = dict(width=1, color='black')
        )
    ))

    fig_map.update_layout(
        geo = dict(
            projection_type = 'natural earth',
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            countrycolor = "rgb(200, 200, 200)",
            coastlinecolor = "rgb(200, 200, 200)",
        ),
        margin = dict(l=0, r=0, t=0, b=0),
        height = 300,
        template="plotly_white"
    )


    lat_sel = ciudades[ciudad_seleccionada]['lat']
    lon_sel = ciudades[ciudad_seleccionada]['lon']
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat_sel}&longitude={lon_sel}&hourly=temperature_2m,windspeed_10m&current_weather=true"

    try:
        response = requests.get(url)
        data = response.json()

        # KPIs
        temp = f"{data['current_weather']['temperature']} °C"
        wind = f"{data['current_weather']['windspeed']} km/h"

        # Gráfica Histórica
        hourly = data['hourly']
        df = pd.DataFrame({
            'Tiempo': hourly['time'],
            'Temp': hourly['temperature_2m'],
            'Viento': hourly['windspeed_10m']
        })

        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=df['Tiempo'], y=df['Temp'], mode='lines', name='Temp (°C)', line=dict(color='#f59e0b', width=3)))
        fig_line.add_trace(go.Scatter(x=df['Tiempo'], y=df['Viento'], mode='lines', name='Viento (km/h)', line=dict(color='#3b82f6', dash='dot')))

        fig_line.update_layout(
            margin=dict(l=40, r=20, t=20, b=40),
            template="plotly_white",
            legend=dict(orientation="h", y=1.1)
        )

        return temp, wind, fig_map, fig_line

    except:
        return "--", "--", fig_map, go.Figure()