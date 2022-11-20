import requests
import random as random
import shutil
import time
import math
import re

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
    url_queue = []
    url_list = []
    calls = 1
    proxy_index = 0
    saved_post_id = ''
    pattern = re.compile(r'\.+|/+', re.IGNORECASE)
    with open("temp/urls_sorted.txt",'r', encoding="utf-8") as data_file:
            for line in data_file:
                data = line.split()
                url_list.append(data[0])
    url_list_position = 9211 # 9211 // normally 0
    url_queue.append(url_list[url_list_position])
    while len(url_queue) != 0:
        if calls >= MAX_REDDIT_CALLS:
            proxy_index = proxy_index + 1 % len(ip_addresses)
        proxy_index = proxy_index % len(ip_addresses)
        proxy = {'http': ip_addresses[proxy_index]}
        print('Using: ' + str(proxy))
        print('Post url: ' + str(url_queue[0]))
        if url_queue[0].endswith('/'):
            retry = 0
            for retry in range(5):
                if retry >= 5:
                    print('Max retries, skipping proxy.')
                    break
            try:   
                response = requests.get('{}.json'.format(url_list[url_list_position]), 
                            proxies=proxy,
                            headers={"User-Agent": random.choice(user_agents)}
                            )
            except Exception as e:
                print('Error {} \n Waiting 300 seconds'.format(e))
                time.sleep(300)

            if retry < 5:
                response = response.json()
                post = response[0]['data']['children'][0]['data']
                if 'gallery' in post['url'] and 'crosspost_parent_list' not in post and post['secure_media'] == None and post['gallery_data'] != None:
                    print('in gallery: ' + str(post['url']))
                    saved_post_id = post['id']
                    for item_index in range(len(post['gallery_data']['items'])):
                        picture_id = post['gallery_data']['items'][item_index]['media_id']
                        url_queue.append('https://i.redd.it/{}.jpg'.format(picture_id))
                elif 'url' in post['url']:
                    print('in url: ' + str(post['url']))
                    saved_post_id = post['id']
                    url_queue.append(post['url'])
                file = open('images/image_info/{}_{}.txt'.format(post['subreddit'], post['id']), "a", encoding="utf-8")
                file.write('upvotes={}'.format(post['ups']) + '\ncreated={}'.format(post['created_utc']) +
                '\nsubsrcibers={}\n'.format(post['subreddit_subscribers'])) 
              
            url_list_position = url_list_position + 1
            url_queue.append(url_list[url_list_position])
            url_queue.pop(0)
        if url_queue[0].endswith('.jpg'):
            image_url = url_queue.pop(0)
            print('Image url: ' + image_url)
            response = requests.get(image_url, 
                    stream=True,
                    proxies=proxy,
                    headers={"User-Agent": random.choice(user_agents)}
                    )
            if response.status_code == 200:
                image_url = re.split(pattern, image_url)
                image_url = image_url[4]
                with open('images/images/{}_{}.jpg'.format(saved_post_id, image_url),'wb') as f:
                    shutil.copyfileobj(response.raw, f)
                print('Image sucessfully downloaded: ','{}_{}.jpg'.format(saved_post_id, image_url))
            else:
                print('Image at https://i.redd.it/{}.jpg couldn\'t be retrieved'.format(image_url))

if __name__ == '__main__':
    main()