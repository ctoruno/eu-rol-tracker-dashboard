"""
Project:        EU ROL Tracker Dashboard
Module Name:    Data Viz Tools
Author:         Carlos Alberto Toruño Paniagua
Creation Date:  November 4th, 2024
Description:    This module contains the code for the different data viz used in the app
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def dynamic_pie(data):

    fig = px.sunburst(
        data, 
        path   = ["associated_pillar", "impact_score_text"], 
        values = "n_articles",
        color  = "associated_pillar",
        color_discrete_map = {
            "Pillar 1": "#292929", 
            "Pillar 2": "#ECCBAE",
            "Pillar 3": "#046C9A",
            "Pillar 4": "#FFB35C",
            "Pillar 5": "#ABDDDE",
            "Pillar 6": "#00A08A",
            "Pillar 7": "#D08F39",
            "Pillar 8": "#FF0000"
        },
        custom_data = ["associated_pillar", "impact_score_text", "n_articles", "share"]
    )
    fig.update_traces(
        sort = False,
        insidetextorientation = "radial",
        hovertemplate = (
            "<b>%{customdata[0]}</b><br>" +
            "<i>%{customdata[1]}</i><br>" +
            "No. of articles: %{customdata[2]}<br>" +
            "Share: %{customdata[3]:.1f}%"
        ),
        hoverlabel = dict(
            font_size   = 15,
            font_family = "Lato"
        )
    )
    fig.add_annotation(
        showarrow = False,
        text = "<i>Click on a pillar to enlarge or bring down the results</i>",
        x    = 0.5,
        y    = -0.1
        )
    
    return fig

def infobars(data):
    fig = px.bar(
        data,
        x = "n_articles",
        y = "associated_pillar",
        color = "impact_score_text",
        color_discrete_map = {
            "Very Positive" : "#046C9A",
            "Positive"      : "#00A08A",
            "Neutral"       : "#F7EADE",
            "Negative"      : "#FFB35C",
            "Very Negative" : "#FF0000"
        },
        title = "Second Stage Classification Results",
        orientation = "h",
        labels = {
            "n_articles": "<i>No. of articles</i>"
        },
        custom_data = ["associated_pillar", "impact_score_text", "n_articles", "share"]
    )
    fig.update_layout(
        yaxis_title = None, 
        legend_title_text = "<i>Associated Impact</i>",
        hoverlabel = dict(
            font_size   = 15,
            font_family = "Lato"
        ),
        template = "plotly_white"
    )
    fig.update_traces(
        hovertemplate = (
            "<b>%{customdata[0]}</b><br>" +
            "<i>%{customdata[1]}</i><br>" +
            "No. of articles: %{customdata[2]}<br>" +
            "(%{customdata[3]:.1f}%)"
        )
    )
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)

    return fig

def sliderline(df):

    # Check the following tutorial: https://blog.stackademic.com/bringing-data-to-life-crafting-animated-timeline-graphs-from-dust-0cbb40ff8737

    df_indexed = pd.DataFrame()
    for index in np.arange(
        start = 0,
        stop  = len(df)+1,
        step  = df["impact_score_text"].nunique()
    ):
        df_slicing = df.iloc[:index].copy()
        df_slicing["frame"] = (index//df["impact_score_text"].nunique())
        df_indexed = pd.concat([df_indexed, df_slicing])

    scatter_plot = px.scatter(
        df_indexed, 
        x               = "week_start", 
        y               = "n_articles", 
        color           = "impact_score_text", 
        animation_frame = "frame",
        color_discrete_map = {
            "Very Positive" : "#046C9A",
            "Positive"      : "#00A08A",
            "Neutral"       : "#F7EADE",
            "Negative"      : "#FFB35C",
            "Very Negative" : "#FF0000"
        },
    )

    for frame in scatter_plot.frames:
        for data in frame.data:
            data.update(mode       = "markers",
                        showlegend = True,
                        opacity    = 1)
            data["x"] = np.take(data["x"], [-1])
            data["y"] = np.take(data["y"], [-1])

    line_plot = px.line(
        df_indexed, 
        x               = "week_start", 
        y               = "n_articles", 
        color           = "impact_score_text", 
        animation_frame = "frame",
        color_discrete_map = {
            "Very Positive" : "#046C9A",
            "Positive"      : "#00A08A",
            "Neutral"       : "#F7EADE",
            "Negative"      : "#FFB35C",
            "Very Negative" : "#FF0000"
        },
        line_shape = "spline"
    )
    line_plot.update_traces(showlegend=False)  

    for frame in line_plot.frames:
        for data in frame.data:
            data.update(mode = "lines", opacity=0.8, showlegend=False)

    combined_plot = go.Figure(
        data   = line_plot.data + scatter_plot.data,
        frames =[
            go.Frame(
                data = line_plot.data + scatter_plot.data, 
                name = scatter_plot.name
            )
            for line_plot, scatter_plot in zip(line_plot.frames, scatter_plot.frames)
        ],
        layout=line_plot.layout
    )
    combined_plot.update_yaxes(
        gridcolor  = "#7a98cf",
        griddash   = "dot",
        gridwidth  = 0.5,
        linewidth  = 2,
        tickwidth  = 2,
        fixedrange = True
    )
    combined_plot.update_xaxes(
        title_font = dict(size=12),
        linewidth  = 2,
        tickwidth  = 2,
        fixedrange = True
    )
    combined_plot.update_traces(
        line   = dict(width = 3),
        marker = dict(size  = 15)
    )

    combined_plot.update_layout(
        font        = dict(size=18),
        yaxis       = dict(tickfont=dict(size=16)),
        xaxis       = dict(tickfont=dict(size=16)),
        showlegend  = True,
        legend      = dict(title="Associated impact"),
        template    = "simple_white",
        title       = "<b>Evolution of News Articles Over Time </b>",
        yaxis_title = "<b>No. of Articles per week</b>",
        xaxis_title = "<b>Week</b>",
        yaxis_showgrid =True,
        xaxis_range =[
            df_indexed['week_start'].min(),
            df_indexed['week_start'].max()
        ],
        yaxis_range=[
            df_indexed['n_articles'].min()*0.75,
            df_indexed['n_articles'].max()*1.25
        ],
        title_x = 0.5
    )
    combined_plot['layout'].pop("sliders")
    combined_plot.layout.updatemenus[0].buttons[0]['args'][1]['frame']['duration'] = 120
    combined_plot.layout.updatemenus[0].buttons[0]['args'][1]['transition']['duration'] = 50
    combined_plot.layout.updatemenus[0].buttons[0]['args'][1]['transition']['redraw'] = False

    return combined_plot

def heatmap(df):
    array = df.to_numpy()
    fig = px.imshow(
        array, 
        text_auto = ".1f", 
        labels    = dict(color = "Percentage (%)"),
        aspect    = "auto", 
        x         = ["Pillar 1", "Pillar 2", "Pillar 3", "Pillar 4", "Pillar 5", "Pillar 6", "Pillar 7", "Pillar 8"],
        y         = ["Pillar 1", "Pillar 2", "Pillar 3", "Pillar 4", "Pillar 5", "Pillar 6", "Pillar 7", "Pillar 8"]
    )
    fig.update_layout(
        title       = "<b>Percentage of co-occurence between pillars</b>"
    )
    return fig

def wordcloud(input, freqs = True):

    if freqs:
        wordcloud = WordCloud(
            width    = 1000, 
            height   = 500, 
            colormap = "twilight",
            relative_scaling = 0.45,
            background_color = "white"
        ).generate_from_frequencies(input)
    else:
        wordcloud = WordCloud(
            width    = 1000, 
            height   = 500, 
            colormap = "twilight",
            relative_scaling = 0.45,
            background_color = "white"
        ).generate(" ".join(input))

    # Display the word cloud using matplotlib
    plt.figure(figsize = (10, 5))
    plt.imshow(wordcloud, interpolation = "bilinear")
    plt.axis("off")

    return plt