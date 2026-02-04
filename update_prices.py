import yfinance as yf
import json
from datetime import datetime
import pytz

# Define the stocks (TWSE stocks need the .TW suffix)
stocks = {
    "0050.TW": "Yuanta Taiwan 50",
    "006208.TW": "Fubon Taiwan 50",
    "00878.TW": "Cathay Sust. Div."
}

def get_stock_data():
    output = {}
    
    for symbol, name in stocks.items():
        try:
            ticker = yf.Ticker(symbol)
            # fast_info provides the most reliable current data
            info = ticker.fast_info
            
            # Get current price
            current_price = info.last_price
            prev_close = info.previous_close
            
            # Calculate change
            change = current_price - prev_close
            change_percent = (change / prev_close) * 100
            
            output[symbol] = {
                "name": name,
                "price": round(current_price, 2),
                "change": round(change, 2),
                "change_percent": round(change_percent, 2),
                "timestamp": datetime.now(pytz.timezone('Asia/Taipei')).strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            
    return output

if __name__ == "__main__":
    data = {
        "last_updated": datetime.now(pytz.timezone('Asia/Taipei')).strftime("%Y-%m-%d %H:%M:%S"),
        "stocks": get_stock_data()
    }
    
    # Save to JSON file that the website will read
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        
    print("Data updated successfully.")