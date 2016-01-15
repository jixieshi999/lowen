@title bat自动化编译

@echo off
@set version=2.1
@if '%1'=='' (
    goto help
)
@if %1==-v (
    echo  .
    python -V
    echo  .
    adb version
    echo  .
    echo Lowen版本号:%version%
    goto endBat
)

@if %1==-h (
    :help
    echo  -------------------帮助文档-------------------------
    echo  
    echo                  -v     版本号
    echo                  -h     帮助文档
    echo                  -p     启动自定义脚本录制
    echo                  -c     清除out目录
    echo                  -s     启动测试服务
    echo                  -monkey     启动monkey测试服务
    echo   
    echo  ----------------------------------------------------
    goto endBat
)

@if %1==-p (
    monkeyrunner %~dp0\tools\monkey_recorder.py
    goto endBat
)

@if %1==-s (
    ::call bin\main.bat %~dp0
    call python bin\launch.py %~dp0
)
@if %1==-c (
    rm -rf out
    goto endBat
)
:: echo 当前路径：%cd%
:: @echo 当前批处理全路径：%~f0
:: @echo 当前批处理目录路径：!cd!
:: echo 当前盘符：%~d0
:: echo 当前路径：%cd%
:: echo 当前执行命令行：%0
:: echo 当前bat文件路径：%~dp0
:: echo 当前bat文件短路径：%~sdp0

    


pause
:endBat