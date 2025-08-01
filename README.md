# Crypto Ticker for Conky

A real-time cryptocurrency price ticker that displays live crypto prices using Conky on Linux systems. This project provides both bash and Python implementations with enhanced error handling, caching, and smart price formatting.

<img width="1258" height="25" alt="2025-08-01_15-45-55" src="https://github.com/user-attachments/assets/dda7765c-4c7a-4fdd-a769-52cec503ece0" />


## 🚀 Features

- **Real-time Updates**: Fetches live prices from Binance API
- **Smart Formatting**: Adaptive decimal places based on price ranges
- **Error Handling**: Robust error handling with fallback to cached data
- **Multiple Implementations**: Both bash and Python versions available
- **User Service**: Runs as a user-level systemd service
- **Logging**: Comprehensive logging for debugging
- **Caching**: Offline operation with cached data

## 📊 Supported Cryptocurrencies

The project currently includes these popular cryptocurrencies by default:

- Bitcoin (BTC)
- Ethereum (ETH)
- Ripple (XRP)
- Cardano (ADA)
- Solana (SOL)
- Litecoin (LTC)
- TRON (TRX)

### 🆕 Adding More Cryptocurrencies

**You can easily add ANY cryptocurrency supported by Binance API!** Simply edit the `SYMBOLS` variable in your chosen script:

#### For Python Version (`pyCryptoTicker.py`):
```python
SYMBOLS = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "ADAUSDT", "SOLUSDT", "LTCUSDT", "TRXUSDT", "DOGEUSDT", "MATICUSDT", "DOTUSDT"]
```

#### For Bash Version (`cryptoConky.sh`):
```bash
SYMBOLS="BTCUSDT ETHUSDT XRPUSDT ADAUSDT SOLUSDT LTCUSDT TRXUSDT DOGEUSDT MATICUSDT DOTUSDT"
```

#### Popular Additions:
- **DOGEUSDT** - Dogecoin
- **MATICUSDT** - Polygon
- **DOTUSDT** - Polkadot
- **LINKUSDT** - Chainlink
- **UNIUSDT** - Uniswap
- **AVAXUSDT** - Avalanche
- **ATOMUSDT** - Cosmos
- **NEARUSDT** - NEAR Protocol

