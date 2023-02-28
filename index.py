from dash import Dash, html, dcc, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])






df = px.data.gapminder()
years = df.year.unique()
continents = df.continent.unique()




table = html.Div(
    dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i, "deletable": True} for i in df.columns],
        data=df.to_dict("records"),
        page_size=10,
        editable=True,
        cell_selectable=True,
        filter_action="native",
        sort_action="native",
        style_table={"overflowX": "auto"},
        row_selectable="multi",
    ),
    className="dbc-row-selectable",
)

dropdown = html.Div([
        dbc.Label("Select indicator (y-axis)"),
        dcc.Dropdown(["gdpPercap", "lifeExp", "pop"],
            "pop",
            id="indicator",
            clearable=False,
        ),
    ], className="mb-4",)

checklist = html.Div([
        dbc.Label("Select Continents"),
        dbc.Checklist(
            id="continents",
            options=[{"label": i, "value": i} for i in continents],
            value=continents,
            inline=True,
        ),
    ],
    className="mb-4",
)

slider = html.Div(
    [
        dbc.Label("Select Years"),
        dcc.RangeSlider(
            years[0],
            years[-1],
            5,
            id="years",
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True},
            value=[years[2], years[-2]],
            className="p-0",
        ),
    ],
    className="mb-4",
)




tab1 = dbc.Tab([dcc.Graph(id="line-chart")], label="Line Chart")
tab2 = dbc.Tab([dcc.Graph(id="scatter-chart")], label="Scatter Chart")
tab3 = dbc.Tab([table], label="Table", className="p-4")





pag1 = dbc.Tab([
    dbc.Row([
        dbc.Col([dbc.Card([dropdown, checklist, slider], body=True,)], width=4),
        dbc.Col([dbc.Card(dbc.Tabs([tab1, tab2, tab3]))], width=8),
    ]),
    ], label='Página 1')
pag2 = dbc.Tab([html.P('Página 2')], label='Página 2')
pag3 = dbc.Tab([html.P('Página 3')], label='Página 3')






app.layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Legend('Dashboard - Exemplo')
                ])            
            ])                
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Card(dbc.Tabs([pag1, pag2, pag3]))
                ])            
            ])                
        ])
    ]),

    

])




## CALLBACKS ##

@callback(
    Output("line-chart", "figure"),
    Output("scatter-chart", "figure"),
    Output("table", "data"),
    Input("indicator", "value"),
    Input("continents", "value"),
    Input("years", "value"),
    #Input(ThemeChangerAIO.ids.radio("theme"), "value"),
)
def update_line_chart(indicator, continent, yrs):
    if continent == [] or indicator is None:
        return {}, {}, []

    dff = df[df.year.between(yrs[0], yrs[1])]
    dff = dff[dff.continent.isin(continent)]
    data = dff.to_dict("records")

    fig = px.line(
        dff,
        x="year",
        y=indicator,
        color="continent",
        line_group="country",
    )

    fig_scatter = px.scatter(
        df.query(f"year=={yrs[1]} & continent=={continent}"),
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        log_x=True,
        size_max=60,
    )

    return fig, fig_scatter, data




## Program ##

if __name__ == '__main__':
    app.run_server(debug=True, port=8888)