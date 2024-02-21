@echo off

REM Check if arguments are provided
if "%~1"=="" (
    echo No arguments provided.
    exit /b
)

REM Loop through each argument
:loop
if "%~1"=="" goto end

echo Argument: %~1

REM Perform operations with the argument here
REM Example: You can echo or perform any operation with the argument

shift
goto loop

:end