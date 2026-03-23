import pandas as pd

df = pd.read_csv("data/history_analysis.csv")

metrics = ["languages_count", "aliases_count", "extensions_count", "filenames_count"]
others = [m for m in df[metrics].iloc[-1].sort_values(ascending=False).index if m != "languages_count"]
metrics_sorted = ["languages_count"] + others

colors = {"languages_count": "#E63946", "aliases_count": "#2A9D8F", "extensions_count": "#E9C46A", "filenames_count": "#457B9D"}
titles = {"languages_count": "Languages", "aliases_count": "Aliases", "extensions_count": "Extensions", "filenames_count": "Filenames"}

from plotly.subplots import make_subplots
import plotly.graph_objects as go

legend_sorted = sorted(metrics_sorted, key=lambda m: df[m].iloc[-1], reverse=True)

fig = make_subplots(
    rows=3, cols=2,
    specs=[[{"colspan": 2}, None], [{}, {}], [{}, {}]],
    subplot_titles=["All Metrics"] + [titles[m] for m in metrics_sorted],
    row_heights=[0.5, 0.25, 0.25],
    vertical_spacing=0.08,
)

# First chart: all 4 metrics (legend order = sorted by last value)
for metric in legend_sorted:
    fig.add_trace(
        go.Scatter(x=df["version"], y=df[metric], line=dict(width=3, color=colors[metric]), name=titles[metric]),
        row=1, col=1,
    )
fig.update_xaxes(tickangle=45, nticks=20, row=1, col=1)

# Individual charts
for i, metric in enumerate(metrics_sorted):
    row, col = divmod(i, 2)
    fig.add_trace(
        go.Scatter(x=df["version"], y=df[metric], line=dict(width=3, color=colors[metric]), name=titles[metric], showlegend=False),
        row=row + 2, col=col + 1,
    )
    fig.update_xaxes(tickangle=45, nticks=20, row=row + 2, col=col + 1)

fig.update_layout(title="History of Languages Known to GitHub (2012 to today, source: GitHub Linguist)", width=1400, height=1600, font=dict(size=17))
fig.write_image("history-chart.png")
fig.show()