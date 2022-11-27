$family = $(Get-AppxPackage "MyCompany.MySuite.MyApp").PackageFamilyName

Invoke-CommandInDesktopPackage `
    -PackageFamilyName $family `
    -AppId "MyConsoleApp1" `
    -Command ".\.venv\scripts\python.exe" `
    -Args "-m debugpy --listen 5678 --wait-for-client src\my_console_app_1.py" `
    -PreventBreakaway
