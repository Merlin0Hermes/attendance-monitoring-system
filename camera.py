import time
from storage import mark_attendance, create_table, clear_attendance
import face_recognition
import cv2
import numpy as np
from pathlib import Path
import streamlit as st

def mark_attendances(names: list[str]):
    create_table()
    for name in names:
        if name == "Unknown":
            continue
        mark_attendance(name)
        st.toast(f"Marked Attendance: {name}")

class FaceDetectionCamera:
    def __init__(self):
        self.st_image = st.empty()
        img_paths = [file for file in Path("database/").iterdir() if file.suffix == ".png"]
        imgs = [face_recognition.load_image_file(path) for path in img_paths]

        self.known_face_encodings = [face_recognition.face_encodings(img)[0] for img in imgs]
        self.known_face_names = [path.stem for path in img_paths]
        self.face_names = []

    def run(self):
        self.st_button = st.button("Mark Attendance", on_click=lambda: mark_attendances(self.face_names))
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("Could not open camera.")
            return
        process_this_frame = True

        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            if process_this_frame:
                small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

                rgb_small_frame = small_frame[:, :, ::-1]
                rgb_small_frame = np.copy(rgb_small_frame)

                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, face_locations
                )

                self.face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(
                        self.known_face_encodings, face_encoding, tolerance=0.54
                    )
                    name = "Unknown"

                    face_distances = face_recognition.face_distance(
                        self.known_face_encodings, face_encoding
                    )
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]

                    self.face_names.append(name)

            process_this_frame = not process_this_frame

            for (top, right, bottom, left), name in zip(face_locations, self.face_names):
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                cv2.rectangle(
                    frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED
                )
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, .7, (255, 255, 255), 1)
            frame = frame[:, :, ::-1]
            self.st_image.image(frame)
            

try:
    cam = FaceDetectionCamera()
    cam.run()
except Exception as e:
    st.error(f"Fatal error: {e}")
    raise


