#!/usr/bin/env monkeyrunner
#coding=utf-8
# Copyright 2010, The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import random
import time
import os
import threading
import signal
from com.android.monkeyrunner import MonkeyRunner

# The format of the file we are parsing is very carfeully constructed.
# Each line corresponds to a single command.  The line is split into 2
# parts with a | character.  Text to the left of the pipe denotes
# which command to run.  The text to the right of the pipe is a python
# dictionary (it can be evaled into existence) that specifies the
# arguments for the command.  In most cases, this directly maps to the
# keyword argument dictionary that could be passed to the underlying
# command. 

# Lookup table to map command strings to functions that implement that
# command.
# MonkeyDevice.touch(x,y,type)
# MonkeyDevice.type(message)
# MonkeyDevice.drag(start,end,duration,steps)
deviceid=''

CMD_MAP = {
    'TOUCH': lambda dev, arg: dev.touch(**arg),
    'DRAG': lambda dev, arg: dev.drag((int(arg["startx"]),int(arg["starty"])),(int(arg["endx"]),int(arg["endy"])),0.1,5),
    'PRESS': lambda dev, arg: dev.press(**arg),
    'TYPE': lambda dev, arg: dev.type(**arg),
    #'TYPE': lambda dev, arg: dev.shell(str(arg["message"])),
    'WAIT': lambda dev, arg: MonkeyRunner.sleep(**arg)
    }
CMD_MAPLog = {
    'TOUCH': lambda f,nowtimes, rest: f.write(nowtimes+'-'+str(rest["x"])+','+str(rest["y"])+'-touch('+str(rest["x"])+','+str(rest["y"])+')\n'),
    'DRAG': lambda f,nowtimes, rest: f.write(nowtimes+'-'+str(rest["startx"])+','+str(rest["starty"])+';'+str(rest["endx"])+','+str(rest["endy"])+'-from('+str(rest["startx"])+','+str(rest["starty"])+');to('+str(rest["endx"])+','+str(rest["endy"])+')\n'),
        
    'PRESS': lambda f,nowtimes, rest: f.write(nowtimes+'-100,500-press('+str(rest["name"])+')\n'),
    'TYPE': lambda f,nowtimes, rest: f.write(nowtimes+'-100,500-TYPE('+str(rest["message"])+')\n'),
    'WAIT': lambda f,nowtimes, rest: f.write(nowtimes+'-100,500-WAIT('+str(rest["seconds"])+')\n')
    }

def logToFile(logfile):
    os.system('adb logcat -v time -s AndroidRuntime > '+logfile)
# Process a single file for the specified device.
def process_file(fp, device,f,outpath):
    outImgpathName="img"
    for line in fp:
        if line.strip()=='':
            continue
        if line.startswith('#'):
            continue
        
        (cmd, rest) = line.split('|')
        try:
            # Parse the pydict
            rest = eval(rest)
        except:
            #print ' -------------debug:unable to parse options cmd --------------------- '
            print '< unknown command >: ',cmd,' ,unable to parse options ',rest
            continue

        if cmd not in CMD_MAP:
            print '< unknown command >: ',cmd
            continue
        #----------------------------------------------------------------------------------------------------------------------------
        #先保存照片截图
        nowtimes=time.strftime('%Y%m%d%H%M%S', time.localtime())
        result = device.takeSnapshot()
        result.writeToFile(outpath+outImgpathName+"/"+nowtimes+'.png','png');
        #----------------------------------------------------------------------------------------------------------------------------

        print '< start excute command >: ',cmd,' ,param : ',rest
        #执行模拟事件
        CMD_MAP[cmd](device, rest)

        
        #----------------------------------------------------------------------------------------------------------------------------
        #将命令写入到日志，用于给图片打码
        if cmd  in CMD_MAPLog:
            CMD_MAPLog[cmd](f,nowtimes, rest)
        #print 'unable to parse options',rest,type(rest)
        MonkeyRunner.sleep(2.0)
        #----------------------------------------------------------------------------------------------------------------------------
