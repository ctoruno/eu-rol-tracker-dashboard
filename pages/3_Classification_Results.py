"""
Project:        EU ROL Tracker Dashboard
Module Name:    Classification Page
Author:         Carlos Alberto Toruño Paniagua
Creation Date:  November 4th, 2024
Description:    This module contains the code of the Classification Results tab for the EU ROL Tracker Dashboard
"""

import numpy as np
import pandas as pd
import streamlit as st
from tools import chord
from tools import data_viz as viz

# Initializing session states fpr country data
if "country_track" not in st.session_state:
    st.session_state["country_track"] = False

def update_tracking(button_name):
    st.session_state[button_name] = True

# Page config
st.set_page_config(
    page_title = "Classification",
    page_icon  = ":material/monitoring:"
)

# Reading CSS styles
with open("styles.css") as stl:
    st.markdown(f"<style>{stl.read()}</style>", 
                unsafe_allow_html=True)

# Header and explanation
st.markdown("<h1 style='text-align: center;'>Media Reports</h1>", 
            unsafe_allow_html=True)
st.markdown(
    """
    <p class='jtext'>
    Welcome to the <strong style="color:#003249">Media Reports tab</strong>. In this page you can search and
    visualize the results a massive webscrapping exercise of newspapers for each of the 27 active members of
    the European Union. To visualize the results, you need to first select a country in order to load the data.
    Once the data is loaded, you will have to search for specific keywords and/or pillars of interest. The
    search tool will list all of the articles that matched your search.
    </p>
    """,
    unsafe_allow_html = True
)

# Country selection
country_selec = st.form("country_selection")
with country_selec:
    country = st.selectbox(
        "Select a country from the list below:",
        [
            "Austria",
            "Belgium",
            "Bulgaria",
            "Croatia",
            "Cyprus",
            "Czechia",
            "Denmark",
            "Estonia",
            "Finland",
            "France",
            "Germany",
            "Greece",
            "Hungary",
            "Ireland",
            "Italy",
            "Latvia",
            "Lithuania",
            "Luxembourg",
            "Malta",
            "Netherlands",
            "Poland",
            "Portugal",
            "Romania",
            "Slovakia",
            "Slovenia",
            "Spain",
            "Sweden"
        ]
    )
    submitted = st.form_submit_button("Load the data!!")
    if submitted:
        update_tracking("country_track")

