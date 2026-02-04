import yfinance as yf
import json
import math
from datetime import datetime
import pytz

# 定義股票
stocks = {
    "0050.TW": "元大台灣50",
    "006208.TW": "富邦台50",
    "00878.TW": "國泰永續高股息"
}

def safe_float(value):
    """將 NaN (無效數值) 轉換為 0，確保 JSON 不會壞掉"""
    if value is None:
        return 0.0
    if isinstance(value, float) and math.isnan(value):
        return 0.0
    return value

def get_stock_data():
    output = {}
    
    for symbol, name in stocks.items():
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.fast_info
            
            # 取得數據並進行安全檢查
            current_price = safe_float(info.last_price)
            prev_close = safe_float(info.previous_close)
            
            if prev_close == 0:
                change = 0
                change_percent = 0
            else:
                change = current_price - prev_close
                change_percent = (change / prev_close) * 100
            
            output[symbol] = {
                "name": name,
                "price": round(current_price, 2),
                "change": round(change, 2),
                "change_percent": round(change_percent, 2),
                "timestamp": datetime.now(pytz.timezone('Asia/Taipei')).strftime("%Y-%m-%d %H:%M:%S")
            }
            print(f"Fetched {symbol}: {current_price}")
            
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            # 如果抓失敗，填入假資料避免整個網頁掛掉
            output[symbol] = {
                "name": name,
                "price": 0,
                "change": 0,
                "change_percent": 0,
                "timestamp": "Error"
            }
            
    return output

if __name__ == "__main__":
    try:
        data = {
            "last_updated": datetime.now(pytz.timezone('Asia/Taipei')).strftime("%Y-%m-%d %H:%M:%S"),
            "stocks": get_stock_data()
        }
        
        # 寫入檔案
        with open("data.json", "w", encoding="utf-8") as f:
            # 這裡不使用 ensure_ascii=False 測試看看，有時候是編碼問題
            # 但為了中文顯示，我們改用標準 unicode 處理
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        print("Data updated successfully.")
        
    except Exception as e:
        print(f"Critical Error: {e}")
        exit(1)
