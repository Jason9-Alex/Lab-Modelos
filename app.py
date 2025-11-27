import dash
from dash import html, dcc
import dash_bootstrap_components as dbc


mathjax_script = ['https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML']
app = dash.Dash(__name__, use_pages=True, 
                external_stylesheets=[dbc.themes.FLATLY],
                external_scripts=[mathjax_script])

app.layout = html.Div([
    html.H1("Tecnicas de modelamiento Matematico", className='app-header'),
    html.Div([
        html.Div([
            html.Div(
                dcc.Link(
                f"{page['name']}", href=page["relative_path"],className='nav-link'),
            )for page in dash.page_registry.values()
        ], className='nav-links'),
    ], className='Navigation'),
    dash.page_container
], className='app-container'),


if __name__ == "__main__":
    app.run(debug=True)