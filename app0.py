import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import plotly
from datetime import date

# Initializing the app and choosing the Theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

# Importing the data
df = pd.read_csv('C:/Users/mattp/Documents/Python Projects/SoSafe/SoSafeHistoryCleaned.csv')
df = df[['PartySize', 'SpaceId', 'LastRegisteredAt', 'LastSeatedAt', 'LastDepartedAt', 'LastVisitRating', 'RequestStatus', 'GuestTags', 'NoShowCount', 'VisitDuration', 'TimeToSeat', 'DaysPassed', 'MonthsPassed']]
# Function to help the filtering later
def date_string_to_date(date_string):
    return pd.to_datetime(date_string, infer_datetime_format=True)

# Creating a groupby object for the data table showing reviews and scans aggregated
review_scan_df = df.groupby(['MonthsPassed']).agg({'MonthsPassed': 'count', 'LastVisitRating':'mean'}).rename(columns={'MonthsPassed':'Scans', 'LastVisitRating':'Average Rating'}).reset_index()
review_scan_df['Average Rating'] = review_scan_df['Average Rating'].apply(lambda x: round(x, 2))
review_scan_df = review_scan_df.rename(columns={"Average Rating": "Avg Rating"})

# Setting the layout for our app
app.layout = html.Div([
    dbc.Row(
            dbc.Col( # Creating a Header for the page
                    html.H1("Restaurant Dashboard"), # Creates a column within the row (max  12 columns per row)
                            width={'size':6, 'offset':4} # Setting the width of the column
                            )),
    dbc.Row(
            dbc.Col( # Subtitle of the page
                    html.H4("Complete History of Scans - Filter Using Custom Input or Arrows"),
                    width={'size':6, 'offset':3}
            )),
    dbc.Row(
            dbc.Col(html.Div([dcc.DatePickerRange( # Creating a date picker to filter the data table
                                id='datepicker_range_input',
                                min_date_allowed=date(2021, 3, 1),
                                max_date_allowed=date(2022, 1, 1),
                                initial_visible_month=date(2021, 1, 1),
                                end_date=date(2021, 12, 1),
                                clearable=True # Allows the date range to be cleared and by consequence the whole data table can be shown
            )]))),
    dbc.Row(
            dbc.Col( # Creating an interactive data table for the user
                    dash_table.DataTable( # Could clean this up quite a bit by making the args a list and using **kwargs
                    id='datatable_interactivity',
                    columns=[
                            {'name': i,
                            'id': i,
                            'deletable': True,
                            'selectable': True, # Allows user to select columns
                            'hideable': True} # Allows user to toggle columns
                            for i in df.columns
                            ],
                    data=df.to_dict('records'), # The contents of the table
                    editable=False, # Allows the cells to be editable
                    filter_action='native', # Allow filtering of data by user('native') or not ('none')
                    sort_action='native', # Enable sorting per column by user ('native') or not ('none')
                    sort_mode='multi', # Enable sorting by 'single' column or 'multi' columns
                    column_selectable='multi', # Enable users to select multiple columns or single for filtering widgets
                    row_selectable='multi', # Enable users to select multiple rows or single row
                    row_deletable=False,
                    hidden_columns=['LastRegisteredAt', 'LastVisitRating', 'RequestStatus', 'GuestTags', 'NoShowCount', 'DaysPassed', 'Month', 'MonthsPassed'], # Enable user to select a single row or not
                    selected_columns=[], # ids of columns that user selects
                    selected_rows=[], # Same as above
                    page_action='native', # All data is passed to table ('native') or not ('none')
                    page_current=0, # Default page of table to show user
                    page_size=10, # Number of rows to display
                    style_header={'backgroundColor': 'rgb(30, 30, 30)'}, # Changing the header color to adhere to black theme
                    style_cell={
                                'minWidth': 130, 'maxWidth': 130, 'width': 130, # Setting width of cellse
                                },
                    style_cell_conditional=[
                    {'if': {'column_id': c},
                    'textAlign': 'left'
                    } for c in ['FirstName', 'GuestTags', 'RequestStatus']], # Formatting the text columns to be left aligned
                    style_header_conditional=[{
                    'if': {'column_editable': True},
                    'backgroundColor': 'rgb(50, 50, 50)',
                    'color': 'white'}],
                    style_data={
                    #'if': {'column_editable': True},
                    'backgroundColor': 'rgb(50, 50, 50)', # Setting background color of table
                    'color': 'white',
                    'whiteSpace': 'normal',
                    'height': 'auto' # Formatting for 2 lines if necessary
                    }))),

    html.Br(),
    html.Br(),
    dbc.Row(
            dbc.Col(html.H2('Scans and Avg Reviews Filtered')),
                    #width={'order':1, 'offset':0})
    ),
    html.Br(),
    dbc.Row(children=[
            dbc.Col( # Refers to the bar graph for the user
                    html.Div(id='bar_container_scans'),
                    width={'size':4, 'order':1, 'offset':0}),
            dbc.Col( # refers to the data table of reviews/scans for the user
                    dash_table.DataTable(
                    id='datatable_reviews_scans',
                    columns=[
                            {'name': i,
                            'id': i,
                            'deletable': False,
                            'selectable': False, # Allows user to select columns
                            'hideable': False} # Allows user to toggle columns
                            for i in review_scan_df.columns
                            ],
                    data=review_scan_df.to_dict('records'), # The contents of the table
                    editable=False, # Allows the cells to be editable
                    filter_action='none', # Allow filtering of data by user('native') or not ('none')
                    sort_action='native', # Enable sorting per column by user ('native') or not ('none')
                    sort_mode='multi', # Enable sorting by 'single' column or 'multi' columns
                    column_selectable='multi', # Enable users to select multiple columns or single for filtering widgets
                    row_selectable='multi', # Enable users to select multiple rows or single row
                    row_deletable=False,
                    selected_columns=[], # ids of columns that user selects
                    selected_rows=[], # Same as above
                    page_action='native', # All data is passed to table ('native') or not ('none')
                    page_current=0, # Default page of table to show user
                    page_size=10, # Number of rows to display
                    style_header={'backgroundColor': 'rgb(30, 30, 30)'}, # Changing the header color to adhere to black theme
                    style_cell={
                                'minWidth': 90, 'maxWidth': 90, 'width': 90, # Setting width of cellse
                                },
                    style_header_conditional=[{
                    'if': {'column_editable': True},
                    'backgroundColor': 'rgb(50, 50, 50)',
                    'color': 'white'}],
                    style_data={
                    #'if': {'column_editable': True},
                    'backgroundColor': 'rgb(50, 50, 50)', # Setting background color of table
                    'color': 'white',
                    'whiteSpace': 'normal',
                    'height': 'auto' # Formatting for 2 lines if necessary
                    })),
            dbc.Col(html.Div(id='review_container'),
                    width={'size':4, 'order':2, 'offset':0})
                    ]),

            # List of things to add:
            # Visit duration avg per day / on linegraph
            # Make instructions on how to filter in dropdown
            # Change the bar graph for the reviews into a line graph of avg / month


])

