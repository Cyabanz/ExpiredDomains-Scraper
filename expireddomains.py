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

        # First, get the login page
        login_page = self.sesh.get('https://www.expireddomains.net/login/', headers=headers)
        print(f"Login page status: {login_page.status_code}")
        
        # Login with credentials
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
                return True
            else:
                print("Authentication failed")
                return False
        elif "The supplied login information are unknown." in response.text:
            print("Login failed: Invalid credentials")
            return False
        elif "accountdeactivated" in response.url:
            print("Login failed: Account deactivated")
            return False
        else:
            print("Login successful")
            return True



    def get_result_data(self):
        headers = {
            'authority': 'www.expireddomains.net',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9,pl-PL;q=0.8,pl;q=0.7,de;q=0.6',
            'referer': 'https://www.expireddomains.net/domain-name-search/',
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        }

        # Try to access the domain data through a different approach
        # First, let's try to access the expired domains page directly
        print("Trying to access expired domains page...")
        expired_response = self.sesh.get('https://www.expireddomains.net/expired-domains/', headers=headers)
        print(f"Expired domains page status: {expired_response.status_code}")
        print(f"Expired domains page URL: {expired_response.url}")
        
        # Check if we can find domain data on the expired domains page
        pq_expired = PyQuery(expired_response.text)
        domain_links_expired = pq_expired('td.field_domain a')
        print(f"Found {len(domain_links_expired)} domain links on expired domains page")
        domain_links_expired_list = list(domain_links_expired.items())
        for i, domain in enumerate(domain_links_expired_list[:5]):  # Show first 5
            print(f"  Domain {i+1}: {domain.text()}")
        
        # Try using the main domain with different search parameters
        params = {
            'q': self.keyword,
        }

        response = self.sesh.get('https://www.expireddomains.net/domain-name-search/', params=params, headers=headers)
        print(f"Search response status: {response.status_code}")
        print(f"Search response URL: {response.url}")
        print(f"Cookies for search: {dict(self.sesh.cookies)}")
        
        pq = PyQuery(response.text)
        
        # Try different selectors to find the result count
        selectors = [
            'div#listing > div.infos.form-inline > strong',
            'div.infos.form-inline strong',
            '.infos strong',
            'strong',
            'div#listing strong'
        ]
        
        result_count = None
        for selector in selectors:
            tag = pq(selector)
            if tag.text() and tag.text().strip():
                try:
                    result_count = int(tag.text().replace(',',''))
                    print(f"Found {result_count} results for keyword: {self.keyword} using selector: {selector}")
                    break
                except:
                    continue
        
        if result_count is not None:
            self.result_max = result_count
            return True
        else:
            # If search doesn't work, try to get domains from the expired domains page
            print(f"Search didn't work, trying to get domains from expired domains page...")
            expired_response = self.sesh.get('https://www.expireddomains.net/expired-domains/', headers=headers)
            pq_expired = PyQuery(expired_response.text)
            domain_links_expired = pq_expired('td.field_domain a')
            
            print(f"Expired domains page response length: {len(expired_response.text)}")
            print(f"Found {len(domain_links_expired)} domain links on expired domains page")
            
            # Try different selectors
            all_links = pq_expired('a')
            print(f"Found {len(all_links)} total links on expired domains page")
            
            # Try to find any table rows
            table_rows = pq_expired('tbody tr')
            print(f"Found {len(table_rows)} table rows on expired domains page")
            
            # Print a snippet of the response to see what's there
            print("Expired domains page snippet:")
            print(expired_response.text[:1000])
            
            if len(domain_links_expired) > 0:
                print(f"Found {len(domain_links_expired)} domains on expired domains page")
                self.result_max = len(domain_links_expired)
                return True
            else:
                print(f"No results found for keyword: {self.keyword}")
                return False

    def scrape(self):
        try:os.remove(f"domains/{self.keyword}.txt")
        except:pass
        scraped = 0
        headers = {
            'authority': 'www.expireddomains.net',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9,pl-PL;q=0.8,pl;q=0.7,de;q=0.6',
            'referer': 'https://www.expireddomains.net/expired-domains/',
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
        
        # Get domains from the expired domains page
        response = self.sesh.get('https://www.expireddomains.net/expired-domains/', headers=headers)
        pq = PyQuery(response.text)
        raw_dom = pq('tbody > tr > td.field_domain > a').items()
        parsed_doms = [d.text() for d in raw_dom if d.text() and '.' in d.text()]
        
        new_doms = '\n'.join(parsed_doms)+'\n'
        
        with open(f"domains/{self.keyword}.txt",'a+') as raw: raw.write(new_doms)
        scraped = len(parsed_doms)
        os.system('clear')
        print(f"CURRENT SESSION\nScraped - {scraped}\nTotal - {self.result_max}\nProgress - {round(((scraped*100)/self.result_max),0)}%\n")
        print(f"Successfully scraped {scraped} domains!")

            
