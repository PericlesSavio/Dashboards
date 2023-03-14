






from dash import Dash, html, dcc, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
import plotly.express as px



df = px.data.gapminder()
years = df.year.unique()
continents = df.continent.unique()




pag1 = dbc.Tab([html.P('Página 1')], label='Página 1')
pag2 = dbc.Tab([html.P('Página 2')], label='Página 2')
pag3 = dbc.Tab([html.P('Página 3')], label='Página 3')







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



controls = dbc.Card([dropdown, checklist, slider],
    body=True,
)


tab1 = dbc.Tab([dcc.Graph(id="line-chart")], label="Line Chart")
tab2 = dbc.Tab([dcc.Graph(id="scatter-chart")], label="Scatter Chart")
tab3 = dbc.Tab([table], label="Table", className="p-4")
tabs = dbc.Card(dbc.Tabs([tab1, tab2, tab3]))








app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

app.layout = dbc.Container([


    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Card(dbc.Tabs([pag1, pag2, pag3]))
                ])            
            ])                
        ])
    ]),

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
        dbc.Col([controls], width=4),
        dbc.Col([tabs], width=8),
    ]),

    dbc.Row([
        dbc.Col([], width=4),
        dbc.Col([], width=8),
    ]),


], fluid=True, style={'height': '100vh'})

#




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




if __name__ == '__main__':
    app.run_server(debug=True, port=8888)