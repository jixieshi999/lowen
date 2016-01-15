###说明
lowen 基于monkeyrunner的android应用的自动化测试，并输出测试结果到html的框架
仿腾讯[utest](http://auto.utest.qq.com/)测试框架

代码有待完善，欢迎有兴趣的朋友一起讨论（目前报表里面使用echarts部分没有写数据处理逻辑，框架已搭好）
###主框架代码1
bin\lowen_play.bat
- 循环执行N个py脚本
- 1.初始化路径，时间
- 2.开启线程记录cpu，内存等日志
- 3.开启线程记录adb log日志
- 4.执行py脚本
- 5.批量处理截图加上水印（通过bin\ImageMarkClickLogo.jar）
- 6.关闭记录日志的线程（关闭窗口）
- 7.读取adb log日志 判断是否crash
- 8.输出html报表

###主框架代码2
bin\launch.py   
遍历mr文件夹下面的所有文件夹，执行mr子文件夹里面的所有mr脚本

###usage
例子1
- 修改mr子目录下面的config.txt配置文件
    + pkgkey 表示包名com.ebest.sfa.xxx
    + apkPathkey apk安装包路径E:/apk/SFA-2.1.0.1-1230-03-beta.apk
    + actkey apk启动activity 路径com.ebest.sfa.xxx/com.ebest.sfa.login.activity.LoginActivity
    + moudlekey 暂时没用到，可以扩展到脚本里面
- 运行lowen -s 开始测试

例子2
- mr目录下新建测试目录，同理例子1配置config.txt
- lowen -p 编辑mr脚本
- 运行lowen -s 开始测试

###mr脚本语法
- 点击：TOUCH|{'x':310,'y':326,'type':'downAndUp',}
- 输入：TYPE|{'message':'1001',}
- 按系统键：PRESS|{'name':'BACK','type':'downAndUp',}
- 滑动：DRAG|{'startx':55,'starty':461,'endx':72,'endy':183,}

	通过lowen -p 编辑mr脚本，可以得到手机屏幕截图，点击截图，得到某一点的坐标，写入到mr脚本里面;
	也可以直接导出到mr文件，但是导出不支持DRAG命令，需要手动编辑mr脚本添加DRAG命令
	详见mr目录下面的例子
	
###运行环境
- windows，安装sdk，jdk，python2.X
- 涉及到bat脚本，python脚本，java 开发，android sdk里面的monkeyrunner框架使用等

###MR脚本语法（滑动事件做了修改,#开头为注释）
- 点击事件：TOUCH|{'x':310,'y':326,'type':'downAndUp',}
- 输入事件：TYPE|{'message':'1001',}
- PRESS事件：PRESS|{'name':'BACK','type':'downAndUp',} PRESS|{'name':'MENU','type':'downAndUp',}
- 等待事件：WAIT|{'seconds':1.0,}
- DRAG事件：DRAG|{'startx':55,'starty':183,'endx':72,'endy':461,}

###部分文件介绍
1. monkey_recorder.py
  -  主要用于录制点击等事件的脚本

2. monkey_playback.py
  -  主要用于执行monkey_recorder.py录制的mr结尾的脚本

3. mr
  -  mr文件夹下面主要放录制的操作脚本
  -  sfadaka1.mr是sfa登陆到进入客户查询列表脚本-支持华为荣耀4A手机

注：如果运行中文乱码，需要将所有py脚本改为utf-8编码

4. testn.py 用于自动化随机模拟测试app的脚本，修改里面的启动app包名
	eg:
	G:\lowen>monkeyrunner tools\testn.py


5. bin\ImageMarkClickLogo.jar
  -  用于图片添加水印的工具包
  -  用法详见testn.py
	'java -jar '+basePath+'bin/ImageMarkClickLogo.jar -l -cl c=#00ECdF s=50 out='+outpath

6. bin\HtmlOutPutCore.jar  
  -  用于将测试结果生成html报表的工具包
  -  用法见bin\main.bat
	java -jar %basePath%\bin\HtmlOutPutCore.jar   out=%currentTestName% path=%basePath% -l apkPath=beta.apk aaptPath=%basePath%bin\aapt.exe result=%rrrstr% starttime=%starttime% endtime=%endtime%

注：如果输出html中文乱码，需要将所有html_model模板改为utf-8编码，jar里面控制的是utf-8编码

###eg:
  -  lowen -s
  -  ![启动命令](http://jixieshi999.github.io/lowen/cmd.jpg )



###demo 地址

- 链接1：[输出列表](http://jixieshi999.github.io/lowen/out/ )

- 链接2：[报表明细](http://jixieshi999.github.io/lowen/out/20160112_162509_SFA/sh.htm)
	
- 链接3：[apk 信息提取参考链接](http://energykey.iteye.com/blog/1856173)

####输出报表（目前报表里面使用echarts部分没有写数据处理逻辑，框架已搭好）
![输出报表](http://jixieshi999.github.io/lowen/detail.jpg )

####操作记录
![输出操作记录](http://jixieshi999.github.io/lowen/pic.jpg )
####输出错误日志
![输出错误日志](http://jixieshi999.github.io/lowen/log.jpg )
####输出报表列表
![输出报表列表](http://jixieshi999.github.io/lowen/list.jpg )