#### How to Find Available Symbols:
1. Visit [Binance API Documentation](https://binance-docs.github.io/apidocs/spot/en/)
2. Check the `/api/v3/ticker/price` endpoint
3. All symbols ending with "USDT" are available

**Note**: The script automatically handles any number of cryptocurrencies you add!

## 🛠️ Requirements

- Linux system with systemd
- Python 3.6+ (for Python version)
- `jq` (for bash version)
- `curl` (for bash version)
- `conky` (for display) - Modern version recommended for best compatibility
- `requests` Python package (for Python version)

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/nazdridoy/cryptoTicker.git
cd cryptoTicker
```

### 2. Install Dependencies

#### For Python Version:
```bash
# Install requests package
pip install requests
# or using uv
uv add requests
```

#### For Bash Version:
```bash
# Install jq (if not already installed)
sudo pacman -S jq  # Arch Linux
# or
sudo apt install jq  # Ubuntu/Debian
```

### 3. Make Scripts Executable
```bash
chmod +x cryptoConky.sh
chmod +x pyCryptoTicker.py
```

## ⚙️ Configuration

### Service Setup

1. **Copy service file to user systemd directory:**
```bash
cp crypto-ticker.service ~/.config/systemd/user/
```

2. **⚠️ IMPORTANT: Update the service file paths**
   
   **You MUST edit the service file to match your repository location:**
   
   ```bash
   # Edit the service file
   nano ~/.config/systemd/user/crypto-ticker.service
   ```
   
   **Change these lines to match your actual repository path:**
   ```ini
   WorkingDirectory=%h/NAZ/config/cryptoTicker
   ExecStart=/usr/bin/python3 %h/NAZ/config/cryptoTicker/pyCryptoTicker.py
   ```
   
   **Examples for different locations:**
   - If cloned to `~/projects/cryptoTicker`: Use `%h/projects/cryptoTicker`
   - If cloned to `~/Desktop/cryptoTicker`: Use `%h/Desktop/cryptoTicker`
   - If cloned to `~/cryptoTicker`: Use `%h/cryptoTicker`

3. **Reload and enable the service:**
```bash
systemctl --user daemon-reload
systemctl --user enable crypto-ticker.service
systemctl --user start crypto-ticker.service
```

**Note**: The `%h` represents your home directory, but you must update the path to match where you cloned the repository.

### Conky Configuration

1. **Copy the conky configuration:**
```bash
cp cryptoConky.conf ~/.conky/
```

2. **Start Conky with the configuration:**
```bash
conky -c ~/.conky/cryptoConky.conf
```

## 🎯 Usage

### Manual Execution

#### Python Version:
```bash
python pyCryptoTicker.py
cat /tmp/cryptoConkyData
```

#### Bash Version:
```bash
./cryptoConky.sh
cat /tmp/cryptoConkyData
```

### Service Management

```bash
# Start the service
systemctl --user start crypto-ticker.service

# Check status
systemctl --user status crypto-ticker.service

# View logs
journalctl --user -u crypto-ticker.service -f

# Stop the service
systemctl --user stop crypto-ticker.service
```

### Conky Toggle Script

Use the included toggle script to easily start/stop the Conky display:

```bash
# Make the script executable
chmod +x cryptoConkyToggle.sh

# Toggle Conky on/off
./cryptoConkyToggle.sh
```

**Note**: The toggle script automatically detects the correct path and works for any user.

## 🔧 Customization

### Adding/Removing Cryptocurrencies

Edit the `SYMBOLS` variable in either script:

```bash
# In cryptoConky.sh
SYMBOLS="BTCUSDT ETHUSDT XRPUSDT ADAUSDT SOLUSDT LTCUSDT TRXUSDT DOGEUSDT"

# In pyCryptoTicker.py
SYMBOLS = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "ADAUSDT", "SOLUSDT", "LTCUSDT", "TRXUSDT", "DOGEUSDT"]
```

### Price Formatting Logic

The Python version uses intelligent decimal formatting:

- **≥ $10,000**: No decimals (e.g., $45,123)
- **≥ $1,000**: 1 decimal (e.g., $3,456.7)
- **≥ $100**: 2 decimals (e.g., $123.45)
- **≥ $10**: 3 decimals (e.g., $12.345)
- **≥ $1**: 4 decimals (e.g., $1.2345)
- **≥ $0.1**: 5 decimals (e.g., $0.12345)
- **< $0.1**: 6 decimals (e.g., $0.012345)

## 📁 Project Structure

```
cryptoTicker/
├── cryptoConky.sh          # Bash implementation
├── pyCryptoTicker.py       # Python implementation
├── cryptoConky.conf        # Conky configuration
├── crypto-ticker.service   # Systemd service file
├── TEMP-Dev/              # Temporary development files
└── README.md              # This file
```

## 🐛 Troubleshooting

### Common Issues

1. **Service not starting:**
   ```bash
   journalctl --user -u crypto-ticker.service -f
   ```

2. **Service path errors:**
   ```bash
   # Check if the service file paths are correct
   cat ~/.config/systemd/user/crypto-ticker.service
   
   # Common error: "No such file or directory"
   # Solution: Update WorkingDirectory and ExecStart paths in the service file
   ```

3. **No data displayed:**
   ```bash
   cat /tmp/cryptoConkyData
   ```

4. **API errors:**
   ```bash
   tail -f /tmp/cryptoConky.log
   ```

### Log Files

- **Service logs**: `journalctl --user -u crypto-ticker.service`
- **Application logs**: `/tmp/cryptoConky.log`
- **Cache file**: `/tmp/cryptoConkyCache.json`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Binance API](https://binance-docs.github.io/apidocs/spot/en/) for providing cryptocurrency data
- [Conky](https://github.com/brndnmtthws/conky) for the desktop widget system
- [jq](https://stedolan.github.io/jq/) for JSON processing in bash

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section
2. Review the logs
3. Open an issue on GitHub

---

**Note**: This project is for educational and personal use. Always verify cryptocurrency data from official sources before making financial decisions. 