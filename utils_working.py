from torch import mode
from ultralytics import YOLO
import streamlit as st
import cv2
import tempfile
from PIL import Image
import pygame
import threading
import io
import PIL.Image

pygame.mixer.init()
pygame.mixer.music.load(
    "warning.mp3"
)  # Make sure alarm.mp3 exists in your project folder
alarm_on = False


def play_alarm():
    pygame.mixer.music.play(-1)


def dispaly_detected_frames(confidence, model, st_frame, image):
    global alarm_on

    # Create persistent placeholders ONCE (so layout doesn't shift)
    if "alert_placeholder" not in st.session_state:
        st.session_state.alert_placeholder = st.empty()
    if "video_placeholder" not in st.session_state:
        st.session_state.video_placeholder = st.empty()

    # Reserve space for alert banner even if nothing is shown
    st.session_state.alert_placeholder.markdown(
        "<div style='height:60px;'></div>", unsafe_allow_html=True
    )

    # Resize frame and predict
    image = cv2.resize(image, (720, int(720 * (9 / 16))))
    result = model.predict(image, conf=confidence)
    boxes = result[0].boxes

    # Display the video frame
    res_plotted = result[0].plot()
    st.session_state.video_placeholder.image(
        res_plotted, caption="Detected Video", channels="BGR", width="content"
    )

    detected_state = None

    # Identify driver state
    if boxes is not None and len(boxes) > 0:
        for box in boxes:
            cls_id = int(box.cls[0])
            class_name = result[0].names[cls_id].lower()

            if class_name == "drowsy":
                detected_state = "drowsy"
                break
            elif class_name == "phone":
                detected_state = "phone"
                break
            elif class_name in ["distracted", "head drop", "smoking", "yawn"]:
                detected_state = "distracted"
                break

    # 🔔 Manage alarm + top alert banner
    if detected_state:
        if not alarm_on:
            alarm_on = True
            threading.Thread(target=play_alarm, daemon=True).start()

        # Choose message
        if detected_state == "drowsy":
            msg = "⚠️ DROWSINESS DETECTED!"
        elif detected_state == "phone":
            msg = "⚠️ PHONE DETECTED!"
        elif detected_state == "distracted":
            msg = "⚠️ DRIVER DISTRACTED!"
        else:
            msg = ""

        # Render top alert banner
        if msg:
            st.session_state.alert_placeholder.markdown(
                f"""
                <div style='background-color:#ff4d4d;
                            padding:15px;
                            border-radius:10px;
                            text-align:center;
                            color:white;
                            font-weight:bold;
                            font-size:18px;
                            height:60px;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            box-shadow:0px 2px 8px rgba(0,0,0,0.2);'>
                    {msg}
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        # Stop alarm and clear banner when normal
        if alarm_on:
            pygame.mixer.music.stop()
            alarm_on = False

        # Keep height reserved so frame doesn’t move up
        st.session_state.alert_placeholder.markdown(
            "<div style='height:60px;'></div>", unsafe_allow_html=True
        )


@st.cache_resource
def load_model(model_path):
    model = YOLO(model_path)
    return model


def infer_uploaded_image(confidence, model):
    source_image = st.sidebar.file_uploader(
        label="Choose an Image", type=["jpg", "png", "jpeg", "bmp", "webp"]
    )
    col1, col2 = st.columns(2)

    with col1:
        if source_image:
            uploaded_img = Image.open(source_image)
            st.image(image=source_image, caption="Uploaded Image", width="content")

    if source_image:
        if st.button("Predict"):
            with st.spinner("Detecting..."):
                result = model.predict(uploaded_img, conf=confidence)
                boxes = result[0].boxes
                result_plotted = result[0].plot()[:, :, ::-1]

                with col2:
                    st.image(
                        result_plotted,
                        caption="Detected Image",
                        width="content",
                    )
                    try:
                        with st.expander("Detection Results"):
                            for box in boxes:
                                st.write(box.xywh)
                    except Exception as e:
                        st.write("Please upload imgae first!")
                        st.write(e)


def infer_uploaded_video(confidence, model):
    source_video = st.sidebar.file_uploader(label="Choose a video")

    col1, col2 = st.columns(2)

    if source_video:
        st.video(source_video)

    if source_video:
        if st.button("Predict"):
            with st.spinner("Detecting..."):
                try:
                    tmpfile = tempfile.NamedTemporaryFile()
                    tempfile.write(source_video.read())
                    vid_cap = cv2.VideoCapture(tmpfile.name)

                    st_frame = st.empty()

                    while vid_cap.isOpened():
                        success, image = vid_cap.read()
                        if success:
                            dispaly_detected_frames(
                                confidence=confidence,
                                model=model,
                                st_frame=st_frame,
                                image=image,
                            )
                        else:
                            vid_cap.release()
                            break
                except Exception as e:
                    st.write(f"Error loading video: {str(e)}")


def infer_webcam(confidence, model):
    try:
        flag = st.button(label="Stop Running")
        vid_cap = cv2.VideoCapture(0)
        st_frame = st.empty()

        while not flag:
            success, image = vid_cap.read()
            if success:
                dispaly_detected_frames(confidence, model, st_frame, image)
            else:
                vid_cap.release()
                break
    except Exception as e:
        st.write(f"Error loading webcam video: {str(e)}")
