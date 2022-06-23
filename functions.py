from datetime import timedelta
from plotly.subplots import make_subplots
import pandas as pd
import plotly.graph_objects as go

def get_week_dates(base_date, start_day, end_day=None):
    """
    Return entire week of dates based on given date limited by start_day and end_day.
    If end_day is None, return only start_day.

    >>> from datetime import date
    >>> get_week_dates(date(2015,1,16), 3, 5)
    [datetime.date(2015, 1, 14), datetime.date(2015, 1, 15), datetime.date(2015, 1, 16)]

    >>> get_week_dates(date(2015,1,15), 2, 5)
    [datetime.date(2015, 1, 13), datetime.date(2015, 1, 14), datetime.date(2015, 1, 15), datetime.date(2015, 1, 16)]
    """
    monday = base_date - timedelta(days=base_date.isoweekday() - 1)
    week_dates = [monday + timedelta(days=i) for i in range(7)]
    return week_dates[start_day - 1:end_day or start_day]


def most_recent_activity_summary(backup_dir, activity_type, activity_id):
    import plotly.graph_objects as go
    from pandas import read_pickle
    import os

    assert os.path.exists(f'{backup_dir}/{activity_type}/{activity_id}.pkl')
    px_df = read_pickle(f'{backup_dir}/{activity_type}/{activity_id}.pkl')

    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05)

    fig.add_trace(
        go.Scatter(x=px_df['time'], y=px_df['heart_rate_ma5'], name='Heart Rate',
        line=dict(color='firebrick')),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=px_df['time'], y=px_df['speed_kmh_ma5'], name='Speed',
        line={'color':'seagreen'}),
        row=2, col=1
    )

    fig.add_trace(
        go.Scatter(x=px_df['time'], y=px_df['elevation'], name='Elevation',
        line={'color':'steelblue'}),
        row=3, col=1
    )

    fig.update_layout(
        template='seaborn',
        margin=dict(l=20, r=20, t=10, b=10),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        showlegend=False
    )
    fig.update_traces(line=dict(width=3.26))
    
    fig['layout']['xaxis']['showgrid'] = False
    fig['layout']['xaxis2']['showgrid'] = False
    fig['layout']['xaxis3']['showgrid'] = False
    fig.update_xaxes(showticklabels=False)
    
    fig['layout']['yaxis']['title']='Heart Rate'
    fig['layout']['yaxis']['color'] = '#FFFFFF'
    fig['layout']['yaxis2']['title']='Speed'
    fig['layout']['yaxis2']['color'] = '#FFFFFF'
    fig['layout']['yaxis3']['title']='Elevation'
    fig['layout']['yaxis3']['color'] = '#FFFFFF'
    fig.update_yaxes(showgrid=False)
    
    return fig


def monthly_aggregate_performance(df):
    
    
    df['startTimeLocal'] = pd.to_datetime(df['startTimeLocal'])
    grouped_df = df.set_index('startTimeLocal').groupby([pd.Grouper(freq='M'), 'activityType']).sum()
    grouped_df['distance'] = grouped_df['distance'] / 1609
    df_agg = df.set_index('startTimeLocal').groupby([pd.Grouper(freq='M'), 'activityType']).agg('mean')
    sorted_vo2_max = df_agg['vO2MaxValue'].groupby('startTimeLocal', group_keys=False).nlargest(1)

    ############################################################

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=list(map(lambda x: x[0], sorted_vo2_max.index)),
            y=sorted_vo2_max,
            name="vO2 Max",
            mode="lines",
            line=dict(dash='dashdot', width=4)),
        secondary_y=True
    )

    fig.add_trace(
        go.Bar(
            x=grouped_df.reset_index()['startTimeLocal'],
            y=grouped_df.reset_index()['distance'],
            name="Distance"),
        secondary_y=False
    )

    fig.update_layout(
        template='seaborn',
        legend_font_color='#FFFFFF')
    fig.update_xaxes(title_text='')
    fig.update_yaxes(showgrid=False)
    fig.update_yaxes(title_text="Distance", secondary_y=False)
    fig.update_yaxes(title_text="vO2 Max", secondary_y=True)
    
    fig['layout']['xaxis']['color'] = '#FFFFFF'
    fig['layout']['yaxis']['title'] = 'Distance'
    fig['layout']['yaxis']['color'] = '#FFFFFF'
    fig['layout']['yaxis2']['title'] = 'vO2 Max'
    fig['layout']['yaxis2']['color'] = '#FFFFFF'

    fig.update_xaxes(showgrid=False, tickangle=315)
    fig.update_yaxes(showgrid=False)
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=10, b=10),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)'
    )

    return fig
