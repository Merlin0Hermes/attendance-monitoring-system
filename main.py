import streamlit as st
from storage import create_table

create_table()

pg = st.navigation( [st.Page("camera.py", title="Attendance"), 
                            st.Page("registration.py", title="Registration"),
                            st.Page("history.py", title="History")])

pg.run()
