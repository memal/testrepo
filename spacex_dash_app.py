# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Read the airline data into pandas dataframe
spacex_df =  pd.read_csv("C:\\Users\\mrmoh\\OneDrive\\Desktop\\spacex_launch_dash.csv")
print(spacex_df.head())
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                    ],
                                    value='ALL',  # Default value is 'ALL'
                                    placeholder="Select a Launch Site here",  # Placeholder text
                                    searchable=True  # Enable search functionality
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    marks={i: str(i) for i in range(0, 10001, 1000)},
                                    value=[min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Calculate total successful launches for all sites
        total_success = len(spacex_df[spacex_df['class'] == 1])
        total_failures = len(spacex_df[spacex_df['class'] == 0])

        # Create a pie chart
        pie_chart = px.pie(
            names=['Success', 'Failures'],
            values=[total_success, total_failures],
            hole=0.3,
            title='Total Successful Launches for All Sites'
        )
    else:
        # Calculate successful and failed launches for the selected site
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        site_success = len(site_data[site_data['class'] == 1])
        site_failures = len(site_data[site_data['class'] == 0])

        # Create a pie chart
        pie_chart = px.pie(
            names=['Success', 'Failures'],
            values=[site_success, site_failures],
            hole=0.3,
            title=f'Successful vs. Failed Launches for {selected_site}'
        )

    return pie_chart

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, selected_payload):
    if selected_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= selected_payload[0]) &
                                (spacex_df['Payload Mass (kg)'] <= selected_payload[1])]
    else:
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        filtered_df = site_data[(site_data['Payload Mass (kg)'] >= selected_payload[0]) &
                                (site_data['Payload Mass (kg)'] <= selected_payload[1])]

    scatter_chart = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload vs. Launch Outcome',
        labels={'Payload Mass (kg)': 'Payload Mass (kg)', 'class': 'Launch Outcome'}
    )

    return scatter_chart

# Run the app
if __name__ == '__main__':
    app.run_server()
