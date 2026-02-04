import yfinance as yf
import json
from datetime import datetime
import pytz

# 定義股票代碼與對應的中文名稱
stocks = {
    "0050.TW": "元大台灣50",
    "006208.TW": "富邦台50",
    "00878.TW": "國泰永續高股息"
}

def get_stock_data():
    output = {}
    
    for symbol, name in stocks.items():
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.fast_info
            
            # 取得即時價格
            current_price = info.last_price
            prev_close = info.previous_close
            
            # 計算漲跌
            change = current_price - prev_close
            change_percent = (change / prev_close) * 100
            
            output[symbol] = {
                "name": name,
                "price": round(current_price, 2),
                "change": round(change, 2),
                "change_percent": round(change_percent, 2),
                # 設定為台北時間
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
    
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False) # ensure_ascii=False 確保中文正常顯示
        
    print("Data updated successfully.")
