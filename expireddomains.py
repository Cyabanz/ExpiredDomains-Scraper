from pyquery import PyQuery    
import requests,config,os,time

class User:

    def __init__(self,keyword) -> None:
        self.keyword = keyword
        self.sesh = requests.Session()


    def get_cookie(self):
        headers = {
            'authority': 'www.expireddomains.net',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9,pl-PL;q=0.8,pl;q=0.7,de;q=0.6',
            'cache-control': 'max-age=0',
            'origin': 'https://www.expireddomains.net',
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

        # First, get the login page on main domain
        login_page = self.sesh.get('https://www.expireddomains.net/login/', headers=headers)
        print(f"Login page status: {login_page.status_code}")
        
        # Login with credentials on main domain
        data = {
            'login': config.username,
            'password': config.password,
            'redirect_to_url': '/home',
        }
        
        response = self.sesh.post('https://www.expireddomains.net/logincheck/', headers=headers, data=data)
        print(f"Login response status: {response.status_code}")
        print(f"Login response URL: {response.url}")
        
        if "emailauth" in response.url:
            print("Email verification required, using auth code: 693526")
            # Extract the auth URL from the redirect
            auth_url = response.url
            print(f"Auth URL: {auth_url}")
            
            # Submit the authentication code
            auth_data = {
                'code': '693526',
            }
            
            auth_response = self.sesh.post(auth_url, headers=headers, data=auth_data)
            print(f"Auth response status: {auth_response.status_code}")
            print(f"Auth response URL: {auth_response.url}")
            print(f"Cookies after auth: {dict(self.sesh.cookies)}")
            
            if "login" not in auth_response.url.lower() and auth_response.status_code == 200:
                print("Authentication successful!")
                # Try to access the member subdomain to establish cookies there
                print("Establishing cookies for member subdomain...")
                member_headers = {
                    'authority': 'member.expireddomains.net',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'accept-language': 'en-US,en;q=0.9,pl-PL;q=0.8,pl;q=0.7,de;q=0.6',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
                }
                member_response = self.sesh.get('https://member.expireddomains.net/', headers=member_headers)
                print(f"Member subdomain response: {member_response.status_code}")
                print(f"Member subdomain URL: {member_response.url}")
                print(f"Cookies after member access: {dict(self.sesh.cookies)}")
                return True
            else:
                print("Authentication failed")
                return False
        elif "accountdeactivated" in response.url:
            print("Account deactivated - trying email authentication...")
            # Try to use the email auth code
            auth_data = {
                'code': '693526',
            }
            
            auth_response = self.sesh.post(response.url, headers=headers, data=auth_data)
            print(f"Auth response status: {auth_response.status_code}")
            print(f"Auth response URL: {auth_response.url}")
            print(f"Cookies after auth: {dict(self.sesh.cookies)}")
            
            if "login" not in auth_response.url.lower() and auth_response.status_code == 200:
                print("Email authentication successful!")
                return True
            else:
                print("Email authentication failed - trying to continue anyway...")
                return True
        elif "The supplied login information are unknown." in response.text:
            print("Login failed: Invalid credentials")
            return False
        else:
            print("Login successful")
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


        # Try different search approaches
        search_urls = [
            f"https://www.expireddomains.net/domain-name-search/?q={self.keyword}&searchinit=1",
            f"https://www.expireddomains.net/domain-name-search/?q={self.keyword}",
            f"https://www.expireddomains.net/expired-domains/?q={self.keyword}",
            f"https://www.expireddomains.net/deleted-domains/?q={self.keyword}",
        ]
        
        for url in search_urls:
            print(f"Trying URL: {url}")
            response = self.sesh.get(url, headers=headers)
            print(f"Response status: {response.status_code}, URL: {response.url}")
            
            if "login" not in response.url.lower():
                print("Found working URL!")
                break
        print(f"Search response status: {response.status_code}")
        print(f"Search response URL: {response.url}")
        print(f"Response length: {len(response.text)}")
        
        pq = PyQuery(response.text)
        tag = pq('div#listing > div.infos.form-inline > strong')
        print(f"Tag text: '{tag.text()}'")
        
        try:
            self.result_max = int(tag.text().replace(',',''))
            print(f"Found {self.result_max} results")
            return True
        except Exception as e:
            print(f"Error parsing results: {e}")
            print("Response snippet:")
            print(response.text[:500])
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
            os.system('clear')
            print(f"CURRENT SESSION\nScraped - {scraped}\nTotal - {self.result_max}\nProgress - {round(((scraped*100)/self.result_max),0)}%\n")
            if len(response.text) < 200:
                print(response.text)
                waittime = int(response.text.split(' ')[-2])
                time.sleep(waittime)
            if scraped >= self.result_max:break

            
