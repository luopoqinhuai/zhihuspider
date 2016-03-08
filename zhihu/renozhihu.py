# -*- coding: utf-8 -*-
'''
  
                $$                                                               
              $$$                                    &&&&$$$$##$$$$$$$$$$$$$$$$$$#$$$           
             $$$              $$$$$$$$$$$$$$$        ##$$$$$$$$$$$$$$$$$$o;       ;             
            $$$$$$$$$$$$$$$  $$$$$$$$$$$$$$$                      *$$o           #             
           $$$    $$$        $$$         $$$          $$$         *$$o        $$$$             
          $$*     $$$        $$$         $$$           $$$$       *$$o       $$$$              
                  $$$        $$$         $$$            $$$$      *$$o     $$$$                
                  $$o        $$$         $$$              $$$     *$$o    $$$o                 
          ;$$$$$$$$$$$$$$$$  $$$         $$$                      *$$o                         
          $$$$$$$$$$$$$$$$$* $$$         $$$     ;$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$         
                 $$$         $$$         $$$                      *$$o                         
                 $$$         $$$         $$$                      *$$o                         
                $$$$$$$      $$$         $$$                      *$$o                         
               $$$;  $$$$    $$$         $$$                      *$$o                         
              $$$$     $$$   $$$$$ $$$$$$$$$                      *$$o                         
           $$$$!       $$      $$$$*                             $$$;                                                 
                                                                  $$$$$$                            
'''
#this need to be replace
mycookie='12c7958-851d-668803aee904; __uUFBQVlRSlZUZlZZdjFXVWpMSThrTGdBYVhTOFBFTU8xTkczMEVVVXhnPT0=|1438601709|84146b376e8ec7c7b62e5c4e0797fb2fc8199e90"; _xsrf=6c28075085379dd72d8080b1a28ded81; __utma=51854390.760506789.1438601674.1438601674.1438601674.1; __utmb=51854390.6.10.1438601674; __utmc=51854390; __utmz=51854390.1438601674.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/21358581; __utmv=51854390.100-1|2=registration_date=20140412=1^3=entry_date=20140412=1'

import urllib2 ,urllib
from bs4 import BeautifulSoup
import platform

import re
import json


from StringIO import StringIO
import gzip

request = urllib2.Request('http://outofmemory.cn/')

