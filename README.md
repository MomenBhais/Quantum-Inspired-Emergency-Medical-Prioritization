# 🏆 COVID-19 & Lung Disease Detection App (Image + Audio)

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-ff4b4b?logo=streamlit)
![TensorFlow](https://img.shields.io/badge/Model-TensorFlow-orange?logo=tensorflow)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

> 🥇 **Awarded 7th Place** at the **Arab Artificial Intelligence Olympiad 2025** for innovation in AI-powered healthcare solutions.

---

## 📌 Overview

The **PulmoAI Detection App** is an advanced AI-powered diagnostic system that detects **COVID-19**, **Viral Pneumonia**, and **normal lung conditions** using both **chest X-ray images** and **cough audio recordings**.

The project was honored with **7th place** in the **Arab AI Olympiad 2026**, showcasing the power of dual-modal AI systems in real-world healthcare settings.

---

## 🚀 Features

- 🖼️ **Chest X-ray Detection**: Classifies X-ray images into COVID-19, Pneumonia, or Normal.
- 🔊 **Cough Audio Analysis**: Accepts uploaded or live-recorded cough audio and classifies it.
- 🧪 **Dual-Modal AI Integration**: Merges both image and audio models for flexible diagnosis.
- 📊 **High Accuracy**: CNN-based models with strong training performance.
- 🌐 **Streamlit Interface**: Fully web-based and user-friendly.
- 🎙️ **Real-time Audio Capture**: Supports live cough recording through microphone.
- 📁 **Cross-platform Compatibility**: Runs on Windows, Linux, macOS.

---

## 🏗️ Tech Stack

| Layer         | Tools & Libraries                                 |
|---------------|---------------------------------------------------|
| Language      | Python 3.8+                                       |
| Interface     | Streamlit, HTML, CSS                              |
| Deep Learning | TensorFlow, Keras, OpenCV, NumPy                  |
| Audio         | Librosa, SoundFile, Matplotlib, streamlit-webrtc |
| Models        | CNN for images and spectrograms                   |
| Deployment    | Local, Docker, or Cloud (optional)                |

---

## 📂 Project Structure

# Quantum-Inspired Emergency Medical Prioritization

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-ff4b4b?logo=streamlit)
![TensorFlow](https://img.shields.io/badge/Model-TensorFlow-orange?logo=tensorflow)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

> 🚀 **Submitted to the Quantum Computing Hackathon 2025** — a quantum-inspired approach to prioritizing emergency medical cases using multimodal AI (image + audio).

---

## 📌 Overview

This repository contains the code and pretrained models for a quantum-inspired emergency triage system that combines chest X-ray image analysis and cough audio classification to assist rapid prioritization in emergency settings.

The project was prepared as a submission to the **Quantum Computing Hackathon 2025**, exploring how classical deep-learning models can be augmented with quantum-inspired decision rules for more robust prioritization.

---

## 🚀 Features

- 🖼️ **Chest X-ray Analysis**: Classifies X-ray images into COVID-19, Viral Pneumonia, or Normal.
- 🔊 **Cough Audio Analysis**: Classifies cough recordings (uploaded or live) into symptomatic categories.
- 🧪 **Dual-Modal Fusion**: Combines image and audio outputs using a quantum-inspired scoring heuristic to produce a triage priority.
- 🌐 **Streamlit UI**: Lightweight web interface for quick evaluations.
- 🎙️ **Live Audio Capture**: Optional microphone-based cough recording for rapid input.
- 📁 **Cross-platform**: Works on Windows, Linux, and macOS.

---

## 🏗️ Tech Stack

| Layer         | Tools & Libraries                                 |
|---------------|---------------------------------------------------|
| Language      | Python 3.8+                                       |
| Interface     | Streamlit, HTML, CSS                              |
| Deep Learning | TensorFlow / Keras, OpenCV, NumPy                 |
| Audio         | Librosa, SoundFile, streamlit-webrtc              |
| Models        | CNNs for images and spectrograms                  |
| Deployment    | Local, Docker, or Cloud (optional)                |

---

## 📂 Project Structure

Root of repository:

```
Quantum-Inspired Emergency Medical Prioritization/
┣ Coughing sound & it Model/
┃ ┣ cough_model_multi.h5
┃ ┗ coughvid-dataset.ipynb
┣ Photo for Lung & it Model/
┃ ┣ Covid_19_downloadable.h5
┃ ┗ covid-19-model.ipynb
┣ StreamlitCode(GUI)/
┃ ┣ covid19_app.py
┃ ┣ health_check.py
┃ ┣ run_app.bat
┃ ┣ requirements.txt
┃ ┗ test_quantum_triage.py
┣ README.md
┗ requirements.txt
```

---

## 🖥️ Installation & Running

### Prerequisites

- Python 3.8+ (3.10+ recommended)
- `pip`
- `ffmpeg` (optional, for some audio processing backends)
- Recommended: virtual environment

### Quick Setup (Windows PowerShell)

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r "StreamlitCode(GUI)/requirements.txt"
```

### Run the Streamlit App

```powershell
cd "StreamlitCode(GUI)"
streamlit run covid19_app.py
# Or use the bundled helper
..\StreamlitCode(GUI)\run_app.bat
```

---

## 🎯 How It Works (High level)

Image classification:
- Input: chest X-ray image (.jpg/.png)
- Preprocessing: OpenCV resize/normalize
- Model: CNN image classifier
- Output: COVID-19, Viral Pneumonia, or Normal

Audio classification:
- Input: cough .wav or live mic recording
- Preprocessing: mel-spectrogram via Librosa
- Model: CNN on spectrogram
- Output: COVID-19–related signal / Symptomatic / Healthy

Fusion & triage:
- Outputs from both modalities are combined by a quantum-inspired scoring heuristic that produces a triage priority (e.g., high/medium/low).

---

## 🧪 Model Summary

| Modality | Input | Model | Notes |
|----------|-------|-------|-------|
| Image    | Chest X-ray (RGB) | CNN | Pretrained H5 available in `Photo for Lung & it Model/` |
| Audio    | Cough (WAV -> Mel) | CNN | Pretrained H5 in `Coughing sound & it Model/` |

---

## 🔧 Notes for Hackathon Submission

- The submission emphasizes a hybrid approach: classical CNNs for perception plus quantum-inspired decision fusion for triage.
- Ensure model file paths in `StreamlitCode(GUI)/covid19_app.py` and `health_check.py` point to the correct `.h5` files before deployment.
- Add any metrics, logs, or demo recordings to support the hackathon submission.

---

## 🧠 Future Work

- Experiment with true quantum/classical hybrid pipelines (Qiskit, PennyLane) for decision fusion.
- Improve dataset diversity and robustness testing.
- Add multilingual UI (Arabic, English, French) and accessibility improvements.

---

## 🧑‍💻 Author

Momen Mohammed Bhais

- GitHub: https://github.com/MomenBhais
- LinkedIn: https://www.linkedin.com/in/momen-bhais-b5739b317
- Email: momenbhais@outlook.com

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## ⚠️ Disclaimer

This project is intended for research and hackathon/demo purposes only. It is not a certified clinical tool and must not be used for medical diagnosis or treatment decisions.
