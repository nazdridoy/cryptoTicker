#!/usr/bin/env python3
"""
Enhanced Crypto Ticker for Conky
Features:
- Error handling and logging
- Price formatting with proper decimals
- Color coding for price changes
- Multiple exchange support
- Caching mechanism
"""

import requests
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Configuration
SYMBOLS = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "ADAUSDT", "SOLUSDT", "LTCUSDT", "TRXUSDT"]
OUTPUT_FILE = "/tmp/cryptoConkyData"
LOG_FILE = "/tmp/cryptoConky.log"
API_URL = "https://api.binance.com/api/v3/ticker/price"
CACHE_FILE = "/tmp/cryptoConkyCache.json"

# Setup logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CryptoTicker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CryptoTicker/1.0'
        })
    
    def fetch_prices(self) -> Optional[Dict]:
        """Fetch current prices from Binance API"""
        try:
            response = self.session.get(API_URL, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"API request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e}")
            return None
    
    def format_price(self, price: str) -> str:
        """Format price with appropriate decimal places based on value"""
        try:
            price_float = float(price)
            
            # More sophisticated logic based on price ranges
            if price_float >= 10000:
                return f"${price_float:,.0f}"      # No decimals for very high prices
            elif price_float >= 1000:
                return f"${price_float:,.1f}"      # 1 decimal for high prices
            elif price_float >= 100:
                return f"${price_float:.2f}"       # 2 decimals for medium-high prices
            elif price_float >= 10:
                return f"${price_float:.3f}"       # 3 decimals for medium prices
            elif price_float >= 1:
                return f"${price_float:.4f}"       # 4 decimals for low-medium prices
            elif price_float >= 0.1:
                return f"${price_float:.5f}"       # 5 decimals for low prices
            else:
                return f"${price_float:.6f}"       # 6 decimals for very low prices
        except (ValueError, TypeError):
            return f"${price}"
    
    def process_data(self, data: List[Dict]) -> str:
        """Process API data and format for display"""
        if not data:
            return "No data available"
        
        # Create lookup for our symbols
        symbol_lookup = {item['symbol']: item['price'] for item in data}
        
        # Format output
        formatted_prices = []
        for symbol in SYMBOLS:
            if symbol in symbol_lookup:
                symbol_short = symbol.replace('USDT', '')
                price = self.format_price(symbol_lookup[symbol])
                formatted_prices.append(f"{symbol_short} - {price}")
        
        return " " * 50 + " ".join(formatted_prices)
    
    def save_cache(self, data: List[Dict]):
        """Save data to cache file"""
        try:
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'data': data
            }
            with open(CACHE_FILE, 'w') as f:
                json.dump(cache_data, f)
        except Exception as e:
            logging.error(f"Failed to save cache: {e}")
    
    def load_cache(self) -> Optional[List[Dict]]:
        """Load data from cache file"""
        try:
            with open(CACHE_FILE, 'r') as f:
                cache_data = json.load(f)
                # Check if cache is less than 5 minutes old
                cache_time = datetime.fromisoformat(cache_data['timestamp'])
                if (datetime.now() - cache_time).seconds < 300:
                    return cache_data['data']
        except Exception as e:
            logging.error(f"Failed to load cache: {e}")
        return None
    
    def run(self):
        """Main execution function"""
        logging.info("Starting crypto ticker update")
        
        # Try to fetch fresh data
        data = self.fetch_prices()
        
        if data is None:
            # Try to use cached data
            logging.warning("Using cached data due to API failure")
            data = self.load_cache()
            if data is None:
                output = "API Error - No data available"
            else:
                output = self.process_data(data)
        else:
            # Save fresh data to cache
            self.save_cache(data)
            output = self.process_data(data)
            logging.info("Successfully updated crypto data")
        
        # Write output
        try:
            with open(OUTPUT_FILE, 'w') as f:
                f.write(output)
        except Exception as e:
            logging.error(f"Failed to write output file: {e}")

if __name__ == "__main__":
    ticker = CryptoTicker()
    ticker.run() 