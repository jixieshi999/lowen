@echo 执行monkey随机测试

echo ----------------------开始测试妈妈购---------------------------------
set currentTestName=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%_MMG
set basePath=g:\lwh\xwandou\code\monkeytest\

::currentTestName表示每一次执行测试脚本的out输出主目录
echo currentTestName:%currentTestName%
mkdir g:\lwh\xwandou\code\monkeytest\out\%currentTestName%
::将写入日志文件夹路径当作参数传给log.bat
start log.bat g:\lwh\xwandou\code\monkeytest\out\%currentTestName%
::此处直接执行monkeyrunner命令，会导致后面的批处理无法运行，需要使用call命令
call monkeyrunner g:\lwh\xwandou\code\monkeytest\tools\monkey_test.py %currentTestName% %basePath%

echo ----------------------结束测试妈妈购---------------------------------
pause