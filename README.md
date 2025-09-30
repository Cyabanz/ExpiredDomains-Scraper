# ExpiredDomains-Scraper
ExpiredDomains Scraper with Automated Account Creation

## Features

- **Automated Account Creation**: Uses Guerrilla Mail API to automatically create temporary email addresses and register accounts on expireddomains.net
- **No Personal Information Required**: No need to use your personal email or credentials
- **Domain Scraping**: Search and scrape expired domains by keyword
- **Rate Limiting**: Built-in delays to avoid detection and bans

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Automated Mode (Recommended)

Simply run the main script and choose automated account creation:

```bash
python main.py
```

When prompted, press Enter or type 'y' to use automated account creation with Guerrilla Mail API.

The script will:
1. Create a temporary email address
2. Generate random credentials
3. Register an account on expireddomains.net
4. Handle email verification if needed
5. Log in and start scraping

### Manual Mode

If you prefer to use your own credentials, type 'n' when prompted and the script will use credentials from `config.py`.

Edit `config.py` to set your credentials:
```python
username = 'your_username'
password = 'your_password'
```

## Files

- `main.py` - Main entry point
- `expireddomains.py` - Domain scraping logic
- `guerrilla_mail.py` - Guerrilla Mail API client
- `account_creator.py` - Automated account creation
- `config.py` - Manual credentials configuration (fallback)

## Disclaimer

The code provided is for educational purposes only and is not intended for any illegal or unethical activity. The code is provided "as is" without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and non-infringement.

I take no responsibility for any consequences resulting from the use of this code. It is the responsibility of the user to ensure that any use of the code complies with all applicable laws and ethical standards. I do not endorse or condone any illegal or unethical activity that may be performed using this code.

The code is intended to be used only as a learning exercise and is not intended for use in any production environment. I do not advise or recommend the use of this code for any scraping or website-checking activity that may be deemed insane or unethical.

By using this code, you agree to hold me harmless from any and all claims, damages, or other liabilities arising from or related to your use of the code.
