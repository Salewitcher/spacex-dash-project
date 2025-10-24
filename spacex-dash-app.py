# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Get max and min payload values for the slider
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# -------------------------
# App Layout
# -------------------------
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Launch Site Dropdown
    dcc.Dropdown(id='site-dropdown',
                 options=[{'label': 'All Sites', 'value': 'ALL'}] +
                         [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True
                 ),
    html.Br(),
    
    # TASK 2: Pie Chart for Success Counts
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    
    html.P("Payload range (Kg):"),
    
    # TASK 3: Payload Range Slider
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                    value=[min_payload, max_payload]
                    ),
    
    # TASK 4: Scatter Chart for Payload vs. Outcome
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# -------------------------
# TASK 2: Pie Chart Callback
# -------------------------
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Pie chart of total success counts for all sites
        fig = px.pie(spacex_df, names='Launch Site', values='class',
                     title='Total Successful Launches by Site')
    else:
        # Filter for selected site
        site_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        success_count = site_df['class'].sum()
        failure_count = site_df.shape[0] - success_count
        fig = px.pie(names=['Success', 'Failure'], values=[success_count, failure_count],
                     title=f'Success vs. Failure for {selected_site}')
    return fig

# -------------------------
# TASK 4: Scatter Chart Callback
# -------------------------
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                             (spacex_df['Payload Mass (kg)'] <= high)]
    
    if selected_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title='Payload vs. Outcome for All Sites')
    else:
        site_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(site_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title=f'Payload vs. Outcome for {selected_site}')
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
