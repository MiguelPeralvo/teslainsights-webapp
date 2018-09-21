import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
from plotly.graph_objs import *
from data import sentiment
import os
from flask_caching import Cache

app = dash.Dash('streaming-teslamonitor-dash_app')
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})
server = app.server


app.layout = html.Div([
    html.Div([
        html.H1("Tesla Monitor", style={'textAlign': 'center'}),
        # html.Img(src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe-inverted.png"),
    ], className='banner'),
    html.Div([
        html.Div([
            html.H4("Tesla Sentiment Low Latency - Tesla Monitor Calculation", style={'textAlign': 'center'})
        ], className='Title'),
        html.Div([
            dcc.Graph(id='tesla-sentiment-quick'),
        ], className='twelve columns tesla-sentiment'),
        dcc.Interval(id='tesla-sentiment-update-quick', interval=10000, n_intervals=0),
    ], className='row wind-speed-row'),
    html.Div([
        html.Div([
            html.H4("Tesla Sentiment Higher Latency - External Sources Aggregation", style={'textAlign': 'center'})
        ], className='Title'),
        html.Div([
            dcc.Graph(id='tesla-sentiment-slow'),
        ], className='twelve columns tesla-sentiment'),
        dcc.Interval(id='tesla-sentiment-update-slow', interval=30000, n_intervals=0),
    ], className='row wind-speed-row'),
], style={'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto', 'marginRight': 'auto', "width": "1200px",
          'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'})


@app.callback(Output('tesla-sentiment-quick', 'figure'), [Input('tesla-sentiment-update-quick', 'n_intervals')])
def get_tesla_sentiment_quick(interval):
    @cache.memoize(timeout=5)
    def get_tesla_sentiment_quick():
        return sentiment.query_tesla_sentiment_quick()

    df = get_tesla_sentiment_quick()

    trace = Scatter(
        y=df['Speed'],
        line=Line(
            color='#42C4F7'
        ),
        hoverinfo='skip',
        error_y=ErrorY(
            type='data',
            array=df['SpeedError'],
            thickness=1.5,
            width=2,
            color='#B4E8FC'
        ),
        mode='lines'
    )

    layout = Layout(
        height=450,
        xaxis=dict(
            range=[0, 200],
            showgrid=False,
            showline=False,
            zeroline=False,
            fixedrange=True,
            tickvals=[0, 50, 100, 150, 200],
            ticktext=['200', '150', '100', '50', '0'],
            title='Time Elapsed (sec)'
        ),
        yaxis=dict(
            range=[min(0, min(df['Speed'])),
                   max(45, max(df['Speed'])+max(df['SpeedError']))],
            showline=False,
            fixedrange=True,
            zeroline=False,
            nticks=max(6, round(df['Speed'].iloc[-1]/10))
        ),
        margin=Margin(
            t=45,
            l=50,
            r=50
        )
    )

    return Figure(data=[trace], layout=layout)


@app.callback(Output('tesla-sentiment-slow', 'figure'), [Input('tesla-sentiment-update-slow', 'n_intervals')])
def get_tesla_sentiment_slow(interval):

    @cache.memoize(timeout=5)
    def get_tesla_sentiment_slow():
        return sentiment.query_tesla_sentiment_slow()

    df = get_tesla_sentiment_slow()
    trace = Scatter(
        y=df['Speed'],
        line=Line(
            color='#42C4F7'
        ),
        hoverinfo='skip',
        error_y=ErrorY(
            type='data',
            array=df['SpeedError'],
            thickness=1.5,
            width=2,
            color='#B4E8FC'
        ),
        mode='lines'
    )

    layout = Layout(
        height=450,
        xaxis=dict(
            range=[0, 200],
            showgrid=False,
            showline=False,
            zeroline=False,
            fixedrange=True,
            tickvals=[0, 50, 100, 150, 200],
            ticktext=['200', '150', '100', '50', '0'],
            title='Time Elapsed (sec)'
        ),
        yaxis=dict(
            range=[min(0, min(df['Speed'])),
                   max(45, max(df['Speed'])+max(df['SpeedError']))],
            showline=False,
            fixedrange=True,
            zeroline=False,
            nticks=max(6, round(df['Speed'].iloc[-1]/10))
        ),
        margin=Margin(
            t=45,
            l=50,
            r=50
        )
    )

    return Figure(data=[trace], layout=layout)


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "https://cdn.rawgit.com/plotly/dash-dash_app-stylesheets/737dc4ab11f7a1a8d6b5645d26f69133d97062ae/dash-wind-streaming.css",
                "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
                "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i"]


for css in external_css:
    app.css.append_css({"external_url": css})

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })

if __name__ == '__main__':
    # dash_app.config["CACHE_TYPE"] = "null"


    app.run_server(use_reloader=False, debug=True)
