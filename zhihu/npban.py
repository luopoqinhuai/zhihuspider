# -*- coding: utf-8 -*-
"""
Created on Mon Aug 03 17:39:13 2015

@author: Reno
"""
from  renozhihu import *



class renozhihuclass:
    all_to_get=set()
    all_user_list=None
    user_to_get_file = "D:/astar/python/zhihu/user_to_get.txt"
    userinfo_url="D:/astar/python/zhihu/userinfo.txt"
    userinfo_counter_url="D:/astar/python/zhihu/userinfocounter.txt"
    userurl_counter_url="D:/astar/python/zhihu/userurlcounter.txt"
    error_url="D:/astar/python/zhihu/errors.txt"
    userinfo_counter=0
    userurl_counter=0
    # session = None
    soup = None
    myhtml=None
    mycounter=9900

    def __init__(self):
        f=open(self.user_to_get_file,'r')
        self.all_user_list=f.readlines()
        f.close()
        
        
        f=open(self.userinfo_counter_url,'r')
        self.userinfo_counter=int(f.read())
        f.close()
        
        f=open(self.userurl_counter_url,'r')
        self.userurl_counter=int(f.read())
        f.close()
        for ff in self.all_user_list:
            if ff.strip() in self.all_to_get:
                print ff,'repeated'
                raise "user urls repeated!!!!!"
            else:
                self.all_to_get.add(ff.strip())
                
    def checkIsRepeat(self,element):
        if element.strip() in self.all_to_get:
            return False
        else:
            return True
        
    def repeated_get_userurl(self):
        if len(self.all_user_list)<=self.userurl_counter:
            raise "user url num error"
        user = User(self.all_user_list[self.userurl_counter].strip())
        fees=user.get_followees()
        print "get followees over"
        fers=user.get_followers()
        print "get followers over"
        try:
            f=open(self.user_to_get_file,'a+')
            if fees is not None:
                for fee in fees:
                    if self.checkIsRepeat(fee[1]):
                        f.write(fee[1]+"\n")
                        self.all_user_list.append(fee[1]+"\n")
                        self.all_to_get.add(fee[1])
            if fers is not None:
                for fee in fers:
                    if self.checkIsRepeat(fee[1]):
                        f.write(fee[1]+"\n")
                        self.all_user_list.append(fee[1]+"\n")
                        self.all_to_get.add(fee[1])
            print "insert followers over"
            f=open(self.userurl_counter_url,'w')
            self.userurl_counter=self.userurl_counter+1
            f.write(str(self.userurl_counter))
            f.close()
            print "info : ",self.userinfo_counter
            print "url : ",self.userurl_counter
        except Exception,e:
            print e
    
    def repeated_get_userinfo(self):
        print "get one info"
        if len(self.all_user_list)<=self.userinfo_counter:
            raise "user info num error"
        user = User(self.all_user_list[self.userinfo_counter].strip())
        if user.iserror:
            f=open(self.error_url,'a+')
            f.write(self.all_user_list[self.userinfo_counter])
            f.close()
        else:
            data=user.get_user_info_toString()
            f=open(self.userinfo_url,'a+')
            f.write(data.encode("utf-8"))
            f.close()
            print "insert one info ",self.userinfo_counter
        f=open(self.userinfo_counter_url,'w')
        self.userinfo_counter=self.userinfo_counter+1
        f.write(str(self.userinfo_counter))
        f.close()
        print "info : ",self.userinfo_counter
        print "url : ",self.userurl_counter

    def mycycle(self):
        #temp=0
        while True:
            if len(self.all_user_list)<=self.userinfo_counter:
                self.repeated_get_userurl()
            else:
                self.repeated_get_userinfo()
                
            #if temp>self.mycounter:
                    #break
            #temp=temp+1


a=renozhihuclass()
a.mycycle()
#a.repeated_get_userurl()
#print a.userurl_counter
#print a.userinfo_counter

#print a.all_to_get
#print a.all_user_list[0]




