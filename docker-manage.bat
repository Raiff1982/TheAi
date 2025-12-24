@echo off
REM Codette AI - Docker Management Script for Windows
REM Usage: docker-manage.bat [command]

setlocal enabledelayedexpansion

REM Configuration
set COMPOSE_FILE=docker-compose.prod.yml
set DOCKERFILE=Dockerfile.prod
set IMAGE_NAME=codette-ai
set IMAGE_TAG=3.0
set CONTAINER_NAME=codette-ai-consciousness

REM Colors (ANSI codes may not work in all Windows terminals)
set "INFO=[INFO]"
set "SUCCESS=[SUCCESS]"
set "WARNING=[WARNING]"
set "ERROR=[ERROR]"

REM Show usage
if "%1"=="" goto show_usage
if /I "%1"=="help" goto show_usage

REM Commands
if /I "%1"=="build" goto cmd_build
if /I "%1"=="push" goto cmd_push
if /I "%1"=="run" goto cmd_run
if /I "%1"=="stop" goto cmd_stop
if /I "%1"=="restart" goto cmd_restart
if /I "%1"=="logs" goto cmd_logs
if /I "%1"=="shell" goto cmd_shell
if /I "%1"=="ps" goto cmd_ps
if /I "%1"=="health" goto cmd_health
if /I "%1"=="status" goto cmd_status
if /I "%1"=="backup" goto cmd_backup
if /I "%1"=="clean" goto cmd_clean
if /I "%1"=="deploy" goto cmd_deploy

echo %ERROR% Unknown command: %1
goto show_usage

:show_usage
echo.
echo Codette AI - Docker Management for Windows
echo.
echo USAGE:
echo     docker-manage.bat [COMMAND]
echo.
echo COMMANDS:
echo     build           Build the Docker image
echo     push            Push image to registry
echo     run             Start the Docker Compose stack
echo     stop            Stop the Docker Compose stack
echo     restart         Restart the Docker Compose stack
echo     logs            Show container logs
echo     shell           Open PowerShell in running container
echo     ps              Show running containers
echo     health          Check system health
echo     status          Show detailed status
echo     backup          Backup persistent data
echo     clean           Clean up containers and volumes
echo     deploy          Deploy to production
echo     help            Show this help message
echo.
echo EXAMPLES:
echo     docker-manage.bat build
echo     docker-manage.bat run
echo     docker-manage.bat logs
echo     docker-manage.bat health
echo.
goto end

:cmd_build
echo %INFO% Building Docker image: %IMAGE_NAME%:%IMAGE_TAG%
docker build -f %DOCKERFILE% -t %IMAGE_NAME%:%IMAGE_TAG% .
if !ERRORLEVEL! EQU 0 (
    echo %SUCCESS% Image built successfully
) else (
    echo %ERROR% Build failed
    exit /b 1
)
goto end

:cmd_push
set "REGISTRY=myregistry.azurecr.io"
if not "%2"=="" set "REGISTRY=%2"
echo %INFO% Pushing image to registry: !REGISTRY!
docker tag %IMAGE_NAME%:%IMAGE_TAG% !REGISTRY!/%IMAGE_NAME%:%IMAGE_TAG%
docker push !REGISTRY!/%IMAGE_NAME%:%IMAGE_TAG%
if !ERRORLEVEL! EQU 0 (
    echo %SUCCESS% Image pushed to registry
) else (
    echo %ERROR% Push failed
    exit /b 1
)
goto end

:cmd_run
echo %INFO% Starting Codette AI stack...
docker-compose -f %COMPOSE_FILE% up -d
if !ERRORLEVEL! EQU 0 (
    echo %SUCCESS% Stack started
    echo %INFO% Waiting for services to initialize...
    timeout /t 40 /nobreak
    cls
    call :cmd_status
) else (
    echo %ERROR% Failed to start stack
    exit /b 1
)
goto end

:cmd_stop
echo %INFO% Stopping Codette AI stack...
docker-compose -f %COMPOSE_FILE% down
if !ERRORLEVEL! EQU 0 (
    echo %SUCCESS% Stack stopped
) else (
    echo %ERROR% Failed to stop stack
    exit /b 1
)
goto end

