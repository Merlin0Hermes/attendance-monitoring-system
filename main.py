import streamlit as st
from storage import create_tables

create_tables()

pg = st.navigation(
    [
        st.Page("camera.py", title="Attendance"),
        st.Page("registration.py", title="Registration"),
        st.Page("history.py", title="History"),
        st.Page("configuration.py", title="Configuration"),
    ]
)

pg.run()
