#!/usr/bin/env python 
#coding=utf-8
import os
import os.path
import sys
import threading
import time
import subprocess
from Tkinter import *

from tkMessageBox import *

#执行mr脚本到设备上
def doPlayCommanByDevice(deviceid,basePath,mr,mrconfig,mrname):

    starttime=time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(int(time.time()))) 
    ss=''
    deviceList={}
    #读取配置信息，存到字典map里面
    try:
        for line in open(mrconfig):  
            if line.startswith('List of devices'):
                filepathhss=sys.argv[0]
            elif line.startswith('#'):
                filepathhss=sys.argv[0]
            elif line.strip()=='':
                filepathhss=sys.argv[0]
            else:
                ss=line.decode('gb2312').encode('utf-8').replace('\n','')
                key=ss.split('=')[0]
                valueA=ss.split('=')[1]
                #print key+'___'+valueA
                deviceList[key]=valueA
    except Exception, e:  
        print str(e)
    #print deviceList
    #print basePath
    currentTestName=deviceList['moudlekey']+'_'+mrname.replace('.mr','')+'_'+deviceid.replace(':','_').replace('.','')+time.strftime("%Y%m%d_%H%M%S", time.localtime(int(time.time()))) 

    #初始化目录
    os.makedirs((basePath+'out\\'+currentTestName).replace('\\','/'))
    os.makedirs((basePath+'out\\'+currentTestName+'\cpuinfo').replace('\\','/'))
    os.makedirs((basePath+'out\\'+currentTestName+'\meminfo').replace('\\','/'))
    subprocess.call('copy '+deviceList['apkPathkey']+' '+' '+basePath+'out\\'+currentTestName+ ' ', shell=True)


    
    #subprocess.call('start '+basePath+r'bin\apkinfo.bat '+deviceList['pkgkey']+' '+basePath+'out\\'+currentTestName+' '+deviceid, shell=True)
    
    #echo ----%time%----2.开启线程记录cpu，内存等日志-------------
    stopevt= threading.Event()
    t1 = threading.Thread(target=doCatchMemInfo,args=(deviceid,deviceList['pkgkey'],basePath+'out\\'+currentTestName,stopevt))
    t1.start()

    #echo ----%time%----3.开启线程记录adb log日志-------------
    subprocess.call('start '+basePath+r'bin\log.bat '+basePath+'out\\'+currentTestName+' '+deviceid+' ', shell=True)


    subprocess.call('call monkeyrunner '+basePath+r'tools\monkey_playbackNew.py pkg='+deviceList['pkgkey']+' apkPath='+deviceList['apkPathkey']+' act='+deviceList['actkey']+'  mr='+mr+'  name='+currentTestName+'  basePath='+basePath+' scale='+deviceList['scalekey']+' screen='+deviceList['screenkey']+' deviceid='+deviceid+'  ', shell=True)


    #echo ----%time%-----5.将照片添加水印------------------
    subprocess.call('java -jar '+basePath+r'bin\ImageMarkClickLogo.jar  -cl c=#000000 s=50 out='+basePath+'out\\'+currentTestName+'\\', shell=True)
    
    #echo ----%time%----6.关闭记录日志的线程（关闭窗口）-------------
    #subprocess.call('taskkill  /FI "WINDOWTITLE eq AndroidInfo_"'+deviceid, shell=True)
    subprocess.call('taskkill  /FI "WINDOWTITLE eq AndroidMonkeyLog_"'+deviceid, shell=True)
    #关闭线程
    stopevt.set()

    #echo ----%time%----7.读取adb log日志 判断是否crash-------------
    rrrstr='1'
    try:
        #ss='修改版本号加内容如下：\n\n'
        for line in open(basePath+'out\\'+currentTestName+r'\androidlog.txt'):  
            if line.find(deviceList['pkgkey']):
                filepathhss=sys.argv[0]
                rrrstr='0'
                break;
    except Exception, e:  
        print str(e)


    #echo ----%time%----8.输出html报表-------------
    endtime=time.strftime("%Y%m%d_%H%M%S", time.localtime(int(time.time()))) 
    subprocess.call('java -jar '+basePath+r'bin\HtmlOutPutCore.jar   out='+currentTestName+' path='+basePath+'  apkPath='+deviceList['apkPathkey']+' aaptPath='+basePath+r'bin\aapt.exe result='+rrrstr+' starttime='+starttime+' endtime='+endtime, shell=True)



