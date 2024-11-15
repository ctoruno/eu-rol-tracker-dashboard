"""
Project:        EU ROL Tracker Dashboard
Module Name:    Frequency Analysis Page
Author:         Carlos Alberto Toruño Paniagua
Creation Date:  November 11th, 2024
Description:    This module contains the code of the Frequency Analysis tab for the EU ROL Tracker Dashboard
"""

import spacy
import numpy as np
import pandas as pd
import streamlit as st
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
st.markdown("<h1 style='text-align: center;'>Frequency Analysis</h1>", 
            unsafe_allow_html=True)
st.markdown(
    """
    <p class='jtext'>
    Welcome to the <strong style="color:#003249">Frequency Analysis tab</strong>. This page is dedicated to
    dive and explore the most frequent terms and entities that were mentioned in the news articles that were 
    classified by the AI. You can omit certain words from the analysis by adding them to the stopwords
    list bellow. Additionally, feel free to use a Term Frequency-Inverse Document Frequency (TF-IDF) weighting
    scheme to analyse the frequencies of terms and entities.
    </p>

    <p class='jtext'>
    Don't forget to click on the <b>Load the data!!</b> button after selecting a country.
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
    stopwords = st.text_area(
        "Custom list of words to omit during the analysis (stopwords):",
        value = f"{country.lower()} say day old year new come",
        help  = "Feel free to customize these stopwords depending on the country."
    )
    tfidf = st.toggle(
        "Would you like to adjust frequencies using a TF-IDF weighting scheme?",
        value = True,
        help = """
        Term Frequency-Inverse Document Frequency (TF-IDF) is a technique used in text 
        mining to measure the importance of a word within a document relative to a 
        collection of documents (known as a corpus).
        """
    )
    submitted = st.form_submit_button("Load the data!!")
    if submitted:
        update_tracking("country_track")

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
    country_data["week_start"] = (
        country_data["published_date"]
        .dt.to_period("W")
        .apply(lambda x: x.start_time)
    )
    country_data["week_start"] = country_data["week_start"].dt.date

    # Adding customized stopwords
    stopwords_full = stopwords.split() + [
        "man", "time", "want", "case", "take", "continue", "end", "woman", "call", "come", "example", "long",
        "austrian", "belgian", "bulgarian", "croatian", "cypriot", "czech",  "danish", "estonian", "finnish", 
        "french", "german", "greek", "hungarian", "irish", "italian", "latvian", "lithuanian", "luxembourgish", 
        "maltese", "dutch", "polish", "portuguese", "romanian", "slovak", "slovene", "spanish", "swedish"
    ]

    # Most frequent terms
    st.markdown(f"<h3>Most frequent terms used in news data</h3>", unsafe_allow_html = True)

    overview1, wordcloud1 = st.tabs(["Overview", "By Pillar"])

    with overview1:

        top_terms_by_pillar = {}
        for pil in ["Pillar 1", "Pillar 2", "Pillar 3", "Pillar 4", "Pillar 5", "Pillar 6", "Pillar 7", "Pillar 8"]:
            texts = country_data[country_data["associated_pillar"] == pil].cleaned_text     
            if tfidf:       
                vectorizer = TfidfVectorizer(
                    stop_words   = stopwords_full, 
                    max_features = 25
                )
            else:
                vectorizer = CountVectorizer(
                    stop_words   = stopwords_full, 
                    max_features = 25
                )
            top_words_vector = vectorizer.fit_transform(texts)            
            term_frequencies = top_words_vector.sum(axis=0).A1
            terms            = vectorizer.get_feature_names_out()            
            top_terms        = sorted(zip(terms, term_frequencies), key=lambda x: x[1], reverse=True)
            top_terms_by_pillar[pil] = [term for term, _ in top_terms]

        top_terms_df = pd.DataFrame(top_terms_by_pillar)
        st.dataframe(
            top_terms_df, 
            hide_index=True,
            use_container_width=True
        )
    
    with wordcloud1:

        wordcloud1_col1, wordcloud1_col2 = st.columns([1,3])

        # Pillar selection for wordcloud
        with wordcloud1_col1: 
            wordcloud_options = st.form("wordcloud_options_1")
            with wordcloud_options:

                pillar_w1 = st.selectbox(
                    "Select a thematic pillar from the list bellow:",
                    ["Pillar 1", "Pillar 2", "Pillar 3", "Pillar 4", "Pillar 5", "Pillar 6", "Pillar 7", "Pillar 8"]
                )
                pillar_subset = (
                    country_data.copy()
                    .loc[country_data["associated_pillar"] == pillar_w1]
                )
                submitted_wordcloud_w1 = st.form_submit_button("Show me the results!!")

        # Pillar Results
        with wordcloud1_col2:
            if submitted_wordcloud_w1:

                preproc_texts = pillar_subset["cleaned_text"]
                if tfidf:       
                    vectorizer = TfidfVectorizer(
                        stop_words = stopwords_full
                    )
                else:
                    vectorizer = CountVectorizer(
                        stop_words = stopwords_full
                    )
                freqmatrix   = vectorizer.fit_transform(preproc_texts)
                scores       = dict(zip(vectorizer.get_feature_names_out(), freqmatrix.sum(axis=0).tolist()[0]))
                wordcloud_1  = viz.wordcloud(scores, freqs = True)
                
                st.markdown("<h4>Most frequent terms used in this Pillar</h4>", unsafe_allow_html = True)
                st.pyplot(wordcloud_1, use_container_width=True)

                top_terms_by_sentiment = {}
                for sent in ["Very Positive", "Positive", "Neutral", "Negative", "Very Negative"]:
                    texts = pillar_subset[pillar_subset["impact_score_text"] == sent].cleaned_text     
                    if tfidf:       
                        vectorizer = TfidfVectorizer(
                            stop_words   = stopwords_full, 
                            max_features = 25
                        )
                    else:
                        vectorizer = CountVectorizer(
                            stop_words   = stopwords_full, 
                            max_features = 25
                        )
                    top_words_vector = vectorizer.fit_transform(texts)            
                    term_frequencies = top_words_vector.sum(axis=0).A1
                    terms            = vectorizer.get_feature_names_out()            
                    top_terms        = sorted(zip(terms, term_frequencies), key=lambda x: x[1], reverse=True)
                    top_terms_by_sentiment[sent] = [term for term, _ in top_terms]

                top_terms_df = pd.DataFrame(top_terms_by_sentiment)
                st.markdown("<h4>Most frequent terms used in this Pillar by associated impact</h4>", unsafe_allow_html = True)
                st.dataframe(
                    top_terms_df, 
                    hide_index=True,
                    use_container_width=True
                )

    st.markdown("----")

    # Most frequent entities
    st.markdown(f"<h3>Most frequent entities mentioned in news data</h3>", unsafe_allow_html = True)

    overview2, wordcloud2 = st.tabs(["Overview", "By Pillar"])

    with overview2:

        top_entities_by_pillar = {}
        for pil in ["Pillar 1", "Pillar 2", "Pillar 3", "Pillar 4", "Pillar 5", "Pillar 6", "Pillar 7", "Pillar 8"]:
            ents = country_data[country_data["associated_pillar"] == pil].entities
            if tfidf:       
                vectorizer = TfidfVectorizer(
                    stop_words   = stopwords_full, 
                    max_features = 25
                )
            else:
                vectorizer = CountVectorizer(
                    stop_words   = stopwords_full, 
                    max_features = 25
                )
            top_entities_vector = vectorizer.fit_transform(ents)            
            ents_frequencies    = top_entities_vector.sum(axis=0).A1
            entities            = vectorizer.get_feature_names_out()            
            top_ents            = sorted(zip(entities, ents_frequencies), key=lambda x: x[1], reverse=True)
            top_entities_by_pillar[pil] = [ent for ent, _ in top_ents]

        top_ents_df = pd.DataFrame(top_entities_by_pillar)
        st.dataframe(
            top_ents_df, 
            hide_index=True,
            use_container_width=True
        )
    
    with wordcloud2:

        wordcloud2_col1, wordcloud2_col2 = st.columns([1,3])

        # Pillar selection for wordcloud
        with wordcloud2_col1: 
            wordcloud_options = st.form("wordcloud_options_2")
            with wordcloud_options:

                pillar_w2 = st.selectbox(
                    "Select a thematic pillar from the list bellow:",
                    ["Pillar 1", "Pillar 2", "Pillar 3", "Pillar 4", "Pillar 5", "Pillar 6", "Pillar 7", "Pillar 8"]
                )
                pillar_subset = (
                    country_data.copy()
                    .loc[country_data["associated_pillar"] == pillar_w2]
                )
                submitted_wordcloud_w2 = st.form_submit_button("Show me the results!!")

        # Pillar Results
        with wordcloud2_col2:
            if submitted_wordcloud_w2:

                entities = pillar_subset["entities"]
                if tfidf:       
                    vectorizer = TfidfVectorizer(
                        stop_words   = stopwords_full
                    )
                else:
                    vectorizer = CountVectorizer(
                        stop_words   = stopwords_full
                    )
                freqmatrix_ents = vectorizer.fit_transform(entities)
                scores_ents     = dict(zip(vectorizer.get_feature_names_out(), freqmatrix_ents.sum(axis=0).tolist()[0]))
                wordcloud_2     = viz.wordcloud(scores_ents, freqs = True)
                
                st.markdown("<h4>Most frequent entities mentioned in this Pillar</h4>", unsafe_allow_html = True)
                st.pyplot(wordcloud_2, use_container_width=True)

                top_ents_by_sentiment = {}
                for sent in ["Very Positive", "Positive", "Neutral", "Negative", "Very Negative"]:
                    ents = pillar_subset[pillar_subset["impact_score_text"] == sent].entities     
                    if tfidf:       
                        vectorizer = TfidfVectorizer(
                            stop_words   = stopwords_full, 
                            max_features = 25
                        )
                    else:
                        vectorizer = CountVectorizer(
                            stop_words   = stopwords_full, 
                            max_features = 25
                        )
                    top_ents_vector  = vectorizer.fit_transform(ents)            
                    ents_frequencies = top_ents_vector.sum(axis=0).A1
                    entities         = vectorizer.get_feature_names_out()            
                    top_ents         = sorted(zip(entities, ents_frequencies), key=lambda x: x[1], reverse=True)
                    top_ents_by_sentiment[sent] = [term for term, _ in top_ents]

                top_ents_df = pd.DataFrame(top_ents_by_sentiment)
                st.markdown("<h4>Most frequent entities mentioned in this Pillar by associated impact</h4>", unsafe_allow_html = True)
                st.dataframe(
                    top_ents_df, 
                    hide_index=True,
                    use_container_width=True
                )