class User:
    user_url = None
    # session = None
    soup = None
    myhtml=None
    iserror=False

    def __init__(self, user_url, user_id=None):
        if user_url == None:
            self.user_id = "匿名用户"
        elif user_url[0:28] != "http://www.zhihu.com/people/":
            raise ValueError("\"" + user_url + "\"" + " : it isn't a user url.")
        else:
            self.user_url = user_url
            if user_id != None:
                self.user_id = user_id
            try:
                self.login_get_soup()
            except:
                iserror=True

    def login_get_soup(self):
        print self.user_url,'\n\n'
        self.getmysoup(self.user_url) 
    
    
    def getmysoup(self,thisurl):
        request = urllib2.Request(thisurl) 
        request.add_header('Cookie',mycookie)
        request.add_header('User-Agent', 'fake-client') 
        request.add_header('Accept-encoding', 'gzip')
        response = urllib2.urlopen(request)
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            self.myhtml = f.read()
            self.soup = BeautifulSoup(self.myhtml,"html.parser")
    
    
    def get_user_info(self):
        #data format name url sex location
        resdatas=[]
        resdatas.append(self.get_user_id())
        resdatas.append(self.user_url)
        self.login_get_soup()
        
        try:
            sex=str(self.soup.find("span",class_="item gender").i)
            if 'icon-profile-male' in sex:
                resdatas.append("male")
            elif 'icon-profile-female' in sex:
                resdatas.append("female")
            else :
                resdatas.append("Do not know")
        except:
            resdatas.append("Do not know")
        try:
            location=self.soup.find("span",class_="location item").string
        except:
            location="no location"
        resdatas.append(location)
        resdatas.append(str(self.get_collections_num()))
        resdatas.append(str(self.get_answers_num()))
        resdatas.append(str(self.get_asks_num()))
        resdatas.append(str(self.get_thanks_num()))
        resdatas.append(str(self.get_agree_num()))
        resdatas.append(str(self.get_followers_num()))
        twos=self.get_zhuanlan_num()
        resdatas.append(str(twos[0]))
        resdatas.append(str(twos[1]))
        return resdatas
    
    def get_user_info_toString(self):
        datas=self.get_user_info()
        print datas
        outres=datas[0]
        outres=outres+"\t"
        length=len(datas)
        for i in range(1,length-1):
            outres=outres+datas[i]+"\t"
        outres=outres+datas[length-1]+"\n"
        return outres
        
        
    
        

    def get_user_id(self):
        if self.user_url == None:
            # print "I'm anonymous user."
            if platform.system() == 'Windows':
                return "匿名用户".decode('utf-8')
            else:
                return "匿名用户"
        else:
            if hasattr(self, "user_id"):
                if platform.system() == 'Windows':
                    return self.user_id.decode('utf-8')
                else:
                    return self.user_id
            else:
                if self.soup == None:
                    self.parser()
                soup = self.soup
                user_id = soup.find("div", class_="title-section ellipsis") \
                    .find("span", class_="name").string.encode("utf-8")
                self.user_id = user_id
                if platform.system() == 'Windows':
                    return user_id.decode('utf-8')
                else:
                    return user_id

    def get_followees_num(self):
        if self.user_url == None:
            print "I'm anonymous user."
            return 0
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            followees_num = int(soup.find("div", class_="zm-profile-side-following zg-clear") \
                                .find("a").strong.string)
            return followees_num

    def get_followers_num(self):
        if self.user_url == None:
            print "I'm anonymous user."
            return 0
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            followers_num = int(soup.find("div", class_="zm-profile-side-following zg-clear") \
                                .find_all("a")[1].strong.string)
            return followers_num

    def get_agree_num(self):
        if self.user_url == None:
            print "I'm anonymous user."
            return 0
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            agree_num = int(soup.find("span", class_="zm-profile-header-user-agree").strong.string)
            return agree_num

    def get_thanks_num(self):
        if self.user_url == None:
            print "I'm anonymous user."
            return 0
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            thanks_num = int(soup.find("span", class_="zm-profile-header-user-thanks").strong.string)
            return thanks_num

    def get_asks_num(self):
        if self.user_url == None:
            print "I'm anonymous user."
            return 0
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            asks_num = int(soup.find_all("span", class_="num")[0].string)
            return asks_num

    def get_answers_num(self):
        if self.user_url == None:
            print "I'm anonymous user."
            return 0
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            answers_num = int(soup.find_all("span", class_="num")[1].string)
            return answers_num

    def get_collections_num(self):
        if self.user_url == None:
            print "I'm anonymous user."
            return 0
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            collections_num = int(soup.find_all("span", class_="num")[3].string)
            return collections_num

    def get_zhuanlan_num(self):
        soup=self.soup
        fsp=soup.find_all("div",class_="zm-profile-side-section-title")
        try:
            zl=fsp[0].a.strong.string
            ht=fsp[1].a.strong.string
        except:
            try:
                zl=fsp[1].a.strong.string
                ht=fsp[2].a.strong.string
            except:
                zl=0
                ht=0
                return (0,0)
        zl_num=int(zl.split(" ")[0])
        ht_num=int(ht.split(" ")[0])
        return (zl_num,ht_num)


            
    def get_followees(self):
        allfollowees=[]
        if self.user_url == None:
            print "I'm anonymous user."
            return
        else:
            followees_num = self.get_followees_num()
            print followees_num
            if followees_num == 0:
                return
            else: 
                followee_url = self.user_url + "/followees"
                self.getmysoup(followee_url)
                soup=self.soup
                for i in xrange((followees_num - 1) / 20 + 1):
                    if i%5==0:
                        print "getting followers sum",followees_num," now is ",i*20
                    
                    if i == 0:
                        user_url_list = soup.find_all("h2", class_="zm-list-content-title")
                        for j in xrange(min(followees_num, 20)):
                            allfollowees.append(( user_url_list[j].a.string , user_url_list[j].a["href"]))
                    else:
                        post_url = "http://www.zhihu.com/node/ProfileFolloweesListV2"
                        _xsrf = soup.find("input", attrs={'name': '_xsrf'})["value"]
                        offset = i * 20
                        hash_id = re.findall("hash_id&quot;: &quot;(.*)&quot;},", self.myhtml)[0]
                        params = json.dumps({"offset": offset, "order_by": "created", "hash_id": hash_id})
                        data = {
                            '_xsrf': str(_xsrf),
                            'method': "next",
                            'params': params
                        }
                        request = urllib2.Request(post_url) 
                        request.add_header('Cookie',mycookie)
                        request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36')
                        request.add_header('Host', "www.zhihu.com")
                        request.add_header('Referer', self.user_url + "/followees")
                        request.add_header('Origin','http://www.zhihu.com')
                        para_data = urllib.urlencode(data)
                        request.add_data(para_data)
                        request.add_header('Accept-encoding', 'gzip')
                        response = urllib2.urlopen(request)
                        if response.info().get('Content-Encoding') == 'gzip':
                            buf = StringIO( response.read())
                            f = gzip.GzipFile(fileobj=buf)
                            htmldata = f.read()
                        else:
                            htmldata=""
                        encodedjson=eval(htmldata)
                        followee_list=encodedjson["msg"]
                        for j in xrange(min(followees_num - i * 20, 20)):
                            tocheckhtml=followee_list[j]
                            tocheckhtml=tocheckhtml.replace('\"','"')
                            tocheckhtml=tocheckhtml.replace('\/','/')
                            followee_soup = BeautifulSoup(tocheckhtml,"lxml")
                            user_link = followee_soup.find("h2", class_="zm-list-content-title").a
                            name=user_link.string
                            nameurl=user_link["href"]
                            if '\u' in name:
                               allfollowees.append(( eval('u'+'"'+name+'"'),nameurl))
                            else:
                                allfollowees.append(( name     ,nameurl))
                return allfollowees   

        
    def get_followers(self):
        allfollowers=[]
        if self.user_url == None:
            print "I'm anonymous user."
            return None
        else:
            followers_num = self.get_followers_num()
            if followers_num == 0:
                return None
            else:
                follower_url = self.user_url + "/followers"
                self.getmysoup(follower_url)
                soup=self.soup
                for i in xrange((followers_num - 1) / 20 + 1):
                    if i%5==0:
                        print "getting followers sum",followers_num," now is ",i*20
                    if i == 0:
                        user_url_list = soup.find_all("h2", class_="zm-list-content-title")
                        for j in xrange(min(followers_num, 20)):
                            allfollowers.append(( user_url_list[j].a.string , user_url_list[j].a["href"]))
                    else:
                        post_url = "http://www.zhihu.com/node/ProfileFollowersListV2"
                        _xsrf = soup.find("input", attrs={'name': '_xsrf'})["value"]
                        offset = i * 20
                        hash_id = re.findall("hash_id&quot;: &quot;(.*)&quot;},", self.myhtml)[0]
                        params = json.dumps({"offset": offset, "order_by": "created", "hash_id": hash_id})
                        data = {
                            '_xsrf': str(_xsrf),
                            'method': "next",
                            'params': params
                        }
                        request = urllib2.Request(post_url) 
                        request.add_header('Cookie',mycookie)
                        request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36')
                        request.add_header('Host', "www.zhihu.com")
                        request.add_header('Referer', follower_url)
                        request.add_header('Origin','http://www.zhihu.com')
                        para_data = urllib.urlencode(data)
                        request.add_data(para_data)
                        request.add_header('Accept-encoding', 'gzip')
                        response = urllib2.urlopen(request)
                        if response.info().get('Content-Encoding') == 'gzip':
                            buf = StringIO( response.read())
                            f = gzip.GzipFile(fileobj=buf)
                            htmldata = f.read()                        
                        else:
                            htmldata=""
                        encodedjson=eval(htmldata)
                        followee_list=encodedjson["msg"]
                        for j in xrange(min(followers_num - i * 20, 20)):
                            tocheckhtml=followee_list[j]
                            tocheckhtml=tocheckhtml.replace('\"','"')
                            tocheckhtml=tocheckhtml.replace('\/','/')
                            followee_soup = BeautifulSoup(tocheckhtml,"lxml")
                            user_link = followee_soup.find("h2", class_="zm-list-content-title").a
                            name=user_link.string
                            nameurl=user_link["href"]
                            if '\u' in name:
                                allfollowers.append(( eval('u'+'"'+name+'"'),nameurl))
                            else:
                                allfollowers.append(( name ,nameurl))
                return allfollowers                  
                





#
reno=User("http://www.zhihu.com/people/lei-nuo-reno")
#reno.get_followees()
print reno.get_user_info()
#datas=reno.get_user_info_toString()
#print type(datas)
#f=open("d:/test.txt",'a+')
#f.write(datas.encode("utf-8"))
#f.close()


#print reno.get_user_id()
#print u'收藏' ,reno.get_collections_num()
#print u'回答' ,reno.get_answers_num()
#print u'提问' ,reno.get_asks_num()
#print u'感谢' ,reno.get_thanks_num()
#print u'赞同' ,reno.get_agree_num()
#print u'被关注' ,reno.get_followers_num()
#print u'关注' ,reno.get_followees_num()



