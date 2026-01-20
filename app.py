from flask import Flask, jsonify, request
import yfinance as yf

app = Flask(__name__)

# Home endpoint
@app.route("/", methods=["GET"])
def home():
    return "Flask Stock Market API is running"

# 1️⃣ Company Information Endpoint (GET)
@app.route("/company/<symbol>", methods=["GET"])
def company_info(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info

    return jsonify({
        "company_name": info.get("longName"),
        "industry": info.get("industry"),
        "sector": info.get("sector"),
        "business_summary": info.get("longBusinessSummary")
    })

# 2️⃣ Stock Market Data Endpoint (GET)
@app.route("/stock/<symbol>", methods=["GET"])
def stock_data(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info

    current_price = info.get("currentPrice")
    previous_close = info.get("previousClose")

    price_change = None
    percentage_change = None

    if current_price and previous_close:
        price_change = round(current_price - previous_close, 2)
        percentage_change = round((price_change / previous_close) * 100, 2)

    return jsonify({
        "symbol": symbol,
        "market_state": info.get("marketState"),
        "current_price": current_price,
        "price_change": price_change,
        "percentage_change": percentage_change,
        "day_high": info.get("dayHigh"),
        "day_low": info.get("dayLow"),
        "previous_close": previous_close,
        "volume": info.get("volume"),
        "currency": info.get("currency")
    })

# 3️⃣ Historical Market Data Endpoint (POST)
@app.route("/history", methods=["POST"])
def history():
    data = request.get_json()

    stock = yf.Ticker(data["symbol"])
    hist = stock.history(start=data["start_date"], end=data["end_date"])

    if hist.empty:
        return jsonify({"error": "No historical data found"}), 404

    return jsonify(hist.reset_index().to_dict(orient="records"))

# 4️⃣ Analytical Insights Endpoint (POST)
@app.route("/analysis", methods=["POST"])
def analysis():
    print("ANALYSIS HIT")
    data = request.get_json()

    stock = yf.Ticker(data["symbol"])
    hist = stock.history(period="1y")

    if hist.empty:
        return jsonify({"error": "No data available for analysis"}), 404

    trend = "Upward" if hist["Close"].iloc[-1] > hist["Close"].iloc[0] else "Downward"

    return jsonify({
        "symbol": data["symbol"],
        "average_price": round(hist["Close"].mean(), 2),
        "highest_price": round(hist["High"].max(), 2),
        "lowest_price": round(hist["Low"].min(), 2),
        "trend": trend
    })

if __name__ == "__main__":
    app.run(debug=True)
