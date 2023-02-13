from altair import Chart, Tooltip

def chart(df, x, y, target) -> Chart:
    ''' Creates a chart using altair and the data from DataFrame. Specified title, size, padding, bg color.
        Utilizes tooltips to display dataframe column names for extra details on plot point.'''
    graph = Chart(df).mark_point().encode(
        x=x,
        y=y,
        color=target
    ).properties(
        padding=30,
        background="Grey",
        title=f"{y} of {x} for {target}"
    ).configure_view(
        width=629,
        height=637
    ).mark_circle(size=100).encode(
        x=x,
        y=y,
        color=target,
        tooltip=Tooltip(df.columns.to_list())
    )

    return graph
