::set localP=%~sdp0config.txt
set localP=%1
for /f "skip=1 tokens=1,2 delims==" %%a IN (%localP%) Do if %2==%%a set %3=%%b& @echo readconfig get %%a, value is %%b
goto :eof