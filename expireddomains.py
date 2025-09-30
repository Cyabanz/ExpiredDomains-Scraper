from pyquery import PyQuery    
import requests,config,os,time

class User:

    def __init__(self,keyword) -> None:
        self.keyword = keyword
        self.sesh = requests.Session()


    def get_cookie(self):

        headers = {
            'authority': 'member.expireddomains.net',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9,pl-PL;q=0.8,pl;q=0.7,de;q=0.6',
            'cache-control': 'max-age=0',
            'origin': 'null',
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-site',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        }

        data = {
            'login': config.username,
            'password': config.password,
            'redirect_to_url': '/home',
        }

        response = self.sesh.post('https://member.expireddomains.net/login/', headers=headers, data=data)

        if "The supplied login information are unknown." in response.text:
            return False
        else:
            return True



    def get_result_data(self):
        headers = {
            'authority': 'member.expireddomains.net',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,pl-PL;q=0.8,pl;q=0.7,de;q=0.6',
            'referer': 'https://member.expireddomains.net/domain-name-search/?q=mikecox&searchinit=1',
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }


        params = {
            'q': self.keyword,
            'position': 'member',
        }

        response = self.sesh.get('https://member.expireddomains.net/domainnamesearch/', params=params, headers=headers)
        pq = PyQuery(response.text)
        tag = pq('div#listing > div.infos.form-inline > strong')
        try:
            self.result_max = int(tag.text().replace(',',''))
            return True
        except:
            return False

    def scrape(self):
        try:os.remove(f"domains/{self.keyword}.txt")
        except:pass
        scraped = 0
        headers = {
            'authority': 'member.expireddomains.net',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9,pl-PL;q=0.8,pl;q=0.7,de;q=0.6',
            'referer': 'https://member.expireddomains.net/domain-name-search/?q=bro',
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        }
        while True:
            params = {
                'start': str(scraped),
                'q': self.keyword,
            }

            response = self.sesh.get('https://member.expireddomains.net/domain-name-search/', params=params, headers=headers)

            pq = PyQuery(response.text)
            raw_dom = pq('tbody > tr > td.field_domain > a').items()
            parsed_doms = [d.text() for d in raw_dom]
            
            new_doms = '\n'.join(parsed_doms)+'\n'
            
            with open(f"domains/{self.keyword}.txt",'a+') as raw: raw.write(new_doms)
            scraped += len(parsed_doms)
            os.system('cls')
            print(f"CURRENT SESSION\nScraped - {scraped}\nTotal - {self.result_max}\nProgress - {round(((scraped*100)/self.result_max),0)}%\n")
            if len(response.text) < 200:
                print(response.text)
                waittime = int(response.text.split(' ')[-2])
                time.sleep(waittime)
            if scraped >= self.result_max:break

            
