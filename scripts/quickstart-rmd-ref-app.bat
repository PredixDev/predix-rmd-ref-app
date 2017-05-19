@ECHO OFF
SETLOCAL ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION
set CURRENTDIR=%cd%
echo "currentdir=!CURRENTDIR!"
SET FILE_NAME=%0
SET BRANCH=master
SET SKIP_SETUP=FALSE
SET CF_URL=""

:GETOPTS
  IF /I [%1] == [--skip-setup] SET SKIP_SETUP=TRUE
  rem Here we call SHIFT twice to remove the switch and value,
  rem   since these are not needed by the .sh script.
  IF /I [%1] == [-b] SET BRANCH=%2& SHIFT & SHIFT
  IF /I [%1] == [--branch] SET BRANCH=%2& SHIFT & SHIFT
  IF /I [%1] == [--cf-url] SET CF_URL=%2& SHIFT & SHIFT
  IF /I [%1] == [--cf-user] SET CF_USER=%2& SHIFT & SHIFT
  IF /I [%1] == [--cf-password] SET CF_PASSWORD=%2& SHIFT & SHIFT
  IF /I [%1] == [--cf-org] SET CF_ORG=%2& SHIFT & SHIFT
  IF /I [%1] == [--cf-space] SET CF_SPACE=%2& SHIFT & SHIFT
  SET QUICKSTART_ARGS=!QUICKSTART_ARGS! %1
  rem echo "#### QUICKSTART_ARGS: !QUICKSTART_ARGS!"
  SHIFT & IF NOT [%1]==[] GOTO :GETOPTS
GOTO :AFTERGETOPTS

CALL :GETOPTS %*
:AFTERGETOPTS

IF [!BRANCH!]==[] (
  ECHO "Usage: %FILE_NAME% -b/--branch <branch>"
  EXIT /b 1
)

SET IZON_BAT=https://raw.githubusercontent.com/PredixDev/izon/master/izon.bat
SET TUTORIAL=https://www.predix.io/resources/tutorials/tutorial-details.html?tutorial_id=1475^&tag^=1719^&journey^=Hello%%20World^&resources^=1475,1569,1523
SET SHELL_SCRIPT_NAME=quickstart-rmd-ref-app.sh
SET APP_NAME=RMD Asset Monitoring Reference App
SET TOOLS=Cloud Foundry CLI, Git, Java JDK, Maven, Node.js, Predix CLI
SET TOOLS_SWITCHES=/cf /git /jdk /maven /nodejs /predixcli

GOTO START

:CHECK_FAIL
  IF NOT !errorlevel! EQU 0 (
    CALL :MANUAL
  )
GOTO :eof

:MANUAL
  ECHO.
  ECHO.
  ECHO Exiting tutorial.  You can manually go through the tutorial steps here
  ECHO !TUTORIAL!
GOTO :eof

:CHECK_PERMISSIONS
    echo Administrative permissions required. Detecting permissions...

    net session >nul 2>&1
    if %errorLevel% == 0 (
        echo Success: Administrative permissions confirmed.
    ) else (
        echo Failure: Current permissions inadequate.  This script installs tools, ensure you are launching Windows Command window by Right clicking and choosing 'Run as Administrator'.
        EXIT /b 1
    )
GOTO :eof

:INIT
  IF not "!CURRENTDIR!"=="!CURRENTDIR:System32=!" (
    ECHO.
    ECHO.
    ECHO Exiting tutorial.  Looks like you are in the system32 directory, please change directories, e.g. \Users\your-login-name
    EXIT /b 1
  )
  IF not "!CURRENTDIR!"=="!CURRENTDIR:\scripts=!" (
    ECHO.
    ECHO.
    ECHO Exiting tutorial.  Please launch the script from the root dir of the project
    EXIT /b 1
  )

  ECHO Let's start by verifying that you have the required tools installed.
  SET /p answer=Should we install the required tools if not already installed (!TOOLS!)?
  IF "!answer!"=="" (
    SET /p answer=Specify yes/no -
  )
  IF "!answer:~0,1!"=="y" SET doInstall=Y
  IF "!answer:~0,1!"=="Y" echo doInstall=Y

  if "!doInstall!"=="Y" (
    CALL :CHECK_PERMISSIONS
    IF NOT !errorlevel! EQU 0 EXIT /b !errorlevel!

    CALL :GET_DEPENDENCIES

    ECHO Calling %TEMP%\setup-windows.bat
    CALL "%TEMP%\setup-windows.bat" !TOOLS_SWITCHES!
    IF NOT !errorlevel! EQU 0 (
      ECHO.
      ECHO "Unable to install tools.  Is there a proxy server?  Perhaps if you go on a regular internet connection (turning off any proxy variables), the tools portion of the install will succeed. Please see detailed instructions about proxies at https://www.predix.io/resources/tutorials/tutorial-details.html?tutorial_id=1565 "
      EXIT /b !errorlevel!
    )
    ECHO.
    ECHO The required tools have been installed. Now you can proceed with the tutorial.
    pause
  )

GOTO :eof

:GET_DEPENDENCIES
  ECHO Getting Dependencies

  powershell -Command "(new-object net.webclient).DownloadFile('!IZON_BAT!','%TEMP%\izon.bat')"
  xcopy /y !CURRENTDIR!\version.json %TEMP%
  CALL %TEMP%\izon.bat READ_DEPENDENCY local-setup LOCAL_SETUP_URL LOCAL_SETUP_BRANCH %TEMP%
  ECHO "LOCAL_SETUP_BRANCH=!LOCAL_SETUP_BRANCH!"
  SET SETUP_WINDOWS=https://raw.githubusercontent.com/PredixDev/local-setup/!LOCAL_SETUP_BRANCH!/setup-windows.bat

  ECHO !SETUP_WINDOWS!
  powershell -Command "(new-object net.webclient).DownloadFile('!SETUP_WINDOWS!','%TEMP%\setup-windows.bat')"

GOTO :eof

:START

PUSHD "%TEMP%"

ECHO.
ECHO Welcome to the %APP_NAME% Quickstart.
ECHO --------------------------------------------------------------
ECHO.
ECHO This is an automated script which will guide you through the tutorial.
ECHO.

if "!SKIP_SETUP!"=="FALSE" (
  CALL :INIT
)
CALL :CHECK_FAIL
IF NOT !errorlevel! EQU 0 EXIT /b !errorlevel!

POPD

PUSHD "%USERPROFILE%"

if !CF_URL!=="" (
  ECHO CF_URL=!CF_URL!
) else (
  rem this is here so jenkins can non-interactively log in to the cloud
  cf login -a !CF_URL! -u !CF_USER! -p !CF_PASSWORD! -o !CF_ORG! -s !CF_SPACE!
)

ECHO Running the !CURRENTDIR!\scripts\%SHELL_SCRIPT_NAME% script using Git-Bash
cd !CURRENTDIR!
ECHO.
"%PROGRAMFILES%\Git\bin\bash" --login -i -- "!CURRENTDIR!\scripts\%SHELL_SCRIPT_NAME%" -b !BRANCH! --skip-setup !QUICKSTART_ARGS!

POPD
