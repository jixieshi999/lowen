#!/usr/bin/env python 
#coding=utf-8
import sys
import random
import time
import os
import logging
from com.android.monkeyrunner import MonkeyRunner as mr
from com.android.monkeyrunner import MonkeyDevice 
from com.android.monkeyrunner import MonkeyImage as mi

print('---------------------- end start --------------------------')




currentTestName=sys.argv[1]
basePath=sys.argv[2]
#basePath="g:/lwh/xwandou/code/monkeytest/"
#currentTestName=time.strftime( '%Y%m%d_%H%M%S', time.localtime() )+'_MMG'
print('< system propory > currentTestName : '+currentTestName  )




device = mr.waitForConnection()
if not device:
    print >> sys.stderr,"fail"
    sys.exit(1)

#定义要启动的Activity  
componentName='com.motherbuy.bmec.android/com.motherbuy.bmec.android.WelcomeActivity'  
#启动特定的Activity  
device.startActivity(component=componentName) 


ret = device.getProperty("build.device")
print('< system propory > build.device : '+str(ret)  )
screen_width = device.getProperty("display.width")
print('< system propory > display.width : '+str(screen_width)  )
screen_height = device.getProperty("display.height")
print('< system propory > display.height : '+str(screen_height)  )
#config path
outpathName="out"
outImgpathName="img"
outpath=basePath+outpathName+"/"+currentTestName+"/"
LOG_FILENAME=outpath+"log.txt"
#makedirs
os.makedirs(outpath+outImgpathName)


f=open(LOG_FILENAME,'w')



'''
阿斯顿
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
for i in range(0, 10):
	#先保存照片截图
	nowtimes=time.strftime('%Y%m%d%H%M%S', time.localtime())
	result = device.takeSnapshot()
	result.writeToFile(outpath+outImgpathName+"/"+nowtimes+'.png','png');


	#模拟随机操作，1点击，2双击，3滑动，4back
	actiontype= random.randint(1, 4)

	if actiontype == 1 or actiontype == 4 :
		
		locationx= random.randint(1, int(screen_width))
		locationy= random.randint(1, int(screen_height))
		print i," x:",locationx,",y:",locationy


		f.write(nowtimes+'-'+str(locationx)+','+str(locationy)+'-touch('+str(locationx)+','+str(locationy)+')\n')
		device.touch(locationy,locationy,MonkeyDevice.DOWN_AND_UP)
	elif  actiontype == 2:

		locationx= random.randint(1, int(screen_width))
		locationy= random.randint(1, int(screen_height))
		print i," x:",locationx,",y:",locationy


		f.write(nowtimes+'-'+str(locationx)+','+str(locationy)+'-double touch('+str(locationx)+','+str(locationy)+')\n')
		device.touch(locationy,locationy,MonkeyDevice.DOWN_AND_UP)
		mr.sleep(0.01)
		device.touch(locationy,locationy,MonkeyDevice.DOWN_AND_UP)
	elif  actiontype == 3:

		llx1= random.randint(1, int(screen_width))
		lly1= random.randint(1, int(screen_height))
		print i," x1:",llx1,",y1:",lly1

		locationx2= random.randint(1, int(screen_width))
		locationy2= random.randint(1, int(screen_height))
		print i," x2:",locationx2,",y2:",locationy2

		f.write(nowtimes+'-'+str(llx1)+','+str(lly1)+';'+str(locationx2)+','+str(locationy2)+'-from('+str(llx1)+','+str(lly1)+');to('+str(locationx2)+','+str(locationy2)+')\n')
		xy1=(llx1,lly1)
		xy2=(locationx2,locationy2)
		device.drag(xy1,xy2,0.1,5)
	
	mr.sleep(1.0)

# 打印0到4

#----------------------------------------------------------------------------------------------------------------------------
#保存最后一次快照
nowtimes=time.strftime('%Y%m%d%H%M%S', time.localtime())
result = device.takeSnapshot()
result.writeToFile(outpath+outImgpathName+"/"+nowtimes+'.png','png');
f.write(nowtimes+'-100,500-final page\n')
#----------------------------------------------------------------------------------------------------------------------------

f.close()
cmdcommand='java -jar '+basePath+'bin/ImageMarkClickLogo.jar  -cl c=#000000 s=50 out='+outpath
os.system(cmdcommand)
os.system('taskkill  /FI "WINDOWTITLE eq AndroidMonkeyLog"')
print('---------------------- end cmd --------------------------')

sys.exit(0)