$ErrorActionPreference = "Stop"
Write-Host "Downloading Python 3.11.9 installer..."
$installerUrl = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
$installerPath = "$env:TEMP\python-installer.exe"

Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath

Write-Host "Installing Python. This may take a minute..."
Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=0 PrependPath=1 Include_test=0 Include_doc=0" -Wait -NoNewWindow

Write-Host "Python Installation Completed."
# Update local session path to immediately use python and pip
$pythonPath = "$env:LOCALAPPDATA\Programs\Python\Python311"
$env:PATH = "$pythonPath\Scripts\;$pythonPath\;$env:PATH"

Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

Write-Host "Installing opencv-python and ultralytics..."
python -m pip install opencv-python ultralytics

Write-Host "Environment Setup Complete!"
