import requests
import random as random
import shutil

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

def main():
    response = requests.get('https://www.reddit.com/r/streetwear/.json', 
                        proxies=proxies,
                        headers={"User-Agent": random.choice(user_agents)}
                        )

    count = 0
    json = response.json()
    next_page = json['data']['after']
    while (next_page != None):
        print(next_page)
        count = count + 1
        response = requests.get('https://www.reddit.com/r/streetwear/.json?after={}&limit=100'.format(next_page), 
                            proxies=proxies,
                            headers={"User-Agent": random.choice(user_agents)}) 
        json = response.json()
        next_page = json['data']['after']
    print('count: ' + str(count))

    response = requests.get('https://i.redd.it/lkq4drngzos91.jpg', 
                        stream = True,
                        proxies=proxies,
                        headers={"User-Agent": random.choice(user_agents)}
                        )
    if response.status_code == 200:
        with open('test.jpg','wb') as f:
            shutil.copyfileobj(response.raw, f)
        print('Image sucessfully Downloaded: ','test.jpg')
    else:
        print('Image Couldn\'t be retrieved')


if __name__=='__main__':
    main()