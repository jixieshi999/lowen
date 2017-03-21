title Lowen
@echo version 2.1
@echo off

::set basePath=g:\lwh\xwandou\code\monkeytest\
set basePath=%1
echo basePath:%basePath%
set mr=%2
set mrconfig=%3
set mrname=%4
set deviceid=%5
echo mr:%mr%
echo mrconfig:%mrconfig%
echo mrname:%mrname%
echo deviceid:%deviceid%



echo -
echo -
echo -

::-------------------------------------------------------step-1-----------------------------------------------------------------------------
echo ----%time%----1.初始化路径，时间-------------

::>>>> 此处路径需要修改 >>>>
echo                 pkg           表示测试的apk包名
::set pkg=com.ebest.sfa
CALL %basePath%bin\readConfig %mrconfig% pkgkey pkg 
ECHO %pkg%
echo                 apkPath       表示测试的apk路径
::set apkPath=E:/lwh/apk/SFADali-2.1.0.1-1230-03-beta.apk
CALL %basePath%bin\readConfig %mrconfig% apkPathkey apkPath 
echo                 act           表示测试的apk启动activity
::set act=com.ebest.sfa/com.ebest.sfa.login.activity.LoginActivity
CALL %basePath%bin\readConfig %mrconfig% actkey act 
echo                 mr            表示测试的apk录制的脚本路径
CALL %basePath%bin\readConfig %mrconfig% moudlekey moudleName 
::<<<< 此处路径需要修改 <<<<

set currentHour=%time:~0,2%
if "%time:~0,1%"==" " set currentHour=0%time:~1,1%
set currentTestName=%moudleName%_%mrname%_%deviceid%_%date:~0,4%%date:~5,2%%date:~8,2%_%currentHour%%time:~3,2%%time:~6,2%
set starttime=%date:~0,4%-%date:~5,2%-%date:~8,2%_%currentHour%:%time:~3,2%:%time:~6,2%
::set basePath=g:\lwh\xwandou\code\monkeytest\
if not exist %basePath%out\%currentTestName% mkdir %basePath%out\%currentTestName%


copy %apkPath% %basePath%out\%currentTestName%\
::-------------------------------------------------------step-1-----------------------------------------------------------------------------


echo ----------------------开始测试 %currentTestName%------------------------------------

::-------------------------------------------------------step-2-----------------------------------------------------------------------------
echo ----%time%----2.开启线程记录cpu，内存等日志-------------
start %basePath%\bin\apkinfo.bat %pkg% %basePath%out\%currentTestName% %deviceid%
::-------------------------------------------------------step-2-----------------------------------------------------------------------------


::-------------------------------------------------------step-3-----------------------------------------------------------------------------
echo ----%time%----3.开启线程记录adb log日志-------------
start %basePath%\bin\log.bat %basePath%out\%currentTestName% %deviceid%
::-------------------------------------------------------step-3-----------------------------------------------------------------------------


::-------------------------------------------------------step-4-----------------------------------------------------------------------------
echo ----%time%----4.执行py脚本-------------
::call monkeyrunner %basePath%tools\monkey_playbackNew.py %basePath%mr\sfadaka2.mr  %currentTestName%  %basePath%
::call monkeyrunner %basePath%tools\monkey_playbackNew.py %basePath%mr\kasfa_huawei_c199.mr  %currentTestName%  %basePath%
::call monkeyrunner %basePath%tools\monkey_playbackNew.py %basePath%mr\kasfa_huawei_c199_qingjia.mr  %currentTestName%  %basePath%
call monkeyrunner %basePath%tools\monkey_playbackNew.py pkg=%pkg% apkPath=%apkPath% act=%act%  mr=%mr%  name=%currentTestName%  basePath=%basePath% scale=scale screen=480.800 deviceid=%deviceid%  
::-------------------------------------------------------step-4-----------------------------------------------------------------------------


::-------------------------------------------------------step-5-----------------------------------------------------------------------------
echo ----%time%-----5.将照片添加水印------------------
java -jar %basePath%bin\ImageMarkClickLogo.jar  -cl c=#000000 s=50 out=%basePath%out\%currentTestName%\
::-------------------------------------------------------step-5-----------------------------------------------------------------------------


::-------------------------------------------------------step-6-----------------------------------------------------------------------------
echo ----%time%----6.关闭记录日志的线程（关闭窗口）-------------
taskkill  /FI "WINDOWTITLE eq AndroidInfo_%deviceid%"
taskkill  /FI "WINDOWTITLE eq AndroidMonkeyLog_%deviceid%"
::-------------------------------------------------------step-6-----------------------------------------------------------------------------


::-------------------------------------------------------step-7-----------------------------------------------------------------------------
echo ----%time%----7.读取adb log日志 判断是否crash-------------
set rrrstr=成功
findstr   %pkg% %basePath%out\%currentTestName%\androidlog.txt
set rrr=%errorlevel%
::if %rrr%==0 echo --------------------脚本(%currentTestName%)运行中Crash------------------- else echo 脚本(%currentTestName%)运行ok
if %rrr%==0 set rrrstr=失败|echo --------------------脚本(%currentTestName%)运行中Crash------------------- else echo 脚本(%currentTestName%)运行ok
::-------------------------------------------------------step-7-----------------------------------------------------------------------------


::-------------------------------------------------------step-8-----------------------------------------------------------------------------
echo ----%time%----8.输出html报表-------------
set currentHour=%time:~0,2%
if "%time:~0,1%"==" " set currentHour=0%time:~1,1%
set endtime=%date:~0,4%-%date:~5,2%-%date:~8,2%_%currentHour%:%time:~3,2%:%time:~6,2%
java -jar %basePath%\bin\HtmlOutPutCore.jar   out=%currentTestName% path=%basePath%  apkPath=%apkPath% aaptPath=%basePath%bin\aapt.exe result=%rrrstr% starttime=%starttime% endtime=%endtime%
::-------------------------------------------------------step-8-----------------------------------------------------------------------------

echo ----------------------结束测试 %currentTestName%------------------------------------






