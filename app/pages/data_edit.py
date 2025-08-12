import streamlit as st
from datetime import datetime

import sys
import os
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..', '..')))

import variables as vr
import utils as ut

def project_edit():

    st.set_page_config(layout="wide")
    with st.sidebar:
        st.title("Entry Edit")
        st.markdown('''
        Change information for this journal entry. If the details are correct, click submit.
        ''')

    # navigation buttons
    if st.button("< Back"):
        st.switch_page("pages/journal.py")

    entry_id = st.session_state["entry_to_edit"]
    journal_entry = st.session_state["journal_data"][entry_id]

    # form for editing information - existing values will already be present in the text boxs/information submission boxes to maintain existing details
    edited_data = ut.journal_form(journal_entry)
    if edited_data:
        st.session_state["entry_to_edit"] = None
        ut.record_journal_data(entry_id, edited_data)
        st.switch_page("pages/journal.py")

project_edit()