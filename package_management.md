## Create virtual environment
python -m venv env_name

## Activate virtual env (Linux/MacOS)
source env_name/bin/activate

## Activate virtual env (Windows)
env_name/Scripts/activate.bat

### Or
env_name\Scripts\activate

## Install dependencies from a file
pip install -r requirements.txt

# Generating the requirements/locked versions
pip freeze > requirements.txt

# Deactivate env
deactivate