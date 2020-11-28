@echo off
set /p port=Enter Arduino Serial PORT:
cmd /k "cd /d \venv\Scripts & activate & cd.. cd.. & python FinalGui.py %port%"


