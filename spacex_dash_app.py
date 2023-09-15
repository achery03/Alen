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
Launch_Site=spacex_df.loc[:,['Launch Site','class']].groupby('Launch Site',as_index=False).mean()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                 dcc.Dropdown(id='site-dropdown',
                            options=[
                             {'label': 'All Sites', 'value': 'ALL'},
                                     {'label': Launch_Site['Launch Site'][0], 'value': Launch_Site['Launch Site'][0]},
                                    {'label': Launch_Site['Launch Site'][1], 'value': Launch_Site['Launch Site'][1]},
                                  {'label': Launch_Site['Launch Site'][2], 'value': Launch_Site['Launch Site'][2]},
                                {'label': Launch_Site['Launch Site'][3], 'value': Launch_Site['Launch Site'][3]},
                                ],
                                    value='ALL',
                                    placeholder="All Sites",
                                    searchable=True
                                        ),
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites

                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div([],id='success-pie-chart'),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                  dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                   # marks={0: '0',
                                    #100: '100'},
                                    value=[min_payload, max_payload]),
                                    
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div([],id='success-payload-scatter-chart'),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='children'),
              Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names=filtered_df['Launch Site'], 
        title='Total Successes')
        return dcc.Graph(figure=fig)
    else:
        filtered_df=spacex_df[spacex_df['Launch Site']==entered_site]
        d_class=filtered_df['class'].value_counts()
        fig=px.pie(d_class, values=d_class, 
        names=d_class.index, 
        title=entered_site+' Success Rate')
        return dcc.Graph(figure=fig)
        # return the outcomes piechart for a selected site
# TASK 4:
#def scatterplot(entered)

#dcc.Graph(
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='children'),
             [Input(component_id='site-dropdown', component_property='value'),
            Input(component_id='payload-slider',component_property='value')])
def scatterplot(entered_site,entered_num):
    filtered_df=spacex_df
    if entered_site=='ALL':
        fig2=px.scatter(filtered_df,x='Payload Mass (kg)',y='class',color='Booster Version Category',title='Payload vs Class Launch Sites',range_x=entered_num)
        return dcc.Graph(figure=fig2)
    else:
        filtered_df=spacex_df[spacex_df['Launch Site']==entered_site]
        fig2=px.scatter(filtered_df,x='Payload Mass (kg)',y='class',color='Booster Version Category',title=entered_site+' Payload vs Launch Site',range_x=entered_num)
        return dcc.Graph(figure=fig2)

# Run the app
if __name__ == '__main__':
    app.run_server(port=8090)
