from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from datetime import datetime

##https://lit-eyrie-59816-7f93c5c96f2e.herokuapp.com/ 

# Création de l'application Dash avec un thème Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Récupération des données
url = "https://raw.githubusercontent.com/chriszapp/datasets/main/books.csv"
df = pd.read_csv(url, on_bad_lines='skip')
df['publication_date'] = pd.to_datetime(df['publication_date'], errors='coerce')
df = df.rename(columns=lambda x: x.strip())

# Définition du layout de l'application
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Visualisation des Données des Livres"), width={"size": 6, "offset": 3})),

    # Sélecteurs pour l'auteur et la plage de dates
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='author-dropdown',
            options=[{'label': author, 'value': author} for author in df['authors'].unique()],
            value=df['authors'].unique()[0],
            className="mb-2"
        ), width=6),
        dbc.Col(dcc.DatePickerRange(
            id='date-picker',
            min_date_allowed=df['publication_date'].min(),
            max_date_allowed=df['publication_date'].max(),
            start_date=datetime(2000, 1, 1),
            end_date=datetime(2020, 12, 31),
            className="mb-2"
        ), width=6)
    ]),

    # Onglets pour différents graphiques
    dbc.Tabs([
        dbc.Tab(label="Bar Chart", tab_id="tab-bar-chart"),
        dbc.Tab(label="Histogram", tab_id="tab-histogram"),
        dbc.Tab(label="Scatter Plot", tab_id="tab-scatter-plot"),
    ], id="tabs", active_tab="tab-bar-chart"),

    # Zone pour afficher les graphiques
    html.Div(id='content')
], fluid=True)

# Callback pour mettre à jour le contenu en fonction de l'onglet sélectionné
@app.callback(
    Output('content', 'children'),
    [Input('tabs', 'active_tab'),
     Input('author-dropdown', 'value'), 
     Input('date-picker', 'start_date'), 
     Input('date-picker', 'end_date')]
)
def render_content(active_tab, selected_author, start_date, end_date):
    filtered_df = df[(df['authors'] == selected_author) & 
                     (df['publication_date'] >= start_date) & 
                     (df['publication_date'] <= end_date)]

    if active_tab == 'tab-bar-chart':
        fig = px.bar(filtered_df, x='title', y='average_rating', color='average_rating',
                     labels={'title': 'Titre', 'average_rating': 'Note Moyenne'})
        return dcc.Graph(figure=fig)

    elif active_tab == 'tab-histogram':
        fig = px.histogram(filtered_df, x='average_rating', nbins=20, title='Répartition des Notes')
        return dcc.Graph(figure=fig)

    elif active_tab == 'tab-scatter-plot':
        fig = px.scatter(filtered_df, x='num_pages', y='average_rating', color='average_rating',
                         title='Nombre de Pages vs Note Moyenne')
        return dcc.Graph(figure=fig)

    return "Sélectionnez un onglet pour afficher les graphiques."

# Exécution de l'application
if __name__ == '__main__':
    app.run_server(debug=True)