#处理缩放坐标的脚本
def process_file_scale(fp, device,f,outpath,rateX,rateY):
    outImgpathName="img"
    for line in fp:
        if line.strip()=='':
            continue
        if line.startswith('#'):
            continue
        
        (cmd, rest) = line.split('|')
        try:
            # Parse the pydict
            rest = eval(rest)
        except:
            #print ' -------------debug:unable to parse options cmd --------------------- '
            print '< unknown command >: ',deviceid,' ',cmd,' ,unable to parse options ',rest
            continue

        if cmd not in CMD_MAP:
            print '< unknown command >: ',deviceid,' ',cmd
            continue
        if cmd=='TOUCH':
            print '< old command >: ',deviceid,' ',rest
            rest["x"]=int(float(rest["x"])*rateX)
            rest["y"]=int(float(rest["y"])*rateY)
            print '< new command >: ',deviceid,' ',rest
        if cmd=='DRAG':
            print '< old command >: ',deviceid,' ',rest
            rest["startx"]=int(float(rest["startx"])*rateX)
            rest["starty"]=int(float(rest["starty"])*rateY)
            rest["endx"]=int(float(rest["endx"])*rateX)
            rest["endy"]=int(float(rest["endy"])*rateY)
            print '< new command >: ',deviceid,' ',rest
            
        #----------------------------------------------------------------------------------------------------------------------------
        #先保存照片截图
        nowtimes=time.strftime('%Y%m%d%H%M%S', time.localtime())
        result = device.takeSnapshot()
        result.writeToFile(outpath+outImgpathName+"/"+nowtimes+'.png','png');
        #----------------------------------------------------------------------------------------------------------------------------

        print '< start excute command >: ',deviceid,' ',cmd,' ,param : ',rest ," ",time.strftime('%Y%m%d%H%M%S', time.localtime())
        #执行模拟事件
        CMD_MAP[cmd](device, rest)

        
        #----------------------------------------------------------------------------------------------------------------------------
        #将命令写入到日志，用于给图片打码
        if cmd  in CMD_MAPLog:
            CMD_MAPLog[cmd](f,nowtimes, rest)
        #print 'unable to parse options',rest,type(rest)
        MonkeyRunner.sleep(2.0)
        #----------------------------------------------------------------------------------------------------------------------------


def exitGracefully(signum, frame):
    print "Exiting Gracefully..."
    filenames=os.getcwd()+deviceid+"devices.txt"

    #http://stackoverflow.com/questions/23416663/monkey-runner-throwing-socket-exception-broken-pipe-on-touuch/28070375#28070375
    #http://stackoverflow.com/questions/12208269/how-do-i-catch-socketexceptions-in-monkeyrunner
    #shell     23267 18413 1323768 27536 ffffffff b6e50b70 S com.android.commands.monkey
    if os.path.exists(filenames):
        os.remove(filenames)
    os.system("adb -s "+deviceid+" shell ps | grep monkey > "+filenames)
    ss=''
    try:
        #ss='修改版本号加内容如下：\n\n'
        for line in open(filenames):  
            if line.startswith('List of devices'):
                filepathhss=sys.argv[0]
            elif line.startswith('   '):
                filepathhss=sys.argv[0]
            elif line.strip()=='':
                filepathhss=sys.argv[0]
            else:
                ss=line.decode('gb2312').encode('utf-8')
                os.system("adb -s "+deviceid+" shell kill -9 "+ss.split()[1])
    except Exception, e:  
        print str(e)
    #subprocess.call(['./killmonkey.sh'])
    sys.exit(1)
