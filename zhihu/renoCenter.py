# -*- coding: utf-8 -*-
"""
Created on Mon Aug 03 17:39:13 2015

@author: Reno
"""
from  renozhihu import *

###
#read num of lines from file
###



def checkIsRepeat(element):
    global all_to_get
    if element in all_to_get:
        return False
    else:
        all_to_get.add(element)
        return True
    



def readOneKofData(filename,offset,lenOfOnce):
    try:
        outdatas=[]
        print filename
        f=open(filename,'r')
        print "readover"
        datas=f.readlines()
        datalength=len(datas)
        if datalength<=offset:
            return [-1,[]]
        
        if datalength-offset<lenOfOnce:
            for i in range(offset,datalength-1):
                outdatas.append(datas[i])
            f.close()
            return [datalength-offset,outdatas]
        else:
            for i in range(offset,offset+lenOfOnce):
                outdatas.append(datas[i])
            f.close()
            return [lenOfOnce,outdatas]
    except Exception,e:
        print e


    
    

def recycle():
    global all_user_list
    NOW=open("latest",'r').read()
    NOW=int(NOW)
    print "NOW is ",NOW
    if NOW==0:
        reno=User("http://www.zhihu.com/people/lei-nuo-reno")
        info = reno.get_user_info_toString()
        userinfo=open("D:/astar/python/zhihu/userinfo.txt",'a+')
        userinfo.write(info)
        userinfo.close()

        followees=reno.get_followees()
        print "get followees over"
        followers=reno.get_followers()
        print "get followers over"
        try:
            f=open("user_to_get.txt",'a+')
            if followees is not None:
                for fee in followees:
                    if checkIsRepeat(fee[1]):
                        f.write(fee[1]+"\n")
            print "insert followees over"
            
            if followers is not None:
                for fee in followers:
                    if checkIsRepeat(fee[1]):
                        f.write(fee[1]+"\n")
            print "insert followers over"
            f.close()
            f2=open("latest",'w')
            f2.write(str(NOW+1))
            f2.close()
        except Exception,e:
            print e
    else:
        reno=User(all_user_list[NOW].strip())
        info = reno.get_user_info_toString()
        userinfo=open("userinfo.txt",'a+')
        userinfo.write(info)
        userinfo.close()
            
        followees=reno.get_followees()
        print "get followees over"
        followers=reno.get_followers()
        print "get followers over"
        try:
            f=open("user_to_get.txt",'a+')
            if followees is not None:
                for fee in followees:
                    if checkIsRepeat(fee[1]):
                        f.write(fee[1]+"\n")
            if followers is not None:
                for fee in followers:
                    if checkIsRepeat(fee[1]):
                        f.write(fee[1]+"\n")
            print "insert followers over"
            f2=open("latest",'w')
            f2.write(str(NOW+1))
            f2.close()
        except Exception,e:
            print e

class renozhihu:
    all_to_get=set()
    all_user_list=None
    user_to_get_file = "D:/astar/python/zhihu/userinfo.txt"
    # session = None
    soup = None
    myhtml=None

    def __init__(self):
        f=open(self.user_to_get_file,'r')
        self.all_user_list=f.readlines()
        f.close()
        for ff in self.all_user_list:
            if True:
                raise "adads"
            else:
                all_to_get.add(ff)

    
a=renozhihu()
#print len(all_user_list),len(all_to_get)
#if len(all_user_list)==len(all_to_get):
#    for i in range(MAXNUM):
#        recycle()  
#    print "ok"    
#else:
#    print '??'
#    pass

