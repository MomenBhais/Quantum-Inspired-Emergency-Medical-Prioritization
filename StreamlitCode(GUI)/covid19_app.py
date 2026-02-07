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
import soundfile as sf
import io
from streamlit_mic_recorder import mic_recorder
from quantum_triage import QuantumTriageOptimizer, PatientCase, format_optimization_report

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

# ------------------- تهيئة حالة الجلسة -------------------
if "audio_path" not in st.session_state:
    st.session_state.audio_path = None
if "recorded_audio_path" not in st.session_state:
    st.session_state.recorded_audio_path = None
if "patients_list" not in st.session_state:
    st.session_state.patients_list = []
if "optimization_result" not in st.session_state:
    st.session_state.optimization_result = None

# ------------------- تحميل النماذج -------------------
@st.cache_resource
def load_image_model():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_path, 'Photo for Lung & it Model', 'Covid_19_downloadable.h5')
    if not os.path.exists(model_path):
        st.error(f"❌ Image model not found at: {model_path}")
        return None
    return load_model(model_path)

@st.cache_resource
def load_audio_model():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_path, 'Coughing sound & it Model', 'cough_model_multi.h5')
    if not os.path.exists(model_path):
        st.error(f"❌ Audio model not found at: {model_path}")
        return None
    return load_model(model_path)

image_model = load_image_model()
audio_model = load_audio_model()

if image_model is None or audio_model is None:
    st.error("❌ Failed to load models. Please ensure both model files exist.")
    st.stop()

# ------------------- الخرائط التصنيفية -------------------
image_class_map = {0: 'Covid', 1: 'Normal', 2: 'Viral Pneumonia'}
audio_class_map = {0: 'COVID-19', 1: 'Symptomatic', 2: 'Healthy'}

# ------------------- تبويبات -------------------
tabs = st.tabs(["Home", "⚛️ Quantum Triage", "About Model", "Contact"])

# ------------------- الصفحة الرئيسية -------------------
with tabs[0]:
    st.markdown('<p class="title">🦠 Covid-19 Detection App (Image & Cough Audio)</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Upload an X-ray image or a cough sound file to detect Covid-19</p>', unsafe_allow_html=True)

    # رفع صورة
    uploaded_image = st.file_uploader("Upload Chest X-ray Image (.jpg/.png)", type=['jpg', 'jpeg', 'png'])

    # رفع صوت
    uploaded_audio = st.file_uploader("Upload Cough Audio (.wav)", type=['wav'])

    st.markdown("### 🎤 أو سجل صوت السعلة مباشرة:")
    
    # إنشاء تسجيل صوتي
    st.info("🔴 اضغط الزر أدناه للبدء في التسجيل - تحدث لمدة 3-5 ثواني")
    
    audio_data = mic_recorder(
        use_container_width=True,
        key="mic_recorder_key"
    )

    # حفظ التسجيل الصوتي في حالة الجلسة (دعم bytes أو base64)
    if audio_data is not None:
        try:
            audio_bytes = audio_data.get("bytes")
            if isinstance(audio_bytes, str):
                import base64
                # handle data:<type>;base64,...
                if "," in audio_bytes:
                    audio_bytes = audio_bytes.split(",", 1)[1]
                audio_bytes = base64.b64decode(audio_bytes)

            path = f"recorded_{uuid.uuid4()}.wav"
            with open(path, "wb") as f:
                f.write(audio_bytes)
            st.session_state.recorded_audio_path = path
            st.success("✅ Recording saved.")
            st.write(f"Saved file: {path} ({os.path.getsize(path)} bytes)")
        except Exception as e:
            st.error("❌ Failed to save recording")
            st.exception(e)

predict_button = st.button("Predict")

