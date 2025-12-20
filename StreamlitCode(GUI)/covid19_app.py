# Import necessary libraries
import streamlit as st
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from PIL import Image
import librosa
import librosa.display
import matplotlib.pyplot as plt
import os
import uuid
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import av
import soundfile as sf

# ------------------- إعداد الصفحة -------------------
st.set_page_config(
    page_title="Covid-19 Detection (Image & Audio)",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------- إعدادات CSS -------------------
def local_css():
    st.markdown(
        """
        <style>
        body {
            background-color: #f0f8ff;
        }
        .title {
            font-size: 50px;
            color: #2E86C1;
            text-align: center;
            font-weight: bold;
        }
        .subtitle {
            font-size: 24px;
            color: #34495E;
            text-align: center;
        }
        .stButton>button {
            background-color: #2E86C1;
            color: white;
            border-radius: 8px;
            height: 3em;
            width: 10em;
            font-size: 16px;
        }
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #2E86C1;
            color: white;
            text-align: center;
            padding: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

local_css()

# ------------------- تحميل النماذج -------------------
@st.cache_resource
def load_image_model():
    return load_model(r"c:\Users\bhais\Downloads\Covid_19_downloadable.h5")

@st.cache_resource
def load_audio_model():
    return load_model(r"c:\Users\bhais\Downloads\cough_model_multi.h5")

image_model = load_image_model()
audio_model = load_audio_model()

# ------------------- الخرائط التصنيفية -------------------
image_class_map = {0: 'Covid', 1: 'Normal', 2: 'Viral Pneumonia'}
audio_class_map = {0: 'COVID-19', 1: 'Symptomatic', 2: 'Healthy'}

# ------------------- تبويبات -------------------
tabs = st.tabs(["Home", "About Model", "Contact"])

# ------------------- الصفحة الرئيسية -------------------
with tabs[0]:
    st.markdown('<p class="title">🦠 Covid-19 Detection App (Image & Cough Audio)</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Upload an X-ray image or a cough sound file to detect Covid-19</p>', unsafe_allow_html=True)

    # رفع صورة
    uploaded_image = st.file_uploader("Upload Chest X-ray Image (.jpg/.png)", type=['jpg', 'jpeg', 'png'])

    # رفع صوت
    uploaded_audio = st.file_uploader("Upload Cough Audio (.wav)", type=['wav'])

    st.markdown("### Or record cough audio below:")
    
    class AudioProcessor(AudioProcessorBase):
        def __init__(self):
            self.frames = []

        def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
            self.frames.append(frame.to_ndarray().flatten())
            return frame

    ctx = webrtc_streamer(
        key="cough-audio",
        audio_receiver_size=1024,
        audio_processor_factory=AudioProcessor,
        media_stream_constraints={"audio": True, "video": False},
    )

# إدارة حالة الجلسة
if "recording" not in st.session_state:
    st.session_state.recording = False
    st.session_state.audio_path = None

# زر بدء التسجيل
if not st.session_state.recording:
    if st.button("Start Recording"):
        st.session_state.recording = True
        st.info("Recording started... Speak now!")

# زر إيقاف التسجيل وحفظه
if st.session_state.recording and st.button("Stop & Save Recording"):
    if ctx and ctx.state.playing and hasattr(ctx.audio_processor, "frames"):
        if len(ctx.audio_processor.frames) > 0:
            audio_np = np.concatenate(ctx.audio_processor.frames, axis=0)
            audio_path = f"recorded_{uuid.uuid4()}.wav"
            sf.write(audio_path, audio_np, 44100)
            st.session_state.audio_path = audio_path
            st.session_state.recording = False
            st.success("Recording stopped and saved.")
            st.audio(audio_path, format="audio/wav")

predict_button = st.button("Predict")

# ------------------- معالجة التنبؤ -------------------
if uploaded_image is not None or uploaded_audio is not None or st.session_state.audio_path:

    # صورة
    if uploaded_image is not None:
        try:
            img = Image.open(uploaded_image).convert("RGB")
            img_display = img.copy()
            img_display.thumbnail((400, 400))
            st.image(img_display, caption='Uploaded Image', use_column_width=False)

            if predict_button:
                with st.spinner("Processing Image..."):
                    new_image = np.array(img.resize((250, 250))).astype("float32") / 255.0
                    new_image = new_image.reshape(1, 250, 250, 3)
                    pred = image_model.predict(new_image)
                    result = image_class_map[np.argmax(pred)]
                st.success(f"This image represents: **{result}** class")

        except Exception as e:
            st.error(f"Error processing image: {e}")

    # صوت
    audio_source = None
    if uploaded_audio is not None:
        audio_source = uploaded_audio
    elif st.session_state.audio_path:
        audio_source = st.session_state.audio_path

    if audio_source is not None and predict_button:
        try:
            if isinstance(audio_source, str):
                st.audio(audio_source, format="audio/wav")

            with st.spinner("Processing Audio..."):
                y, sr = librosa.load(audio_source, sr=22050)
                mel_spec = librosa.feature.melspectrogram(y=y, sr=sr)
                mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

                fig = plt.figure(figsize=(2.24, 2.24), dpi=100)
                librosa.display.specshow(mel_spec_db, sr=sr, x_axis='time', y_axis='mel')
                plt.axis('off')
                tmp_filename = f"temp_{uuid.uuid4()}.png"
                plt.savefig(tmp_filename, bbox_inches='tight', pad_inches=0)
                plt.close(fig)

                img = Image.open(tmp_filename).resize((64, 64)).convert('RGB')
                os.remove(tmp_filename)

                audio_input = np.array(img) / 255.0
                audio_input = audio_input.reshape(1, 64, 64, 3)

                pred = audio_model.predict(audio_input)
                result = audio_class_map[np.argmax(pred)]

            st.success(f"This cough audio indicates: **{result}**")
        except Exception as e:
            st.error(f"Error processing audio: {e}")

elif predict_button:
    st.warning("Please upload a file or record audio before predicting.")

# ------------------- تبويب معلومات -------------------
with tabs[1]:
    st.markdown('<h2 class="title">📊 About the Model</h2>', unsafe_allow_html=True)
    st.markdown("""
    ### 🖼️ Image Classification Model
    - **Input**: Chest X-ray images
    - **Classes**: Covid, Normal, Viral Pneumonia
    - **Model**: CNN
    - **Accuracy**: 95%
    
    ### 🔊 Audio Classification Model
    - **Input**: Cough WAV audio
    - **Processing**: Converts audio to mel-spectrogram images
    - **Classes**: COVID-19, Symptomatic, Healthy
    - **Model**: CNN with spectrogram input
    - **Accuracy**: ~90%

    ### Notes
    - Make sure the audio is clear and properly formatted.
    - X-ray images should be high-quality and properly aligned.
    """)

# ------------------- تبويب التواصل -------------------
with tabs[2]:
    st.markdown('<h2 class="title">📞 Contact Us</h2>', unsafe_allow_html=True)
    st.markdown("""
    For any inquiries or support, please reach out to us:

    - **Email**: [momenbhais@outlook.com](mailto:momenbhais@outlook.com)
    - **Email**: [arwahajahja2005@gmail.com](mailto:arwahajahja2005@gmail.com)
    - **LinkedIn**: [Our LinkedIn](https://www.linkedin.com/in/momen-bhais-b5739b317/)
    - **GitHub**: [Our GitHub](https://github.com/MomenBhais)
    """)

# ------------------- الفوتر -------------------
st.markdown(
    """
    <div class="footer">
        &copy; 2025 Lung disease Detection App | Developed PulmoAI Team
    </div>
    """,
    unsafe_allow_html=True
)
