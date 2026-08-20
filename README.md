# InfoStealer

Program that collects system and browser information with keylogger.

## Features

### Collected information

#### System information:

- External IP
- network adapters
- saved Wi-Fi passwords (plaintext)
- Windows product key
- installed antivirus
- domain membership

#### Chromium browser data:

- Saved passwords (Login Data) - using Chrome-App-Bound-Encryption-Decryption
- Cookies
- Autofill data (Web Data)
- Browsing history
- Credit card data
- Browser extensions

### Keylogger

Program logs every keystroke made by a user

### Clipboard

Program logs user's clipboard content

### AutoStart

Programs starts automatically on system startup

### Sending data via Telegram

Program sends harvested data every 20 seconds

## Usage

Run:

`git clone https://github.com/Jimi090/InfoStealer.git`

`cd InfoStealer`

Create a Telegram Bot:

1. Install Telegram
2. Go to `u/BotFather` on Telegram
3. Send `/newbot`
4. Follow the steps to get your token
5. Send `/start` to your bot. You will receive your token
6. Send random message to your bot e.g. `aaa`
7. Go to `https://api.telegram.org/bot{YOUR_BOT_TOKEN}/getUpdates` to get your chat_id
8. Create .env file containing:
   `TELEGRAM_TOKEN=YOUR_TOKEN`
   `CHAT_ID=YOUR_CHAT_ID`

Compile the script:

`pip install pyinstaller`

`python.exe -m PyInstaller --one-file  .\main.py`

The output .exe file is a finished program.

Change the name of the file to the one in python config variables. Default is `ClientInfo.exe`

## Project Purpose

This project is intended for educational and security research purposes. Testing should only be performed on systems and
data you own or have explicit permission to use.

## Project Structure

[main.py](/main.py) → main program

[chromiumExtractor.exe](/chromiumExtractor.exe) → Chrome-App-Bound-Encryption-Decryption

[LICENSE](/LICENSE) → MIT License

[THIRD-PARTY-NOTICES.txt](/THIRD-PARTY-NOTICES.txt) → Third-party software used

## Technologies

- Python 3.14.6
- Python Libraries
- Chrome-App-Bound-Encryption-Decryption
- SQLite

## LICENSE

Project is under MIT License

## Third-party software

This project includes third-party software:

- **Chrome-App-Bound-Encryption-Decryption** — Copyright (c) 2025 Alexander 'xaitax' Hagenah — MIT License.
- **SQLite** — public-domain software; copyright is disclaimed by the SQLite source.

See [`THIRD-PARTY-NOTICES.txt`](THIRD-PARTY-NOTICES.txt) for the applicable notices.

## HackClub

Project was made for ISPY HackClub Program [link](https://ispy.hackclub.com/)