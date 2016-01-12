import sys
from com.android.monkeyrunner import MonkeyRunner as mr
from com.android.monkeyrunner import MonkeyDevice 
from com.android.monkeyrunner import MonkeyImage as mi

device = mr.waitForConnection()
if not device:
    print >> sys.stderr,"fail"
    sys.exit(1)


device.touch(360,1069,MonkeyDevice.DOWN_AND_UP)
mr.sleep(1.0)
'''
是的
TOUCH|{'x':360,'y':1069,'type':'downAndUp',}
TOUCH|{'x':335,'y':1112,'type':'downAndUp',}
TOUCH|{'x':42,'y':485,'type':'downAndUp',}
TOUCH|{'x':40,'y':709,'type':'downAndUp',}
TOUCH|{'x':270,'y':794,'type':'downAndUp',}
TOUCH|{'x':477,'y':1104,'type':'downAndUp',}
TOUCH|{'x':542,'y':1133,'type':'downAndUp',}
TOUCH|{'x':375,'y':1136,'type':'downAndUp',}
TOUCH|{'x':236,'y':765,'type':'downAndUp',}
TOUCH|{'x':621,'y':549,'type':'downAndUp',}
TOUCH|{'x':654,'y':858,'type':'downAndUp',}
TOUCH|{'x':645,'y':541,'type':'downAndUp',}
'''


mr.sleep(3.0)
result = device.takeSnapshot()
 

#保存图片
result.writeToFile('g:/lwh/xwandou/code/monkeytest/shotend.png','png');

