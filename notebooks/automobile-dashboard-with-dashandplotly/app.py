import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv'
)

app = dash.Dash(__name__)

# List of years
year_list = [i for i in range(1980, 2024)]

app.layout = html.Div([
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'fontSize': 24
        }
    ),

    # Select Statistics Dropdown
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            placeholder='Select a report type',
            style={
                'width': '80%',
                'padding': '3px',
                'fontSize': '20px',
                'textAlignLast': 'center'
            }
        )
    ], style={'textAlign': 'center', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'marginBottom': '20px'}),

    # Select Year Dropdown
    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select year',
            style={
                'width': '80%',
                'padding': '3px',
                'fontSize': '20px',
                'textAlignLast': 'center'
            }
        )
    ], style={'textAlign': 'center', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'marginBottom': '30px'}),

    # Output charts container
    html.Div(id='output-container', className='chart-grid',
             style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '30px', 'justifyContent': 'center'})
])

# Disable/Enable year dropdown
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    return True

# Update output charts
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'),
     Input('select-year', 'value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        chart1_data = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        chart1 = dcc.Graph(
            figure=px.line(chart1_data, x='Year', y='Automobile_Sales',
                           title='Average Automobile Sales over Recession Periods'))

        chart2_data = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        chart2 = dcc.Graph(
            figure=px.bar(chart2_data, x='Vehicle_Type', y='Automobile_Sales',
                          title='Average Vehicles Sold by Type during Recession'))

        chart3_data = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        chart3 = dcc.Graph(
            figure=px.pie(chart3_data, values='Advertising_Expenditure', names='Vehicle_Type',
                          title='Advertisement Share by Vehicle Type during Recession'))

        chart4_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        chart4 = dcc.Graph(
            figure=px.bar(chart4_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
                          labels={'unemployment_rate': 'Unemployment Rate',
                                  'Automobile_Sales': 'Average Automobile Sales'},
                          title='Effect of Unemployment Rate on Vehicle Type and Sales'))

        return [
            html.Div(className='chart-item', children=[html.Div(children=chart1), html.Div(children=chart2)],
                     style={'display': 'flex', 'gap': '30px', 'flex': '1 1 100%'}),
            html.Div(className='chart-item', children=[html.Div(children=chart3), html.Div(children=chart4)],
                     style={'display': 'flex', 'gap': '30px', 'flex': '1 1 100%'})
        ]

    elif selected_statistics == 'Yearly Statistics' and input_year:
        yearly_data = data[data['Year'] == input_year]

        chart1_data = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        chart1 = dcc.Graph(
            figure=px.line(chart1_data, x='Year', y='Automobile_Sales',
                           title='Average Automobile Sales over Years'))

        chart2_data = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        chart2 = dcc.Graph(
            figure=px.line(chart2_data, x='Month', y='Automobile_Sales',
                           title='Total Monthly Automobile Sales'))

        chart3_data = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        chart3 = dcc.Graph(
            figure=px.bar(chart3_data, x='Vehicle_Type', y='Automobile_Sales',
                          title=f'Average Vehicles Sold by Vehicle Type in the year {input_year}'))

        chart4_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        chart4 = dcc.Graph(
            figure=px.pie(chart4_data, values='Advertising_Expenditure', names='Vehicle_Type',
                          title='Total Advertisement Expenditure for Each Vehicle'))

        return [
            html.Div(className='chart-item', children=[html.Div(children=chart1), html.Div(children=chart2)],
                     style={'display': 'flex', 'gap': '30px', 'flex': '1 1 100%'}),
            html.Div(className='chart-item', children=[html.Div(children=chart3), html.Div(children=chart4)],
                     style={'display': 'flex', 'gap': '30px', 'flex': '1 1 100%'})
        ]

    return []  # If nothing is selected


if __name__ == '__main__':
    app.run(debug=True)
