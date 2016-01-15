title bat自动化编译

@echo 主入口文件
@echo off
echo 改文件已经废弃，使用bin\launch.py遍历启动mr目录下面所有的脚本------------

::set basePath=g:\lwh\xwandou\code\monkeytest\
set basePath=%1
echo basePath:%basePath%



echo -
echo -
echo -
echo ----------------------开始测试sfa------------------------------------

::-------------------------------------------------------step-1-----------------------------------------------------------------------------
echo ----%time%----1.初始化路径，时间-------------

::>>>> 此处路径需要修改 >>>>
echo                 pkg           表示测试的apk包名
set pkg=com.ebest.sfa
echo                 apkPath       表示测试的apk路径
set apkPath=E:/lwh/apk/SFADali-2.1.0.1-1230-03-beta.apk
echo                 act           表示测试的apk启动activity
set act=com.ebest.sfa/com.ebest.sfa.login.activity.LoginActivity
echo                 mr            表示测试的apk录制的脚本路径
set mr=%basePath%mr\kasfa_SCH-I869_qingjia.mr
::<<<< 此处路径需要修改 <<<<

set currentHour=%time:~0,2%
if "%time:~0,1%"==" " set currentHour=0%time:~1,1%
set currentTestName=%date:~0,4%%date:~5,2%%date:~8,2%_%currentHour%%time:~3,2%%time:~6,2%_SFA
set starttime=%date:~0,4%-%date:~5,2%-%date:~8,2%_%currentHour%:%time:~3,2%:%time:~6,2%
::set basePath=g:\lwh\xwandou\code\monkeytest\
if not exist %basePath%out\%currentTestName% mkdir %basePath%out\%currentTestName%


::-------------------------------------------------------step-1-----------------------------------------------------------------------------



::-------------------------------------------------------step-2-----------------------------------------------------------------------------
echo ----%time%----2.开启线程记录cpu，内存等日志-------------
start %basePath%\bin\apkinfo.bat %pkg% %basePath%out\%currentTestName%
::-------------------------------------------------------step-2-----------------------------------------------------------------------------


::-------------------------------------------------------step-3-----------------------------------------------------------------------------
echo ----%time%----3.开启线程记录adb log日志-------------
start %basePath%\bin\log.bat %basePath%out\%currentTestName%
::-------------------------------------------------------step-3-----------------------------------------------------------------------------


::-------------------------------------------------------step-4-----------------------------------------------------------------------------
echo ----%time%----4.执行py脚本-------------
::call monkeyrunner %basePath%tools\monkey_playbackNew.py %basePath%mr\sfadaka2.mr  %currentTestName%  %basePath%
::call monkeyrunner %basePath%tools\monkey_playbackNew.py %basePath%mr\kasfa_huawei_c199.mr  %currentTestName%  %basePath%
::call monkeyrunner %basePath%tools\monkey_playbackNew.py %basePath%mr\kasfa_huawei_c199_qingjia.mr  %currentTestName%  %basePath%
call monkeyrunner %basePath%tools\monkey_playbackNew.py pkg=%pkg% apkPath=%apkPath% act=%act%  mr=%mr%  name=%currentTestName%  basePath=%basePath% scale=scale screen=480.800 
::-------------------------------------------------------step-4-----------------------------------------------------------------------------


::-------------------------------------------------------step-5-----------------------------------------------------------------------------
echo ----%time%-----5.将照片添加水印------------------
java -jar %basePath%bin\ImageMarkClickLogo.jar  -cl c=#000000 s=50 out=%basePath%out\%currentTestName%\
::-------------------------------------------------------step-5-----------------------------------------------------------------------------


::-------------------------------------------------------step-6-----------------------------------------------------------------------------
echo ----%time%----6.关闭记录日志的线程（关闭窗口）-------------
taskkill  /FI "WINDOWTITLE eq AndroidInfo"
taskkill  /FI "WINDOWTITLE eq AndroidMonkeyLog"
::-------------------------------------------------------step-6-----------------------------------------------------------------------------


::-------------------------------------------------------step-7-----------------------------------------------------------------------------
echo ----%time%----7.读取adb log日志 判断是否crash-------------
set rrrstr=成功
findstr   "com.ebest.sfa" %basePath%out\%currentTestName%\androidlog.txt
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

echo ----------------------结束测试sfa------------------------------------




echo -
echo -
echo -

echo ----------------------开始测试妈妈购---------------------------------
::-------------------------------------------------------step-1-----------------------------------------------------------------------------
echo ----%time%----1.初始化路径，时间-------------

