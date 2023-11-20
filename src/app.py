from dash import Dash, dcc, html, Input, Output, State
import sys
from pathlib import Path
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import load_figure_template

sys.path.append(str(Path('.').absolute()) + '/src/utils')
sys.path.append(str(Path('.').absolute()) + '/utils')

# Import class and functions
from electricity_output_calc import SolarPanelSystem
from find_tilt_and_direction_value import find_tilt_and_direction_value
from calc_years_until_breakeven import calc_years_until_breakeven
from PVGIS_ETL import coordinates_to_insolation_mean

# Import the data for cities and solar packages
from data_dicts import packages_dict, years_list
from data_dicts import zone_1_predicted_prices, zone_2_predicted_prices, zone_3_predicted_prices, zone_4_predicted_prices


list_of_prices_by_zone = [zone_1_predicted_prices,
                          zone_2_predicted_prices,
                          zone_3_predicted_prices,
                          zone_4_predicted_prices]

# Load the "superhero" themed figure template from dash-bootstrap-templates library,
# adds it to plotly.io, and makes it the default figure template.
load_figure_template("superhero")

# Create a Dash app with Bootstrap "superhero" theme
app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])
server = app.server

# Load the price prognoses data
price_prognoses_data = pd.read_csv(r'data/predicted_prices_withzones.csv')
data = pd.read_csv(r'data/Electricity generation by source - Sweden.csv')
df = pd.DataFrame(data)
df.drop(columns=['Unnamed: 0'], inplace=True)
sums = df.sum()
fig1 = px.pie(names=sums.index, values=sums.values)
fig1.update_traces(pull=[0,0,0,0,0,0,0,0,0.2])
fig1.update_layout(
    # title='Energy source distribution in Sweden',
    title_font=dict(size=24),  # Adjust the size (30 in this example) as needed
    plot_bgcolor="#11293D"
)

# Create the line graph for the price predictions
prognoses_fig = px.line(price_prognoses_data, 
                        x='Year', 
                        y=['Predicted kWh price', 'zone1', 'zone2', 'zone3', 'zone4'] 
                        )
prognoses_fig.update_traces(name="zone 1", selector=dict(name="zone1"))
prognoses_fig.update_traces(name="zone 2", selector=dict(name="zone2"))
prognoses_fig.update_traces(name="zone 3", selector=dict(name="zone3"))
prognoses_fig.update_traces(name="zone 4", selector=dict(name="zone4"))
# Update the size of the title in the line graph
prognoses_fig.update_layout(
    # title_text='Price Forecast (per electricity zone)',
    title_font=dict(size=24),  # Adjust the size (30 in this example) as needed
    legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"),
    yaxis_title="predicted price (SEK/kWh)",
    xaxis_title="",
    plot_bgcolor="#11293D"
)


# Create the gauge figure
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=15,
    domain={'x': [0, 1], 'y': [0, 1],
            'row': 0, 'column': 0},
    # title={'text': "Years until breakeven"},
    gauge={'bar': {'color': "#f98435"}  # Change the color here
    }))

# Create the graph for the profitability
insolation_mean = 950
tilt_and_direction = find_tilt_and_direction_value(20, '225 SV')
my_system = SolarPanelSystem(system_cost=packages_dict['12 solar panels']['system_cost'],
                             system_effect_kWp=packages_dict['12 solar panels']['system_effect'],
                             insolation=insolation_mean,
                             tilt_and_direction=tilt_and_direction)
profit_values = my_system.profitability_over_time(zone_1_predicted_prices)
years_profit_df = pd.DataFrame({'Years': years_list, 'Profit': profit_values})

# round the values for hover output purposes (round -3 means even thousands, round -2 will give one "decimal")
years_profit_df['Profit'] = [round(x, -2) if abs(x) > 1000 else x for x in profit_values]

main_fig = px.bar(years_profit_df, x='Years', y='Profit', hover_data={'Profit':':.2f'})
main_fig.update_layout(title_x=0.5, title_font=dict(size=24))  # You can adjust the size (24 in this example) as needed
main_fig.update_layout(plot_bgcolor="#11293D")

# Create textbox input
city_textbox = dcc.Input(
    id='city-textbox',
    type='text',
    placeholder='Input City',
    value='Kiruna',
    className='mb-3',
    style={'color': 'black', 'width': '100%'}
)

