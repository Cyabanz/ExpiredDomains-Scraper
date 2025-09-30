# Implementation Summary: Automated Account Creation

## What Was Implemented

I've successfully added **automated account creation** to your ExpiredDomains scraper using the **Guerrilla Mail API**. You no longer need to use your personal account!

## New Files Created

### 1. `guerrilla_mail.py` (4.3 KB)
**Guerrilla Mail API Client**
- `GuerrillaMailClient` class for interacting with Guerrilla Mail API
- `get_email_address()` - Creates temporary email addresses
- `set_email_user()` - Sets custom email usernames
- `check_email()` - Checks for new emails
- `fetch_email()` - Fetches full email content
- `wait_for_email()` - Waits for verification emails
- `generate_random_credentials()` - Creates random username/password

### 2. `account_creator.py` (6.8 KB)
**Automated Account Registration**
- `ExpiredDomainsAccountCreator` class
- Automatically creates temporary email addresses
- Generates random credentials
- Registers accounts on expireddomains.net
- Handles email verification
- Returns working credentials for immediate use

### 3. `auto_scrape.py` (1.4 KB)
**Fully Automated Scraper**
- No user interaction required
- Command-line usage: `python auto_scrape.py <keyword>`
- Automatically creates account and scrapes
- Perfect for automation scripts

### 4. `test_guerrilla_mail.py` (2.0 KB)
**Testing Utility**
- Tests Guerrilla Mail API functionality
- Demonstrates temporary email creation
- Verifies email checking capabilities
- Useful for debugging

### 5. `requirements.txt`
**Dependencies**
- `requests>=2.28.0` - HTTP library
- `pyquery>=2.0.0` - HTML parsing

### 6. `USAGE_GUIDE.md`
**Comprehensive Usage Documentation**
- Step-by-step instructions
- Multiple usage modes
- Examples and troubleshooting
- Security notes

## Modified Files

### `main.py`
**Changes:**
- Added automated account creation option
- Prompts user for automation preference
- Falls back to config.py if automation fails
- Passes credentials to User class

**Before:**
```python
user = User(keyword)
```

**After:**
```python
username, password = get_or_create_account()
user = User(keyword, username, password)
```

### `expireddomains.py`
**Changes:**
- Updated `User.__init__()` to accept username/password parameters
- Removed dependency on config module for credentials
- Now uses instance variables instead of config variables

**Before:**
```python
def __init__(self, keyword) -> None:
    self.keyword = keyword
    # Uses config.username and config.password
```

**After:**
```python
def __init__(self, keyword, username=None, password=None) -> None:
    self.username = username
    self.password = password
    # Uses self.username and self.password
```

### `README.md`
**Updated with:**
- Feature list highlighting automation
- Installation instructions
- Usage examples for both automated and manual modes
- File descriptions

## How It Works

### Automated Flow:

```
1. User runs: python main.py
   ↓
2. Script prompts: Use automated account creation? (y/n)
   ↓
3. User confirms (Enter or 'y')
   ↓
4. Guerrilla Mail API creates temporary email
   ↓
5. Random credentials generated
   ↓
6. Account registered on expireddomains.net
   ↓
7. Email verification handled (if needed)
   ↓
8. User enters search keyword
   ↓
9. Scraper logs in and scrapes domains
   ↓
10. Results saved to domains/<keyword>.txt
```

### Fully Automated Flow:

```
1. User runs: python auto_scrape.py cars
   ↓
2. Account automatically created in background
   ↓
3. Logs in and searches for "cars"
   ↓
4. Results saved to domains/cars.txt
```

## Key Features

✅ **Zero Personal Information Required**
- Temporary emails from Guerrilla Mail
- Random generated usernames
- Secure random passwords
- No email verification needed on your end

✅ **Multiple Usage Modes**
- Interactive mode (main.py)
- Fully automated mode (auto_scrape.py)
- Manual mode (config.py fallback)
- Test mode (test_guerrilla_mail.py)

✅ **Robust Error Handling**
- Falls back to manual credentials if automation fails
- Handles registration errors
- Retries on username conflicts
- Comprehensive error messages

✅ **Developer Friendly**
- Well-documented code
- Modular design
- Easy to extend
- Test utilities included

## Usage Examples

