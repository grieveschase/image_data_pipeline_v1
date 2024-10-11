@echo off 
REM Change current working dir to location of bat file.
pushd %~dp0

REM cd up into application dir
cd ..

REM Set Regular Python as Default, assumes python already is installed, used if no python paths below are available.
set "main_py=python"


REM Find and Set the python path to use for venv setup.
REM NOTE: Add your own python path to p2 ir p3 if not listed in other variables.
REM p1: Chase Local Python Path. 
set "p1=C:\Python312\python.exe" 
set "p2=add_your_own_python_path_here" 
REM Extra User defined Path.
set "p3=add_your_own_python_path_here" 

for %%a in (%p1% %p2% %p3%) do (
    if exist %%a (
        set main_py=%%a
    )
)

REM Check Python Version is 3.9 or higher. Exit if not. 
%main_py%  .\setup\check_py_vers.py
set RETURN_CODE=%ERRORLEVEL%
if NOT %RETURN_CODE% == 0 (
    echo Bad Python Version. Expect 3.9.x or higher. Exiting Script. No venv created.
    popd
    exit
)

echo PYTHON PATH TO BE USED: %main_py% 

REM Create venv. Uprade some stuff.
ECHO #### Creating Python Virtual Environment ####
%main_py% -m venv venv
set "py_venv=.\venv\Scripts\python"
set "pip_venv=.\venv\Scripts\pip"

%py_venv% -m pip install --upgrade pip
REM pip install requirements.
%pip_venv% install -r .\setup\requirements\requirements.txt


REM Change current working dir back to original call location.
popd

ECHO ### PYTHON VENV SETUP DONE ###
