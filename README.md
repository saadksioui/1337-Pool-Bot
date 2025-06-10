# 1337 Pool Bot

A Python bot that monitors the 1337 admission pool page and sends email notifications when a new pool becomes available.

## Features

- Logs into [admission.1337.ma](https://admission.1337.ma/users/sign_in) using your credentials
- Monitors the pool page for changes
- Sends email notifications when a new pool is posted
- Uses Playwright for browser automation and Gmail for notifications

## Requirements

- Python 3.7+
- Google Chrome (for Playwright)
- Gmail account (for sending notifications)

## Installation

1. **Clone the repository**

   ```sh
   git clone https://github.com/saadksioui/1337-Pool-Bot.git
   cd 1337-pool-bot
   ```

2. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers**

   ```sh
   playwright install
   ```

4. **Configure environment variables**

   - Copy `.env.example` to `.env` and fill in your credentials:

     ```
     cp .env.example .env
     ```

   - Edit `.env` with your 1337 and email credentials.

## Usage

Run the bot:

```sh
python bot.py
```

The bot will log in, monitor the pool page, and send an email notification when a new pool is available.

## Environment Variables

See [.env.example](.env.example) for required variables:

- `1337_USERNAME` and `1337_PASSWORD`: Your 1337.ma login credentials
- `EMAIL_ADDRESS` and `EMAIL_PASSWORD`: Gmail address and app password
- `EMAIL_TO`: Recipient email address

## Notes

- For Gmail, you may need to use an [App Password](https://support.google.com/accounts/answer/185833) if 2FA is enabled.
- The bot uses Chrome at `C:/Program Files/Google/Chrome/Application/chrome.exe` by default. Change the path in [`bot.py`](bot.py) if needed.

## License

MIT License