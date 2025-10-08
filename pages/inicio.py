import dash    
from dash import html, dcc

dash.register_page(__name__, path='/', name='Inicio')

layout = html.Div(children=[ 
    html.Div(children = [
        html.H1(
            "Presentacion del Curso",className="Title" ),
        dcc.Markdown('''
        Nombre : Jason Alex 
                     '''),
        dcc.Markdown('''             
        Apellidos :Limaymanta Curo
                     '''),
        dcc.Markdown('''
        Curso : Tecnicas de Modelamiento Matematico
                     '''),
        dcc.Markdown('''
        Universidad : Universidad Nacional Mayoir de San Marcos
                     '''),
                     dcc.Markdown('''
        Facultad : Facultad de Ciencias Matematicas
                                  '''),
                                  dcc.Markdown('''
        Escuela : Computacion Cientifica
                        '''),
dcc.Markdown('''
        Semestre : 2025-II
                        ''')]
        , className="content left" ),    

    #contenedor derecho
    html.Div(children=[
        html.H1("Intereses", className="title"),
        dcc.Markdown('''
        Mis intereses son la programacion, el modelamiento matematico y 
        la inteligencia artificial. 
        '''),
        dcc.Markdown('''
         Me gusta mucho la programacion y el desarrollo de software,
        ya que me permite crear soluciones innovadoras y eficientes para diversos problemas.   
          '''),
          dcc.Markdown('''
        Mis espectativas de el cursos , son aprender nuevas tecnicas y herramientas
        que me permitan mejorar mis habilidades en el modelamiento matematico y aplicarlas en proyectos reales''')
    ],className="content right")
],className="page-container" )
