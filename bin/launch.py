#!/usr/bin/env python 
#coding=utf-8
import os
import os.path
import sys
from Tkinter import *

from tkMessageBox import *

root=sys.argv[1]
rootdir = root+"mr"                                  
if(False==os.path.exists(rootdir)):
    os.mkdir(rootdir)
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
                    if os.path.exists(rootdir+"/"+dirname+"/config.txt"):
                        if fff.endswith('mr'):
                            print " run command : ",commmd
                            os.system(commmd)
                    else:
                        print "Error, config.txt file is missing...path:"+rootdir+"/"+dirname+"/config.txt"
                        #message = "错误，缺少config.txt 配置文件...路径:"+rootdir+"/"+dirname+"/config.txt"
                            #break
                    #print "filename is: " + fff
            if(len(ff)==0):
                #showerror("错误", "mr目录下 " + dirname+"目录里面没有测试脚本，请参考mr_samples目录下面的测试脚本目录添加文件")
                print "dir " + dirname+" missing mr script files,please copy inner dir from mr_samples "
        #print  "请先在mr目录下添加测试脚本目录，请参考mr_samples目录下面的测试脚本目录" 
        #for filename in filenames:                        
            #print "parent is: " + parent
            #print "filename is: " + filename
            #print "the full name of the file is: " + os.path.join(parent,filename)
        break
os.system("start "+root+"out\index.htm")