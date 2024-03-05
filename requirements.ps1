
# Install winget

Invoke-WebRequest -Uri https://aka.ms/getwinget -OutFile Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle
Invoke-WebRequest -Uri https://aka.ms/Microsoft.VCLibs.x64.14.00.Desktop.appx -OutFile Microsoft.VCLibs.x64.14.00.Desktop.appx
Invoke-WebRequest -Uri https://github.com/microsoft/microsoft-ui-xaml/releases/download/v2.7.3/Microsoft.UI.Xaml.2.7.x64.appx -OutFile Microsoft.UI.Xaml.2.7.x64.appx
Add-AppxPackage Microsoft.VCLibs.x64.14.00.Desktop.appx
Add-AppxPackage Microsoft.UI.Xaml.2.7.x64.appx
Add-AppxPackage Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle
$URL = "https://api.github.com/repos/microsoft/winget-cli/releases/latest"
$LicenseFileURL = (Invoke-WebRequest -Uri $URL).Content | ConvertFrom-Json |
        Select-Object -ExpandProperty "assets" |
        Where-Object "browser_download_url" -Match '.xml' |
        Select-Object -ExpandProperty "browser_download_url"
Invoke-WebRequest -Uri $LicenseFileURL -OutFile  'license.xml'
Add-AppxProvisionedPackage -PackagePath "Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle" -LicensePath 'license.xml' -online 


winget install --id Google.Chrome
winget install --id SublimeHQ.SublimeText.4
winget install --id Git.Git -e --source winget
winget install --id Python.Python.3.8 -l C:\Python3.8


###########start new powershell########

python -m pip install --upgrade pip

pip install update
pip install seleniumbase
pip install selenium 
pip install pandas
pip install bs4
pip install webdriver_manager

cd Documents
git clone https://github.com/Cocozzj/GPT_code_pub.git
cd ./GPT_code_pub


###########upload file########

### under GPT_code_pub folder
scp Web_data/GPTs_info/* gpts@cs-pluto.cs.umn.edu:~/upload_data/GPTs_info/

# Thinkpad: 'C:\Program Files\Google\Chrome\Application'>.\chrome.exe --remote-debugging-port=9223 --user-data-dir="C:\Users\cocoz\Downloads\selenium\selenium1\ChromeProfile"
# VMare: 'C:\Program Files\Google\Chrome\Application'>.\chrome.exe --remote-debugging-port=9223 --user-data-dir="C:\Users\Zejun\Downloads\selenium\selenium1\ChromeProfile"
# Lenovo(ps): 'C:\Program Files\Google\Chrome\Application'>.\chrome.exe --remote-debugging-port=9223 --user-data-dir='C:\Downloads\selenium\selenium1\ChromeProfile'
# Anlan(ps) 'C:\Program Files (x86)\Google\Chrome\Application'>.\chrome.exe --remote-debugging-port=9223 --user-data-dir='/home/zejun/Downloads/selenium/selenium1/ChromeProfile'
# Linux '/opt/google/chrome/google-chrome'

chrome://settings/clearBrowserData