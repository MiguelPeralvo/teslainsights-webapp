import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
from dash.dependencies import Input, Output, State, Event
from data import data_sentiment
from viz import viz_sentiment
import os
from flask_caching import Cache
import traceback
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = dash.Dash('streaming-insights-dash_app')
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})
server = app.server
url_global_sentiment_url = f'{os.getenv("TESLAMONITOR_WEBSERVICE_URL")}/{os.getenv("TESLAMONITOR_WEBSERVICE_GLOBAL_SENTIMENTS_SEGMENT")}'
# url_global_sentiment_url = f'http://0.0.0.0:8080/{os.getenv("TESLAMONITOR_WEBSERVICE_GLOBAL_SENTIMENTS_SEGMENT")}'
# url_global_sentiment_url = f'http://0.0.0.0:9091/{os.getenv("TESLAMONITOR_WEBSERVICE_GLOBAL_SENTIMENTS_SEGMENT")}'


app.layout = html.Div([
    html.Div([
        html.H1("Tesla Insights - Demo Mode", style={'textAlign': 'center'}),
        # html.Img(src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe-inverted.png"),
    ], className='banner'),
    html.Div([
        html.Div([
            html.H4("Tesla Insights - Social Sentiment - Last day", style={'textAlign': 'center', 'vertical-align': 'bottom'}),
            dcc.Graph(id='tesla-sentiment-quick'),
        ], className='Title'),
        dcc.Interval(id='tesla-sentiment-update-quick', interval=30000, n_intervals=0),
    ], className='row wind-speed-row', style={'width': '98%', 'display': 'inline-block'}),
    html.Div([
        html.Div([
            html.H4("Tesla Insights - Social Sentiment - Last days", style={'textAlign': 'center', 'vertical-align': 'bottom'}),
            dcc.Graph(id='tesla-sentiment-slow'),
        ], className='Title'),
        dcc.Interval(id='tesla-sentiment-update-slow', interval=120000, n_intervals=0),
    ], className='row wind-speed-row', style={'width': '49%', 'display': 'inline-block'}),
    html.Div([
        html.Div([
            html.H4("Tesla Insights - Social Sentiment - Last weeks", style={'textAlign': 'center', 'vertical-align': 'bottom'}),
            dcc.Graph(id='tesla-sentiment-historical'),
        ], className='Title'),
        dcc.Interval(id='tesla-sentiment-update-historical', interval=600000, n_intervals=0),
    ], className='row wind-speed-row', style={'width': '49%', 'display': 'inline-block'}),
    html.Div([
        html.Div([
            html.H4("External computation - Social Sentiment - Last weeks", style={'textAlign': 'center', 'vertical-align': 'bottom'}),
            dcc.Graph(id='external-social-sentiment-historical'),
        ], className='Title'),
        dcc.Interval(id='external-social-sentiment-update-historical', interval=600000, n_intervals=0),
    ], className='row wind-speed-row', style={'width': '49%', 'display': 'inline-block'}),
    html.Div([
        html.Div([
            html.H4("External computation - News Sentiment - Last weeks", style={'textAlign': 'center', 'vertical-align': 'bottom'}),
            dcc.Graph(id='external-news-sentiment-historical'),
        ], className='Title'),
        dcc.Interval(id='external-news-sentiment-update-historical', interval=600000, n_intervals=0),
    ], className='row wind-speed-row', style={'width': '49%', 'display': 'inline-block'}),
], style={'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto', 'marginRight': 'auto', "width": "1280px",
          'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'})


