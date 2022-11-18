import requests
import random as random
import shutil
import time
import math
import os
import argparse
import re


proxies = [
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
proxies = {
    'https': '20.229.33.75:8080',
    'https': '20.234.198.245:8080',
    'https': '92.205.22.114:38080',
    'https': '172.104.60.117:3128',
    'https': '49.0.2.242:8090',
    'https': '117.251.103.186:8080',
    'http': '103.49.202.252:80',
    'http': '1.255.134.136:3128',
    'http': '185.162.230.114:80',
    'http': '91.101.251.212:80',
    'http': '80.48.119.28:8080',
    'http': '198.49.68.80:80',
    'http': '169.57.1.85:8123',
    'http': '83.229.73.175:80',
    'http': '187.217.54.84:80',
    'http': '165.154.226.12:80',
    'http': '139.99.237.62:80',
    'http':'83.229.72.174:80',
    'http': '20.205.46.128:80',
    'http': '20.111.54.16:80',
    'http': '209.201.29.20:80',
    'http':'221.132.28.18:8090',
    }


user_agents = [
    'Firefox: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Firefox: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Chrome: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'Safari: Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
    'Edge: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53'
    ]

    # print(response['data'][0]['preview']) #individual pic
    # print(response['data'][0]['url'])
    # print(response['data'][0]['created_utc'])
    # print(response['data'][0]['link_flair_css_class'])
    # print(response['data'][0]['subreddit_subscribers'])
    # print(response['data'][0]['upvote_ratio'])
    # print(response['data'][0]['media_metadata'])
    # Maybe image resolution
    # Need to grab the post time
    # Need to grab the upvote ratio
    # Need to grab community size
    # For individual pics all I need is the url

    # YOU CAN EXTRACT GALLERY URLS, https://preview.redd.it/quk3m6qqxey91.jpg?width=2871&amp;format=pjpg&amp;auto=webp&amp;s=dafbffa08b196b69b2693504cfcb945caa206ebf
    # REPLACE &amp with & and links work!

    # Functionality:
    # cmd line args (subreddit, deleted, resume, url list or download)
    # resume file 
    ## Tmp file
    ## Contains last action and progress
    ## Save urls to file called url and url sorted 


def main():
    parser = argparse.ArgumentParser(
        prog='RedditImageScraper',
        description='A scraper to download all images from a specified subreddit.'
    )

    parser.add_argument('-r', dest='resume', default=False, required=False, action='store_true',
        help='Resume scraper using resume file.')

    args = parser.parse_args()
    try:
        if not os.path.isdir('temp'):
            os.mkdir('temp')

        if not os.path.isdir('images'):
            os.mkdir('images')
    except:
        print('Error with directories.')
    url_list = []
    action='a'
    progress=0
    threads=1
    try: 
        if not os.path.isfile('temp\.resume') and not args.resume:
            resume = open("temp\.resume", 'w', encoding='utf-8')
            resume.write('action=' + str(action) + '\n')
            resume.write('progress=' + str(progress) + '\n')
            resume.write('threads=' + str(threads) + '\n')
        else:
            resume = open("temp\.resume", 'r', encoding='utf-8')
            action = resume.readline()
            action = re.split('=|, |\n', action)
            action = action[1]
            progress = resume.readline()
            progress = re.split('=|, |\n', progress)
            progress = progress[1]
            threads = resume.readline()
            threads = re.split('=|, |\n', threads)
            threads = threads[1]
    except:
        print('Error with resume.')

    if action != 'a' and action != 'd':
        print('Invalid action')
    if int(progress) < 0:
        print('Invalid progress')
    if int(threads) < 0:
        print('Invalid threads ')

    if action == 'a':
        # USE RESULTS TO HIT REDDIT API FOR UPDATED/IN DEPTH INFO
        MAX_PUSHSHIFT_CALLS = 5
        page_count = 1
        calls = 1
        epoch = math.floor(time.time())
        file = open("temp/urls.txt", "a", encoding="utf-8")
        posts = 1
        total_posts = 1
        while(posts > 0):
            for calls in range (MAX_PUSHSHIFT_CALLS):
                response = requests.get('https://api.pushshift.io/reddit/search/submission/?subreddit=streetwear&sort=desc&size=250&before={}'.format(epoch), 
                            proxies=proxies,
                            headers={"User-Agent": random.choice(user_agents)}
                            )
                print(response)
                response = response.json()
                posts = len(response['data'])

                if (posts == 0):
                    break
            
                for x in range(posts):
                    if ('removed_by_category' not in response['data'][x]) and ('link_flair_text' in response['data'][x] and response['data'][x]['link_flair_text'] == 'WDYWT'):
                        url_list.append(response['data'][x]['full_link'])
                        resume = open("temp\.resume", 'w', encoding='utf-8')
                        resume.write('action=' + str(action) + '\n')
                        resume.write('progress=' + str(progress) + '\n')
                        progress = total_posts
                        total_posts = total_posts + 1
                        resume.write('threads=' + str(threads) + '\n')
                        file.write(response['data'][x]['full_link'] + '\n') #change var name
        
                    else:
                        epoch = response['data'][x]['created_utc'] 

                calls = calls + 1
                page_count = page_count + 1
                print('last epoch: ' + str(epoch))
                print('pages: ' + str(page_count - 1))
                time.sleep(3)
            calls = 1


        action = 'd'
        progress = 0
        resume = open("temp\.resume", 'w', encoding='utf-8')
        resume.write('action=' + str(action) + '\n')
        resume.write('progress=' + str(progress) + '\n')
        resume.write('threads=' + str(threads) + '\n')
    elif action == 'd':
    # if response.status_code == 200:
    #     # with open('test.jpg','wb') as f:
    #     #     shutil.copyfileobj(response.raw, f)
    #     print('Image sucessfully Downloaded: ','test.jpg')
    # else:
    #     print('Image Couldn\'t be retrieved')
        print('d')

if __name__=='__main__':
    main()