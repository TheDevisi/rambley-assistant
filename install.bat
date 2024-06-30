@echo off

echo Checking if Python installed...
python --version > nul 2>&1
if errorlevel 1 (
    echo Python not found. Please install Python 3.10 from the official website.
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

echo Updating settings.json file with your API key...

powershell -Command "if (Test-Path 'settings.json') { 
    $json = Get-Content 'settings.json' | ConvertFrom-Json; 
    $json.user_api_token = '%API_KEY%'; 
    $json | ConvertTo-Json | Set-Content 'settings.json'; 
} else { 
    $json = @{ user_api_token = '%API_KEY%' }; 
    $json | ConvertTo-Json | Set-Content 'settings.json'; 
}"

if errorlevel 1 (
    echo Failed to update settings.json.
    pause
    exit /b 1
)

echo Success.
pause
