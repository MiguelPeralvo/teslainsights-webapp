from plotly.graph_objs import *
import pandas as pd


def get_tesla_sentiment_graph(
        df, data_line_color='#42C4F7', error_line_color='#B4E8FC'
):
    # TODO: Adjust the x axis to the number of data points.
    n_rows = len(df)
    n_bins = int(n_rows / 4)

    trace = Scatter(
        # x=df['ts'],
        y=df['sentiment_absolute'],
        line=Line(
            color=data_line_color
        ),
        hoverinfo='skip',
        error_y=ErrorY(
            type='data',
            array=df['volatility'],
            thickness=1.5,
            width=2,
            color=error_line_color
        ),
        mode='lines'
    )

    layout = Layout(
        height=450,
        xaxis=dict(
            range=[0, n_rows],
            showgrid=False,
            showline=False,
            zeroline=False,
            fixedrange=True,
            tickvals=[0, n_bins, 2*n_bins, 3*n_bins, n_rows-1],
            ticktext=[
                str(pd.to_datetime(df.iloc[0]['min_created_at_epoch_ms'], unit='ms')).replace(' ', '<br />'),
                str(pd.to_datetime(round(df.iloc[n_bins]['created_at_epoch_ms']/1000)*1000, unit='ms')).replace(' ', '<br />'),
                str(pd.to_datetime(round(df.iloc[2*n_bins]['created_at_epoch_ms']/1000)*1000, unit='ms')).replace(' ', '<br />'),
                str(pd.to_datetime(round(df.iloc[3*n_bins]['created_at_epoch_ms']/1000)*1000, unit='ms')).replace(' ', '<br />'),
                str(pd.to_datetime(df.iloc[n_rows-1]['max_created_at_epoch_ms'], unit='ms')).replace(' ', '<br />'),
            ],
            title='Date/Time (UTC)'
        ),
        yaxis=dict(
            range=[max(0, min(df['sentiment_absolute']) - 1.5*max(df['volatility']) if n_rows > 0 else 0),
                   max(45, max(df['sentiment_absolute']) + 1.5*max(df['volatility'])) if n_rows > 0 else 45],
            showline=False,
            fixedrange=True,
            zeroline=False,
            nticks=max(6, round(df['sentiment_absolute'].iloc[-1] / 10) if n_rows > 0 else 6)
        ),
        margin=Margin(
            t=5,
            l=50,
            r=50
        )
    )

    return Figure(data=[trace], layout=layout)


# def get_tesla_slow_sentiment_graph(df):
#
#     trace = Scatter(
#         # x=df['ts'],
#         y=df['sentiment_absolute'],
#         line=Line(
#             color='#42C4F7'
#         ),
#         hoverinfo='skip',
#         error_y=ErrorY(
#             type='data',
#             array=df['volatility'],
#             thickness=1.5,
#             width=2,
#             color='#B4E8FC'
#         ),
#         mode='lines'
#     )
#
#     layout = Layout(
#         height=450,
#         xaxis=dict(
#             range=[0, 200],
#             showgrid=False,
#             showline=False,
#             zeroline=False,
#             fixedrange=True,
#             tickvals=[0, 50, 100, 150, 200],
#             ticktext=['200', '150', '100', '50', '0'],
#             title='Time Elapsed (sec)'
#         ),
#         yaxis=dict(
#             range=[min(0, min(df['sentiment_absolute'])),
#                    max(45, max(df['sentiment_absolute']) + max(df['volatility']))],
#             showline=False,
#             fixedrange=True,
#             zeroline=False,
#             nticks=max(6, round(df['sentiment_absolute'].iloc[-1] / 10))
#         ),
#         margin=Margin(
#             t=45,
#             l=50,
#             r=50
#         )
#     )
#
#     return Figure(data=[trace], layout=layout)