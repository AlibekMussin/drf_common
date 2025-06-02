@echo off
SETLOCAL

REM ���� � python � ����������� �����
SET "VENV_PATH=venv\Scripts\python.exe"

IF NOT EXIST %VENV_PATH% (
    echo ? Cant find venv. Create it first:
    echo     python -m venv venv
    EXIT /B 1
)

REM ���������� ���������
echo ?? Running migrations...
%VENV_PATH% manage.py migrate

echo ?? Creating superuser...
%VENV_PATH% manage.py createsuperuser

echo ? DONE! You are perfect
ENDLOCAL
