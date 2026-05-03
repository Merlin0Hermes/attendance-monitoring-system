import streamlit as st

pg = st.navigation( [st.Page("camera.py", title="Attendance"), 
                            st.Page("registration.py", title="Registration"),
                            st.Page("history.py", title="History")])

pg.run()
