#!/usr/local/bin/python
# coding:utf-8 
from urllib import urlretrieve
from xml.dom import minidom
from time import sleep
import json
import urllib2
import os
from urllib import quote
XML_FILE_PATH = "result"
LOG_FILE_PATH = "log"
USER_NAMES_FILE = 'names'
ALL_IDS=''
xml_string =''
TOPIC_LIST = ["创想48小时"]
TOPIC_FILE = "topic_name"
counter = 0
step = 5

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
	global TOPIC_LIST
	global TOPIC_FILE 

	urlretrieve("http://192.168.1.140/geek/gettopic",TOPIC_FILE);
	result = file(TOPIC_FILE).readline()
	print "result:"+result
	if result == 'none':
		print '没了'
		return
	topic_obj = json.loads(result)
	topic_name =topic_obj["topic"] 
	sender_name = topic_obj["name"]
	print 'nametype:'+str(type(sender_name))
	f = file("sender",'w')
	f.write(sender_name.encode('utf-8'))
	f.close()

	urlretrieve("http://api.t.sina.com.cn/statuses/search.xml?source=3709681010&q="+topic_name.encode('gb2312'),XML_FILE_PATH);
	#xml_file = file(XML_FILE_PATH)
	#while True:
	# 	line = xml_file.readline()
	#	xml_string+=line
	#	if len(line) == 0:
	#		break
	#xml_file.close()
	#dom  = minidom.parse(xml_string);

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

	i = 0;	
	print "counter:"+str(counter);
	if counter % step == 0:
		print "clear"
		if os.path.exists("pic"):
			delete_file_folder("pic")

	if not os.path.exists("pic"):
		os.mkdir("pic")

	for pic in picurl_list:	
		urlretrieve(pic,"pic/pic_"+str(counter)+"_"+str(i)+".jpg")
		i+=1
	print user_names+'\n'
	print picurl_list

	f = file(USER_NAMES_FILE,'w')
	f.write(user_names.encode('utf-8'))
	f.close()

	f = file(LOG_FILE_PATH,'w')
	f.write(ALL_IDS)
	f.close()
	counter+=1

while True:
	if counter != 0:
		sleep(3)
	run()	

