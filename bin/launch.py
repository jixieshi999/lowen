#!/usr/bin/env python 
#coding=utf-8
import os
import os.path
import sys

root=sys.argv[1]
rootdir = root+"mr"                                  

for parent,dirnames,filenames in os.walk(rootdir):    
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
                    message = "Error, config.txt file is missing...path:"+rootdir+"/"+dirname+"/config.txt"
                    #break
                #print "filename is: " + fff
                #print "commmd is: " + commmd
        #print  "------------------------" 
    #for filename in filenames:                        
        #print "parent is: " + parent
        #print "filename is: " + filename
        #print "the full name of the file is: " + os.path.join(parent,filename)