@app.callback(Output('tesla-sentiment-quick', 'figure'), [Input('tesla-sentiment-update-quick', 'n_intervals')])
def get_tesla_sentiment_quick(interval):
    global url_global_sentiment_url

    @cache.memoize(timeout=15)
    def get_tesla_sentiment_quick_internal(url, params):
        return data_sentiment.query_tesla_sentiment(url, params)

    delta_ts = datetime.utcnow() - datetime(1970, 1, 1)

    # Bypass potential parameter memoization, but prevent excessive different requests if under attack
    utc_now = int((delta_ts.days * 24 * 60 * 60 + (delta_ts.seconds//10)*10)) * 1000  # + delta_ts.microseconds / 1000.0)

    params = {
        # 'from_ms_ago': 600000,
        'from_created_epoch_ms': utc_now - 86400000,
        'limit': 250,
        'downsample_freq': 400,
        # 'sample_rate': 0.99,
        'sentiment_type': 'teslamonitor',
    }

    df = get_tesla_sentiment_quick_internal(url_global_sentiment_url, params)
    return viz_sentiment.get_tesla_sentiment_graph(df)

@app.callback(Output('tesla-sentiment-slow', 'figure'), [Input('tesla-sentiment-update-slow', 'n_intervals')])
def get_tesla_sentiment_slow(interval):
    global url_global_sentiment_url

    @cache.memoize(timeout=60)
    def get_tesla_sentiment_slow_internal(url, params):
        return data_sentiment.query_tesla_sentiment(url, params)

    params = {
        'from_ms_ago': 5760000000,
        # 'from_created_epoch_ms': 1532441907000,
        'limit': 150,
        'downsample_freq': 1200,
        # 'sample_rate': 1.00,
        'sentiment_type': 'teslamonitor',
    }

    df = get_tesla_sentiment_slow_internal(url_global_sentiment_url, params)
    return viz_sentiment.get_tesla_sentiment_graph(df)

@app.callback(Output('tesla-sentiment-historical', 'figure'), [Input('tesla-sentiment-update-historical', 'n_intervals')])
def get_tesla_sentiment_historical(interval):
    global url_global_sentiment_url

    @cache.memoize(timeout=300)
    def get_tesla_sentiment_historical_internal(url, params):
        return data_sentiment.query_tesla_sentiment(url, params)

    params = {
        'from_ms_ago': 8640000000,
        # 'from_created_epoch_ms': 1532441907000,
        'limit': 150,
        'downsample_freq': 21600,
        'sentiment_type': 'teslamonitor',
        #'sentiment_type': 'global_external_ensemble',
    }

    df = get_tesla_sentiment_historical_internal(url_global_sentiment_url, params)
    return viz_sentiment.get_tesla_sentiment_graph(df)


@app.callback(Output('external-social-sentiment-historical', 'figure'), [Input('external-social-sentiment-update-historical', 'n_intervals')])
def get_external_social_sentiment_historical(interval):
    global url_global_sentiment_url

    @cache.memoize(timeout=300)
    def get_external_social_sentiment_historical_internal(url, params):
        return data_sentiment.query_tesla_sentiment(url, params)

    params = {
        'from_ms_ago': 8640000000,
        # 'from_created_epoch_ms': 1532441907000,
        'limit': 150,
        'downsample_freq': 21600,
        'sentiment_type': 'social_external_ensemble',
        #'sentiment_type': 'global_external_ensemble',
    }

    df = get_external_social_sentiment_historical_internal(url_global_sentiment_url, params)
    return viz_sentiment.get_tesla_sentiment_graph(df, data_line_color='#F75441', error_line_color='#F2978C')


@app.callback(Output('external-news-sentiment-historical', 'figure'), [Input('external-news-sentiment-update-historical', 'n_intervals')])
def get_external_news_sentiment_historical(interval):
    global url_global_sentiment_url

    @cache.memoize(timeout=300)
    def get_external_news_sentiment_historical_internal(url, params):
        return data_sentiment.query_tesla_sentiment(url, params)

    params = {
        'from_ms_ago': 8640000000,
        # 'from_created_epoch_ms': 1532441907000,
        'limit': 150,
        'downsample_freq': 21600,
        'sentiment_type': 'news_external_ensemble',
        #'sentiment_type': 'global_external_ensemble',
    }

    df = get_external_news_sentiment_historical_internal(url_global_sentiment_url, params)
    return viz_sentiment.get_tesla_sentiment_graph(df, data_line_color='#DA3EF9', error_line_color='#E6A9F2')

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

app.scripts.append_script({
    'external_url': 'https://cdn.rawgit.com/MiguelPeralvo/teslamonitor-webapp/c3c6fae4/dash_app/gtag.js'
})

if __name__ == '__main__':
    app.run_server(use_reloader=False, debug=True)
