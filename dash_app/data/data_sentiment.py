import pandas as pd
import sqlite3
import datetime as dt


def query_tesla_sentiment_slow():
    now = dt.datetime.now()
    sec = now.second
    minute = now.minute
    hour = now.hour

    total_time = (hour * 3600) + (minute * 60) + (sec)

    con = sqlite3.connect("./data/wind-data.db")
    df = pd.read_sql_query('SELECT rowid as ts, Speed as sentiment, SpeedError as volatility from Wind where\
                            rowid > "{}" AND rowid <= "{}";'
                            .format(total_time-200, total_time), con)
    return df


def query_tesla_sentiment_quick():
    now = dt.datetime.now()
    sec = now.second
    minute = now.minute
    hour = now.hour

    total_time = (hour * 3600) + (minute * 60) + (sec)

    con = sqlite3.connect("./data/wind-data.db")
    df = pd.read_sql_query('SELECT rowid as ts, Speed as sentiment, SpeedError as volatility from Wind where\
                            rowid > "{}" AND rowid <= "{}";'
                            .format(total_time-200, total_time), con)
    return df

