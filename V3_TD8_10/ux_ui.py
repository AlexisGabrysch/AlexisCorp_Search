# Code créée par la AlexisCorp

# Application DASH lien

# === http://127.0.0.1:8050/ ===


# Importation des differents modules

import dash

from dash import dcc, html, Input, Output, State

import scrapper as sc


# Cration d'une application Dash
app = dash.Dash(__name__)


# Creer un input pour les mots

input_words = dcc.Input(id="mots_a_rechercher", type="text", placeholder="Entrez les mots à rechercher" , style={

            'textAlign': 'center',      # Implementation des styles

            'color': "#4a5759",

              'padding' : "0.5rem 1.2rem" ,

              'border-radius' : "10px"  

        })

# Creer un bouton pour valider les mots choisis

validation_button = html.Button(id="valider_button", n_clicks=0, children="VALIDER")

# Creer une sortie pour les resultats

output_results = html.Div(id="resultats")

# Appel de la fonction de similarite

def get_similarity(mots_a_rechercher):
    
    return sc.corpus2.recherche_par_similarite_cosinus(mots_a_rechercher, 10)

# Mise a jour callback

@app.callback(
        
    Output("resultats", "children"),

    Input("valider_button", "n_clicks"),

    State("mots_a_rechercher", "value")

)

# Fonction mise a jour des valeurs

def update_results(n_clicks, mots_a_rechercher):

    if n_clicks is None or n_clicks == 0 or mots_a_rechercher is None or mots_a_rechercher == "":   # Test sur bouton et valeur

        return []
    
    print(mots_a_rechercher)

    results = get_similarity(mots_a_rechercher)     # Appel de la fonction
   
    return [

        html.Li(         # Sortir en liste pour affichage

            val

        )
        
        for val in enumerate(results)

    ]


# Eviter que cela se repete

update_results.interval = None

# Definition de l'affichage de l'application par layout

app.layout = html.Div(style={'font-family': 'Montserrat'}, children=[
    
    html.H1(style = {"background-color":'#4a5759',      # Titre en H1
                     
                     "margin": "10px",              # Implementation des styles

                     'textAlign': 'center',

                     'font-family': 'Montserrat',

            'color': '#7FDBFF' },
            
            children = "Welcome On AlexisCorp Search", ),

    html.Div(children = input_words, style={            # Zone de texte utilisateur

            'textAlign': 'center', 'background-color' : '#f7e1d7'} ),       # Implementation des styles

    html.Div (children = validation_button , style={            # Bouton de validation

            'textAlign': 'center', 'background-color' : '#f7e1d7'} ),       # Implementation des styles

    html.Div (children = output_results , style={           # Affichage des resultats

            'textAlign': 'left',

            'margin' : '5%', 'background-color' : '#f7e1d7'} )          # Implementation des styles

])

# Execute l'application

if __name__ == "__main__":

    app.run_server(debug=True)



#   Code créée par la AlexisCorp pour le AlexisCorp Search