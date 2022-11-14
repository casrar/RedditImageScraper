import requests
import random as random
import shutil
import time
import math

proxies = {
    'http': '103.49.202.252:80',
    'http': '1.255.134.136:3128',
    'http': '185.162.230.114:80',
    'http':'91.101.251.212:80'
    }

user_agents = [
    'Firefox: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Firefox: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Chrome: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'Safari: Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
    'Edge: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53'
    ]

# print(response)
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
    # resume file (epoch time, page #)


def main():
    # response = requests.get('https://api.pushshift.io/reddit/search/submission/?link_flair_text=WDYWT&subreddit=streetwear&size=1&after=3d', 
    #                     proxies=proxies,
    #                     headers={"User-Agent": random.choice(user_agents)}
    #                     )
    # response = response.json()
    # print(response['data'][0]['full_link'])


    #USE RESULTS TO HIT REDDIT API FOR UPDATED/IN DEPTH INFO
    MAX_API_CALLS = 5
    page_count = 1
    calls = 1
    # epoch = math.floor(time.time())
    epoch = 1304170869 # remove later 
    file = open("urls.txt", "a", encoding="utf-8")
    posts = 1
    while(posts > 0):
        for calls in range (MAX_API_CALLS):
            response = requests.get('https://api.pushshift.io/reddit/search/submission/?subreddit=streetwear&sort=desc&size=250&before={}'.format(epoch), 
                        proxies=proxies,
                        headers={"User-Agent": random.choice(user_agents)}
                        )
            print(response)
            response = response.json()
            posts = len(response['data'])

            if (posts == 0):
                break
        
            i = 0
            for x in range(posts):
                if ('removed_by_category' not in response['data'][x]) and ('link_flair_text' in response['data'][x] and response['data'][x]['link_flair_text'] == 'WDYWT'):
                    file.write(response['data'][x]['full_link'] + '\n')
                    i = i + 1
                else:
                    i = i + 1
                epoch = response['data'][x]['created_utc'] 

            calls = calls + 1
            page_count = page_count + 1
            print('last epoch: ' + str(epoch))
            print('pages: ' + str(page_count - 1))
            time.sleep(3)
        calls = 1
        

    # if response.status_code == 200:
    #     # with open('test.jpg','wb') as f:
    #     #     shutil.copyfileobj(response.raw, f)
    #     print('Image sucessfully Downloaded: ','test.jpg')
    # else:
    #     print('Image Couldn\'t be retrieved')




if __name__=='__main__':
    main()