# ------------------- معالجة التنبؤ -------------------
if uploaded_image is not None or uploaded_audio is not None or st.session_state.recorded_audio_path is not None:

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
    elif st.session_state.recorded_audio_path:
        audio_source = st.session_state.recorded_audio_path

    if audio_source is not None and predict_button:
        try:
            if isinstance(audio_source, str):
                st.audio(audio_source, format="audio/wav")

            with st.spinner("Processing Audio..."):
                y = None
                sr = None
                # Read audio using soundfile. Handle both path (str) and uploaded file-like objects.
                try:
                    import soundfile as sf
                    if isinstance(audio_source, str):
                        y, sr = sf.read(audio_source, dtype='float32')
                    else:
                        # uploaded_audio is a Streamlit UploadedFile; read bytes and use BytesIO
                        try:
                            audio_source.seek(0)
                        except Exception:
                            pass
                        audio_bytes = audio_source.read()
                        bio = io.BytesIO(audio_bytes)
                        y, sr = sf.read(bio, dtype='float32')

                    # if stereo, convert to mono
                    if hasattr(y, 'ndim') and y.ndim > 1:
                        y = np.mean(y, axis=1)
                except Exception as inner_e:
                    # Try converting with pydub (handles webm/ogg/mp3 produced by browser)
                    try:
                        from pydub import AudioSegment
                        if isinstance(audio_source, str):
                            seg = AudioSegment.from_file(audio_source)
                        else:
                            try:
                                audio_source.seek(0)
                            except Exception:
                                pass
                            audio_bytes = audio_source.read()
                            seg = AudioSegment.from_file(io.BytesIO(audio_bytes))

                        wav_bio = io.BytesIO()
                        seg.export(wav_bio, format="wav")
                        wav_bio.seek(0)
                        import soundfile as sf
                        y, sr = sf.read(wav_bio, dtype='float32')
                        if hasattr(y, 'ndim') and y.ndim > 1:
                            y = np.mean(y, axis=1)
                    except Exception as inner2:
                        st.error("Failed to load audio file for processing. If your recording is not WAV, install pydub and ffmpeg: `pip install pydub` and ensure ffmpeg is on PATH.")
                        st.exception(inner2)
                        raise inner2

                duration = None
                try:
                    duration = len(y) / float(sr)
                    st.write(f"Audio duration: {duration:.2f} seconds, sample rate: {sr}")
                except Exception:
                    pass

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
            st.error("Error processing audio — see details below:")
            st.exception(e)

elif predict_button:
    st.warning("Please upload a file or record audio before predicting.")

