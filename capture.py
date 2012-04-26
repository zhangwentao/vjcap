#!/usr/local/bin/python
# coding:utf-8 
from urllib import urlretrieve
from xml.dom import minidom
from time import sleep
import json
import os
from urllib import quote
XML_FILE_PATH = "result"
LOG_FILE_PATH = "log"
USER_NAMES_FILE = 'names'
SENDER_NAME_FILE = 'sender'
PICS_URL = './pic/'
ALL_IDS=''
xml_string =''
TOPIC_FILE = "topic_name"
counter = 0
step =10 

def make_dir(dir_name):
    retry = True
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    while retry:
        try:
            # per Apalala, sleeping before the makedirs() eliminates the exception!
            sleep(0.001)
            os.makedirs(dir_name)
        except OSError, e:
            #time.sleep(0.001) # moved to before the makedirs() call 
            #print "ErrorNo: %s (%s)" % (e.errno, errno.errorcode[e.errno])
            if e.errno != 13: # eaccess
                raise
        else:
            retry = False



def delete_file_folder(src):
    '''delete files and folders'''
    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            pass
    elif os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc=os.path.join(src,item)
            delete_file_folder(itemsrc) 
        try:
            os.rmdir(src)
        except:
            pass
	
def run():
	global step
	global counter
	global XML_FILE_PATH
	global LOG_FILE_PATH
	global ALL_IDS
	global xml_string
	global TOPIC_FILE 

	urlretrieve("http://192.168.1.140/geek/gettopic",TOPIC_FILE);
	result = file(TOPIC_FILE).readline()
	print "topic info:"+result

	if result == 'none':
		print '没有新话题'
		return
	else:
		print '新话题来了'

	topic_obj = json.loads(result)
	topic_name =topic_obj["topic"] 
	sender_name = topic_obj["name"]
	f = file(SENDER_NAME_FILE,'w')
	f.write((sender_name).encode('gb2312'))
	f.close()

	urlretrieve("http://api.t.sina.com.cn/statuses/search.xml?source=3709681010&q="+topic_name.encode('gb2312'),XML_FILE_PATH);

	dom  = minidom.parse(XML_FILE_PATH);
	root = dom.documentElement
	users = root.getElementsByTagName("user")
	user_names = u''
	picurl_list = [];	
	for user in users:
		ALL_IDS+=str(user.getElementsByTagName("id")[0].childNodes[0].data)+'\n'
		picurl_list.append(user.getElementsByTagName("profile_image_url")[0].childNodes[0].data)
		user_name=user.getElementsByTagName("name")[0].childNodes[0].data
		user_names+=user_name;

		
	print "第"+str(counter)+"个话题:"+topic_name.encode("utf-8");
	if counter % step == 0:
		print "清空图片文件"
		if os.path.exists(PICS_URL):
			delete_file_folder(PICS_URL)

	if not os.path.exists(PICS_URL):
		make_dir(PICS_URL)

	print '下载话题相关头像'
	i = 0;
	for pic in picurl_list:	
		urlretrieve(pic,PICS_URL+"pic_"+str(counter)+"_"+str(i)+".jpg")
		i+=1
	print '下载完成'

	f = file(USER_NAMES_FILE,'w')
	f.write(topic_name.encode('gb2312'))
	f.close()

	f = file(LOG_FILE_PATH,'w')
	f.write(ALL_IDS)
	f.close()
	counter+=1

while True:
	if counter != 0:
		sleep(3)
	run()	
