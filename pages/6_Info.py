"""
Project:        EU ROL Tracker Dashboard
Module Name:    Info Page
Author:         Carlos Alberto Toruño Paniagua
Creation Date:  November 4th, 2024
Description:    This module contains the code of the Information tab for the EU ROL Tracker Dashboard
"""

import streamlit as st

# Header and explanation
st.markdown("<h1 style='text-align: center;'>Information</h1>", 
            unsafe_allow_html=True)
st.markdown(
    """
    <b>Author(s):</b> 
    <ul>
        <li>Carlos Alberto Toruño Paniagua</li>
    </ul>

    <h4>Source Code:</h4>
    <p class='jtext'>
    The EU Rule of Law Tracker was programmed entirely in Python using the <a href="https://streamlit.io/" target="_blank">Streamlit</a>
    web framework. The code is publicly available in this 
    <a href="https://github.com/ctoruno/eu-rol-tracker-dashboard" target="_blank">GitHub Repository</a>.
    </p>

    <h4>Disclaimer:</h4>

    <p class='jtext'>
    The information provided in this online tool is for general informational purposes only. While the previously
    stated author(s) strive to provide accurate and up-to-date information, we make no representations or 
    warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability, or 
    availability with respect to the information, products, services, or related data contained in this app 
    for any purpose. Any reliance you place on such information is therefore strictly at your own risk.
    </p>

    <p class='jtext'>
    Please note that the data presented in this online tool <b>SHOULD NOT</B> be taken as official information 
    of any kind. This online tool is a personal project of the previously stated author(s). Every effort is made 
    to keep the tool up and running smoothly but this was a pilot project with a delimited deadline.
    </p>

    <p class='jtext'>
    The inclusion of any links in this online tool does not necessarily imply a recommendation or endorse 
    the views expressed within them.
    </p>

    <h4>License:</h4>
    The EU Rule of Law Tracker is an open-source application that is licensed under the Creative Commons 
    Attribution-NonCommercial 4.0 International license. This means that anyone is free to use, modify, and 
    distribute the software, subject to the terms and conditions of the previously stated license.
    By using this online tool, you acknowledge and agree to be bound by the terms and conditions of the 
    Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) license.
    """,
    unsafe_allow_html = True
)