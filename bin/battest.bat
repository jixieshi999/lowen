title bat自动化编译
@echo 当前路径：%cd%
@echo 当前批处理全路径：%~f0
@echo 当前批处理目录路径：!cd!
echo 当前盘符：%~d0
echo 当前路径：%cd%
echo 当前执行命令行：%0
echo 当前bat文件路径：%~dp0
echo 当前bat文件短路径：%~sdp0

rem----------------------------我是分割线------------------------------------------------------

rem cd g:/lwh/battest
set localP=%~sdp0
rem 进入bat文件夹所在盘符
%localP:~0,2%
rem 进入bat文件夹所在目录
cd %localP%

rem----------------------------我是分割线------------------------------------------------------

@echo ***************初始化目录***************

rem rm -rf xlstest
rem mkdir xlstest
rm -rf release

mkdir release


rem----------------------------我是分割线------------------------------------------------------

@echo ***************读取配置的svn目录***************

CALL readConfig svnpath svnpathValue 
ECHO %svnpathValue%


CALL readConfig propath propathValue 
ECHO %propathValue%

CALL readConfig versionName versionNameValue 
ECHO %versionNameValue%

CALL readConfig versionCode versionCodeValue 
ECHO %versionCodeValue%

rem----------------------------我是分割线------------------------------------------------------

@echo ***************拉取代码测试***************
if EXIST .\%propathValue% (echo %propathValue%文件已存在) else ( svn co %svnpathValue% %propathValue%)
cd %propathValue%
svn update
rm -rf AndroidManifestNew.xml

rem----------------------------我是分割线------------------------------------------------------

@echo ***************修改编译版本号，渠道等***************
rem sed  's/android:versionName="\(.*\)"/android:versionName="%versionNameValue%"/g' AndroidManifest.xml >>AndroidManifestNew.xml
rem -i表示修改源文件
rem sed  -i 's/android:versionName="\[\\d\\.\]*"/android:versionName="%versionNameValue%"/g' AndroidManifest.xml 
sed  -i 's/android:versionName="\(.*\)"/android:versionName="%versionNameValue%"/g;s/android:versionCode="\(.*\)"/android:versionCode="%versionCodeValue%"/g' AndroidManifest.xml



rem sed  -i 's/android:versionCode="[\\d\\.]*"/android:versionCode="%versionCodeValue%"/g' AndroidManifest.xml  
rem sed  -i 's/android:versionCode"\(.*\)"/android:versionCode="%versionCodeValue%"/g' AndroidManifest.xml  


rem----------------------------我是分割线------------------------------------------------------

@echo ***************start表示开新CMD窗口运行，不阻塞当前流程（相当于线程）***************
rem start ant release
@echo ***************开始编译版本***************
rem ant release

cd ..

@echo ***************复制文件命令***************
rem 这里当编译完成之后查看bin文件夹里面是否有release.apk文件则知道是否编译成功
if EXIST .\%propathValue%\问题列表.xlsx copy /y .\%propathValue%\问题列表.xlsx .\release\%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%.apk


pause