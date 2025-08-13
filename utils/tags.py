import streamlit as st
from typing import Union
import numpy as np
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..')))

import variables as vr

def access_mood_color_v1(mood: str) -> str:       

    #TODO: error handling
    # - check mood data in session state
    # - check mood in mood data

    mood_df = st.session_state["mood_data"]
    # get colour name
    color_str = mood_df[mood_df[vr.mood_col_name] == mood][vr.color_col_name].iloc[0]
    # get colour html
    color = vr.mood_colors_v1.get(color_str, "#e0e0e0")

    return color

def access_mood_color(mood: str) -> str:       

    #TODO: error handling
    # - check mood data in session state
    # - check mood in mood data

    mood_df = st.session_state["mood_data"]
    # get colour name
    color_str = mood_df[mood_df[vr.mood_col_name] == mood][vr.color_col_name].iloc[0]
    # get sentiment
    sentiment = mood_df[mood_df[vr.mood_col_name] == mood][vr.sentiment_col_name].iloc[0]
    # get colour html
    color_info = vr.mood_colors_v2.get(sentiment, {}).get(color_str, {})
    background_color = color_info.get("background", "#e0e0e0")
    text_color = color_info.get("text", "#2F4F4F")

    return (background_color, text_color)

def create_mood_tags(tags: list, display:bool=True):
    """
    Given a list of moods, present them in the app using HTML
    Parameters
    ----------
    tags: list
        Tags to present

    Returns
    -------
    str
        html for tags
    """
    tag_html = ""
    for tag in tags:
        background_color, text_color = access_mood_color(tag)
        tag_html += f'<span style="background-color:{background_color};color:{text_color};border-radius:5px;padding:5px;margin:2px;display:inline-block;">{tag}</span>'

    if display:
        st.markdown(tag_html, unsafe_allow_html=True)

    return tag_html

def convert_list_to_bullet_points(l: Union[list, set], quote: bool = False) -> Union[list, str]:
    """
    Some items in the session state will be a list of objects. Convert this into a html bullet point list so that it can displayed in the front end
    Parameters
    ----------
    l: list
        list of objects to be made into bullet points
    quote: bool
        if True, list contains quotes from a text. When creating the bullet point list, add quote marks around each object

    Returns
    -------
    str
        html string defining bullet point list
    list
        if the input was not a list, return the input
    """
    if isinstance(l, list) or isinstance(l, set):
        if quote:
            l = [f"\"{i}\"" for i in l]
        combined_str = "<ul style='padding-left: 20px;'>"
        for item in l:
            combined_str += f"<li style='margin-bottom: 5px;'>{item}</li>"
        combined_str += "</ul>"
        return combined_str
    else:
        return l
    
def create_grid_of_buttons(l: list, selected_tags: set, max_button_chars:int=25, gap_chars:int=3):
    """
    Given a list of items, present them as buttons in a grid
    Parameters
    ----------
    l: list
        Items for which we create buttons
    selected_tags: set
        The existing selection - if we now make additional selections, this'll be appended to selected_tags
    max_buttons_char: int (optional)
        Max number of characters row of buttons - make this smaller to have less buttons per row
    gap_chars: int (optional)
        Number of characters to use in between buttons to space them out a bit
    """

    subset = []
    list_of_grouped_buttons = []
    length = 0
    
    for i, tag in enumerate(l, start=1):
        # if we haven't got any tags in our subset or adding the next element won't cause us to go over the max characters
        if (len(subset) == 0) or ((length + len(tag) + gap_chars) <= max_button_chars):
            subset.append(tag)
            length += len(tag) + gap_chars
        # if the length with the next tag is too long or the line is already too long (due to a long tag)
        elif ((length + len(tag) + gap_chars) > max_button_chars) or length > max_button_chars:
            list_of_grouped_buttons.append(subset)
            # restart with the next tag
            subset = [tag]
            length = len(tag)
        if i == len(l):
            list_of_grouped_buttons.append(subset)

    # iterating through the groups of buttons created
    for list_of_buttons in list_of_grouped_buttons:
        # calculate the desired width of each button on the row
        total_len = sum([len(i) for i in list_of_buttons])
        ratios = [np.sqrt(len(i)/total_len) for i in list_of_buttons]
        # create columns using the calculated ratios
        button_cols = st.columns(ratios)
        for i, tag in enumerate(list_of_buttons, start=0):
            with button_cols[i]:
                # create button
                # (I had tried to use the colour as a key so that we can customise buttons with the same colour, but streamlit wants key to be unique for each element)
                if st.button(tag, key=tag, use_container_width=True):
                    selected_tags.add(tag)

    return selected_tags