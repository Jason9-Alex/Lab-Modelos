import dash
from dash import html, dcc, Input, Output, State, callback
import numpy as np
import plotly.graph_objs as go

dash.register_page(__name__, path='/campo_vectorial', name='Campo Vectorial')

layout = html.Div([
    html.Div([
        html.H4("Campo Vectorial", className="title"),

        html.Div([
            html.Label("Ecuacion dx/dt ="),
            dcc.Input(id="input-fx", type="text", value="np.sin(X)", className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Ecuacion dy/dt ="),
            dcc.Input(id="input-fy", type="text", value="np.cos(Y)", className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Rango de el eje X : "),
            dcc.Input(id="input-xmax", type="number", value=5, className="input-field")
        ], className="input-group"),
     
        html.Div([
            html.Label("Rango de el eje Y :"),
            dcc.Input(id="input-ymax", type="number", value=5, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Mallado"),
            dcc.Input(id="input-n", type="number", value=15, className="input-field")
        ], className="input-group"),

        html.Button("Generar campo", id="btn-generar", className="btn-generar"),

        html.Div([
            html.H4("Ejemplos de ecuaciones"),
            html.P("• dx/dt = X , dy/dt = Y "),
            html.P("• dx/dt = -Y , dy/dt = X "),
            html.P("• dx/dt = X+Y , dy/dt = np.cos(Y) ")
        ])
    ], className="content left"),

    html.Div([
        html.H3("Visualizacion del Campo Vectorial", className="title"),
        dcc.Graph(id="graph-campo-vectorial", style={'height': '450', 'width': '100%'})
    ], className="content right"),
], className="page-container")


@callback(
    Output("graph-campo-vectorial", "figure"),
    Input("btn-generar", "n_clicks"),
    State("input-fx", "value"),
    State("input-fy", "value"),
    State("input-xmax", "value"),
    State("input-ymax", "value"),
    State("input-n", "value"),
    prevent_initial_call=False
)
def graficar_campo(n_clicks, fx_str, fy_str, xmax, ymax, n):
    
    # Malla
    x = np.linspace(-xmax, xmax, n)
    y = np.linspace(-ymax, ymax, n)
    X, Y = np.meshgrid(x, y)

    try:
        diccionario = {
            'X': X,
            'Y': Y,
            'np': np,
            'sin': np.sin,
            'cos': np.cos,
            'tan': np.tan,
            'sqrt': np.sqrt,
            'exp': np.exp,
            'pi': np.pi,
            'e': np.e
        }

        fx = eval(fx_str, locals= diccionario)
        fy = eval(fy_str, locals= diccionario)

        mag_max = np.max(np.sqrt(fx**2 + fy**2))
        mag_min = np.min(np.sqrt(fx**2 + fy**2))


    except Exception as e:
        fx = np.zeros_like(X)
        fy = np.zeros_like(Y)


    fig = go.Figure()

    # Dibujar vectores
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            x0, y0 = X[i, j], Y[i, j]
            x1, y1 = x0 + fx[i, j], y0 + fy[i, j]
        
            fig.add_trace(go.Scatter(
                x=[x0, x1],
                y=[y0, y1],
                mode='lines+markers',
                line=dict(color='blue', width=2),
                marker=dict(size=[3,5], color=['blue','red']),
                showlegend=False,
                hovertemplate=f"Punto:({x0:.1f}, {y0:.1f})<br>Vector:({fx[i,j]:.2f}, {fy[i,j]:.2f})<extra></extra>"
            ))

    fig.update_layout(
        title=dict(
            text=f'<b>Campo Vectorial: dx/dt={fx_str}, dy/dt={fy_str}</b>',
            x=0.5,
            font=dict(size=16, color='green')
        ),
        xaxis_title="Eje X",
        yaxis_title="Eje Y",
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=80, b=40),
        paper_bgcolor='lightyellow',
        font=dict(
            family="Outfit",
            size=12,
            color="black"
        )
    )
    
    fig.update_xaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='Lightpink',
        zeroline=True, 
        zerolinewidth=2, 
        zerolinecolor='red',
        range=[-xmax*1.1, xmax*1.1]
    )
    
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='Lightpink',
        zeroline=True, 
        zerolinewidth=2, 
        zerolinecolor='red',
        range=[-ymax*1.1, ymax*1.1]
    )
    
    return fig