# ------------------- تبويب النظام الكوانتمي -------------------
with tabs[1]:
    st.markdown('<h2 class="title">⚛️ Quantum-Inspired Emergency Triage</h2>', unsafe_allow_html=True)
    st.markdown("""
    **Smart Resource Allocation for Emergency Medical Situations**
    
    This system uses **Quantum-Inspired Optimization** (Simulated Annealing on QUBO formulation) 
    to optimally allocate limited medical resources (e.g., ventilators) based on patient severity, 
    medical urgency, and resource constraints.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏥 Add Patient Case")
        
        patient_name = st.text_input("Patient Name", value=f"Patient_{len(st.session_state.patients_list)+1}")
        patient_id = st.text_input("Patient ID", value=f"ID_{uuid.uuid4().hex[:6].upper()}")
        
        col_a, col_b = st.columns(2)
        with col_a:
            severity = st.slider("Severity Score (0-1)", 0.0, 1.0, 0.5, step=0.1,
                                help="Based on AI analysis: 0=Normal, 1=Critical")
        with col_b:
            priority = st.slider("Medical Priority (0-1)", 0.0, 1.0, 0.5, step=0.1,
                                help="Urgency level: 0=Routine, 1=Emergency")
        
        col_c, col_d = st.columns(2)
        with col_c:
            age = st.number_input("Patient Age", min_value=0, max_value=120, value=40)
        with col_d:
            duration = st.number_input("Est. Duration (hours)", min_value=1, max_value=72, value=24)
        
        needs_vent = st.checkbox("Needs Ventilator", value=True)
        has_alt = st.checkbox("Has Alternative Treatment Available", value=False)
        
        if st.button("➕ Add Patient to Queue", use_container_width=True):
            new_patient = PatientCase(
                patient_id=patient_id,
                name=patient_name,
                severity_score=severity,
                needs_ventilator=needs_vent,
                expected_duration_hours=duration,
                age=age,
                has_alternative_treatment=has_alt,
                priority_factor=priority
            )
            st.session_state.patients_list.append(new_patient)
            st.success(f"✅ {patient_name} added to queue!")
    
    with col2:
        st.subheader("🔧 System Configuration")
        
        num_ventilators = st.slider("Available Ventilators", min_value=1, max_value=100, 
                                   value=min(10, len(st.session_state.patients_list) // 2 or 5))
        max_hours = st.slider("Max Total Ventilator-Hours", min_value=100, max_value=1000, 
                             value=500, step=50)
        
        st.info(f"""
        **Current Queue:**
        - Patients: {len(st.session_state.patients_list)}
        - Ventilators Available: {num_ventilators}
        - Max Duration: {max_hours} hours
        """)
    
    # Display current patients
    if st.session_state.patients_list:
        st.subheader("👥 Current Patient Queue")
        
        patient_df_data = []
        for idx, p in enumerate(st.session_state.patients_list, 1):
            patient_df_data.append({
                "Rank": idx,
                "Name": p.name,
                "ID": p.patient_id,
                "Severity": f"{p.severity_score:.1%}",
                "Priority": f"{p.priority_factor:.1%}",
                "Age": p.age,
                "Duration (h)": p.expected_duration_hours,
                "Needs Vent": "✅" if p.needs_ventilator else "❌"
            })
        
        st.dataframe(patient_df_data, use_container_width=True, hide_index=True)
        
        # Quantum Optimization Button
        if st.button("🚀 Run Quantum-Inspired Optimization", use_container_width=True, 
                    help="Compute optimal resource allocation using Simulated Annealing"):
            with st.spinner("⚛️ Computing optimal allocation via Quantum-Inspired QUBO solver..."):
                optimizer = QuantumTriageOptimizer(
                    num_ventilators=num_ventilators,
                    max_total_hours=max_hours
                )
                result = optimizer.optimize(st.session_state.patients_list)
                st.session_state.optimization_result = result
            
            st.success("✅ Optimization complete!")
    
    # Display Optimization Results
    if st.session_state.optimization_result:
        st.subheader("📊 Optimization Results")
        
        result = st.session_state.optimization_result
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Ventilators Used", f"{result['total_ventilators_used']}/{result['available_ventilators']}")
        with col2:
            st.metric("Total Hours", f"{result['total_hours_used']} h")
        with col3:
            st.metric("Lives Saved Est.", f"{result['estimated_lives_saved']}")
        with col4:
            st.metric("Algorithm", "Quantum-Inspired", delta="QAOA-like")
        
        # Allocation Table
        st.markdown("### 🎯 Priority Allocation Order")
        
        alloc_data = []
        for alloc in result['allocation']:
            alloc_data.append({
                "Rank": alloc['rank'],
                "Patient": alloc['name'],
                "Severity": f"{'🔴' * int(alloc['severity']*5)}{'⚪' * (5-int(alloc['severity']*5))}",
                "Priority Score": f"{alloc['priority_value']:.3f}",
                "Status": "✅ ALLOCATED" if alloc.get('allocated_ventilator') else "⏸️ WAITING",
                "Duration": f"{alloc.get('duration_hours', '-')} h" if alloc.get('allocated_ventilator') else "-",
                "Note": alloc.get('reason', '-')
            })
        
        st.dataframe(alloc_data, use_container_width=True, hide_index=True)
        
        # Technical Report
        with st.expander("📋 Detailed Optimization Report"):
            report = format_optimization_report(result)
            st.code(report, language="text")
        
        # Clear button
        if st.button("🗑️ Clear Queue", use_container_width=True):
            st.session_state.patients_list = []
            st.session_state.optimization_result = None
            st.rerun()

# ------------------- تبويب معلومات -------------------
with tabs[2]:
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
with tabs[3]:
    st.markdown('<h2 class="title">📞 Contact Us</h2>', unsafe_allow_html=True)
    st.markdown("""
    For any inquiries or support, please reach out to us:

    - **Email**: [momenbhais@outlook.com](mailto:momenbhais@outlook.com)
   
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
