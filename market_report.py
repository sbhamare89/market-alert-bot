import subprocess
import sys

# Auto install missing packages
def install_if_missing(package):
  try:
    __import__(package)
  except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for pkg in ['requests', 'yfinance', 'forex_python']:
  install_if_missing(pkg)

import requests
import datetime
import yfinance as yf
from forex_python.converter import CurrencyRates

import os

# Load from github secrets if used
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

def send_telegram_message(message):
  url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
  data = {'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}
  requests.post(url, data=data)

def get_nifty_50():
    nifty = yf.Ticker("^NSEI")
    data = nifty.history(period="1d")
    return data['Close'].iloc[-1]

def get_goldbees():
    gold = yf.Ticker("GOLDBEES.BO")
    data = gold.history(period="1d")
    return data['Close'].iloc[-1]

def get_exchange_rates():
    # Ticker for USD/INR and SAR/INR
    usd_inr_ticker = yf.Ticker("USDINR=X")
    sar_inr_ticker = yf.Ticker("SARINR=X")
    
    # Fetch historical data for both
    usd_inr_data = usd_inr_ticker.history(period="1d")
    sar_inr_data = sar_inr_ticker.history(period="1d")
    
    # Get the closing rate for each
    usd_inr = usd_inr_data['Close'].iloc[-1]
    sar_inr = sar_inr_data['Close'].iloc[-1]
    
    return usd_inr, sar_inr

def main():
  try:
    nifty = get_nifty_50()
    gold = get_goldbees()
    usd_inr, sar_inr = get_exchange_rates()
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = (
      f"*📊 Morning Market Snapshot* ({today})\n\n"
      f"Nifty 50 : {nifty:.2f}\n"
      f"Gold Bees: ₹{gold:.2f}\n"
      f"💵 USD/INR: ₹{usd_inr:.2f}\n"
      f"🇸🇦 SAR/INR: ₹{sar_inr:.2f}"
    )
    send_telegram_message(message)
  except Exception as e:
    send_telegram_message(f" FAILED to fetch data: {e}")

if __name__ == "__main__":
  main()
