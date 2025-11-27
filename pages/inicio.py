import dash
from dash import html, dcc

dash.register_page(__name__, path='/', name='Inicio')

# Defino el texto aquí arriba para mantener el 'layout' limpio y legible
info_alumno = '''
**Nombre:** Jason Alex  
**Apellidos:** Limaymanta Curo  
**Curso:** Técnicas de Modelamiento Matemático  
**Universidad:** Universidad Nacional Mayor de San Marcos  
**Facultad:** Facultad de Ciencias Matemáticas  
**Escuela:** Computación Científica  
**Semestre:** 2025-II
'''

layout = html.Div(children=[ 
    
    # --- CONTENEDOR IZQUIERDO: Datos ---
    html.Div(children=[
        html.H1("Presentación del Curso", className="title"),
        
        # Usamos un solo Markdown. El CSS se encargará de darle el espacio correcto entre líneas.
        dcc.Markdown(info_alumno)
        
    ], className="content left"),    

    # --- CONTENEDOR DERECHO: Intereses ---
    html.Div(children=[
        html.H1("Intereses", className="title"),
        
        # Aquí separé los párrafos lógicamente
        dcc.Markdown('''
        **Mis intereses son** la programación, el modelamiento matemático y la inteligencia artificial. 
        '''),
        
        dcc.Markdown('''
        Me gusta mucho la **programación y el desarrollo de software**, ya que me permite crear soluciones innovadoras y eficientes para diversos problemas.   
        '''),
        
        dcc.Markdown('''
        **Mis expectativas del curso** son aprender nuevas técnicas y herramientas que me permitan mejorar mis habilidades en el modelamiento matemático y aplicarlas en proyectos reales.
        ''')
        
    ], className="content right")

], className="page-container")