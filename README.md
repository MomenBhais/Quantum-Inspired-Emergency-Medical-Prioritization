# Quantum-Inspired Emergency Medical Prioritization — Hackathon 2026

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-ff4b4b?logo=streamlit)
![TensorFlow](https://img.shields.io/badge/Model-TensorFlow-orange?logo=tensorflow)

> 🚀 Submission prepared for the **Quantum Computing Hackathon 2026**. This repository implements a quantum-inspired triage heuristic that fuses chest X-ray image analysis and cough-audio classification for emergency prioritization.

---

## What’s in this repo

- Multimodal demo code (image + audio) using classical CNNs.
- Pretrained model files (H5) for image and audio classifiers.
- A Streamlit-based GUI for quick demos and manual evaluation.
- A project brief PDF: `Quantum-Inspired-Emergency-Medical-Prioritization.pdf` (demo / proposal).

---

## Project structure (actual files)

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
┣ Quantum-Inspired-Emergency-Medical-Prioritization.pdf
┣ README.md
┗ linkes for datasets in kaggel.txt
```

Notes: there is currently no `LICENSE` file in the repository; if you intend MIT licensing, add a `LICENSE` file at the project root.

---

## Installation (Windows PowerShell)

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r "StreamlitCode(GUI)/requirements.txt"
```

## Running the demo

From the project root, run the bundled script or start Streamlit directly:

```powershell
.\StreamlitCode(GUI)\run_app.bat
# or
cd "StreamlitCode(GUI)"
streamlit run covid19_app.py
```

---

## Notes on models & paths

- Image model file: `Photo for Lung & it Model/Covid_19_downloadable.h5`
- Audio model file: `Coughing sound & it Model/cough_model_multi.h5`

Make sure the paths referenced in `StreamlitCode(GUI)/covid19_app.py` and `StreamlitCode(GUI)/health_check.py` match the filenames above.

---

## Hackathon notes

- Approach: classical CNNs for perception + a quantum-inspired decision fusion heuristic for triage scoring.
- Suggested supporting artifacts for submission: brief PDF (included), demo video, sample inputs and evaluation metrics.

---

## Future work

- Integrate true quantum-classical hybrid methods (Qiskit, PennyLane) for decision fusion.
- Expand datasets and perform robustness evaluation.
- Add Arabic/English multilingual UI and accessibility features.

---

## Author

Momen Mohammed Bhais — momenbhais@outlook.com

GitHub: https://github.com/MomenBhais

---

## License

Intended: MIT. (No `LICENSE` file found in the repo — add one if you want to publish under MIT.)

---

## Disclaimer

This project is a research/hackathon demo and not a certified clinical tool. Do not use for diagnosis or treatment decisions.
