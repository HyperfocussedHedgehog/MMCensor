@echo off
if not exist .\mmc-home.txt ( echo "Do not run this directly, only run bat files in the main MMC folder" && pause && exit 2 )
@echo on
call bat_files/check-prereqs.bat
call bat_files/uninstall-tensorrt-50xx.bat
powershell -Command "Invoke-WebRequest https://github.com/winpython/winpython/releases/download/8.2.20240618final/Winpython64-3.12.4.1dot.exe -OutFile Winpython64-3.12.4.1dot.exe"
Winpython64-3.12.4.1dot.exe --help -o"winpython-tensorrt-50xx" -y
del Winpython64-3.12.4.1dot.exe
call winpython-tensorrt-50xx/WPy64-31241/scripts/env_for_icons.bat
pip debug --verbose
pip install -r installation_helpers/requirements_tensorrt-50xx.txt --extra-index-url https://download.pytorch.org/whl/cu128 --cache-dir pip-cache/ --extra-index-url https://pypi.nvidia.com --prefer-binary --log install-log-tensorrt-50xx-verbose.txt --verbose
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu128
cd mmc_code
python -m mmcensor.setup.make_engine
copy ..\bat_files\run-tensorrt-50xx.bat ..\run-tensorrt-50xx.bat
copy ..\bat_files\uninstall-tensorrt-50xx.bat ..\uninstall-tensorrt-50xx.bat
pause