::>>>> 此处路径需要修改 >>>>
::pkg 表示测试的apk包名
set pkg=com.motherbuy.bmec.android
::apkPath 表示测试的apk路径
set apkPath=G:/lwh/zhenkun/B2C1.apk
::act 表示测试的apk启动activity
set act=com.motherbuy.bmec.android/com.motherbuy.bmec.android.WelcomeActivity
::mr 表示测试的apk录制的脚本路径
::set mr=%basePath%mr\kasfa_SCH-I869_qingjia.mr
::<<<< 此处路径需要修改 <<<<

set currentHour=%time:~0,2%
if "%time:~0,1%"==" " set currentHour=0%time:~1,1%
set currentTestName=%date:~0,4%%date:~5,2%%date:~8,2%_%currentHour%%time:~3,2%%time:~6,2%_MMG
set starttime=%date:~0,4%-%date:~5,2%-%date:~8,2%_%currentHour%:%time:~3,2%:%time:~6,2%
::currentTestName表示每一次执行测试脚本的out输出主目录

echo currentTestName:%currentTestName%
if not exist %basePath%out\%currentTestName% mkdir %basePath%out\%currentTestName%
::-------------------------------------------------------step-1-----------------------------------------------------------------------------


::-------------------------------------------------------step-2-----------------------------------------------------------------------------
echo ----%time%----2.开启线程记录cpu，内存等日志-------------
::开启运行内存cpu日志记录
start %basePath%\bin\apkinfo.bat %pkg% %basePath%out\%currentTestName%
::-------------------------------------------------------step-2-----------------------------------------------------------------------------


::-------------------------------------------------------step-3-----------------------------------------------------------------------------
echo ----%time%----3.开启线程记录adb log日志-------------
::将写入日志文件夹路径当作参数传给log.bat
start %basePath%\bin\log.bat %basePath%out\%currentTestName%
::-------------------------------------------------------step-3-----------------------------------------------------------------------------


::-------------------------------------------------------step-4-----------------------------------------------------------------------------
echo ----%time%----4.执行py脚本-------------
::此处直接执行monkeyrunner命令，会导致后面的批处理无法运行，需要使用call命令
call monkeyrunner %basePath%tools\monkey_test.py  name=%currentTestName%  basePath=%basePath% pkg=%pkg% apkPath=%apkPath% act=%act% 
::-------------------------------------------------------step-4-----------------------------------------------------------------------------


::-------------------------------------------------------step-5-----------------------------------------------------------------------------
echo ----%time%----5.将照片添加水印------------------
java -jar %basePath%bin\ImageMarkClickLogo.jar  -cl c=#000000 s=50 out=%basePath%out\%currentTestName%\
::-------------------------------------------------------step-5-----------------------------------------------------------------------------


::-------------------------------------------------------step-6-----------------------------------------------------------------------------
echo ----%time%----6.关闭记录日志的线程（关闭窗口）-------------
::关闭运行内存cpu日志记录
taskkill  /FI "WINDOWTITLE eq AndroidInfo"
taskkill  /FI "WINDOWTITLE eq AndroidMonkeyLog"
::-------------------------------------------------------step-6-----------------------------------------------------------------------------


::-------------------------------------------------------step-7-----------------------------------------------------------------------------
echo ----%time%----7.读取adb log日志 判断是否crash-------------
set rrrstr=成功
findstr   %pkg% %basePath%out\%currentTestName%\androidlog.txt

set rrr=%errorlevel%
if %rrr%==0 set rrrstr=失败|echo --------------------脚本(%currentTestName%)运行中Crash------------------- else echo 脚本(%currentTestName%)运行ok
::-------------------------------------------------------step-7-----------------------------------------------------------------------------



::-------------------------------------------------------step-8-----------------------------------------------------------------------------
echo ----%time%----8.输出html报表-------------
set currentHour=%time:~0,2%
if "%time:~0,1%"==" " set currentHour=0%time:~1,1%
set endtime=%date:~0,4%-%date:~5,2%-%date:~8,2%_%currentHour%:%time:~3,2%:%time:~6,2%
java -jar %basePath%\bin\HtmlOutPutCore.jar   out=%currentTestName% path=%basePath% -l   apkPath=%apkPath% aaptPath=%basePath%bin\aapt.exe result=%rrrstr% starttime=%starttime% endtime=%endtime%
::-------------------------------------------------------step-8-----------------------------------------------------------------------------

echo ----------------------结束测试妈妈购---------------------------------


echo -
echo -
echo -


:: 查找标题为AndroidMonkeyLog的进程
:: tasklist /FI "WINDOWTITLE eq AndroidMonkeyLog"
:: taskkill  /FI "WINDOWTITLE eq AndroidMonkeyLog"

pause


