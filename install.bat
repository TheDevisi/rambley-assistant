@echo off

echo Checking if Python installed...
python --version > nul 2>&1
if errorlevel 1 (
    echo Python not found. Please install Python 3.10 from official web site.
    pause
    exit /b 1
)

echo Installing requirements from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo Unexpected error.
    pause
    exit /b 1
)

set /p API_KEY=Please, enter your API key (see more on GitHub):
echo Your API: %API_KEY%

echo Creating or updating settings.json...
(
echo{
echo    "is_first_startup": false,
echo    "user_api_token": "%API_KEY%"
echo}
) > settings.json

echo Success.
pause
