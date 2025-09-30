# Usage Guide - Automated Account Creation

## Overview

This ExpiredDomains scraper now includes **automated account creation** using the Guerrilla Mail API. You no longer need to use your personal email or create accounts manually!

## Quick Start

### Option 1: Interactive Mode (Recommended for first-time users)

```bash
python main.py
```

You'll be prompted:
1. **Use automated account creation?** - Press Enter or type 'y'
2. The script will automatically:
   - Create a temporary email via Guerrilla Mail API
   - Generate random credentials
   - Register on expireddomains.net
   - Handle verification (if needed)
3. **Enter keyword** - Type your search keyword (e.g., "cars", "tech", "food")
4. The scraper will run and save results to `domains/<keyword>.txt`

### Option 2: Fully Automated Mode (No prompts)

```bash
python auto_scrape.py <keyword>
```

Example:
```bash
python auto_scrape.py cars
```

This automatically creates an account and starts scraping immediately.

### Option 3: Manual Credentials Mode

If you prefer to use your own account:

```bash
python main.py
```

1. Type 'n' when asked about automated account creation
2. Edit `config.py` with your credentials:
   ```python
   username = 'your_username'
   password = 'your_password'
   ```

## Testing the Guerrilla Mail API

Test the temporary email functionality:

```bash
python test_guerrilla_mail.py
```

This will:
- Create a temporary email address
- Test custom usernames
- Check for incoming emails
- Display your temporary email address

## How It Works

### Automated Account Creation Flow

1. **Guerrilla Mail Client** (`guerrilla_mail.py`)
   - Connects to Guerrilla Mail API
   - Creates temporary email addresses
   - Checks for verification emails
   - Extracts verification links

2. **Account Creator** (`account_creator.py`)
   - Generates random credentials
   - Registers account on expireddomains.net
   - Handles email verification
   - Returns working credentials

3. **Main Scraper** (`expireddomains.py`)
   - Uses provided credentials (auto or manual)
   - Logs into expireddomains.net
   - Searches and scrapes domains
   - Saves results to file

## Features

✅ **No Personal Information Required**
- Temporary email addresses
- Random generated usernames
- Secure random passwords

✅ **Fully Automated**
- One command to run
- No manual registration
- Automatic verification handling

✅ **Fallback Support**
- Falls back to manual credentials if automation fails
- Flexible configuration options

✅ **Rate Limiting Built-in**
- 5-second delays between requests
- 200 domain limit per session (configurable)
- Prevents account bans

## File Structure

```
/workspace/
├── main.py                    # Interactive main script
├── auto_scrape.py            # Fully automated script
├── expireddomains.py         # Scraping logic
├── guerrilla_mail.py         # Guerrilla Mail API client
├── account_creator.py        # Automated account creation
├── test_guerrilla_mail.py   # Test script for Guerrilla Mail
├── config.py                 # Manual credentials (fallback)
├── requirements.txt          # Python dependencies
└── domains/                  # Output directory for scraped domains
```

## Troubleshooting

### If automated account creation fails:

1. **Check internet connection** - Guerrilla Mail API requires internet access
2. **Try again** - Sometimes temporary services are busy
3. **Use manual mode** - Set credentials in `config.py` and type 'n' at prompt

### If scraping fails:

1. **Check credentials** - Verify login was successful
2. **Check keyword** - Some keywords may have no results
3. **Rate limiting** - Wait a few minutes if you've been scraping heavily

## API Information

**Guerrilla Mail API:**
- Base URL: `https://api.guerrillamail.com/ajax.php`
- No registration required
- No API keys needed
- Free to use
- Provides temporary email addresses
- Emails expire after ~1 hour

## Security Notes

- Temporary emails are public and insecure
- Don't use for sensitive information
- Credentials are randomly generated per session
- No personal data is stored or transmitted

## Examples

**Example 1: Search for car-related domains**
```bash
python auto_scrape.py cars
# Results saved to domains/cars.txt
```

**Example 2: Search for education domains**
```bash
python auto_scrape.py education
# Results saved to domains/education.txt
```

**Example 3: Interactive mode with custom keyword**
```bash
python main.py
# Choose automated creation
# Enter keyword: technology
# Results saved to domains/technology.txt
```

## Support

For issues or questions:
1. Check this usage guide
2. Review the README.md
3. Test individual components with test scripts
4. Check error messages for specific issues

---

**Happy scraping! 🚀**