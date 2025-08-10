# optional and required fields 
import streamlit as st
import uuid
import json

import sys
import os
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..', '..')))

import variables as vr
import utils as ut

def data_entry():

    st.set_page_config(layout="wide")

    with st.sidebar:
        st.title("Add a Journal Entry")
        st.markdown('''
        Record your thoughts and feelings here.
        ''')
        st.write('Made with ❤️ by Beth')

    # form for submitting new journal entry
    with st.form(border=True, key="journal_entry"):

        cols = st.columns(2)
        # DATE AND TIME
        with cols[0]:
            datetime_cols = st.columns([0.6, 0.4])
            with datetime_cols[0]:
                date = st.date_input("Date & Time", "today")
            with datetime_cols[1]:
                time = st.time_input("time", "now", label_visibility="hidden")

        # MOOD(S)
        with cols[1]:
            moods = st.multiselect("Mood", st.session_state["positive_tags"] + st.session_state["negative_tags"])

        # ANXIETY
        def stringify(i:int = 0) -> str:
            return vr.anxiety_strings[i-1]
        
        anxiety = st.select_slider(
            "Anxiety", 
            options=list(range(1, 11)), 
            value=1,
            format_func=stringify)
        
        # COMMENTS
        comments = st.text_area("Context and Comments", help="What situation are you in that is influencing your mood?")
        
        # THOUGHTS
        thoughts = st.text_area("Thoughts", help="What's running through your mind?\nUse a new line to separate bullet points.")

        # FEELINGS
        feelings = st.text_area("Feelings", help="How are these thoughts and stimuli making you feel?\nUse a new line to separate bullet points.")

        # TRIGGERS
        triggers = st.text_area("Triggers", help="What external stimuli are influencing your thoughts and feelings?\nUse a new line to separate bullet points.")

        # with submit, create ID
        submit = st.form_submit_button(label = 'Save')
        
    # update project dataset with new submission
    if submit:
        entry_id = str(uuid.uuid4())
        date_str = date.strftime("%Y-%m-%d")
        time_str = time.strftime("%H:%M:00")
        data = {
            "datetime":date_str + "T" + time_str,
            "mood":moods,
            "anxiety":anxiety,
            "thoughts":thoughts,
            "feelings":feelings,
            "triggers":triggers,
            "comments":comments
        }
        # save new data entry to session state
        st.session_state["journal_data"][entry_id] = data
        # update recorded moods in session state
        st.session_state["recorded_moods"] = list(set(st.session_state["recorded_moods"] + moods))
        # update local file
        data_loc = os.path.join(vr.data_dir, vr.journal_blob_name)
        with open(data_loc, 'w') as f:
            json.dump(st.session_state["journal_data"], f)
        # navigate to calendar view
        st.switch_page("pages/data_analysis.py")

data_entry()