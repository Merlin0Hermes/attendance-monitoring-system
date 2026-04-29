import streamlit as st
import pandas as pd
import cv2 as cv

pg = st.navigation( [st.Page("camera.py", title="Camera"), 
                            st.Page("registration.py", title="Registration"),
                            st.Page("history.py", title="History")])

pg.run()
