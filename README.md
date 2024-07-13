# novel_change

## Setup Local Windows environment

### Install python 3.8.7 (do not add to path) from https://www.python.org/downloads/release/python-387
   Due to dependency limitations a Python version that supports spacy and scispacy has to be used

### Create a Python 3.8.7 virtual environment (call ptyhon from the Python 3.8.7 instalation)
   %APPDATA%\..\Local\Programs\Python\Python38\python -m venv dev_env

### Activate Python virtual environment
  dev_env\Scripts\activate

### Update pip
   python -m pip install --upgrade pip

### Install requirements
   python -m pip install -r requirements_windows.txt
  
   
