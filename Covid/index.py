from dash import Dash, html, dcc, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

###


url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
url_recovered = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

confirmed = pd.read_csv(url_confirmed)
deaths = pd.read_csv(url_deaths)
recovered = pd.read_csv(url_recovered)

# Unpivot data frames
date1 = confirmed.columns[4:]
total_confirmed = confirmed.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], value_vars=date1, var_name='date', value_name='confirmed')
date2 = deaths.columns[4:]
total_deaths = deaths.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], value_vars=date2, var_name='date', value_name='death')
date3 = recovered.columns[4:]
total_recovered = recovered.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], value_vars=date3, var_name='date', value_name='recovered')

# Merging data frames
covid_data = total_confirmed.merge(right=total_deaths, how='left', on=['Province/State', 'Country/Region', 'date', 'Lat', 'Long'])
covid_data = covid_data.merge(right=total_recovered, how='left', on=['Province/State', 'Country/Region', 'date', 'Lat', 'Long'])

# Converting date column from string to proper date format
covid_data['date'] = pd.to_datetime(covid_data['date'])

# Check how many missing value naN
covid_data.isna().sum()

# Replace naN with 0
covid_data['recovered'] = covid_data['recovered'].fillna(0)

# Calculate new column
covid_data['active'] = covid_data['confirmed'] - covid_data['death'] - covid_data['recovered']

covid_data_1 = covid_data.groupby(['date'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()

covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()

# create dictionary of list
covid_data_dict = covid_data[['Country/Region', 'Lat', 'Long']]
#list_locations = covid_data_dict.set_index('Country/Region')[['Lat', 'Long']].T.to_dict('dict')




###




app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

#app.head = [html.Link(rel='stylesheet', href='./static/style.css')]





app.layout = dbc.Container([

    html.Div([
        html.Legend('Covid-19')
    ], id="titulo"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Global Deaths'),
                    html.P(f"{covid_data_1['confirmed'].iloc[-1]:,.0f}"),
                    html.P('novos:  ' + f"{covid_data_1['confirmed'].iloc[-1] - covid_data_1['confirmed'].iloc[-2]:,.0f} "
                   + ' (' + str(round(((covid_data_1['confirmed'].iloc[-1] - covid_data_1['confirmed'].iloc[-2]) /
                                       covid_data_1['confirmed'].iloc[-1]) * 100, 2)) + '%)')
                ])
            ])], width=3),

         dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Global Deaths'),
                    html.P(f"{covid_data_1['death'].iloc[-1]:,.0f}"),
                    html.P('novos:  ' + f"{covid_data_1['death'].iloc[-1] - covid_data_1['death'].iloc[-2]:,.0f} "
                   + ' (' + str(round(((covid_data_1['death'].iloc[-1] - covid_data_1['death'].iloc[-2]) /
                                       covid_data_1['death'].iloc[-1]) * 100, 2)) + '%)')
                ])
            ])], width=3),
        
         dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Global Recovered'),
                    html.P(f"{covid_data_1['recovered'].iloc[-1]:,.0f}"),
                    html.P('novos:  ' + f"{covid_data_1['recovered'].iloc[-1] - covid_data_1['recovered'].iloc[-2]:,.0f} "
                   + ' (' + str(round(((covid_data_1['recovered'].iloc[-1] - covid_data_1['recovered'].iloc[-2]) /
                                       covid_data_1['recovered'].iloc[-1]) * 100, 2)) + '%)')
                ])
            ])], width=3),
        
         dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Global Active'),
                    html.P(f"{covid_data_1['active'].iloc[-1]:,.0f}"),
                    html.P('novos:  ' + f"{covid_data_1['active'].iloc[-1] - covid_data_1['active'].iloc[-2]:,.0f} "
                   + ' (' + str(round(((covid_data_1['active'].iloc[-1] - covid_data_1['active'].iloc[-2]) /
                                       covid_data_1['active'].iloc[-1]) * 100, 2)) + '%)')
                ])
            ])], width=3),
    ]),
    dbc.Row([
        dbc.Col(html.Div('Coluna 1'), width=4),
        dbc.Col(html.Div('Coluna 2'), width=4),
        dbc.Col(html.Div('Coluna 3'), width=4),
    ]),
])





## CALLBACKS #####################################################





## Program ##

if __name__ == '__main__':
    app.run_server(debug=True, port=9999)