### Example 1: Interactive Mode
```bash
$ python main.py
Use automated account creation? (y/n) [default: y]: ← Press Enter

============================================================
AUTOMATED ACCOUNT CREATION
============================================================

[1/4] Creating temporary email address...
[GuerrillaMail] Created temporary email: abc123@guerrillamail.com

[2/4] Generating random credentials...
Username: xyz789qwer
Password: aB3$xY9zK!m

[3/4] Registering account on expireddomains.net...
Registration submitted successfully

[4/4] Checking for verification email...

============================================================
ACCOUNT CREATED SUCCESSFULLY!
============================================================

Please enter keyword:
- cars ← User enters keyword

Scraping...
```

### Example 2: Fully Automated
```bash
$ python auto_scrape.py technology

[INFO] Starting automated scrape for keyword: technology
[INFO] Using automated account creation with Guerrilla Mail API
[GuerrillaMail] Created temporary email: def456@guerrillamail.com
[INFO] Logging in with automated account...
[INFO] Searching for domains with keyword: technology
[INFO] Starting scrape...

CURRENT SESSION
Scraped - 50
Limit - 200
Total Available - 1234
Progress - 25%

[SUCCESS] Scraping completed! Check domains/technology.txt
```

### Example 3: Test Guerrilla Mail
```bash
$ python test_guerrilla_mail.py

============================================================
GUERRILLA MAIL API TEST
============================================================

[1] Creating temporary email address...
✓ Successfully created: ghi789@guerrillamail.com

[2] Testing custom username...
✓ Updated to: testuser123@guerrillamail.com

[3] Checking for emails...
✓ Found 0 email(s)

============================================================
TEST COMPLETED
============================================================
```

## Benefits

### Before (Manual Mode)
❌ Required personal email address
❌ Manual account registration
❌ Manual email verification
❌ Risk of exposing personal information
❌ One account per email

### After (Automated Mode)
✅ No personal information needed
✅ Automatic account creation
✅ Automatic verification handling
✅ Complete privacy
✅ Unlimited accounts on demand

## Technical Details

### Guerrilla Mail API
- **Endpoint:** `https://api.guerrillamail.com/ajax.php`
- **Authentication:** None required
- **Rate Limiting:** Generous, no strict limits
- **Email Lifetime:** ~1 hour
- **Format:** JSON responses
- **Methods Used:**
  - `get_email_address` - Create new email
  - `set_email_user` - Customize username
  - `check_email` - Poll for new emails
  - `fetch_email` - Get email content

### Security Considerations
- Temporary emails are disposable
- No sensitive data should be sent to them
- Emails are public and can be accessed by anyone who knows the address
- Perfect for one-time registrations
- Credentials are randomly generated and unique per session

## Dependencies

Only 2 Python packages required:
```
requests>=2.28.0  # For HTTP requests
pyquery>=2.0.0    # For HTML parsing
```

Install with:
```bash
pip install -r requirements.txt
```

## Configuration

### No Configuration Required!
The automated mode works out of the box with zero configuration.

### Optional: Manual Mode Fallback
Edit `config.py` if you want to use manual credentials:
```python
username = 'your_username' 
password = 'your_password'
```

## Testing

Test the implementation:

```bash
# Test Guerrilla Mail API
python test_guerrilla_mail.py

# Test automated account creation (interactive)
python main.py
# Choose 'y' for automation

# Test fully automated mode
python auto_scrape.py test
```

## Future Enhancements (Optional)

Potential improvements you could add:
- [ ] Save created credentials to a file for reuse
- [ ] Support multiple temporary email providers
- [ ] Add CAPTCHA solving integration
- [ ] Implement account pool management
- [ ] Add proxy support for IP rotation
- [ ] Create web UI for easier use

## Summary

✅ **Automated account creation implemented**
✅ **Guerrilla Mail API integrated**
✅ **No personal account needed**
✅ **Multiple usage modes available**
✅ **Comprehensive documentation provided**
✅ **Backward compatible with manual mode**
✅ **Zero configuration required**

**You can now scrape ExpiredDomains without using your personal account!**

---

**Need help?** Check `USAGE_GUIDE.md` for detailed instructions.

**Ready to use?** Run `python main.py` and press Enter!