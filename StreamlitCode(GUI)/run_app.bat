@echo off
REM Activate conda environment and run Streamlit app (Windows)
call C:\Users\bhais\anaconda3\Scripts\activate.bat pulmoai







pauseC:\Users\bhais\anaconda3\envs\pulmoai\Scripts\streamlit.exe run "%~dp0covid19_app.py")  exit /b 1  pause  echo Failed to activate conda environment 'pulmoai'. Make sure it exists.nif %ERRORLEVEL% NEQ 0 (