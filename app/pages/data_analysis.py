import streamlit as st
from streamlit_calendar import calendar
import pandas as pd
import json
import sys
import os
from datetime import datetime, timedelta
from uuid import uuid4
from ast import literal_eval
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..', '..')))

import variables as vr
import utils as ut

def initialise_session_state() -> None:

    if "mood_data" not in st.session_state:
        mood_df = pd.read_csv(os.path.join(vr.data_dir, vr.mood_data_filename))
        st.session_state["mood_data"] = mood_df
    # all moods available for selection
    if "all_tags" not in st.session_state:
        all_tags = list(st.session_state["mood_data"]["Mood"].unique())
        all_tags.sort()
        st.session_state["all_tags"] = all_tags
    # when the user makes a selection of tags for filtering moods
    if "selected_tags" not in st.session_state:
        st.session_state['selected_tags'] = set()
    if "journal_data" not in st.session_state:
        data_loc = os.path.join(vr.data_dir, vr.journal_blob_name)
        with open(data_loc) as f:
            d = json.load(f)
        st.session_state["journal_data"] = d

def access_mood_color(mood: str) -> str:        

    mood_df = st.session_state["mood_data"]
    color = mood_df[mood_df.Mood == mood]["Color"].iloc[0]

    return color

def create_calendar_event(event_id: str) -> list:
    """

    """
    print(event_id)
    event_info = st.session_state["journal_data"][event_id]
    print(event_info)

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

def data_analysis():

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
        st.session_state['selected_tags'] = ut.create_grid_of_buttons(st.session_state["all_tags"], st.session_state['selected_tags'])

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

    # generate calendar data from journal data
    calendar_events = []
    for event in st.session_state["journal_data"].keys():
        calendar_event = create_calendar_event(event)
        calendar_events += calendar_event
    # filter events by mood
    if st.session_state["selected_tags"]:
        calendar_events = [i for i in calendar_events if i["title"] in st.session_state["selected_tags"]]

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

    mood_calendar = calendar(
        events=calendar_events,
        options=calendar_options,
        custom_css=custom_css,
        key='calendar', # Assign a widget key to prevent state loss
        )
    st.write(mood_calendar)

data_analysis()