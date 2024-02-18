# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # Dropdown for selecting launch site
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'}  # Default option
                                    ] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],  # Launch sites options
                                    value='ALL',  # Default value
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                ),
                                
                                html.Br(),

                                # Placeholder for the pie chart
                                html.Div(dcc.Graph(id='success-pie-chart')),

                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # RangeSlider for selecting payload
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    marks={i: f'{i}' for i in range(0, 10001, 1000)},
                                    value=[0, 10000]  # Initial slider range
                                ),

                                html.Br(),

                                # Placeholder for the scatter chart
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
                                    if entered_site == 'ALL':
                                        # Filter the DataFrame for successes
                                        success_df = spacex_df[spacex_df['class'] == 1]
                                        # Generate a pie chart to show distribution of successes across different sites
                                        fig = px.pie(success_df, names='Launch Site',
                                        # Use all rows in the spacex_df DataFrame to render a pie chart of total success launches
                                        #fig = px.pie(spacex_df, names='class', 
                                                    title='Total Success Launches for All Sites')
                                    else:
                                        # Filter the spacex_df DataFrame based on the selected site
                                        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
                                        fig = px.pie(filtered_df, names='class', 
                                                    title=f'Success Launches for {entered_site}',
                                                    color='class',
                                                    color_discrete_map={0: 'red', 1: 'green'}) 
    
                                    # Update pie chart layout for better appearance
                                    fig.update_traces(textinfo='percent+label')
                                    fig.update_layout(transition_duration=500)
                                    return fig
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter(selected_site, payload_range):
                                    # Filter based on the selected payload range
                                    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                                                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]

                                    if selected_site == 'ALL':
                                        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                                                        color='Booster Version Category',
                                                        title='Launch Outcomes vs. Payload Mass for All Sites',
                                                        labels={'class': 'Launch Outcome'})
                                    else:
                                        # Further filter based on the selected launch site
                                        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
                                        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                                                        color='Booster Version Category',
                                                        title=f'Launch Outcomes vs. Payload Mass for {selected_site}',
                                                        labels={'class': 'Launch Outcome'})
    
                                    # Update scatter plot layout
                                    fig.update_layout(xaxis_title='Payload Mass (kg)', yaxis_title='Launch Outcome', 
                                                        yaxis=dict(tickmode='array', tickvals=[0, 1], ticktext=['Failure', 'Success']),
                                                        coloraxis_colorbar=dict(title='Booster Version'))
                                    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
