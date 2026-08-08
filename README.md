# trekking_management_app_v1
This is a diploma capstone project for modern application development 1, App where adventurers can look for trekking routes along with guides.

# How to setup
## For windows:
**step 1:** download and extract the zip files

**step 2:** open command prompt/cmd or Windows PowerShell change you present working directory to the app folder you just extracted

cmd/powershell:
```cmd
winget install Python
```
check if you have install the python by running
```cmd
python --version
```
it should show the installed python version

**step 3:** then we creat a virtual environment 

in cmd/powershell:
```cmd
python -m venv venv
```
after this you should see a venv named forlder in the pwd

**step 4:** we activate the virtual environment

in cmd/powershell:
```cmd
venv\Scripts\activate.bat
```
you should see (venv) at the start of your prompt.

**step 5:** installing required files

in cmd/powershell:
```cmd
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```
**step 6:** check if there is a file called instance if not

in cmd/powershell:
```cmd
mkdir instance
```
**step 7:** running the app.py

in cmd/powershell:
```cmd
python app.py
```
**step 8:** now you can open any browser and type:
127.0.0.1:5000 or localhost:5000 
and the website should be accessible \o/

## For Linux:
**step 1:** download and extract the zip files

**step 2:** open your terminal or bash and change you present working directory to the app folder you just extracted

in bash:
```bash
sudo apt install Python3
```
check if you have install the python by running

```bash
python3 --version
```
it should show the installed python version

**step 3:** then we creat a virtual environment 

```bash
python3 -m venv venv
```
after this you should see a venv named forlder in the pwd

**step 4:** we activate the virtual environment

```bash
source venv/bin/activate 
```
you should see (venv) at the start of your prompt.

**step 5:** installing required files

```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
**step 6:** check if there is a file called instance if not

```bash
mkdir instance
```
**step 7:** running the app.py

```bash
python3 app.py
```
**step 8:** now you can open any browser and type:
127.0.0.1:5000 or localhost:5000 
and the website should be accessible \o/
