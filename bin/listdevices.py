# coding=utf-8
'''
发送带附件邮件
小五义：http://www.cnblogs.com/xiaowuyi
'''

import os
import os.path
import sys
import time


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

except Exception, e:  
    print str(e)

for i in range(len(deviceList)):
    print i,deviceList[i]