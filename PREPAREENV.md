###Create a virtual environment

- Create a virtual environment by running the following command
  
  On Windows :

        python -m venv env

  On Linux/macOS

        python3 -m venv env

- Activate the virtual environment. Run the below at the prompt from the folder where you created the virtual environment

        ./env/Scripts/activate

- Once successfully activated the terminal prompt changes to

        (env) PS C:\repos\personal\source-code-helper>

- Install requirements

        pip3 install -r requirements.txt       


        pip3 freeze > requirements.txt

- Packages
  
        pip install pyside6
        pip install ruamel.yaml
        pip install psycopg2
        pip install dearpygui
        pip install cryptography
