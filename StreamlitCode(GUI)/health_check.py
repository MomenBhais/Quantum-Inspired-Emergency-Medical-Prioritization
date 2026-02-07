import os
import shutil
print('Checking environment...')
print('Python:', shutil.which('python') or 'Not found')
print('Streamlit:', shutil.which('streamlit') or 'Not found')
print('FFmpeg:', shutil.which('ffmpeg') or 'Not found')
print('Files present:')
print(' Image model:', os.path.exists(os.path.join('..','Photo for Lung & it Model','Covid_19_downloadable.h5')))
print(' Audio model:', os.path.exists(os.path.join('..','Coughing sound & it Model','cough_model_multi.h5')))
