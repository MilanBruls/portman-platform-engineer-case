@echo off
REM Task Scheduler: "Momentum Overlay", trigger: monthly, first weekday, 08:30, run whether user is logged on or not
cd /d C:\Desk\models\momentum
"C:\Python39\python.exe" momentum_overlay.py >> C:\Desk\models\momentum\log.txt 2>&1
if errorlevel 1 (
  echo %date% %time% FAILED >> C:\Desk\models\momentum\log.txt
)
REM mail the weights to the desk
powershell -File C:\Desk\tools\mail_weights.ps1
