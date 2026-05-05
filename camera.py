from storage import mark_attendance
import cv2 as cv
import numpy as np
from pathlib import Path
import face_recognition
import streamlit as st

TOLERANCE = 0.50
SCALE = 2

st.set_page_config(page_title="Attendance")
st.header("Attendance")


def mark_attendances(names: list[str]):
    for name in names:
        if name == "Unknown":
            st.warning("Face not recognized.")
            continue
        mark_attendance(name)
        st.success(f"Marked Attendance: {name}")


class FaceDetectionCamera:
    def __init__(self):
        self.st_image = st.empty()

        img_paths = list(Path("database/").glob("*.png"))
        if not img_paths:
            st.error("No face images found in database.")
        imgs = [face_recognition.load_image_file(path) for path in img_paths]

        self.known_face_encodings = [
            face_recognition.face_encodings(img)[0] for img in imgs
        ]
        self.known_face_names = [path.stem for path in img_paths]
        self.face_names = []

    def run(self):
        cap = cv.VideoCapture(0)

        self.st_button = st.button(
            "Mark Attendance", on_click=lambda: mark_attendances(self.face_names)
        )
        if not cap.isOpened():
            st.error("Could not open camera.")
            return
        process_this_frame = True

        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            if process_this_frame:
                small_frame = cv.resize(frame, (0, 0), fx=1.0 / SCALE, fy=1.0 / SCALE)

                rgb_small_frame = small_frame[:, :, ::-1]
                rgb_small_frame = np.copy(rgb_small_frame)

                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, face_locations
                )

                self.face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(
                        self.known_face_encodings, face_encoding, tolerance=TOLERANCE
                    )
                    name = "Unknown"

                    face_distances = face_recognition.face_distance(
                        self.known_face_encodings, face_encoding
                    )
                    if len(face_distances) == 0:
                        break
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]

                    self.face_names.append(name)

            process_this_frame = not process_this_frame

            for (top, right, bottom, left), name in zip(
                face_locations, self.face_names
            ):
                top *= SCALE
                right *= SCALE
                bottom *= SCALE
                left *= SCALE
                cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv.rectangle(
                    frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv.FILLED
                )
                font = cv.FONT_HERSHEY_DUPLEX
                cv.putText(
                    frame, name, (left + 6, bottom - 6), font, 0.7, (255, 255, 255), 1
                )
            frame = frame[:, :, ::-1]
            self.st_image.image(frame)

    def __del__(self):
        cv.destroyAllWindows()


try:
    cam = FaceDetectionCamera()
    cam.run()
except Exception as e:
    st.error(f"Fatal error: {e}")
    raise
