import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Registration")

with st.form("image_upload"):
    input_img = st.file_uploader("Upload a clear photo")
    name = st.text_input("Enter student name")
    submitted = st.form_submit_button("Submit")
    if submitted:
        if input_img is not None and name is not None:
            img = Image.open(input_img)
            img.save(f"database/{name}.png", "PNG")
            
        

