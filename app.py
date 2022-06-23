import os
from pydoc import classname

import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd

import functions as funcs
from constants import TODAY, WEEKDATES, SIDEBAR_STYLE, BACKUP_DIR

app = Dash(__name__)
df = pd.read_pickle('../garmin/backup-garmin-connect/activities_exhausted.pkl')
# week_dates = funcs.get_week_dates(TODAY, 1, 7)
# week_begin = week_dates[0]
# this_week = pd.to_datetime(df['startTimeLocal']).dt.date >= week_begin


most_recent_activity = df.iloc[-1, :]
mr_id = most_recent_activity['activityId']
mr_type = most_recent_activity['activityType']
mr_name = most_recent_activity['activityName']
mr_location = most_recent_activity['locationName']
mr_dist = most_recent_activity['distance']
mr_elev = most_recent_activity['elevationGain']
mr_duration = most_recent_activity['duration']
mr_avg_hr = most_recent_activity['averageHR']


#############################################

app = Dash(external_stylesheets=[dbc.themes.DARKLY])
app.layout = html.Div([
    
    # NAVIGATION BAR
    html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Activities", href="#")),
                dbc.NavItem(dbc.NavLink("Statistics", href="#")),
                dbc.NavItem(dbc.NavLink("Leaderboards", href="#")),
                dbc.NavItem(dbc.NavLink("Progress", href="#")),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("username_here", header=True),
                        dbc.DropdownMenuItem("Profile", href="#"),
                        dbc.DropdownMenuItem("Clubs", href="#"),
                        dbc.DropdownMenuItem("Settings", href="#"),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="More",
                ),
            ],
            brand="Garmin Connect EXplore",
            brand_href="#",
            color="primary",
            dark=True,
        )]),
    
    # BREADCRUMBS
    html.Div([
        dbc.Breadcrumb(
            items=[
                {"label": "Docs", "href": "/docs", "external_link": True},
                {"label": "Components", "href": "/docs/components", "external_link": True},
                {"label": "Breadcrumb", "active": True},
            ],
        )
    ]),
    
    # BODY
    html.Div([
        html.Div([
            html.Label(f'Most Recent Activity: {mr_name}'),
            html.Div([
                dbc.Badge(f"Location: {mr_location}", color="primary"),
                dbc.Badge(f"Type: {mr_type}", color="success"),
                dbc.Badge(f"ID: {mr_id}", color="secondary")
            ], className='badges'),
            dcc.Graph(figure=funcs.most_recent_activity_summary(BACKUP_DIR, mr_type, mr_id))
        ], style={'order':1}, className='card'),

        html.Div([
            html.Label('Aggregate Performance per Month'),
            html.Div([
                dbc.Badge(f"Distance: {df['distance'].divide(1609).sum()} miles", color="primary"),
                dbc.Badge(f"Duration: {df['distance'].divide(3600).sum()} hours", color="success"),
                dbc.Badge(f"Elevation: {df['elevationGain'].sum()} meters", color="secondary")
            ], className='badges'),
            dcc.Graph(figure=funcs.monthly_aggregate_performance(df))
        ], style={'order':2, 'flex': 2}, className='card')    
        
    ], className='card_row'),

    html.Div([
        html.Div([
            html.Label(f'Most Recent: {mr_name}'),
            html.Div([
                dbc.Badge(f"Location: {mr_location}", color="primary"),
                dbc.Badge(f"Type: {mr_type}", color="success"),
                dbc.Badge(f"ID: {mr_id}", color="secondary")
            ], className='badges'),
            dcc.Graph(figure=funcs.most_recent_activity_summary(BACKUP_DIR, mr_type, mr_id))
        ], style={'order':1}, className='card'),

        html.Div([
            html.Label(f'Most Recent: {mr_name}'),
            html.Div([
                dbc.Badge(f"Location: {mr_location}", color="primary"),
                dbc.Badge(f"Type: {mr_type}", color="success"),
                dbc.Badge(f"ID: {mr_id}", color="secondary")
            ], className='badges'),
            dcc.Graph(figure=funcs.most_recent_activity_summary(BACKUP_DIR, mr_type, mr_id))
        ], style={'order':2}, className='card'),

        html.Div([
            html.Label(f'Most Recent: {mr_name}'),
            html.Div([
                dbc.Badge(f"Location: {mr_location}", color="primary"),
                dbc.Badge(f"Type: {mr_type}", color="success"),
                dbc.Badge(f"ID: {mr_id}", color="secondary")
            ], className='badges'),
            dcc.Graph(figure=funcs.most_recent_activity_summary(BACKUP_DIR, mr_type, mr_id))
        ], style={'order':3}, className='card'),        
        
    ], className='card_row')
])


#############################################
if __name__ == '__main__':
    app.run_server(debug=True)
