@echo off
@setlocal

rem ***********************************************************************
rem * 
rem *  Module:
rem *  VectorRender plugin for Maya
rem *
rem *  Copyright (c) by Alias Systems,
rem *  a division of Silicon Graphics Canada Ltd.  All rights reserved.
rem *
rem *  This file allows VectorRender for Maya, to render .ma/.mb files.
rem *
rem ***********************************************************************

rem **
rem ** Find the Maya installation. If the MAYA_INSTALL_PATH variable is set, 
rem ** then rem use that location, otherwise use the default value 
rem ** (set by the installer when Vector Render for Maya is installed).
rem **

if "%MAYA_INSTALL_PATH%" == "" (
	set MAYA_INSTALL_PATH=<MAYAINSTALLDIR>
)

rem ** 
rem ** Find the VectorRender plugin for Maya. If the MAYATOVECTOR
rem ** variable is set, then use that location, otherwise use the 
rem ** default location.
rem **

if "%MAYATOVECTOR%" == "" (
	set MAYATOVECTOR=<MAYAPLUGINSDIR>
)

rem **
rem ** Check for "pause" option
rem **

set VRPAUSE=false
if "%1" == "-nosplash" (
	set VRPAUSE=true
	shift
)

rem **
rem ** Check for missing arguments 
rem **

if "%1" == "" (
	echo.
	echo.
	echo Error: Not enough arguments specified.
	echo.
	echo.
	goto HELP
)

rem **
rem ** Check for help 
rem **

if "%1" == "-help" (
	goto HELP
)

rem ** We can render now if VectorRender plugin and Maya are
rem ** installed in known locations. 
rem **
rem ** Make sure VectorRender plugin for Maya can be found
rem ** 

if NOT EXIST "%MAYATOVECTOR%\VectorRender.mll" (
	echo.
	echo.
	echo Error: Could not find VectorRender plugin for Maya installation
	echo        in "%MAYATOVECTOR%".  Please verify that you have 
	echo        correctly installed the software there, or set the
	echo        MAYATOVECTOR environment variable to point to the actual
	echo        installation location.
	echo.
	echo        For example:
	echo.
	echo        SET MAYATOVECTOR=C:\Program Files\Alias\
	echo.

	pause
	goto END
)

rem **
rem ** Make sure Maya installation can be found
rem **

if NOT EXIST "%MAYA_INSTALL_PATH%\bin\mayabatch.exe" (
	echo.
	echo.
	echo Error: Could not find Maya installation in 
	echo        "%MAYA_INSTALL_PATH%".  Please verify that you
	echo        have correctly installed the software there, or
	echo        set the MAYA_INSTALL_PATH variable to point to the
	echo        actual installation location.
	echo.
	echo        For example:
	echo.
	echo        SET MAYA_INSTALL_PATH=C:\Program Files\Alias\Maya
	echo.

    	pause
	goto END
)

:RENDER

rem **
rem ** Build the render command
rem **

set RENDERCOMMAND="%MAYA_INSTALL_PATH%\bin\mayabatch" %* -command vectorRenderExecuteBatch

echo.
echo Starting render... 
echo Command: %RENDERCOMMAND%
echo.

rem **
rem ** Invoke the render command
rem **

%RENDERCOMMAND%

echo.
echo Rendering complete.  
echo.

rem **
rem ** Check to see if we want to pause
rem **

if "%VRPAUSE%" == "true" (
	pause
)
goto END

:HELP

echo.
echo.
echo Usage: mayaVectorRender -help 
echo.
echo        Prints help information for this command.         
echo.
echo        mayaVectorRender -file sceneFile [ -proj projectName ] 
echo                                         [ -log  LogfileName ]
echo.
echo        Batch renders a Maya scene file using vector render plugin
echo.
echo        for Maya. If no project is specified, the current project 
echo.
echo        is used.
echo.

pause

:END

@endlocal

