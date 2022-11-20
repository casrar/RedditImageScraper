import requests
import random as random
import shutil
import time
import math

ip_addresses = [
        '20.229.33.75:8080',
        '20.234.198.245:8080',
        '92.205.22.114:38080',
        '172.104.60.117:3128',
        '49.0.2.242:8090',
        '117.251.103.186:8080',
        '103.49.202.252:80',
        '1.255.134.136:3128',
        '185.162.230.114:80',
        '91.101.251.212:80',
        '80.48.119.28:8080',
        '198.49.68.80:80',
        '169.57.1.85:8123',
        '83.229.73.175:80',
        '187.217.54.84:80',
        '165.154.226.12:80',
        '139.99.237.62:80',
        '83.229.72.174:80',
        '20.205.46.128:80',
        '20.111.54.16:80',
        '209.201.29.20:80',
        '221.132.28.18:8090',
    ]

user_agents = [
    'Firefox: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Firefox: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Chrome: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'Safari: Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
    'Edge: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    ]

def main(): 
    MAX_REDDIT_CALLS = 25
    url_list = []
    with open("temp/urls_sorted.txt",'r', encoding="utf-8") as data_file:
            for line in data_file:
                data = line.split()
                url_list.append(data[0])
  
    calls = 1
    url_list_position = 51626 #
    url_count = 32957 # 
    proxy_index = 0
    while(url_list_position < len(url_list)):
        proxy_index = proxy_index % len(ip_addresses)
        proxy = {'http': ip_addresses[proxy_index]}
        print('Using: ' + str(proxy))
        for calls in range (MAX_REDDIT_CALLS):
            retry = 0
            for retry in range(5):
                if retry >= 5:
                        print('Max retries, skipping proxy.')
                        break
                try:
                    retry = 0
                    for retry in range(5):
                        response = requests.get('{}.json'.format(url_list[url_list_position]), 
                                    proxies=proxy,
                                    headers={"User-Agent": random.choice(user_agents)}
                                    )
                        if response.status_code == 200:
                            break
                except Exception as e:
                    print('Error {} \n Waiting 300 seconds'.format(e))
                    time.sleep(300)                

            print(response)
            response = response.json()
            if (response[0]['data']['children'][0]['data']['removed_by_category'] == None):
                print(url_list[url_list_position])
                file.write(url_list[url_list_position] + '\n')
                url_count = url_count + 1
            url_list_position = url_list_position + 1
            calls = calls + 1
        print('urls: ' + str(url_count))
        
    print('urls: ' + url_count)

if __name__=='__main__':
    main()

