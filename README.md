# novel_change

## Setup Local Windows environment

### Install python 3.8.7 (do not add to path) from https://www.python.org/downloads/release/python-387
   Due to dependency limitations on nmslib, a Python version that supports spacy and scispacy has to be used

### Create a Python 3.8.7 virtual environment (call python from the Python 3.8.7 instalation)
   %APPDATA%\..\Local\Programs\Python\Python38\python -m venv dev_env

### Activate Python virtual environment
  dev_env\Scripts\activate

### Update pip
   python -m pip install --upgrade pip

### Install requirements
   python -m pip install -r requirements_windows.txt

   if asked to install msbuild tools , follow the instructions during requirements installation and repeat requirements installation

## Setup Local Ubuntu environment

### Install python 3.10 
   
### Create a Python 3.10 virtual environment 
   python -m venv dev_env

### Activate Python virtual environment
  source dev_env/bin/activate

### Update pip
   python -m pip install --upgrade pip

### Install requirements
   python -m pip install -r requirements_ubuntu-latest.txt

## Setup Local MacOS environment

### Install python 3.10 
   
### Create a Python 3.10 virtual environment 
   python -m venv dev_env

### Activate Python virtual environment
  source dev_env/bin/activate

### Update pip
   python -m pip install --upgrade pip

### Install requirements
   CFLAGS="-mavx -DWARN(a)=(a)" python -m pip install -r requirements_macos-latest.txt
  
   