# Create text div under textbox
insolation_response_div = html.Div(id="text-output-insolation", style={'font-size': '14px',
                                                                       'color': 'grey',
                                                                       'margin-top': '0px',
                                                                       'text-align': 'center'})
centered_city_input_row = dbc.Row(
    dbc.Col(
        [
            html.Label("Enter City"),
            city_textbox,
            insolation_response_div,
        ],
        lg=4, md=6, sm=8, xs=12,  # Specify different widths for different screen sizes
        className="mb-3",
    ),
    justify="center",  # Center the row contents horizontally
    align="center",    # Center the row contents vertically
)


# Create Dropdowns for the second graph
pricezone_dropdown = dcc.Dropdown(
    id='pricezone-dropdown',
    options=['SE1', 'SE2', 'SE3', 'SE4'],
    value='SE1',
    className='mb-3',
    style={'color': 'black', 'width': '100%'}  # Apply Bootstrap classes
)

package_dropdown = dcc.Dropdown(
    id='package-dropdown',
    options=['12 solar panels', '25 solar panels', '35 solar panels', '45 solar panels'],
    value='25 solar panels',
    className='mb-3',
    style={'color': 'black', 'width': '100%'}  # Apply Bootstrap classes
)

angle_dropdown = dcc.Dropdown(
    id='angle-dropdown',
    options=['0°', '10°', '20°', '30°', '40°', '50°', '60°', '70°', '80°', '90°'],
    value='40°',
    className='mb-3',
    style={'color': 'black', 'width': '100%'}  # Apply Bootstrap classes
)
direction_dropdown = dcc.Dropdown(
    id='direction-dropdown',
    options=['West', 'South West', 'South', 'South East', 'East'],
    value='West',
    className='mb-3',
    style={'color': 'black', 'width': '100%'}  # Apply Bootstrap classes
)
dropdown_row = dbc.Row([
    
    dbc.Col([
        html.Label("Select Electricity Price Zone"),
        pricezone_dropdown,
    ], width=3,lg=3, md=3, sm=6, xs=12),  # Adjust the width as needed

    dbc.Col([
        html.Label("Select Package"),
        package_dropdown,
    ], width=3,lg=3, md=3, sm=6, xs=12),  # Adjust the width as needed

    dbc.Col([
        html.Label("Select Tilt"),
        angle_dropdown,
    ], width=3,lg=3, md=3, sm=6, xs=12),  # Adjust the width as needed

    dbc.Col([
        html.Label("Select Direction"),
        direction_dropdown,
    ], width=3,lg=3, md=3, sm=6, xs=12),  # Adjust the width as needed
], className="mb-3")


# Callback for city text input
@app.callback(
        Output('text-output', 'children'),
        Output('text-output-insolation', 'children'),
        State("city-textbox", "value"),
        Input("city-textbox", "n_submit")
)

def print_city(city, n_submit):
    global insolation_mean
    insolation_mean = coordinates_to_insolation_mean(city)
    
    insolation_string = f"Avg insolation: {insolation_mean:.1f}"

    return None, insolation_string



