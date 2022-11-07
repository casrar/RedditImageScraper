import requests
import random as random
import shutil
import time

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
    # print(response['data'][0]['url']) access to url on gallery
    # Maybe image resolution
    # _1rZYMD_4xY3gRcSS3p8ODO _3a2ZHWaih05DgAOtvu6cIo UPVOTE BUTTON
    # Need to grab the post time
    # Need to grab the upvote ratio
    # Need to grab community size
    # For individual pics all I need is the url
    # For galleries I need to open link for page, find html with images and download images 

def main():
    # response = requests.get('https://api.pushshift.io/reddit/search/submission/?link_flair_text=WDYWT&subreddit=streetwear&size=250&after=0d', 
    #                     proxies=proxies,
    #                     headers={"User-Agent": random.choice(user_agents)}
    #                     )
    # response = response.json()
    # print()


    # USE RESULTS TO HIT REDDIT API FOR UPDATED/IN DEPTH INFO
    MAX_API_CALLS = 5
    page_count = 1
    calls = 1
    file = open("urls.txt", "a", encoding="utf-8")
    while(True):
        for calls in range (MAX_API_CALLS):
            response = requests.get('https://api.pushshift.io/reddit/search/submission/' 
                                    + '?link_flair_text=WDYWT&subreddit=streetwear&size=250&after={}d'.format(page_count), 
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
                if 'removed_by_category' not in response['data'][x]:
                    # print(response['data'][x]['url'])
                    file.write(response['data'][x]['url'] + '\n')
                    i = i + 1
                else:
                    # print('removed')
                    i = i + 1
                # print(i)

            calls = calls + 1
            page_count = page_count + 1
            # print(calls)
            print('pages: ' + str(page_count))
            time.sleep(3)
        calls = 1
        


    # response = requests.get('https://www.reddit.com/r/streetwear/new/.json', 
    #                     proxies=proxies,
    #                     headers={"User-Agent": random.choice(user_agents)}
    #                     )

    # count = 0
    # json = response.json()
    # next_page = json['data']['after']
    # post_list = []

    # while (next_page != None):
    #     print(next_page)
    #     dist = json['data']['dist']
    #     count = count + 1
    #     response = requests.get('https://www.reddit.com/r/streetwear/new/.json?after={}&limit=100'.format(next_page), 
    #                         proxies=proxies,
    #                         headers={"User-Agent": random.choice(user_agents)}
    #                         ) 

    #     for i in range(dist):
    #         post = json['data']['children'][i]['data']
    #         flair = post['link_flair_text']
    #         created = post['created_utc']
    #         subreddit_subscribers = post['subreddit_subscribers']
    #         url = post['url']
    #         saved_post = (flair, created, subreddit_subscribers, url)
    #         post_list.append(saved_post)

    #     json = response.json()
    #     next_page = json['data']['after']


    # print('count: ' + str(count))
    # print('posts: ' + str(len(post_list)))

    # response = requests.get('https://preview.redd.it/rx482lzocnx91.jpg?width=960&amp;crop=smart&amp;auto=webp&amp;s=ab1f175d91f00becc20aaf1fa1b259ab209bda16', 
    #                     stream = True,
    #                     proxies=proxies,
    #                     headers={"User-Agent": random.choice(user_agents)}
    #                     )

    # if response.status_code == 200:
    #     # with open('test.jpg','wb') as f:
    #     #     shutil.copyfileobj(response.raw, f)
    #     print('Image sucessfully Downloaded: ','test.jpg')
    # else:
    #     print('Image Couldn\'t be retrieved')




if __name__=='__main__':
    main()