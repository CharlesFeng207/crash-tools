@echo off 
set adb="%~dp0\adb.exe"
echo %adb%
%adb% devices
%adb% shell dumpsys dropbox --print > logs\log-crash_%date:~6,4%_%date:~3,2%_%date:~0,2%_%Time:~0,2%_%Time:~3,2%_%Time:~6,2%.txt
pause