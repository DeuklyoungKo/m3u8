import sys
import string
import m3u8
import time
import json
from json import JSONDecodeError

import re
import m3u8
from m3u8 import protocol
from m3u8.parser import save_segment_custom_value

# ref) https://docs.python.org/ko/3/library/urllib.parse.html
from urllib.parse import urlparse
from urllib.parse import urljoin

# ref) https://stackoverflow.com/questions/54481532/is-there-a-way-to-get-a-webpages-network-activity-which-you-can-see-on-chrome
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options


print("program start")

# m3u8Url = "https://naver-mbc-c.smartmediarep.com/smc/naver/adaptive/eng/M12_CA202001140056/2f6d62632f6d6263706c75732f617263686976652f656e742f323032302f30312f31342f47413230323030313134303030332f43413230323030313134303035362f43413230323030313134303035362e736d696c/0-0-0/content_384000.m3u8?solexpire=1645704951&solpathlen=219&soltoken=27d91a462144651ca77d9cd69c33ab73&soltokenrule=c29sZXhwaXJlfHNvbHBhdGhsZW58c29sdXVpZA==&soluriver=2&soluuid=6d36e450-d52a-49fc-8116-4dc2bb59b872"
m3u8UrlListUrl = None
maxBandWidth = 0
targetM3u8Url = None
targetM3u8UrlSub = None
targetResolution = None

#yoururl = "https://tv.naver.com/v/23040889?plClips=false:24753153:23040889:22630198:1315359:22198415:21172127:21035217:24511820:24132678:19928208:21556883:19807223:18224818:16705764:24838042:25249830:14109927:14109438:14109796:14109277:14225544:14133915:14297198:14257891:14109928:14175749:14109504:14109506:14110013:14109573:14109574:12063149:9769769:19830142:14109732:24037483:10860633:5981667:8005752:14302908&query=%EC%B8%84"
yoururl = "https://www.pornhub.com/view_video.php?viewkey=ph5cd31b0635edf"






# TODO sample url of m3u8 file does not exist. check mp4 file
# yoururl = "https://tv.naver.com/v/14109438?plClips=false:24753153:23040889:22630198:1315359:22198415:21172127:21035217:24511820:24132678:19928208:21556883:19807223:18224818:16705764:24838042:25249830:14109927:14109438:14109796:14109277:14225544:14133915:14297198:14257891:14109928:14175749:14109504:14109506:14110013:14109573:14109574:12063149:9769769:19830142:14109732:24037483:10860633:5981667:8005752:14302908&query=%EC%B8%84"

print("yoururl : " + yoururl)


def get_perf_log_on_load(self, url, headless = True, filter = None):

    # init Chrome driver (Selenium)
    options = Options()
    options.headless = headless
    cap = DesiredCapabilities.CHROME
    cap['loggingPrefs'] = {'performance': 'ALL'}
    driver = webdriver.Chrome(executable_path="E:/Lecture/python/chromedriver_v98.exe", service_args=["--verbose", "--log-path=E:/Lecture/python/chromedriver.log"])

    # record and parse performance log
    driver.get(url)
    if filter: log = [item for item in driver.get_log('performance')
                      if filter in str(item)]
    else: log = driver.get_log('performance')
    driver.close()

    return log


'''
def checkListDataByJson(dataListJson,fileForWrite):
    dataType = type(dataListJson)
    print("dataType ==============================")
    print(dataType)
    print(dataListJson)
    fileForWrite.write("\n")
    fileForWrite.write("dataListJson ==============================")    
    fileForWrite.write("\n")
    fileForWrite.write(dataListJson)
'''


def check_list_data(dataList, fileForWrite):
    
    global m3u8UrlListUrl

    dataType = type(dataList)
    # print("dataType top ==============================")
    # print(dataType)
    # fileForWrite.write("\n")
    # fileForWrite.write("dataType top ============================== : ")
    # fileForWrite.write(str(dataType))


    # if(isinstance(dataType,list) or isinstance(dataType,dict) or isinstance(dataType,object)):
    if(isinstance(dataList,list)):
        for item in dataList:
            # print("dataType ============================== list")
            # fileForWrite.write("\n")
            # fileForWrite.write("dataType ============================== list")
            check_list_data(item,fileForWrite)
    elif(isinstance(dataList,dict)):
        for itemName, itemValue in dataList.items():
            # print("dataType ============================== dict")
            # fileForWrite.write("\n")
            # fileForWrite.write("dataType ============================== dict : itemName : ")
            # fileForWrite.write(itemName)
            check_list_data(itemValue,fileForWrite)

    elif(isinstance(dataList,str)):
        # print("dataType ============================== str")
        # fileForWrite.write("\n")
        # fileForWrite.write("dataType ============================== str")
        # fileForWrite.write("\n")
        # fileForWrite.write(dataList)
        # print(dataList)

        try:
            dataListJson = json.loads(dataList)
            # print("dataListJson ============================== type : ")
            # print(type(dataListJson))

            check_list_data(dataListJson,fileForWrite)

        except JSONDecodeError:
            # print("JSONDecodeError : ")
            # print(dataList)

            if(".m3u8" in dataList):
                fileForWrite.write("\n")
                fileForWrite.write(dataList)  
                print(".m3u8 file is found")
                if m3u8UrlListUrl is None:
                    m3u8UrlListUrl = dataList

    elif(isinstance(dataList,int)):
        # print("dataType ============================== int")
        # fileForWrite.write("\n")
        # fileForWrite.write("dataType ============================== int")        
        # fileForWrite.write("\n")
        # fileForWrite.write(str(dataList))        
        # print(str(dataList))
        pass

    else:
        # print("dataType ============================== else")
        # fileForWrite.write("\n")
        # fileForWrite.write("dataType ============================== else")        
        # fileForWrite.write("\n")
        # fileForWrite.write(str(dataType))
        # print(str(dataType))
        pass
    