#抓取内存和cpu信息
def doCatchMemInfo(deviceid,pkg,out,stopevt):
    i = 0
    while not stopevt.isSet():
        time.sleep(1)
        endtime=time.strftime("%Y%m%d_%H%M%S", time.localtime(int(time.time()))) 
        #print 'adb -s '+deviceid+' shell dumpsys meminfo '+pkg+' |grep "TOTAL">>'+out+'\meminfo\\'+endtime+'meminfo.txt'+'     '+str(i)
        #print 'adb -s '+deviceid+' shell  top -n 1 -d 0.5 | grep '+pkg+'>>'+out+'\cpuinfo\\'+endtime+'cpuinfo.txt'
        subprocess.call('adb -s '+deviceid+' shell dumpsys meminfo '+pkg+' |grep "TOTAL">>'+out+'\meminfo\\'+endtime+'meminfo.txt', shell=True)
        subprocess.call('adb -s '+deviceid+' shell  top -n 1 -d 0.5 | grep '+pkg+'>>'+out+'\cpuinfo\\'+endtime+'cpuinfo.txt', shell=True)
        i=i+1

#遍历mr目录执行脚本
#deviceid为设备ID
def doCommandByDevice(deviceid):
    if deviceid=='':
        return
    root=sys.argv[1]
    rootdir = root+"mr"                                  
    if(False==os.path.exists(rootdir)):
        os.mkdir(rootdir)
    print " run command : ",deviceid+" "+time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(int(time.time()))) 
    for parent,dirnames,filenames in os.walk(rootdir):    
        #print "ds is: " + str(dirnames)+" fs:"+str(filenames)+" parent:"+parent+" r:"+rootdir
        if parent.endswith(rootdir):
            if(len(dirnames)==0):
                showerror("错误", "mr目录为空，请参考mr_samples目录下面的测试脚本目录添加文件")
                break
            for dirname in  dirnames:                        
            #print "parent is: " + parent #a你好
            #print  "----------dirname is: " + dirname
                for pp,dd,ff in os.walk(rootdir+"/"+dirname): 
                    #print  "dirname: "+dirname+" ----------dd is: " + dd
                    for fff in ff:
                        commmd=""+root+"bin/lowen_play.bat "+root+" "+rootdir+"/"+dirname+"/"+fff+" "+rootdir+"/"+dirname+"/config.txt"+" "+fff
                        #print commmd
                        if os.path.exists(rootdir+"/"+dirname+"/config.txt"):
                            if fff.endswith('mr'):
                                print " run command : ",commmd," "+deviceid+" "+time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(int(time.time()))) 
                                #os.system(commmd+" "+deviceid)
                                doPlayCommanByDevice(deviceid,root,rootdir+"/"+dirname+"/"+fff,rootdir+"/"+dirname+"/config.txt",fff)
                        else:
                            print "Error, config.txt file is missing...path:"+rootdir+"/"+dirname+"/config.txt"+" "+time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(int(time.time()))) 
                            #message = "错误，缺少config.txt 配置文件...路径:"+rootdir+"/"+dirname+"/config.txt"
                                #break
                        #print "filename is: " + fff
                if(len(ff)==0):
                    #showerror("错误", "mr目录下 " + dirname+"目录里面没有测试脚本，请参考mr_samples目录下面的测试脚本目录添加文件")
                    print "dir " + dirname+" missing mr script files,please copy inner dir from mr_samples "+" "+time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(int(time.time()))) 
            #print  "请先在mr目录下添加测试脚本目录，请参考mr_samples目录下面的测试脚本目录" 
            #for filename in filenames:                        
                #print "parent is: " + parent
                #print "filename is: " + filename
                #print "the full name of the file is: " + os.path.join(parent,filename)
            break

if __name__ == '__main__':

    filenames=os.getcwd()+"devices.txt"

    #读取系统连接N个设备名称
    if os.path.exists(filenames):
        os.remove(filenames)
    os.system("adb devices > "+filenames)
    ss=''
    deviceList=[]
    try:
        for line in open(filenames):  
            if line.startswith('List of devices'):
                filepathhss=sys.argv[0]
            elif line.startswith('   '):
                filepathhss=sys.argv[0]
            elif line.strip()=='':
                filepathhss=sys.argv[0]
            else:
                ss=line.decode('gb2312').encode('utf-8')+'\n'
                deviceList.append(ss.split()[0])
        print deviceList
    except Exception, e:  
        print str(e)

    #开启N个线程执行N个设备的脚本
    threads = []
    for i in range(len(deviceList)):
        t1 = threading.Thread(target=doCommandByDevice,args=(deviceList[i],))
        print "device"  ,deviceList[i]
        t1.start()
        threads.append(t1)

    for i in threads:
        i.join()
    print "------------------end------------------------------------------------------- \n "  