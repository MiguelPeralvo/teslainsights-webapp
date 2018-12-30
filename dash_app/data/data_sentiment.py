import pandas as pd
import sqlite3
import numpy as np
import traceback
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
from requests import Request
import datetime as dt


def query_tesla_sentiment(url, params):

    try:
        df = generate_data(params)
        # url = Request('GET', f'{url}', params=params).prepare().url
        # # We revert the dataframe for the visualisation.
        # df = pd.read_json(url).iloc[::-1]
        # # TODO: Calculate volatility
        # df['volatility'] = df['sentiment_absolute'].rolling(20).std()
        # df['volatility'] = df['volatility'].bfill()
        # # df['volatility'] = np.random.uniform(0, 5, df.shape[0])
    except:
        logger.warning(f'Problem when accessing url {url}: {traceback.format_exc()}')
        df = pd.DataFrame(columns=['sentiment_type', 'sentiment_seconds_back', 'bin', 'created_at_epoch_ms',
                               'sentiment_absolute', 'sentiment_normalized',' min_created_at_epoch_ms',
                               'max_created_at_epoch_ms', 'volatility'
                               ]
                      )

    return df


def generate_data(params):
    df = pd.DataFrame(columns=['sentiment_type', 'sentiment_seconds_back', 'bin', 'created_at_epoch_ms',
                               'sentiment_absolute', 'sentiment_normalized',' min_created_at_epoch_ms',
                               'max_created_at_epoch_ms', 'volatility'
                               ]
                      )

    return df


    # delta_ts = datetime.utcnow() - datetime(1970, 1, 1)
    #
    # # Bypass potential parameter memoization, but prevent excessive different requests if under attack
    # utc_now = int(
    #     (delta_ts.days * 24 * 60 * 60 + (delta_ts.seconds // 10) * 10)) * 1000  # + delta_ts.microseconds / 1000.0)

    # sentiment_type, sentiment_seconds_back, bin, created_at_epoch_ms, sentiment_absolute, sentiment_normalized, min_created_at_epoch_ms, max_created_at_epoch_ms
    # social_teslamonitor, 43200, 3865191, 1546076256500, 43.0140000, NULL, 1546076216000, 1546076286000
    # social_teslamonitor, 43200, 3865190, 1546076000658, 45.2756579, NULL, 1546075850000, 1546076179000

    # get_tesla_sentiment_quick
    # params = {
    #     # 'from_ms_ago': 600000,
    #     'from_created_epoch_ms': utc_now - 86400000,
    #     'limit': 250,
    #     'downsample_freq': 400,
    #     # 'sample_rate': 0.99,
    #     'sentiment_type': 'teslamonitor',
    # }
    # {
    #     "created_at_epoch_ms": 1546076286000,
    #     "max_created_at_epoch_ms": 1546076286000,
    #     "min_created_at_epoch_ms": 1546076286000,
    #     "sentiment_absolute": 42.945,
    #     "sentiment_normalized": null,
    #     "sentiment_seconds_back": 43200,
    #     "sentiment_type": "social_teslamonitor"
    # },


    # get_tesla_sentiment_slow

    # params = {
    #     'from_ms_ago': 5760000000,
    #     # 'from_created_epoch_ms': 1532441907000,
    #     'limit': 150,
    #     'downsample_freq': 1200,
    #     # 'sample_rate': 1.00,
    #     'sentiment_type': 'teslamonitor',
    # }



    # get_tesla_sentiment_historical

    # params = {
    #     'from_ms_ago': 8640000000,
    #     # 'from_created_epoch_ms': 1532441907000,
    #     'limit': 150,
    #     'downsample_freq': 21600,
    #     'sentiment_type': 'teslamonitor',
    #     #'sentiment_type': 'global_external_ensemble',
    # }
    # {
    #     "created_at_epoch_ms": 1546076287000,
    #     "max_created_at_epoch_ms": 1546076287000,
    #     "min_created_at_epoch_ms": 1546076287000,
    #     "sentiment_absolute": 57.537,
    #     "sentiment_normalized": null,
    #     "sentiment_seconds_back": 43200,
    #     "sentiment_type": "global_external_ensemble"
    # },



    # get_external_social_sentiment_historical


    #     params = {
    #         'from_ms_ago': 8640000000,
    #         # 'from_created_epoch_ms': 1532441907000,
    #         'limit': 150,
    #         'downsample_freq': 21600,
    #         'sentiment_type': 'social_external_ensemble',
    #
    #     }
    # {
    #     "created_at_epoch_ms": 1546076287000,
    #     "max_created_at_epoch_ms": 1546076287000,
    #     "min_created_at_epoch_ms": 1546076287000,
    #     "sentiment_absolute": 35.0,
    #     "sentiment_normalized": null,
    #     "sentiment_seconds_back": 43200,
    #     "sentiment_type": "social_external_ensemble"
    # },



    # get_external_news_sentiment_historical

    # params = {
    #     'from_ms_ago': 8640000000,
    #     # 'from_created_epoch_ms': 1532441907000,
    #     'limit': 150,
    #     'downsample_freq': 21600,
    #     'sentiment_type': 'news_external_ensemble',
    #
    # }
    # {
    #     "created_at_epoch_ms": 1546076287000,
    #     "max_created_at_epoch_ms": 1546076287000,
    #     "min_created_at_epoch_ms": 1546076287000,
    #     "sentiment_absolute": 80.22,
    #     "sentiment_normalized": null,
    #     "sentiment_seconds_back": 43200,
    #     "sentiment_type": "news_external_ensemble"
    # },


