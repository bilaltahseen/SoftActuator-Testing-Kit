@echo off
set /p pressure=Type Pressure Filename with extension:
set /p force=Type Force Filename with extension:
cmd /k "cd /d \venv\Scripts & activate & cd.. cd.. & python GraphPlot.py %pressure% %force%"


