#导入我们需要用到的包和类并且起别名
import sys
from com.android.monkeyrunner import MonkeyRunner as mr
from com.android.monkeyrunner import MonkeyDevice as md
from com.android.monkeyrunner import MonkeyImage as mi

#connect device 连接设备
#第一个参数为等待连接设备时间
#第二个参数为具体连接的设备
device = mr.waitForConnection(1.0,'emulator-5554')
if not device:
    print >> sys.stderr,"fail"
    sys.exit(1)
#定义要启动的Activity
componentName='kg.monkey/.MonkeyActivity'
#启动特定的Activity
device.startActivity(component=componentName)
mr.sleep(3.0)
#do someting 进行我们的操作
#输入 a s d
device.type('asd')
#输入回车
device.press('KEYCODE_ENTER')
#return keyboard 点击返回用于取消等下看到截图的下方的白条
#device.press('KEYCODE_BACK')
#------
#takeSnapshot截图
mr.sleep(3.0)
result = device.takeSnapshot()
 
#save to file 保存到文件
result.writeToFile('takeSnapshot\\result1.png','png');

