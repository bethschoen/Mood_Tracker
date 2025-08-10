import streamlit as st
from streamlit_calendar import calendar
import pandas as pd
import json
import sys
import os
from datetime import datetime, timedelta
import pathlib
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..', '..')))

import variables as vr
import utils as ut

def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

def initialise_session_state() -> None:

    if "mood_data" not in st.session_state:
        mood_df = pd.read_csv(os.path.join(vr.data_dir, vr.mood_data_filename))
        st.session_state["mood_data"] = mood_df
    
    ## Assume nothing else is in the session state

        # all moods available for selection
        positive_sentiment_str = "Positive"
        sorted_positive_tags = mood_df[mood_df[vr.sentiment_col_name] == positive_sentiment_str].sort_values(by=[vr.color_int_col_name, vr.mood_col_name], ascending=True)
        positive_tags_list = list(sorted_positive_tags[vr.mood_col_name].unique())
        st.session_state["positive_tags"] = positive_tags_list

        negative_sentiment_str = "Negative"
        sorted_negative_tags = mood_df[mood_df[vr.sentiment_col_name] == negative_sentiment_str].sort_values(by=[vr.color_int_col_name, vr.mood_col_name], ascending=True)
        negative_tags_list = list(sorted_negative_tags[vr.mood_col_name].unique())
        st.session_state["negative_tags"] = negative_tags_list

        # when the user makes a selection of tags for filtering moods
        st.session_state['selected_tags'] = set()

        # journal data
        data_loc = os.path.join(vr.data_dir, vr.journal_blob_name)
        with open(data_loc) as f:
            d = json.load(f)
        st.session_state["journal_data"] = d

def access_mood_color(mood: str) -> str:        

    mood_df = st.session_state["mood_data"]
    color = mood_df[mood_df.Mood == mood][vr.color_col_name].iloc[0]

    return color

def create_mood_calendar_event(event_id: str) -> list:
    """
    Return a list as mood is array
    """
    event_info = st.session_state["journal_data"][event_id]

    mood_array = event_info["mood"]
    start_time = datetime.strptime(event_info["datetime"], "%Y-%m-%dT%H:%M:%S")
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
    end_time = start_time + timedelta(minutes=10)
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S")

    calendar_data = []
    for mood in mood_array:
        color_str = access_mood_color(mood)
        color = vr.mood_colors[color_str]
        calendar_event = {
            "title":mood,
            "color":color,
            "start":start_time_str,
            "end":end_time_str
        }
        calendar_data.append(calendar_event)

    return calendar_data

def create_anxiety_calendar_event(event_id: str) -> dict:
    """
    Return event only as only one anxiety score is recorded
    """
    event_info = st.session_state["journal_data"][event_id]

    anxiety_score = event_info["anxiety"]
    anxiety_str = vr.anxiety_strings[anxiety_score-1]
    start_time = datetime.strptime(event_info["datetime"], "%Y-%m-%dT%H:%M:%S")
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
    end_time = start_time + timedelta(minutes=10)
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S")

    color = vr.anxiety_colors[anxiety_score-1]
    calendar_event = {
        "title":anxiety_str,
        "color":color,
        "start":start_time_str,
        "end":end_time_str
    }

    return calendar_event

def plot_anxiety(dates, scores):

    return

def data_analysis():

    css_path = pathlib.Path(vr.style_dir)
    load_css(css_path)
    st.set_page_config(layout="wide")
    initialise_session_state()

    with st.sidebar:
        st.title("Data Analysis")
        st.markdown('''
        Explore the moods you've tracked to uncover trends, spot recurring feelings, and gain insights into how your emotions shift throughout your days and weeks.
        ''')
        if st.button("Clear selection", key="cs"):
            st.session_state['selected_tags'] = set()

        # Filtering buttons
        st.markdown("**Moods**")
        st.markdown("Positive")
        st.session_state['selected_tags'] = ut.create_grid_of_buttons(st.session_state["positive_tags"], st.session_state['selected_tags'])
        st.markdown("Negative")
        st.session_state['selected_tags'] = ut.create_grid_of_buttons(st.session_state["negative_tags"], st.session_state['selected_tags'])

    calendar_options = {
        "editable": True,
        "selectable": True,
        "initialView": "daygrid",
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridDay,dayGridWeek,dayGridMonth",
        },
        "initialDate": datetime.now().strftime("%Y-%m-%d"),
        "initialView": "dayGridMonth",
    }

    # generate two calendars from journal data
    mood_calendar_events = []
    anxiety_calendar_events = []
    for event in st.session_state["journal_data"].keys():
        ## mood
        mood_calendar_event = create_mood_calendar_event(event)
        mood_calendar_events += mood_calendar_event
        ## anxiety
        anxiety_calendar_event = create_anxiety_calendar_event(event)
        anxiety_calendar_events.append(anxiety_calendar_event)

    ## filter events by mood
    if st.session_state["selected_tags"]:
        mood_calendar_events = [i for i in mood_calendar_events if i["title"] in st.session_state["selected_tags"]]

    custom_css="""
        .fc-event-past {
            opacity: 0.8;
        }
        .fc-event-time {
            font-style: italic;
        }
        .fc-event-title {
            font-weight: 700;
        }
        .fc-toolbar-title {
            font-size: 2rem;
        }
    """

    calendar_options = {
        "Mood":mood_calendar_events,
        "Anxiety":anxiety_calendar_events,
    }

    chosen_calendar = st.selectbox(
        "calendar select",
        tuple(calendar_options.keys()),
        label_visibility="collapsed"
    )

    mood_calendar = calendar(
        events=calendar_options[chosen_calendar],
        options=calendar_options,
        custom_css=custom_css,
        key='calendar', # Assign a widget key to prevent state loss
        )
    st.write(mood_calendar)

data_analysis()