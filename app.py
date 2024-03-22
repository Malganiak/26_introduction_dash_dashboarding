import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

# Charger les données à partir du fichier CSV
data = pd.read_csv('arbres10percent.csv')

# Créer un DataFrame à partir des données
df = pd.DataFrame(data)

# Sélectionner les colonnes nécessaires
selected_columns = ['DOMANIALITE', 'STADE DE DEVELOPPEMENT', 'CIRCONFERENCE (cm)', 'HAUTEUR (m)', 'geo_point_2d']
df_selected = df[selected_columns]

# Supprimer les lignes avec des valeurs manquantes
df_selected = df_selected.dropna()

# Créer l'application Dash
app = dash.Dash(__name__)

# Options pour la liste déroulante (DOMANIALITE)
domanialite_options = [{'label': domanialite, 'value': domanialite} for domanialite in df_selected['DOMANIALITE'].unique()]

# Options pour la liste déroulante (STADE DE DEVELOPPEMENT)
stade_options = [{'label': stade, 'value': stade} for stade in df_selected['STADE DE DEVELOPPEMENT'].unique()]

# Mise en page de l'application
app.layout = html.Div([
    html.H1("Histogramme de la circonférence d'un arbre en fonction de sa domanialité et de son stade de développement"),
    
    # Liste déroulante pour choisir la DOMANIALITE
    dcc.Dropdown(
        id='domanialite-dropdown',
        options=domanialite_options,
        value=df_selected['DOMANIALITE'].iloc[0],  # Valeur initiale
        multi=False
    ),
    
    # Liste déroulante pour choisir le STADE DE DEVELOPPEMENT sur l'histogramme de CIRCONFERENCE
    dcc.Dropdown(
        id='stade-circonference-dropdown',
        options=stade_options,
        value=df_selected['STADE DE DEVELOPPEMENT'].iloc[0],  # Valeur initiale
        multi=False
    ),
    
    # Graphique histogramme pour CIRCONFERENCE
    dcc.Graph(id='histogram-circonference'),
    
    html.Hr(),  # Ligne horizontale pour séparer les deux histogrammes
    
    html.H1("Histogramme de la hauteur d'un arbre en fonction de sa domanialité et de son stade de développement"),
    
    # Liste déroulante pour choisir la DOMANIALITE sur l'histogramme de HAUTEUR
    dcc.Dropdown(
        id='domanialite-hauteur-dropdown',
        options=domanialite_options,
        value=df_selected['DOMANIALITE'].iloc[0],  # Valeur initiale
        multi=False
    ),
    
    # Liste déroulante pour choisir le STADE DE DEVELOPPEMENT sur l'histogramme de HAUTEUR
    dcc.Dropdown(
        id='stade-hauteur-dropdown',
        options=stade_options,
        value=df_selected['STADE DE DEVELOPPEMENT'].iloc[0],  # Valeur initiale
        multi=False
    ),
    
    # Graphique histogramme pour HAUTEUR
    dcc.Graph(id='histogram-hauteur'),

    # Ajout des listes déroulantes pour la carte
    html.Hr(),  # Ligne horizontale pour séparer les histogrammes de la carte
    
    html.H1("Carte des arbres en fonction de la domanialité et du stade de développement"),
    
    # Liste déroulante pour choisir la DOMANIALITE pour la carte
    dcc.Dropdown(
        id='domanialite-map-dropdown',
        options=domanialite_options,
        value=df_selected['DOMANIALITE'].iloc[0],  # Valeur initiale
        multi=False
    ),
    
    # Liste déroulante pour choisir le STADE DE DEVELOPPEMENT pour la carte
    dcc.Dropdown(
        id='stade-map-dropdown',
        options=stade_options,
        value=df_selected['STADE DE DEVELOPPEMENT'].iloc[0],  # Valeur initiale
        multi=False
    ),
    
    # Graphique pour la carte
    dcc.Graph(id='tree-map'),  # Assurez-vous que l'ID est unique
])

# Callback pour mettre à jour l'histogramme de CIRCONFERENCE en fonction de la sélection de DOMANIALITE et STADE DE DEVELOPPEMENT
@app.callback(
    Output('histogram-circonference', 'figure'),
    [Input('domanialite-dropdown', 'value'),
     Input('stade-circonference-dropdown', 'value')]
)
def update_histogram_circonference(selected_domanialite, selected_stade_circonference):
    filtered_df = df_selected[(df_selected['DOMANIALITE'] == selected_domanialite) & (df_selected['STADE DE DEVELOPPEMENT'] == selected_stade_circonference)]
    
    # Utilisez Plotly Express pour créer l'histogramme de CIRCONFERENCE
    fig = px.histogram(filtered_df, x='CIRCONFERENCE (cm)', histfunc='count',
                       title=f'Histogramme de CIRCONFERENCE pour {selected_domanialite} et {selected_stade_circonference}')
    
    return fig

# Callback pour mettre à jour l'histogramme de HAUTEUR en fonction de la sélection de DOMANIALITE et STADE DE DEVELOPPEMENT
@app.callback(
    Output('histogram-hauteur', 'figure'),
    [Input('domanialite-hauteur-dropdown', 'value'),
     Input('stade-hauteur-dropdown', 'value')]
)
def update_histogram_hauteur(selected_domanialite_hauteur, selected_stade_hauteur):
    filtered_df = df_selected[(df_selected['DOMANIALITE'] == selected_domanialite_hauteur) & (df_selected['STADE DE DEVELOPPEMENT'] == selected_stade_hauteur)]
    
    # Utilisez Plotly Express pour créer l'histogramme de HAUTEUR
    fig = px.histogram(filtered_df, x='HAUTEUR (m)', histfunc='count',
                       title=f'Histogramme de HAUTEUR pour {selected_domanialite_hauteur} et {selected_stade_hauteur}')
    
    return fig

# Callback pour mettre à jour la carte en fonction de la sélection de DOMANIALITE et STADE DE DEVELOPPEMENT
@app.callback(
    Output('tree-map', 'figure'),
    [Input('domanialite-map-dropdown', 'value'),
     Input('stade-map-dropdown', 'value')]
)
def update_tree_map(selected_domanialite_map, selected_stade_map):
    filtered_df = df_selected[(df_selected['DOMANIALITE'] == selected_domanialite_map) & (df_selected['STADE DE DEVELOPPEMENT'] == selected_stade_map)]
    
    # Utilisez Plotly Express pour créer la carte avec les arbres
    fig = px.scatter_mapbox(filtered_df, 
                            lat=filtered_df['geo_point_2d'].apply(lambda x: float(x.split(',')[0])),
                            lon=filtered_df['geo_point_2d'].apply(lambda x: float(x.split(',')[1])),
                            hover_data=['DOMANIALITE', 'STADE DE DEVELOPPEMENT', 'CIRCONFERENCE (cm)', 'HAUTEUR (m)'],
                            title=f'Carte des arbres pour {selected_domanialite_map} et {selected_stade_map}',
                            mapbox_style="carto-positron",  # Vous pouvez changer le style de la carte
                            height=500
                            )
    
    return fig

# Exécutez l'application
if __name__ == '__main__':
    app.run_server(debug=True)
