"""
Project:        EU ROL Tracker Dashboard
Module Name:    Search Page
Author:         Carlos Alberto Toruño Paniagua
Creation Date:  November 2nd, 2024
Description:    This module contains the code of the Search Engine tab for the EU ROL Tracker Dashboard
"""

import json
import re
import pandas as pd
import streamlit as st
import streamlit.components.v1 as stc

if "country_track" not in st.session_state:
    st.session_state["country_track"] = False
if "search_track" not in st.session_state:
    st.session_state["search_track"] = False

def update_tracking(button_name):
    st.session_state[button_name] = True

# Page config
st.set_page_config(
    page_title = "Search",
    page_icon  = ":material/database:"
)

# Reading CSS styles
with open("styles.css") as stl:
    st.markdown(f"<style>{stl.read()}</style>", 
                unsafe_allow_html=True)

# Header and explanation
st.markdown("<h1 style='text-align: center;'>Search Engine</h1>", 
            unsafe_allow_html=True)
st.markdown(
    """
    <p class='jtext'>
    Welcome to the <strong style="color:#003249">Search Engine</strong>. In this page you can search and
    visualize the results a massive webscrapping exercise of newspapers for each of the 27 active members of
    the European Union.
    </p>
    <p class='jtext'>
    To visualize the results, you need to first select a country in order to access the country database.
    Once the data is loaded, you will have to search for specific keywords of interest. Below, you can find
    a few example on how to use the keywords input box to narrow your results.
    </p>
    <p class='jtext'>
    Finally, due to the massive size
    volume of the data, you also need to filter down your query to a specific thematic pillar and an associated
    sentiment. Once you are ready, click on <b>SEARCH</b> to see the list of articles that matched your search.
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

    search_engine = st.container()
    with search_engine:
        st.markdown(
            "<h4>Search articles based on:</h4>", 
            unsafe_allow_html = True
        )
        with st.expander("Click here to see examples on how to use the Search Engine"):
            st.markdown(
                """
                <i>The search engine supports Regular Expressions when searching for keywords. See the following examples:</i>
                - <i>If you want to search for articles containing the words "European" OR "funds", meaning that you only need ONE of 
                these words to appear in the article, you can type</i>:
                ```
                European|funds
                ```

                - <i>If you want to search for articles containing BOTH words "European" AND "funds" (but not necessarily together), 
                you can type</i>:
                ```
                \\bEuropean\\b.*\\bfunds\\b|\\bfunds\\b.*\\bEuropean\\b
                ```

                - <i>If you want to search for articles containing an exact match of "European funds", you can type</i>:
                ```
                \\bEuropean\\s+funds\\b
                ```
                """, 
                unsafe_allow_html = True
            )
        keywords = st.text_input("The following keywords:")
        assoc_pillar = st.selectbox(
            "Limit the search to a specific pillar",
            ["Pillar "+str(n) for n in range(1,9)]
        )
        assoc_sentiment = st.selectbox(
            "Limit the search to a specific sentiment",
            ["Very Positive", "Positive", "Neutral", "Negative", "Very Negative"]
        )
        search_button = st.button("Search")

    if search_button:

        session_state = True

        # Transforming keywords
        keys = []
        keywords = re.sub(" OR ", "|", keywords)
        for key in keywords.split():
            regexkey = f"(?=.*{key})"
            keys.append(regexkey)
        keys = "^" + "".join(keys)
        
        # Filtering results
        filtered_data = (
            country_data.copy()
            .loc[(country_data["associated_pillar"] == assoc_pillar) & (country_data["impact_score_text"] == assoc_sentiment)]
        )
        results = filtered_data[filtered_data["summary"].str.contains(keys, case = False)]

        # Success Box
        nresults = len(results.index)
        st.success(f"Your search returned {nresults} results.")

        for index, row in results.iterrows():

            with st.container():
                title   = row["title_trans"]
                sumdesc = row["summary"]
                body    = row["content_trans"]
                score   = row["impact_score_text"]
                date    = row["published_date"].strftime("%B %d, %Y")
                source  = row["domain_url"]
                link    = row["link"]

                variable_html_layout = f"""
                                    <div>
                                        <h4>{title}</h4>
                                        <p class='jtext'><strong>Summary:</strong></p>
                                        <p class='vdesc'>{sumdesc}</h4>
                                        <br>
                                        <div class="row">
                                            <div class="column">
                                                <p class='jtext'><strong>Source:</strong> {source}</p>
                                            </div>
                                            <div class="column">
                                                <p class='jtext'><strong>Publishing date:</strong> {date}</p>
                                            </div> 
                                        </div>
                                        <div class="row">
                                            <div class="column">
                                                <p class='jtext'><strong>Impact score:</strong> {score}</p>
                                            </div>
                                            <div class="column">
                                                <p class='jtext'><strong>URL:</strong>
                                                    <a href='{link}' target='_blank'>Click here to open in a new tab</a>
                                                </p>
                                            </div> 
                                        </div>
                                    </div>
                                    """
            
                st.markdown(variable_html_layout, unsafe_allow_html = True)
                with st.expander("Full content"):
                    stc.html(body, scrolling = True)
                
                st.markdown("---")