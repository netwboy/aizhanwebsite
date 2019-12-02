#-*- coding: utf-8 -*-
'''
利用爱站进行轮询查询整个C段内的网站
'''
   
import socket
import sys
import json
import requests
import re
import time
import _thread
#私钥
key = "[此处请填写您在https://www.aizhan.com/apistore/detail_29/申请的私钥]"
def scan(ip_str):
    '''
    检测扫描端口是否开启
    然后利用aizhan旁站进行遍历
    '''
    global key
    port = '80'
    cs=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    address=(str(ip_str),int(port))
    status = cs.connect_ex((address))
    #若返回的结果为0表示端口开启
    if(status == 0):
        websites = ip_str + " :\n"
        allinfo = json.loads(request_get("https://apistore.aizhan.com/site/dnsinfos/"+key, {'query' : ip_str , 'page' : 1}))
        if allinfo['code'] == 200000:
            i=2
            for _awinfoarray in allinfo['data']['domains']:
                websites = websites + _awinfoarray['domain'] + "\n"
            while (i <= int(allinfo['data']['total_pages'])):
                pageinfo = json.loads(request_get("https://apistore.aizhan.com/site/dnsinfos/"+key, {'query' : ip_str , 'page' : i}))
                i += 1
                if pageinfo['code'] == 200000:
                    for _winfoarray in pageinfo['data']['domains']:
                        websites = websites + _winfoarray['domain'] + "\n"
        print(websites)
    cs.close()
       
def find_ip(ip_prefix):
    '''
    给出当前的192.168.1 ，然后扫描整个段所有地址
    '''
    for i in range(1,256):
        ip = '%s.%s'%(ip_prefix,i)
        _thread.start_new_thread(scan, (ip,))
        time.sleep(0.4)

def request_get(url, params):
    res3 = requests.get(url, params=params)
    res3 = res3.content.decode('utf-8')
    return res3
        
if __name__ == "__main__":
    commandargs = sys.argv[1:]
    args = "".join(commandargs)    
      
    ip_prefix = '.'.join(args.split('.')[:-1])
    find_ip(ip_prefix)