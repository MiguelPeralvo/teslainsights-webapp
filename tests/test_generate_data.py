from datetime import datetime
import os
import traceback
import unittest

import dash_app.data.data_sentiment as data

class MyTestCase(unittest.TestCase):

    def test_get_teslamonitor(self):
        delta_ts = datetime.utcnow() - datetime(1970, 1, 1)

        # Bypass potential parameter memoization, but prevent excessive different requests if under attack
        utc_now = int(
            (delta_ts.days * 24 * 60 * 60 + (delta_ts.seconds // 10) * 10)) * 1000  # + delta_ts.microseconds / 1000.0)

        df_quick = data.generate_data({
            # 'from_ms_ago': 600000,
            'from_created_epoch_ms': utc_now - 86400000,
            'limit': 250,
            'downsample_freq': 400,
            # 'sample_rate': 0.99,
            'sentiment_type': 'teslamonitor',
        })

        print(df_quick['created_at_epoch_ms'].min())
        print(df_quick.iloc[0]['created_at_epoch_ms'])
        print(df_quick['created_at_epoch_ms'].max())
        print(len(df_quick))

        df_slow = data.generate_data({
            # 'from_ms_ago': 600000,
            'from_ms_ago': 5760000000,
            # 'from_created_epoch_ms': 1532441907000,
            'limit': 150,
            'downsample_freq': 1200,
            # 'sample_rate': 1.00,
            'sentiment_type': 'teslamonitor',
        })

        print(df_slow['created_at_epoch_ms'].min())
        print(df_slow['created_at_epoch_ms'].max())


        df_historical = data.generate_data({
            'from_ms_ago': 8640000000,
            # 'from_created_epoch_ms': 1532441907000,
            'limit': 150,
            'downsample_freq': 21600,
            'sentiment_type': 'teslamonitor',
            #'sentiment_type': 'global_external_ensemble',
        })

        print(df_historical['created_at_epoch_ms'].min())
        print(df_historical['created_at_epoch_ms'].max())


if __name__ == '__main__':
    unittest.main()