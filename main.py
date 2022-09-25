# importing required libraries
import os
from pathlib import Path

import dash
import pandas as pd
import plotly.express as px
from dash import html, dcc, Input, Output

# Colleting the data
data_file = os.path.join(Path(__file__).parent, 'data', 'time_series_covid19_confirmed_US.csv')
df = pd.read_csv(data_file)

# Counting the number of confirmed cases each day for each state
df_state_lvl = df.groupby('Province_State', as_index=False).sum()
# print(df_state_lvl.head())
df_melt = df_state_lvl.melt(id_vars=['Province_State'],
                            value_vars=df_state_lvl.columns[
                                (df_state_lvl.columns.str[-2:] == '21') | (df_state_lvl.columns.str[-2:] == '20')])
# Selecting options in province states
ops = df_melt['Province_State'].unique()

app = dash.Dash()
server = app.server  # configure the server
app.layout = html.Div(children=
                      [html.Div('Hello World From Dash.'),
                       html.H1('H1 tag here'),
                       html.Div(
                           dcc.Dropdown(id='dropdown',
                                        options=ops
                                        )
                       ),
                       dcc.Graph(id='fig1')

                       ]

                      )


@app.callback(Output(component_id='fig1', component_property='figure'),
              Input(component_id='dropdown', component_property='value'))
def update_graph(state):
    df_state = df_melt.loc[df_melt['Province_State'] == state]
    fig = px.line(df_state, x='variable', y='value', title=f'{state} cumulative case counts')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
