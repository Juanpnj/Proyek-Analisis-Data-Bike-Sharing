# Proyek-Analisis-Data-Bike-Sharing
 
## Setup Environment - Anaconda
```
conda create --name main-ds python=3.10
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
python -m venv env
env/Scripts/activate.bat
pip freeze > requirements.txt
```

## Run steamlit app
```
streamlit run dashboard.py
```