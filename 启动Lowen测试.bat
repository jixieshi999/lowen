set currentHour=%time:~0,2%
if "%time:~0,1%"==" " set currentHour=0%time:~1,1%
set currentTestName=_%date:~0,4%%date:~5,2%%date:~8,2%_%currentHour%%time:~3,2%%time:~6,2%
lowen -s  > %~dp0\out\log_%currentTestName%.txt