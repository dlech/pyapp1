$family = $(Get-AppxPackage "MyCompany.MySuite.MyApp").PackageFamilyName

Invoke-CommandInDesktopPackage `
    -PackageFamilyName $family `
    -AppId "MyConsoleApp1" `
    -Command ".\.venv\Scripts\python.exe" `
    -Args "-i src\my_console_app_1.py" `
    -PreventBreakaway