if st.session_state["country_track"]:

    st.markdown(f"<h2>{country}</h2>", unsafe_allow_html = True)

    # Loading data
    country_data = pd.read_parquet(f"data/news-data/{country}_master.parquet.gzip")
    country_data["published_date"] = pd.to_datetime(country_data['published_date'])
    country_data["impact_score_text"] = (
        country_data["impact_score"].map(
            { 
                0 : "Undefined",
                1 : "Very Negative",
                2 : "Negative",
                3 : "Neutral",
                4 : "Positive",
                5 : "Very Positive",
            }
        )
    )
    country_data["week_start"] = (
        country_data["published_date"]
        .dt.to_period("W")
        .apply(lambda x: x.start_time)
    )
    country_data["week_start"] = country_data["week_start"].dt.date


    summary_per_pillar = (
        country_data.copy()
        .loc[country_data["impact_score"] > 0]
        .groupby(["associated_pillar", "impact_score", "impact_score_text"])
        .agg(n_articles=("id", "count"))
        .reset_index()
    )
    summary_per_pillar["pillar_order"] = summary_per_pillar["associated_pillar"].replace({
        "Pillar 1": 1, 
        "Pillar 2": 2,
        "Pillar 3": 3,
        "Pillar 4": 4,
        "Pillar 5": 5,
        "Pillar 6": 6,
        "Pillar 7": 7,
        "Pillar 8": 8
    })
    summary_per_pillar["share"] = (summary_per_pillar["n_articles"] / summary_per_pillar.groupby("associated_pillar")["n_articles"].transform("sum"))*100
    summary_per_pillar_sorted = summary_per_pillar.sort_values(["pillar_order", "impact_score"], ascending=[True, False])

    nrows     = len(country_data.drop_duplicates(subset='id'))
    nrows_fmt = "{:,}".format(nrows)

    st.markdown(
        f"""
        A total of {nrows_fmt} articles were read and classified by the Large Language Model along with a in-depth description of
        the <a href="https://ctoruno.github.io/eu-rol-tracker/#conceptual-framework1" target="_blank">conceptual framework 
        used in this pilot project</a>. During a <a href="https://ctoruno.github.io/eu-rol-tracker/#first-stage-broad-classification"
        target="_blank">first stage</a>, the model was tasked to do a wide classification to distinguish news articles related
        to our conceptual framework, from those that were unrelated. During a <a href="https://ctoruno.github.io/eu-rol-tracker/#second-stage-pillar-classification"
        target="_blank">second stage</a>, the model was asked to further classify news articles into the specific pillars
        that the news article was related to.

        The thematic pillars are:

        - Pillar 1: Constraints on Government Powers
        - Pillar 2: Abscense of Corruption
        - Pillar 3: Open Government
        - Pillar 4: Fundamental Freedoms
        - Pillar 5: Order & Security
        - Pillar 6: Regulatory Enforcement
        - Pillar 7: Civil Justice
        - Pillar 8: Criminal Justice
        
        The model was also asked to assign an impact score based on how would the events narrated in the news article affect
        the specific pillar. The results of the second stage classification for {country} are shown below:
        """,
        unsafe_allow_html = True
    )

    bars, tabs1 = st.tabs(["Chart", "Table"])

    with bars:
        infobars = viz.infobars(summary_per_pillar_sorted)
        st.plotly_chart(infobars, config = {"modeBarButtonsToRemove": ["select", "lasso"]})

    with tabs1:
        st.dataframe(
            summary_per_pillar_sorted[["associated_pillar", "impact_score_text", "n_articles", "share"]], 
            use_container_width=True,
            hide_index=True
        )
    
    summary_per_week = (
        country_data.copy()
        .loc[country_data["impact_score"] > 0]
        .drop_duplicates(subset = "id")
        .groupby(["week_start", "impact_score", "impact_score_text"])
        .agg(n_articles=("id", "count"))
        .reset_index()
    )
    summary_per_week_sorted = summary_per_week.sort_values(["week_start", "impact_score"])
    summary_pw = (
        summary_per_week_sorted.copy()
        .groupby(["week_start"])
        .agg(
            n_articles = ("n_articles", "sum")
        )
        .reset_index()
    )
    max_week = summary_pw.loc[summary_pw["n_articles"] == np.max(summary_pw["n_articles"]), "week_start"].iloc[0].strftime("%B %d, %Y")
    max_arts_week = np.max(summary_pw["n_articles"])
    avg_arts_week = np.mean(summary_pw["n_articles"])

    st.markdown(
        f"""
        We can also track the evolution of news articles over time. For the specific case of <b>{country}</b>,
        the tracker was able to detect an average of <b>{round(avg_arts_week)}</b> articles per week. 
        Being <b>{max_week}</b> the week with the highest number of articles recorded with a total of 
        <b>{max_arts_week}</b> articles. You can visualize the evolution of articles by associated impact
        in the chart below:
        """,
        unsafe_allow_html = True
    )

    sliderline = viz.sliderline(summary_per_week_sorted)
    st.plotly_chart(sliderline, config = {"modeBarButtonsToRemove": ["select", "lasso"]})

    st.markdown(
        f"""
        <br>
        During the classification stage, a single news article can be associated to multiple thematic pillars. 
        Therefore, it is very important to analyze the co-occurences found by the AI. As a general rule, Pillar 1 
        "Constraints on Government Powers", Pillar 4 "Fundamental Freedoms", and Pillar 8 "Criminal Justice" usually
        present strong co-occurence with all the other thematic pillars. You can explore the co-occurence between pillars
        through thre different visualizations below:
        <br><br>
        """,
        unsafe_allow_html = True
    )

    chord_chart, heat, tabs2 = st.tabs(["Chord", "Heatmap", "Table"])

    subset4cooc = (
        country_data.copy()
        .drop_duplicates(subset="id")
        .loc[:,["pillar_1", "pillar_2", "pillar_3", "pillar_4", "pillar_5", "pillar_6", "pillar_7", "pillar_8"]]
    )
    co_occurence_matrix = subset4cooc.T.dot(subset4cooc)
    total_sum = co_occurence_matrix.sum()
    co_occurrence_percentage = (co_occurence_matrix / total_sum) * 100

    with chord_chart:
        co_occurence_matrix.columns = ["Pillar 1", "Pillar 2", "Pillar 3", "Pillar 4", "Pillar 5", "Pillar 6", "Pillar 7", "Pillar 8"]
        co_occurence_matrix.index   = ["Pillar 1", "Pillar 2", "Pillar 3", "Pillar 4", "Pillar 5", "Pillar 6", "Pillar 7", "Pillar 8"] 
        co_occurence = chord.make_filled_chord(
            co_occurence_matrix,
            ideo_colors=["#001B2E", "#294C60", "#ADB6C4", "#FFE9C2", "#721121", "#FFC49B", "#434A42", "#806D40", ]
        )
        st.plotly_chart(co_occurence, config = {"modeBarButtonsToRemove": ["select", "lasso"]})
    with heat:
        heatmap = viz.heatmap(co_occurrence_percentage)
        st.plotly_chart(heatmap)
    with tabs2:
        st.write(co_occurrence_percentage)
    
    

    
    

    