#--------------------------------------------------------------------------------------------------------------
# Creating a callback to update the data property of the datatable: datatable_interactivity
@app.callback(
    Output('datatable_interactivity', 'data'),
    [Input('datepicker_range_input', 'start_date'),
    Input('datepicker_range_input', 'end_date')])

def update_table_rows(start_date, end_date):
    data = df.to_dict('records')
    if start_date and end_date:
        mask = (date_string_to_date(df['LastDepartedAt']) >= date_string_to_date(start_date)) & (
                date_string_to_date(df['LastDepartedAt']) <= date_string_to_date(end_date))
        data=df.loc[mask].to_dict('records')
    return data

#--------------------------------------------------------------------------------------------------------------
# Creating the callback for the scans / month graph
@app.callback(
    Output(component_id='bar_container_scans', component_property='children'), # Creates the output based on the input,,
    [Input(component_id='datatable_interactivity', component_property='derived_virtual_data'),
    Input(component_id='datatable_interactivity', component_property='derived_virtual_selected_rows'), # The rest of the rows for input are just a display of what can be customized
    Input(component_id='datatable_interactivity', component_property='derived_virtual_selected_row_ids'),
    Input(component_id='datatable_interactivity', component_property='selected_rows'),
    Input(component_id='datatable_interactivity', component_property='derived_virtual_indices'),
    Input(component_id='datatable_interactivity', component_property='derived_virtual_row_ids'),
    Input(component_id='datatable_interactivity', component_property='active_cell'),
    Input(component_id='datatable_interactivity', component_property='selected_cell')]
)

#def update_bar(all_rows_data, selected_row_indices, selected_row_names, selected_rows, order_of_rows_indices, order_of_rows_names, active_cell, selected_cell):
def update_bar(filtered_rows_data, selected_row_indices, slct_rows_names, selected_rows,
               order_of_rows_indices, order_of_rows_names, active_cell, selected_cell):
    df_line = pd.DataFrame(filtered_rows_data) # Creates a df from the rows left after user filtering
    df_line = df_line.groupby('DaysPassed')['LastSeatedAt'].count() # Counts PhoneNumber as a column, because it's unique
    df_line = df_line.reset_index(drop=False).rename(columns={'LastSeatedAt': 'Scans'}) # Renames the count column to indicate the scans being counted

    return [
            dcc.Graph(id='scans_filtered_months',
                        figure = px.line(df_line, x='DaysPassed', y='Scans',
                                title='Scans per Day from Filtered Data',
                                template='plotly_dark',
                                height=300))
    ]



    # Creates a histogram from the filtered data of the scans/month
    #return [
    # dcc.Graph(id='scans_filtered_month',
    #            figure=px.histogram(data_frame=df_bar, x='MonthsPassed',
    #             category_orders={'MonthsPassed': [0,1,2,3,4,5]},
    #             title='Scans Per Month from Filtered Data',
    #             template='plotly_dark',
    #             height=300))
    #        ]

#-----------------------------------------------------------------------------------------------------------------------------------------
# Creating the callback for the reviews graph
@app.callback(Output(component_id='review_container', component_property='children'), # Creates the output based on the input,,
    [Input(component_id='datatable_interactivity', component_property='derived_virtual_data'),
    Input(component_id='datatable_interactivity', component_property='derived_virtual_selected_rows')])

# Function for the reviews graph
def update_reviews(filtered_rows_data, selected_rows):
    df_reviews = pd.DataFrame(filtered_rows_data) # Must make a copy of the table for graph to work

    return [
            dcc.Graph(id='review_container',
                        figure=px.histogram(
                        data_frame=df_reviews,
                        x='LastVisitRating',
                        title='Reviews from Filtered Data',
                        template='plotly_dark',
                        height=300
                        ).update_layout(
                                xaxis = dict(
                                        tickmode = 'array',
                                        tickvals = [1, 5, 10],
                                        ticktext = ['One', 'Five', 'Ten'])))
            ]





if __name__ == '__main__':
    app.run_server(debug=True)