def main():
    #file = sys.argv[1]
    signal.signal(signal.SIGINT, exitGracefully)
    global deviceid

    print('---------------------- start cmd --------------------------')
    
    #----------------------------------------------------------------------------------------------------------------------------
    #初始化系统路径
    #config path
    #currentTestName=time.strftime( '%Y%m%d_%H%M%S', time.localtime() )+'_SFA'
    #currentTestName=sys.argv[2]
    #basePath=sys.argv[3]
    #是否需要以基准分辨率缩放,默认800*480
    for argv in sys.argv:
        print ('< system args >  : '+deviceid+' '+argv  )
        if argv.startswith('mr='):
            file = argv[3:]
        if argv.startswith('basePath='):
            basePath = argv[9:]
        if argv.startswith('name='):
            currentTestName = argv[5:]
        if argv.startswith('screen='):
            baseWidth=argv[7:].split('.')[0]
            baseHeigth=argv[7:].split('.')[1]
        if argv.startswith('scale='):
            needScale=argv[6:]
            baseWidth='480'
            baseHeigth='800'
        if argv.startswith('pkg='):
            pkg=argv[4:]
        if argv.startswith('apkPath='):
            apkPath=argv[8:]
        if argv.startswith('act='):
            startActivity=argv[4:]
        if argv.startswith('deviceid='):
            deviceid=argv[9:]
            
    #print(needScale,baseWidth,baseHeigth)
    fp = open(file, 'r')
    #basePath="g:/lwh/xwandou/code/monkeytest/"
    #print('< system propory > time : '+currentTestName  )
    outpathName="out"
    outImgpathName="img"
    #basePath="g:/lwh/xwandou/code/monkeytest/"
    outpath=basePath+outpathName+"/"+currentTestName+"/"
    LOG_FILENAME=outpath+"log.txt"
    #makedirs
    os.makedirs(outpath+outImgpathName)
    #----------------------------------------------------------------------------------------------------------------------------


    device = MonkeyRunner.waitForConnection(50,deviceid)
    

    
    #device.removePackage ('com.ebest.sfa') 
    print('< system   > device : '+deviceid+' '+pkg +" "+time.strftime('%Y%m%d%H%M%S', time.localtime()) )
    device.removePackage (pkg) 
    #device.installPackage('E:/lwh/apk/SFADali-2.1.0.1-1230-03-beta.apk')
    device.installPackage(apkPath)
    #定义要启动的Activity  
    #componentName='com.motherbuy.bmec.android/com.motherbuy.bmec.android.WelcomeActivity'  
    #componentName='com.ebest.sfa/com.ebest.sfa.login.activity.LoginActivity'   
    componentName=startActivity  
    
    loffilepath=outpath+"adblog.txt"
    #logToFile(loffilepath)
    t1 = threading.Thread(target=logToFile,args=(loffilepath))
    t1.setDaemon(True)
    #t1.start()

    #启动特定的Activity  
    device.startActivity(component=componentName) 

    #----------------------------------------------------------------------------------------------------------------------------
    #获取系统参数
    ret = device.getProperty("build.device")
    print('< system propory > device : '+deviceid+' '+str(ret) +" "+time.strftime('%Y%m%d%H%M%S', time.localtime()) )
    screen_width = device.getProperty("display.width")
    print('< system propory > display.width : '+deviceid+' '+str(screen_width)+" "+time.strftime('%Y%m%d%H%M%S', time.localtime())  )
    screen_height = device.getProperty("display.height")
    print('< system propory > display.height : '+deviceid+' '+str(screen_height)+" "+time.strftime('%Y%m%d%H%M%S', time.localtime())  )
    #----------------------------------------------------------------------------------------------------------------------------







    MonkeyRunner.sleep(3.0)

    f=open(LOG_FILENAME,'w')

    
    if needScale.startswith('scale'):
        process_file_scale(fp, device,f,outpath,float(screen_width)/float(baseWidth),float(screen_height)/float(baseHeigth))
    else:
        process_file(fp, device,f,outpath)
        
    fp.close();


    #----------------------------------------------------------------------------------------------------------------------------
    #保存最后一次快照
    nowtimes=time.strftime('%Y%m%d%H%M%S', time.localtime())
    result = device.takeSnapshot()
    result.writeToFile(outpath+outImgpathName+"/"+nowtimes+'.png','png');
    f.write(nowtimes+'-100,500-final page\n')
    #----------------------------------------------------------------------------------------------------------------------------

    f.close()

    #----------------------------------------------------------------------------------------------------------------------------
    #将照片添加水印
    #cmdcommand='java -jar '+basePath+'bin/ImageMarkClickLogo.jar  -cl c=#ff0000 s=50 out='+outpath
    #cmdcommand='java -jar '+basePath+'bin/ImageMarkClickLogo.jar -l -cl c=#000000 s=50 out='+outpath
    #os.system(cmdcommand)
    #----------------------------------------------------------------------------------------------------------------------------

    
    #t1.stop()
    #t1.join()
    
    #os.system('taskkill  /FI "WINDOWTITLE eq AndroidMonkeyLog"')
    print('---------------------- end cmd ----'+deviceid+' '+'----------------------' +" "+time.strftime('%Y%m%d%H%M%S', time.localtime()))
    

if __name__ == '__main__':
    main()




