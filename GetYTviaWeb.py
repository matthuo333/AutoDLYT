# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 21:19:20 2023

@author: Guang Huo
"""

from selenium import webdriver
from lxml import etree
#import requests
import time
import youtube_dl
import yt_dlp #not available on 2023 02 18 for main youtube-dl, so use this library
from os import rename
import re
import shutil

searchname = input("Please input a search name ： \n")



class YoutubeSearch(object) :


    #Inital for webdriver
    browser = webdriver.Chrome(r'C:\Users\matt_4215\Desktop\chromedriver_win32\chromedriver.exe')
    #browser.maximize_window()  
    #browser.get('https://www.youtube.com') 


    def GetSearcResults(self,searchname) :
    
        self.browser.get('https://www.youtube.com')
        time.sleep(8)
        
        input_box = self.browser.find_element_by_tag_name('input')
        try:
            input_box.send_keys(searchname)
            print('搜索KEY：',searchname)
        except Exception as e:
            print('fail')

        time.sleep(3)
        #定位搜索按钮
        button = self.browser.find_element_by_id('search-icon-legacy')
        try:
        #点击搜索按钮
            button.click()
            print('成功搜索')
        except Exception as e:
            print('fail搜索')

        time.sleep(5)
     

        source = self.browser.page_source

        html = etree.HTML(source)

        urllist = html.xpath('//h3//a[@id="video-title"]/@href')
        searchlist = html.xpath('//a[@id="video-title"]/@title')

        print("searchlist2 : ")
        j = 0
        for i in searchlist : 
            print("[",j,"]",searchlist[j])
            j += 1

        print("urllist2 : ")
        j = 0
        for i in urllist : 
            print("[",j,"]",urllist[j])
            j += 1
        #self.browser.quit()
        
        return searchlist,urllist

    def DownloadVideo(self,OptIndex,searchlist,urllist) :

        #OptIndex = input("\n Please input a search name ： \n")
        OptIndex = int(OptIndex)
        print("Old Filename :", searchlist[OptIndex])

        # Download video using Youtube-dl

        class MyLogger(object):
            def debug(self, msg):
                pass

            def warning(self, msg):
                pass

            def error(self, msg):
                print("matt error:",msg)

        def my_hook(d):
            if d['status'] == 'downloading':
                time = d['eta']
                # print(time)
                # m,s = divmod(time,60)
                # h,m = divmod(m,60)
                # print("%d:%02d:%02d"%(h,m,s))
                print('percent:{:.0%}'.format(d['downloaded_bytes']/d['total_bytes']))
                # print("剩余时间:{}".format(d['eta']))
                # print("已经下载:{}".format(d['downloaded_bytes']))
            elif d['status'] == 'finished':
                # specialChars = r'\/:*?*<>|"' # refer to https://zhuanlan.zhihu.com/p/343985720
                # for specialChar in specialChars:
                # searchlist[OptIndex] = searchlist[OptIndex].replace(specialChar, '')# refer to https://blog.csdn.net/SeeTheWorld518/article/details/47346143
                #newfilename = searchlist[OptIndex].strip()
                cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9^\b^\000^ ^-]")
                newfilename = cop.sub('', searchlist[OptIndex])
                print("New Filename :", newfilename)
                #file_name = r'/root/{}.mp4'.format(newfilename)
                file_name = r'D:\MattQsync\行业\NF+TVBOX\RSA\code\YT code\{}.mp4'.format(newfilename)
                
                rename(d['filename'], file_name)
                print('下载完成{}'.format(file_name))
                #shutil.move(file_name,r'D:\MattQsync\行业\NF+TVBOX\RSA\code\YT code\{}.mp4'.format(newfilename))
               # print("File move finished")


        ydl_opts = {
            #    'format': 'bestaudio/best',
            'outtmpl': '%(id)s%(ext)s',
            'format': 'best',
            #    'postprocessors': [{
            #        'key': 'FFmpegExtractAudio',
            #        'preferredcodec': 'mp3',
            #        'preferredquality': '192',
            #    }],
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
        }
        try :
            #with youtube_dl.YoutubeDL(ydl_opts) as ydl: # it is not available until 2023 02 18 due to 'Unable to extract uploader id'
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(['https://www.youtube.com/{}'.format(urllist[OptIndex])])
        except Exception as e:
            print('Download Fail')

matttest = YoutubeSearch()
(searchlist,urllist) = matttest.GetSearcResults(searchname)
OptIndex = input("\n Please input a search name ： \n")
matttest.DownloadVideo(OptIndex,searchlist,urllist)
