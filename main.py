from expireddomains import User
from account_creator import get_or_create_account
import config

# Check if user wants to use automated account creation
use_auto = input('Use automated account creation? (y/n) [default: y]: ').strip().lower()
if use_auto == '' or use_auto == 'y':
    print("\n[INFO] Using automated account creation with Guerrilla Mail API")
    username, password = get_or_create_account()
    
    if not username or not password:
        print("\n[WARNING] Automated account creation failed")
        print("[INFO] Falling back to config.py credentials")
        username = config.username
        password = config.password
else:
    print("\n[INFO] Using credentials from config.py")
    username = config.username
    password = config.password

keyword = input('\nPlease enter keyword:\n- ')

user = User(keyword, username, password)
login = user.get_cookie()
if login == False:
    print('USER CREDENTIALS ARE WRONG')
    quit()
data = user.get_result_data()
if data == False:
    print('No records matching keyword')
    quit()
user.scrape()