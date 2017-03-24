#!/usr/bin/env python 
#coding=utf-8
import os
import os.path
import sys
import threading
from Tkinter import *
from time import ctime,sleep

from tkMessageBox import *


def doCommandByDevice(deviceid):
    if deviceid=='':
        return
    root=sys.argv[1]
    rootdir = root+"mr"                                  
    if(False==os.path.exists(rootdir)):
        os.mkdir(rootdir)
    print " run command : ",deviceid+" "+ctime()
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
                        print commmd
                        if os.path.exists(rootdir+"/"+dirname+"/config.txt"):
                            if fff.endswith('mr'):
                                print " run command : ",commmd," "+deviceid+" "+ctime()
                                os.system(commmd+" "+deviceid)
                        else:
                            print "Error, config.txt file is missing...path:"+rootdir+"/"+dirname+"/config.txt"+" "+ctime()
                            #message = "错误，缺少config.txt 配置文件...路径:"+rootdir+"/"+dirname+"/config.txt"
                                #break
                        #print "filename is: " + fff
                if(len(ff)==0):
                    #showerror("错误", "mr目录下 " + dirname+"目录里面没有测试脚本，请参考mr_samples目录下面的测试脚本目录添加文件")
                    print "dir " + dirname+" missing mr script files,please copy inner dir from mr_samples "+" "+ctime()
            #print  "请先在mr目录下添加测试脚本目录，请参考mr_samples目录下面的测试脚本目录" 
            #for filename in filenames:                        
                #print "parent is: " + parent
                #print "filename is: " + filename
                #print "the full name of the file is: " + os.path.join(parent,filename)
            break

def testtestCmd(deviceid):
    for i in range(10):
        print "I was listening to %s. %s" %(deviceid,ctime())
        sleep(3)
def testtest(deviceList):
    for i in range(10000):
        isrun=1
        for k in range(len(deviceList)):
            if deviceList[k].stopped:
                isrun=2
        if isrun==1:
            break
        sleep(10)
    print "end listening to  %s" %(ctime())
if __name__ == '__main__':

    filenames=os.getcwd()+"devices.txt"

    #构造附件1
    if os.path.exists(filenames):
        os.remove(filenames)
    os.system("adb devices > "+filenames)
    ss=''
    deviceList=[]
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
                ss=line.decode('gb2312').encode('utf-8')+'\n'
                deviceList.append(ss.split()[0])
        #print deviceList
    except Exception, e:  
        print str(e)

    threads = []
    for i in range(len(deviceList)):
        #t1 = threading.Thread(target=doCommandByDevice,args=(deviceList[i],))
        t1 = threading.Thread(target=doCommandByDevice,args=(deviceList[i],))
        print "device"  ,deviceList[i]
        #t1.setDaemon(True)
        t1.start()
        threads.append(t1)

    t1 = threading.Thread(target=testtest,args=(threads,))
    t1.setDaemon(True)
    #t1.start()
    #t1.join()
    print "------------------end------------------------------------------------------- \n "  