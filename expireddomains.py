from pyquery import PyQuery    
import requests,config,os,time

class User:

    def __init__(self,keyword) -> None:
        self.keyword = keyword
        self.sesh = requests.Session()


    def get_cookie(self):
        # Try to access without login first
        headers = {
            'authority': 'www.expireddomains.net',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9,pl-PL;q=0.8,pl;q=0.7,de;q=0.6',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        }

        # Try accessing the search page directly without login
        print("Trying to access without login...")
        test_response = self.sesh.get('https://www.expireddomains.net/domain-name-search/', headers=headers)
        print(f"Direct access status: {test_response.status_code}")
        print(f"Direct access URL: {test_response.url}")
        
        if "login" not in test_response.url.lower() and test_response.status_code == 200:
            print("Direct access successful - no login required")
            return True
        
        # If direct access doesn't work, try with login
        print("Direct access failed, trying with login...")
        
        # First, get the login page to see the form structure
        login_page = self.sesh.get('https://www.expireddomains.net/login/', headers=headers)
        print(f"Login page status: {login_page.status_code}")
        
        # Look for form fields in the HTML
        pq = PyQuery(login_page.text)
        forms = pq('form')
        print(f"Found {len(forms)} forms on login page")
        for i, form in enumerate(forms.items()):
            print(f"Form {i+1} action: {form.attr('action')}")
            inputs = form('input')
            for inp in inputs.items():
                print(f"  Input: name='{inp.attr('name')}', type='{inp.attr('type')}'")
        
        # Try different field names that might be used
        data_options = [
            {
                'login': config.username,
                'password': config.password,
                'redirect_to_url': '/home',
            },
            {
                'username': config.username,
                'password': config.password,
                'redirect_to_url': '/home',
            },
            {
                'user': config.username,
                'pass': config.password,
                'redirect_to_url': '/home',
            },
            {
                'email': config.username,
                'password': config.password,
                'redirect_to_url': '/home',
            }
        ]

        for i, data in enumerate(data_options):
            print(f"Trying data option {i+1}: {list(data.keys())}")
            response = self.sesh.post('https://www.expireddomains.net/logincheck/', headers=headers, data=data)
            
            print(f"Login response status: {response.status_code}")
            print(f"Login response URL: {response.url}")
            print(f"Cookies after login: {dict(self.sesh.cookies)}")

            if "The supplied login information are unknown." in response.text:
                print("Login failed: Invalid credentials")
                continue
            elif "accountdeactivated" in response.url:
                print("Login failed: Account deactivated")
                print(f"Error page content: {response.text[:200]}")
                continue
            elif "Login" in response.text and "title" in response.text.lower():
                print("Login failed: Still on login page")
                continue
            else:
                print("Login successful")
                return True
        
        print("All login attempts failed")
        return False



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

        response = self.sesh.get('https://www.expireddomains.net/domainnamesearch/', params=params, headers=headers)
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
            print(f"No results found for keyword: {self.keyword}")
            print(f"Response text length: {len(response.text)}")
            # Print a snippet of the response to debug
            print("Response snippet:")
            print(response.text[:1000])
            
            # Try to find any domain results in the response
            domain_links = pq('a[href*="domain"]')
            print(f"Found {len(domain_links)} domain links")
            domain_links_list = list(domain_links.items())
            for i, link in enumerate(domain_links_list[:5]):  # Show first 5
                print(f"  Link {i+1}: {link.text()} -> {link.attr('href')}")
            
            # Try to find domain names in the response
            domain_names = pq('td.field_domain a')
            print(f"Found {len(domain_names)} domain names")
            domain_names_list = list(domain_names.items())
            for i, domain in enumerate(domain_names_list[:5]):  # Show first 5
                print(f"  Domain {i+1}: {domain.text()}")
            
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

            response = self.sesh.get('https://www.expireddomains.net/domain-name-search/', params=params, headers=headers)

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

            
