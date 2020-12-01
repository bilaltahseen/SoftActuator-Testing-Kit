@echo off
set /p pressure=Type Filename with extension:
cmd /k "cd /d \venv\Scripts & activate & cd.. cd.. & python GraphPlot.py %pressure%"


