import streamlit as st

# Page Navigation
pages = [
    st.Page("pages/data_entry.py", title="Data Entry - Mood Tracker", icon="📝"),
    st.Page("pages/data_analysis.py", title="Home - Mood Tracker", icon="📅", default=True),
    st.Page("pages/journal.py", title="Journal - Mood Tracker", icon="📖")
]

pg = st.navigation(pages, position="hidden")

# Running the app
pg.run()