#!/bin/bash

# Define symbols as a space-separated string
SYMBOLS="BTCUSDT ETHUSDT XRPUSDT ADAUSDT SOLUSDT LTCUSDT TRXUSDT"

# Log file for debugging
LOG_FILE="/tmp/cryptoConky.log"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Convert space-separated symbols to JSON array format for jq
JQ_SYMBOLS=$(echo "$SYMBOLS" | tr ' ' '\n' | jq -R . | jq -s .)

# Fetch data with error handling
RESPONSE=$(curl -s --max-time 10 "https://api.binance.com/api/v3/ticker/price")

if [ $? -ne 0 ]; then
    log_message "ERROR: Failed to fetch data from Binance API"
    # Use cached data if available, otherwise show error
    if [ -f "/tmp/cryptoConkyData" ]; then
        echo "API Error - Using cached data" > /tmp/cryptoConkyData.tmp
        cat /tmp/cryptoConkyData >> /tmp/cryptoConkyData.tmp
        mv /tmp/cryptoConkyData.tmp /tmp/cryptoConkyData
    else
        echo "API Error - No data available" > /tmp/cryptoConkyData
    fi
    exit 1
fi

# Process data with error handling
(printf "%50s" " "; echo "$RESPONSE" | \
jq -r --argjson symbols "$JQ_SYMBOLS" '
  def order: reduce ($symbols | to_entries[]) as {key: $k, value: $v} ({};
    . + {($v): $k}
  );
  [.[] | select(.symbol as $s | $symbols | index($s) != null)] |
  sort_by(order[.symbol]) |
  .[] | "\(.symbol | sub("USDT$"; "")) - $\(.price | tonumber | .* 1000 | floor / 1000)"
' | \
tr '\n' ' ') > /tmp/cryptoConkyData

# Check if processing was successful
if [ $? -eq 0 ] && [ -s /tmp/cryptoConkyData ]; then
    log_message "SUCCESS: Data updated successfully"
else
    log_message "ERROR: Failed to process data"
    echo "Data processing error" > /tmp/cryptoConkyData
fi

