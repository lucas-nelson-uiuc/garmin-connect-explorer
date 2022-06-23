from datetime import date
import functions as funcs
from pandas import read_pickle


### FILE ORGANIZATION

BACKUP_DIR = '../garmin/backup-garmin-connect'

### DATETIME OBJECTS

TODAY = date.today()
WEEKDATES = funcs.get_week_dates(TODAY, 1, 7)

### dbc, css

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "4rem 1rem 2rem",
    "background-color": "#f8f9fa",
}

### df

# df = read_pickle('../garmin/backup-garmin-connect/activities_exhasuted.pkl')
# MOST_RECENT_ACTIVITY = df.iloc[-1, :]