# Callback for updating the chart
@app.callback(
    [Output('line-chart', 'figure'),
     Output('circle-with-number', 'figure')],
    [Input('pricezone-dropdown', 'value'),
     Input('package-dropdown', 'value'),
     Input('angle-dropdown', 'value'),
     Input('direction-dropdown', 'value'),
     Input('text-output', 'children')]
)
def update_output(selected_zone, selected_package, selected_angle, selected_direction, dummy_val):
    
    selected_list_of_prices = None
    electricity_zone_names = ['SE1', 'SE2', 'SE3', 'SE4']
    for i in range(len(electricity_zone_names)):
        if selected_zone == electricity_zone_names[i]:
            selected_list_of_prices = list_of_prices_by_zone[i]
            break
    

    # replace user friendly value with the real csv file name (of direction)
    direction_dropdown_values = ['West', 'South West', 'South', 'South East', 'East']
    direction_csv_columns = ['270 V', '225 SV', '180 S', '135 SO', '90 E']
    for i in range(len(direction_dropdown_values)):
        if selected_direction == direction_dropdown_values[i]:
            selected_direction = direction_csv_columns[i]
            break


    # update the bar chart
    selected_angle = selected_angle[:selected_angle.find('°')]
    tilt_and_direction = find_tilt_and_direction_value(int(selected_angle), selected_direction)
    
    global insolation_mean

    my_system = SolarPanelSystem(system_cost=packages_dict[selected_package]['system_cost'],
                                 system_effect_kWp=packages_dict[selected_package]['system_effect'],
                                 insolation=insolation_mean,
                                 tilt_and_direction=tilt_and_direction)
    
    profit_values = my_system.profitability_over_time(selected_list_of_prices)
    years_profit_df = pd.DataFrame({'Years': years_list, 'Profit': profit_values})
    
    # round the values for hover output purposes (round -3 means even thousands, round -2 will give one "decimal")
    years_profit_df['Profit'] = [round(x, -2) if abs(x) > 1000 else x for x in profit_values]

    main_fig = px.bar(years_profit_df, x='Years', y='Profit')
    main_fig.update_layout(title_x=0.05, title_font=dict(size=24),  # Adjust the size as needed
                      xaxis=dict(title_font=dict(size=20)),  # Adjust the size for x-axis title
                      yaxis=dict(title_font=dict(size=20))  # Adjust the size for y-axis title
                      )
    main_fig.update_layout(yaxis_title="Profitability (SEK)", xaxis_title="",plot_bgcolor="#11293D")

    # update the numerical figure
    fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=calc_years_until_breakeven(years_list, profit_values),
    domain={'x': [0, 1], 'y': [0, 1],
            'row': 0, 'column': 0},
    # title={'text': "Years until breakeven"},
    gauge={'bar': {'color': "#f98435"},
            'axis': {'range': [0, 30]}  # Change the color here
    }))
    fig.update_layout(
    # title=dict(text="Years until breakeven", font=dict(size=24)),  # Adjust the size (30 in this example) as needed
    plot_bgcolor="#11293D"
    )
    
    return main_fig, fig


# Define the app layout
app.layout = dbc.Container(fluid=True, children=[
    html.Div([
        # Add the gauge indicator here
        dbc.Row(
            [
                dbc.Col(dcc.Loading(
                    [
                        dbc.Row(
                            dbc.Col([
                                html.H1('Solar Panels: Return on Invested Capital', style={'font-size': '54px', 'font-weight': 'bold', 'text-align': 'center', 'margin-bottom': '20px'}),
                            ],
                                width=7,
                                className="mb-3",
                                lg=7, md=10, sm=12, xs=12,
                                style={"margin-top": "40px"}
                            ),
                            className="justify-content-center",
                        ),
                        # Add the new row to center the city input row
                        dbc.Row(
                            dbc.Col(centered_city_input_row, width=7),
                            className="justify-content-center",
                        ),
                        # # dbc.Row(
                        # #     dbc.Col(html.Div(id="text-output-insolation"),
                        # #     className="justify-content-center")

                        # ),
                        dbc.Row(
                            [
                                dbc.Col(dropdown_row, width=7),
                            ],
                            className="justify-content-center",
                        ),
                       dbc.Row(
            [
                dbc.Col([
                    html.H2("Return of investment", style={'font-size': '30px', 'font-weight': 'bold', 'text-align': 'center'}),
                    dcc.Graph(id='line-chart', figure=main_fig, style={'width': '100%'}),
                ], lg=6, xs=12),  # lg=6 for normal displays, xs=12 for mobile displays
                dbc.Col([
                    html.H2("Years until breakeven", style={'font-size': '30px', 'font-weight': 'bold', 'text-align': 'center', 'margin-bottom': '0px'}),
                    dcc.Graph(id='circle-with-number', figure=fig, style={'width': '100%'}),
                ], lg=6, xs=12),
            ],
            className="mt-5",
                        ),
                         dbc.Row(
            [
                dbc.Col([
                    html.H2("Energy source distribution in Sweden", style={'font-size': '30px', 'font-weight': 'bold', 'text-align': 'center'}),
                    dcc.Graph(figure=fig1, style={'width': '100%'}),
                ], lg=6, xs=12),
                dbc.Col([
                    html.H2("Price forecast (per electricity zone)", style={'font-size': '30px', 'font-weight': 'bold', 'text-align': 'center'}),
                    dcc.Graph(figure=prognoses_fig, style={'width': '100%'}),
                ], lg=6, xs=12),
            ],
            className="mt-5",
                        ),
                    ],
                )),
            ],
        ),
        html.Div(id="text-output"),
    ]),
])

if __name__ == "__main__":
    app.run_server(debug=True)
