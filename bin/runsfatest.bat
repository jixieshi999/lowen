@echo 执行sfa 录制脚本测试

echo ----------------------开始测试sfa------------------------------------

set currentTestName=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%_SFA
set basePath=g:\lwh\xwandou\code\monkeytest\

mkdir g:\lwh\xwandou\code\monkeytest\out\%currentTestName%
start log.bat g:\lwh\xwandou\code\monkeytest\out\%currentTestName%
@echo tasklist /FI "WINDOWTITLE eq AndroidMonkeyLog"
call monkeyrunner g:\lwh\xwandou\code\monkeytest\tools\monkey_playbackNew.py G:\lwh\xwandou\code\monkeytest\mr\sfadaka2.mr  %currentTestName%  %basePath%

echo ----------------------结束测试sfa------------------------------------

pause