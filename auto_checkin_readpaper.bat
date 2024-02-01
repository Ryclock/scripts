@echo off
set "readpaper_path=D:\ReadPaper\ReadPaper.exe"

start "" /min "%readpaper_path%" > NUL 2>&1
IF NOT %errorlevel%==0 (
    exit /b %errorlevel%
)

timeout /t 10 > NUL
IF NOT %errorlevel%==0 (
    exit /b %errorlevel%
)

tasklist /fi "imagename eq ReadPaper.exe" | find /i /n "ReadPaper.exe" > NUL
if NOT "%ERRORLEVEL%"=="0" (
    exit /b 1
)

taskkill /f /im "ReadPaper.exe" > NUL
IF NOT %errorlevel%==0 (
    exit /b %errorlevel%
)

exit