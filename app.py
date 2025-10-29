from ultralytics import YOLO
from utils import infer_uploaded_image, infer_uploaded_video, infer_webcam
import streamlit as st

# setting page layout
st.set_page_config(
    page_title="Drowsiness Detection Using YOLOv11",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Home Page Heading
st.title("Drowsiness Detecction using YOLOv11")

# sidebar
st.sidebar.header("DL Model Config")

# model option
task_type = st.sidebar.selectbox("Select Task", ["Detection"])

confidence = float(st.sidebar.slider("Select Model Confidence", 30, 100, 50)) / 100

model_path = "trained_model/best.pt"

# load pretrained YOLO model
try:
    model = YOLO(model_path)
except Exception as e:
    st.error("Unable to load model. Refer below:")
    st.error(f"Exception: {str(e)}")

# source
SOURCES_LIST = ["Image", "Video", "Webcam"]

# image/video options
st.sidebar.header(("Image/Video Config"))
source_selectbox = st.sidebar.selectbox("Select Source", SOURCES_LIST)

source_img = None

if source_selectbox == SOURCES_LIST[0]:
    infer_uploaded_image(confidence, model)
elif source_selectbox == SOURCES_LIST[1]:  # Video
    infer_uploaded_video(confidence, model)
elif source_selectbox == SOURCES_LIST[2]:  # Webcam
    infer_webcam(confidence, model)
else:
    st.error("Currently only 'Image' and 'Video' source are implemented")
