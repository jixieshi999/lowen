title bat自动化编译
@echo 当前路径：%cd%
@echo 当前批处理全路径：%~f0
@echo 当前批处理目录路径：!cd!
echo 当前盘符：%~d0
echo 当前路径：%cd%
echo 当前执行命令行：%0
echo 当前bat文件路径：%~dp0
echo 当前bat文件短路径：%~sdp0

call bin\main.bat %~dp0
pause