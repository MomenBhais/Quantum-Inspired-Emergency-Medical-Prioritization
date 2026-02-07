Setup & Run — PulmoAI Streamlit App

Quick steps to prepare and run locally (Windows, using conda env `pulmoai`):

1) Create/activate environment and install requirements (once):

```powershell
conda create -n pulmoai python=3.10 -y
conda activate pulmoai
pip install -r requirements.txt
# (optional) If sound recording conversion fails, install ffmpeg:
conda install -n pulmoai -c conda-forge ffmpeg -y
```

2) Run the app:

```powershell
# from this directory (StreamlitCode(GUI))
run_app.bat
# or
C:\Users\bhais\anaconda3\envs\pulmoai\Scripts\streamlit.exe run "covid19_app.py"
```

3) Troubleshooting checklist before the competition:
- Ensure `Covid_19_downloadable.h5` exists at: `../Photo for Lung & it Model/Covid_19_downloadable.h5`
- Ensure `cough_model_multi.h5` exists at: `../Coughing sound & it Model/cough_model_multi.h5`
- ffmpeg installed and on PATH (required for converting browser recordings):
  - `ffmpeg -version` should return a version
- Confirm packages installed: `pip list` shows `streamlit`, `tensorflow`, `pydub`, `pyarrow`, `soundfile`, `librosa`.

4) Quick local health-check (optional):
- Start the app and open http://localhost:8508
- Upload a short WAV test file, press `Predict` — confirm model returns a class.
- Record via the recorder, press `Predict` — confirm recording is saved and predicted.

If you want, I can also commit these changes and create a ZIP of the `StreamlitCode(GUI)` folder for submission.
