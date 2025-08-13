import streamlit as st
from streamlit_calendar import calendar
import pandas as pd
import json
import sys
import os
from datetime import datetime, timedelta
import pathlib
current_dir = os.path.dirname(__file__)
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

import variables as vr

def create_styles_file():
    """
    THIS WILL OVERWRITE THE ENTIRE FILE so make sure nothing has been hard coded in there
    """
    style_file = os.path.join(root_dir, vr.style_dir)
    # empty the file
    open(style_file, 'w').close()

    # read csv data
    mood_data_path = os.path.join(root_dir, vr.data_dir, vr.mood_data_filename)
    mood_df = pd.read_csv(mood_data_path)

    # join to colours in variables
    background_color_html_col_name = "background_color_html"
    text_color_html_col_name = "text_color_html"
    mood_df[background_color_html_col_name] = mood_df.apply(lambda row: vr.mood_colors_v2.get(row[vr.sentiment_col_name], {}).get(row[vr.color_col_name], {}).get("background", "#e0e0e0"), axis=1)
    mood_df[text_color_html_col_name] = mood_df.apply(lambda row: vr.mood_colors_v2.get(row[vr.sentiment_col_name], {}).get(row[vr.color_col_name], {}).get("text", "#e0e0e0"), axis=1)
    mood_dict = mood_df[[vr.mood_col_name, background_color_html_col_name, text_color_html_col_name]].set_index(vr.mood_col_name).to_dict(orient="index")

    # create css entry for mood and colour
    for mood, color in mood_dict.items():
        css_string = f"""
.st-key-{mood} button {{
    background-color: {color[background_color_html_col_name]};
    color: {color[text_color_html_col_name]};
}}
"""
        # write to file
        with open(style_file, "a") as myfile:
            myfile.write(css_string)

if __name__ == "__main__":
    create_styles_file()