:cmd_restart
echo %INFO% Restarting Codette AI stack...
docker-compose -f %COMPOSE_FILE% restart
if !ERRORLEVEL! EQU 0 (
    echo %SUCCESS% Stack restarted
) else (
    echo %ERROR% Failed to restart stack
    exit /b 1
)
goto end

:cmd_logs
echo %INFO% Showing Codette AI logs (Ctrl+C to exit)...
docker-compose -f %COMPOSE_FILE% logs -f %2 %3 %4 codette-ai
goto end

:cmd_shell
echo %INFO% Opening PowerShell in container...
docker exec -it %CONTAINER_NAME% powershell.exe
goto end

:cmd_ps
echo %INFO% Running containers:
docker-compose -f %COMPOSE_FILE% ps
goto end

:cmd_health
setlocal enabledelayedexpansion
echo %INFO% Checking Codette AI health...
docker exec %CONTAINER_NAME% python /app/health_check.py >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    echo %SUCCESS% Codette AI is healthy
) else (
    echo %ERROR% Codette AI health check failed
)

echo %INFO% Checking web interface availability...
timeout /t 2 /nobreak >nul
powershell -NoProfile -Command "try { $null = Invoke-WebRequest -Uri 'http://localhost:7860/' -TimeoutSec 5 -ErrorAction Stop; Write-Host '[SUCCESS] Gradio interface is available at http://localhost:7860' } catch { Write-Host '[WARNING] Gradio interface not available' }"

echo.
echo %INFO% Access points:
echo   - Gradio UI:    http://localhost:7860
echo   - Prometheus:   http://localhost:9090
echo   - Grafana:      http://localhost:3000 (admin/admin)
goto end

:cmd_status
echo.
echo ======================================
echo       Codette AI Status
echo ======================================
echo.
echo Running containers:
call :cmd_ps
echo.
echo System access points:
echo   - Gradio UI:    http://localhost:7860
echo   - Prometheus:   http://localhost:9090
echo   - Grafana:      http://localhost:3000 (admin/admin)
echo.
echo Docker statistics:
docker stats --no-stream %CONTAINER_NAME% 2>nul || (
    echo %WARNING% Container not running
)
goto end

:cmd_backup
setlocal enabledelayedexpansion
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
set BACKUP_DIR=backups\!mydate!_!mytime!

if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

echo %INFO% Backing up persistent data to !BACKUP_DIR!...

REM Backup database
echo %INFO% Backing up database...
docker exec %CONTAINER_NAME% sqlite3 /app/data/codette_data.db ".backup '/tmp/db.backup'" 2>nul
docker cp %CONTAINER_NAME%:/tmp/db.backup "%BACKUP_DIR%\db.backup" 2>nul || (
    echo %WARNING% Database backup skipped (optional)
)

REM Backup quantum state
echo %INFO% Backing up quantum state...
docker cp %CONTAINER_NAME%:/app/data/quantum_cocoon.json "%BACKUP_DIR%\" 2>nul || (
    echo %WARNING% Quantum state backup skipped (optional)
)

echo %SUCCESS% Backup completed: !BACKUP_DIR!
goto end

:cmd_clean
setlocal
echo %WARNING% This will remove all containers, networks, and volumes
set /p confirm="Continue? (y/n): "
if /I not "%confirm%"=="y" (
    echo %INFO% Clean cancelled
    goto end
)

echo %INFO% Cleaning up...
docker-compose -f %COMPOSE_FILE% down -v
if !ERRORLEVEL! EQU 0 (
    echo %SUCCESS% Cleanup completed
) else (
    echo %ERROR% Cleanup failed
    exit /b 1
)
goto end

:cmd_deploy
setlocal
echo %WARNING% Production deployment will start Codette AI services
set /p confirm="Continue? (y/n): "
if /I not "%confirm%"=="y" (
    echo %INFO% Deployment cancelled
    goto end
)

echo %INFO% Building image for production...
call :cmd_build
if !ERRORLEVEL! NEQ 0 exit /b 1

echo %INFO% Starting production stack...
docker-compose -f %COMPOSE_FILE% up -d
if !ERRORLEVEL! EQU 0 (
    echo %SUCCESS% Production deployment started
    echo %INFO% Waiting for services to initialize...
    timeout /t 40 /nobreak
    cls
    call :cmd_status
) else (
    echo %ERROR% Failed to deploy
    exit /b 1
)
goto end

:end
endlocal
exit /b 0
