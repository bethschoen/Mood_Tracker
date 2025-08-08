import streamlit as st
from typing import Union
import numpy as np

def display_tags(tags: list, tag_colours: dict):
    """
    Given a list of tags, present them in the app using HTML
    Parameters
    ----------
    tags: list
        Tags to present
    tag_colours: dict
        Colours associated to the tag

    Returns
    -------
    str
        html for tags
    """
    tag_html = ""
    for tag in tags:
        colour = tag_colours.get(tag, "#e0e0e0")  # Default color if tag not in dictionary
        tag_html += f'<span style="background-color:{colour};color:#FFFFFF;border-radius:5px;padding:5px;margin:2px;display:inline-block;">{tag}</span>'
    #st.markdown(tag_html, unsafe_allow_html=True)

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

    for list_of_buttons in list_of_grouped_buttons:
        total_len = sum([len(i) for i in list_of_buttons])
        ratios = [np.sqrt(len(i)/total_len) for i in list_of_buttons]
        button_cols = st.columns(ratios)
        for i, tag in enumerate(list_of_buttons, start=0):
            with button_cols[i]:
                if st.button(tag, key=tag, use_container_width=True):
                    selected_tags.add(tag)

    return selected_tags