@echo off
if not exist .\mmc-home.txt ( echo "Do not run this directly, only run bat files in the main MMC folder" && pause && exit 2 )
@echo on
if exist .\winpython-tensorrt-50xx\ rmdir .\winpython-tensorrt-50xx\ /q /s
if exist install-log-tensorrt-50xx.txt del /q install-log-tensorrt-50xx.txt
if exist install-log-tensorrt-50xx-verbose.txt del /q install-log-tensorrt-50xx-verbose.txt
if exist .\neuralnet_models\640m-640.engine del /q .\neuralnet_models\640m-640.engine
if exist .\neuralnet_models\640m-1280.engine del /q .\neuralnet_models\640m-1280.engine
if exist .\neuralnet_models\640m-2560.engine del /q .\neuralnet_models\640m-2560.engine
if exist run-tensorrt-50xx.bat del /q run-tensorrt-50xx.bat
REM taken from https://stackoverflow.com/questions/20329355/how-to-make-a-batch-file-delete-itself to delete the uninstall file as well
(goto) 2>nul & if exist uninstall-tensorrt-50xx.bat del /q uninstall-tensorrt-50xx.bat
