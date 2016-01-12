set localP=%~sdp0config.txt
for /f "skip=1 tokens=1,2 delims==" %%a IN (%localP%) Do if %1==%%a set %2=%%b& @echo readconfig get %%a, value is %%b
goto :eof