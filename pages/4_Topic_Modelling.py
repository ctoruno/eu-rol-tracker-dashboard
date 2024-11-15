"""
Project:        EU ROL Tracker Dashboard
Module Name:    Frequency Analysis Page
Author:         Carlos Alberto Toruño Paniagua
Creation Date:  November 11th, 2024
Description:    This module contains the code of the Frequency Analysis tab for the EU ROL Tracker Dashboard
"""
import gensim
from gensim import corpora

import numpy as np
import pandas as pd
import streamlit as st
import gensim
from gensim import corpora
import pyLDAvis
import pyLDAvis.gensim
from tools import data_viz as viz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

# Initializing session states fpr country data
if "country_track" not in st.session_state:
    st.session_state["country_track"] = False

def update_tracking(button_name):
    st.session_state[button_name] = True

# Page config
st.set_page_config(
    page_title = "Classification",
    page_icon  = ":material/monitoring:",
    layout     = "wide"
)

# Reading CSS styles
with open("styles.css") as stl:
    st.markdown(f"<style>{stl.read()}</style>", 
                unsafe_allow_html=True)

# Header and explanation
st.markdown("<h1 style='text-align: center;'>Topic Modelling</h1>", 
            unsafe_allow_html=True)
st.markdown(
    """
    <p class='jtext'>
    Welcome to the <strong style="color:#003249">Topic Modelling tab</strong>. Here you can find a tool to apply topic
    modelling techniques to a set of news articles. Topic Modelling techniques help you quickly understand what a large 
    collection of texts are about. Through the use of different algorithms, these techniques group similar words together 
    and identify recurring patterns, which represent topics. These topics are not pre-defined but are discovered 
    automatically based on the words in the text. It's a great way to summarize and organize large amounts of text 
    into meaningful themes, helping us see what's being talked about most often.
    </p>

    <p class='jtext'>
    Don't forget to click on the <b>Show me the results!!</b> button after selecting a country.
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
    pillar = st.selectbox(
        "Select a thematic pillar from the list bellow:",
        ["Pillar 1", "Pillar 2", "Pillar 3", "Pillar 4", "Pillar 5", "Pillar 6", "Pillar 7", "Pillar 8"]
    )
    num_topics = st.number_input(
        "Please select a predefined number of topics:",
        min_value = 1,
        max_value = 15,
        value     = 4,
        help      = """
        Start with 4 topics as the predefined value and then adjust the number of topics depending on your results.
        """ 
    )
    sentiments = st.multiselect(
        "(Optional) Please select the sentiment(s) you would like the analysis to focus on:",
        ["Very Positive", "Positive", "Neutral", "Negative", "Very Negative"],
        default = ["Negative", "Very Negative"]
    )
    submitted = st.form_submit_button("Show me the results!!")
    if submitted:
        update_tracking("country_track")
    st.markdown(
        """
        <p class='jtext'><i>
        This might take a while, so please be patient while the model prepares the topics and visualizations
        for you.<br>You might also want to close the left panel of the web app to fully visualize the results
        in your screen.
        </i></p>
        """,
        unsafe_allow_html = True
    )
    

if st.session_state["country_track"]:

    st.markdown(f"<h2>{country}</h2>", unsafe_allow_html = True)

    # Loading and subsetting data
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
    pillar_subset = (
        country_data.copy()
        .loc[country_data["associated_pillar"] == pillar]
    )
    if sentiments:
        pillar_subset = pillar_subset.loc[pillar_subset["impact_score_text"].isin(sentiments)]

    # Creating corpora
    input_text = pillar_subset.cleaned_text.to_list()
    tokens     = [text.split() if isinstance(text, str) else text for text in input_text]
    dictionary = corpora.Dictionary(tokens)
    corpus = [dictionary.doc2bow(text) for text in tokens]

    # Train LDA model
    lda_model = gensim.models.ldamodel.LdaModel(
        corpus, 
        num_topics = num_topics, 
        id2word    = dictionary, 
        passes     = 15
    )

    # Visualize the LDA model
    lda = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
    pyLDAvis.save_html(lda, "lda.html")
    with open("./lda.html", "r") as f:
        html_string = f.read()
    st.components.v1.html(
        html_string, 
        width  = 1300, 
        height = 850, 
        scrolling = True
    )

    # st.markdown("----")

    # # Identify the dominant topic for each document
    # doc_topics = [lda_model[doc] for doc in corpus]
    # dominant_topics = []
    # for i, doc_topic in enumerate(doc_topics):
    #     dominant_topic = sorted(doc_topic, key=lambda x: x[1], reverse=True)[0][0]
    #     dominant_topics.append((i, dominant_topic, input_text[i]))

    # # Create a DataFrame with document index, dominant topic, and text
    # df_dominant_topics = pd.DataFrame(dominant_topics, columns=["Doc_ID", "Dominant_Topic", "Text"])

    # # View sample documents for each topic
    # num_samples_per_topic = 5 
    # sampled_docs = df_dominant_topics.groupby("Dominant_Topic").apply(lambda x: x.sample(num_samples_per_topic), include_groups=False)
    # sampled_docs = sampled_docs.reset_index(drop=False)

    # st.dataframe(
    #     sampled_docs, 
    #     hide_index=True,
    #     use_container_width=True
    # )