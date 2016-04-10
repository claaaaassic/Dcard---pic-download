#-*- coding: utf-8 -*-

'''
Dcard sex forum picture download
only can download jpg format
need Internet

get_page_url_number()
'https://www.dcard.tw/api/forum/此欄可自行更換不同看板/'
預設sex版
'''


import requests
import json
from lxml import etree
import shutil
import re


def download_pic(url):
	res = requests.get(url, stream = True , timeout = 10.0)
	match = re.search('\w+.jpg',url)
	fname = match.group(0) # 檔案名稱 網址.jpg
	f = open(fname, 'wb')
	shutil.copyfileobj(res.raw, f)
	f.close()
	del res


def get_page_url_number(page):
	response = requests.get( 'https://www.dcard.tw/api/forum/sex/' + str(page) + '/' )
	data = json.loads(response.text)
	for info in data:
		page_url_number_list.append(info['id'])


# http://i.imgur.com/xxxxxxx.jpg
# http://i.imgur.com/\w+.jpg  
# 表示  http://i.imgur.com/ \w任意字符 +表示前者一個或一個以上 .jpg
def get_pic_url(content):
	match1 = re.findall('http://i.imgur.com/\w+.jpg', content)
	match2 = re.findall('http://imgur.com/\w+.jpg', content)
	return match1 + match2
	

if __name__ == '__main__':

	page_url_number_list = list()
	for i in range(1,50): 	# 後面數字 自訂下載頁數
		get_page_url_number(i)
		print 'download page number %s ...' % i

	print 'search %s pages' % len(page_url_number_list)
	while page_url_number_list :
		number = page_url_number_list.pop(0)
		print number
		r = requests.get( 'https://www.dcard.tw/api/post/all/' + str(number) )
		data = json.loads(r.text)
		content = data['version'][0]['content']			# content = 內文
		pic_url_list = get_pic_url(content)

		for pic_url in pic_url_list:
			print pic_url
			download_pic(pic_url)

	print '\nsuccessful'


