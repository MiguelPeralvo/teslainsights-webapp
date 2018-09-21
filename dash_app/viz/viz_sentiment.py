from plotly.graph_objs import *


def get_tesla_sentiment_graph(df):

    trace = Scatter(
        # x=df['ts'],
        y=df['sentiment'],
        line=Line(
            color='#42C4F7'
        ),
        hoverinfo='skip',
        error_y=ErrorY(
            type='data',
            array=df['volatility'],
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
            range=[min(0, min(df['sentiment'])),
                   max(45, max(df['sentiment']) + max(df['volatility']))],
            showline=False,
            fixedrange=True,
            zeroline=False,
            nticks=max(6, round(df['sentiment'].iloc[-1] / 10))
        ),
        margin=Margin(
            t=45,
            l=50,
            r=50
        )
    )

    return Figure(data=[trace], layout=layout)