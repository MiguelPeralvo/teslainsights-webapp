from plotly.graph_objs import *


def get_tesla_sentiment_graph(df, data_line_color='#42C4F7', error_line_color='#B4E8FC'):
    n_rows = len(df)

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
            range=[0, 250],
            showgrid=False,
            showline=False,
            zeroline=False,
            fixedrange=True,
            tickvals=[0, 500, 1000, 1500, 2000, 2500],
            ticktext=['2500', '2000', '1500', '1000', '500', '0'],
            title='Time Elapsed (sec)'
        ),
        yaxis=dict(
            range=[max(0, min(df['sentiment_absolute']) - 2*max(df['volatility']) if n_rows > 0 else 0),
                   max(45, max(df['sentiment_absolute']) + 2*max(df['volatility'])) if n_rows > 0 else 45],
            showline=False,
            fixedrange=True,
            zeroline=False,
            nticks=max(6, round(df['sentiment_absolute'].iloc[-1] / 10) if n_rows > 0 else 6)
        ),
        margin=Margin(
            t=45,
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