#print(playlist)

# print(playlist.segments)
# print(playlist.target_duration)


# print("playlist.dumps()")
# print(playlist.dumps())

# if you already have the content as string, use

# playlist = m3u8.loads('#EXTM3U8 ... etc ... ')

# print("playlist.dumps()")
# print(playlist.dumps())

print("================================")
# result = get_perf_log_on_load(True,"https://tv.naver.com/v/23040889?plClips=false:24753153:23040889:22630198:1315359:22198415:21172127:21035217:24511820:24132678:19928208:21556883:19807223:18224818:16705764:24838042:25249830:14109927:14109438:14109796:14109277:14225544:14133915:14297198:14257891:14109928:14175749:14109504:14109506:14110013:14109573:14109574:12063149:9769769:19830142:14109732:24037483:10860633:5981667:8005752:14302908&query=%EC%B8%84")

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome(executable_path='E:/Lecture/python/chromedriver_v98.exe', desired_capabilities=caps, service_args=["--verbose", "--log-path=E:/Lecture/python/chromedriver.log"])
driver.get(yoururl)


time.sleep(5) # wait for all the data to arrive. 
# print("================================")
# perf = driver.get_log('performance')
# print(perf)

filter = "message"
if filter: perfs = [item for item in driver.get_log('performance')
                    if filter in str(item)]
else: perfs = driver.get_log('performance')
# print(perf)

with open('E:/Lecture/python/perf.txt', 'w') as f:
    f.write(str(perfs))
    f.close

with open('E:/Lecture/python/performance.txt', 'w') as f:
    print("network list check")
    check_list_data(perfs,f)
    f.close()

# print(type(driver.get_log('performance')))

# listSample = [1,2,3,4]
# print(type(listSample))
# print(isinstance(listSample,list))
driver.quit()

print("network list have checked")

print("m3u8UrlListUrl url ============================= ")
print(m3u8UrlListUrl)

if m3u8UrlListUrl is None:
    print("m3u8 file is not found")
    sys.exit(0)


print("get m3u8 Url List Url ===========================================")
m3u8UrlList = m3u8.load(m3u8UrlListUrl)  # this could also be an absolute filename

print(m3u8UrlList.dumps())


variant_m3u8 = m3u8.loads(m3u8UrlList.dumps())
variant_m3u8.is_variant    # in this case will be True

print("variant_m3u8.is_variant")

for playlist in variant_m3u8.playlists:
    print("playlist")
    print(playlist.uri)
    print(playlist.stream_info.bandwidth)

    if maxBandWidth < playlist.stream_info.bandwidth:
        maxBandWidth = playlist.stream_info.bandwidth
        targetM3u8UrlSub = playlist.uri

print("targetM3u8Url")
print(maxBandWidth)
print(targetM3u8UrlSub)

# for iframe_playlist in variant_m3u8.iframe_playlists:
#     print("playlist")
#     print(iframe_playlist.uri)
#     print(iframe_playlist.iframe_stream_info.bandwidth)    


m3u8UrlparseResult = urlparse(m3u8UrlListUrl)
m3u8UrlQuery = m3u8UrlparseResult.query
downloadPath = f'{m3u8UrlparseResult.scheme}://{m3u8UrlparseResult.netloc}{m3u8UrlparseResult.path}'

targetM3u8Url = urljoin(downloadPath,targetM3u8UrlSub)

print("get m3u8 Url ===========================================")
print("targetM3u8Url")
print(targetM3u8Url)

targetPlaylist = m3u8.load(targetM3u8Url)  # this could also be an absolute filename


print("targetPlaylist.dumps()")
print(targetPlaylist.dumps())

targetPlay = m3u8.loads(targetPlaylist.dumps())

print("targetPlay.is_variant")
print(targetPlay.is_variant)


# print("targetPlaylist.dumps()")
# print(targetPlaylist.dumps())

# print("targetPlaylist.segments[0].uri")
# print(targetPlaylist.segments[0].uri)



# targetPlaylist = m3u8.loads(targetPlaylist.dumps())


# for targetPlay in targetPlaylist:
#     print("targetPlay")
#     print(targetPlay)


# print("targetPlaylist.base_path")
# print(targetPlaylist.base_path)


# first_segment_props = targetVideo.segments[0].custom_parser_values['extinf_props']
# print(first_segment_props['tvg-id'])  # 'channel1'
# print(first_segment_props['group-title'])  # 'Group1'
# print(first_segment_props['catchup-type'])  # 'flussonic'