from storage import save_image
import numpy
import streamlit as st
from PIL import Image
import face_recognition as fr

st.header("Registration")
st.set_page_config(page_title="Registration")

with st.form("image_upload", clear_on_submit=True):
    input_img = st.file_uploader("Upload student photo", type="image/*", max_upload_size=20)
    name = st.text_input("Enter student name")
    submitted = st.form_submit_button("Submit")
    if submitted:
        if input_img is not None and name != "":
            img = Image.open(input_img)
            rgb_img = img.convert('RGB')

            face_locations = fr.face_locations(numpy.array(rgb_img))
            if len(face_locations) != 1:
                st.error("Invalid face image")
                st.stop()

            save_image(name, rgb_img)
            st.success(f"Successfully added image for {name}")
        elif input_img is None:
            st.error("Image is missing")
        elif name == "":
            st.error("Name is missing")

                
            
            
        

