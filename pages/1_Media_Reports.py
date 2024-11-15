"""
Project:        EU ROL Tracker Dashboard
Module Name:    Media Reports Page
Author:         Carlos Alberto Toruño Paniagua
Creation Date:  November 2nd, 2024
Description:    This module contains the code of the Media Reportss tab for the EU ROL Tracker Dashboard
"""

import json
import re
import pandas as pd
import streamlit as st

# Initializing session states fpr country data
if "country_track" not in st.session_state:
    st.session_state["country_track"] = False

def update_tracking(button_name):
    st.session_state[button_name] = True

# Page config
st.set_page_config(
    page_title = "Codebooks",
    page_icon  = ":material/bookmarks:",
    layout     = "wide"
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
    submitted = st.form_submit_button("Load the data!!")
    if submitted:
        update_tracking("country_track")

if st.session_state["country_track"]:

    st.markdown(f"<h2>{country}</h2>", unsafe_allow_html = True)

    # Loading data for country
    country_data = pd.read_parquet(f"data/news-data/{country}_master.parquet.gzip")
    with open(f"data/summaries/{country.lower()}.json", "r") as file:
        summary_data = json.load(file)

    # Displaying general information
    sources =  "".join([f"\n\n- <a href='https://{link}' target='_blank'>{link}</a>" for link in country_data["domain_url"].drop_duplicates().to_list()])
    country_data["published_date"] = pd.to_datetime(country_data['published_date'])
    min_date  = min(country_data["published_date"]).strftime("%B %d, %Y")
    max_date  = max(country_data["published_date"]).strftime("%B %d, %Y")
    nrows     = len(country_data.drop_duplicates(subset='id'))
    nrows_fmt = "{:,}".format(nrows)
    st.markdown(
        f"""
        <p class='jtext'>
        Data for <strong style="color:#003249">{country}</strong> was extracted from the following sources:
        {sources}
        </p>
        """,
        unsafe_allow_html = True
    )
    st.markdown(
        f"""
        <p class='jtext'>
        The data for this country spans from <b>{min_date}</b> to <b>{max_date}</b>. For a total of {nrows_fmt} articles.
        </p>

        <p class='jtext'>
        Below, you can find a brief summary of the main issues and events related to each one of the 8 pillars of the Rule of Law. <b>The
        summaries were produced using AI</b>, after the model was presented with the project's theoretical framework. Therefore, 
        please read the summaries carefully.
        </p>

        <p class='jtext'>
        For most countries, the scale of information is massive and it can be overwhelming. Therefore, we suggest reading the general 
        summaries per pillar presented bellow to identify relevant issues of interest. Once you have identified specific issues, feel free 
        to use the <strong style="color:#003249">Search Engine</strong> page.
        </p>
        """,
        unsafe_allow_html = True
    )

    # Generating pillar tabs
    pillar_names = {
        "Pillar 1": "Constraints on Government Powers",
        "Pillar 2": "Absence of Corruption",
        "Pillar 3": "Open Government",
        "Pillar 4": "Fundamental Freedoms",
        "Pillar 5": "Order and Security",
        "Pillar 6": "Regulatory Enforcement",
        "Pillar 7": "Civil Justice",
        "Pillar 8": "Criminal Justice"
    }

    counter = 1
    for tab in st.tabs(["Pillar "+str(n) for n in range(1,9)]):
        with tab:
            tab_name = f"Pillar {counter}"
            st.write(f"## {pillar_names[tab_name]}")
            st.markdown(
                f"""
                <p class='jtext'>
                Below, you will find the most important issues that the Language Model identified as worth to be highlighted 
                regarding the news articles extracted for <strong style="color:#003249">{country}, {tab_name}: {pillar_names[tab_name]}</strong>.
                The summaries displayed below might vary in extention <i>depending on the extent of information extracted for each country</i>.
                </p>
                """,
                unsafe_allow_html = True
            )
            
            # Generating sentiment expanders
            for sentiment, summary in summary_data[tab_name].items():
                with st.expander(sentiment):
                    cleaned_summary = re.sub(r"\* \*\*", "- **", summary)
                    cleaned_summary = re.sub(r"\n\n    ", "\n\n", cleaned_summary)
                    cleaned_summary = re.sub(r"## .*\n", "", cleaned_summary)
                    st.write(cleaned_summary)




        counter = counter + 1

    

