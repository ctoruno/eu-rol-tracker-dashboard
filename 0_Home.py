"""
Project:        EU ROL Tracker Dashboard
Module Name:    Master app script
Author:         Carlos Alberto Toruño Paniagua
Creation Date:  November 1st, 2024
Description:    This module contains the home page code for the EU ROL Tracker Dashboard
"""

import streamlit as st
import pandas as pd

# Page config
st.set_page_config(
    page_title = "Home",
    page_icon  = "house"
)

# Reading CSS styles
with open("styles.css") as stl:
    st.markdown(f"<style>{stl.read()}</style>", 
                unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>EU Rule of Law Tracker</h1>", 
            unsafe_allow_html=True)
st.markdown(
    """
    <p class='jtext'>
    Welcome to the EU Rule of Law Tracker, a pilot project aimed at systematically tracking, classifying, 
    and analyzing social and political events related to the rule of law across the 27 member states 
    of the European Union. This initiative makes use of news archives and Large Language Models 
    (LLM) in order to produce a systematized database for researchers to assess and validate perceptions 
    on the rule of Law in the targeted countries.
    </p>

    <p class='jtext'>
    For a in-depth description of the conceptual framework; extraction, translation, classification, and
    summarization of the data; or the NLP techniques used in the analysis of the data, please feel free 
    to check the <a href='https://ctoruno.github.io/eu-rol-tracker/' target= '_blank'>Methodological 
    Manuscript in this link</a>.
    </p>

    <p class='jtext'>
    In the <strong style="color:#003249">Media Reports tab</strong> you'll encounter a series of summaries
    produced by AI after organizing, classifying, and summarizing the input data. The results are presented 
    by country, thematic pillar, and sentiment.
    </p>

    <p class='jtext'>
    The <strong style="color:#003249">Classification Results tab</strong> contains general information on the
    distribution of news related to the Rule of Law, Justice, and Governance framework. The classification was 
    entirely done by AI in over 800,000 news articles from 211 newspapers based in EU member states.
    </p>

    <p class='jtext'>
    The <strong style="color:#003249">Frequency Analysis tab</strong> have some interactive tools to dive into
    the most frequent terms and entities mentioned in the news data. Basic NLP techniques like text processing
    and  named entity recognition were used for this analysis.
    </p>

    <p class='jtext'>
    In the <strong style="color:#003249">Search Engine tab</strong> you can search into the app database for
    articles containing specific keywords. Use it to dive into the raw data that was used to produce the media
    reports and analysis used in this tool.
    </p>
    
    <p class='jtext'>
    If you're curious for more details about the app or if you have questions, suggestions or you want to report 
    a bug,  hop on over to the <strong style="color:#003249">Info tab</strong> in the left side bar panel.
    </p>
    """,
    unsafe_allow_html = True
)