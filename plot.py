import plotly.express as px

def generate_plot(df, output_html='plot.html'):
    fig = px.scatter_geo(
        df,
        lat='latitude',
        lon='longitude',
        size='magnitude',
        color='depth',
        hover_name='title',
        hover_data={
            'magnitude': True,
            'depth': True,
            'latitude': False,
            'longitude': False,
            'url': False  # Optional: don't show
        },
        projection='natural earth',
        title='Earthquake Map (Last Month)',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(geo=dict(showland=True, showcountries=True))
    fig.write_html(output_html)
