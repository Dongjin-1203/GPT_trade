import os
import time
import json
import pyupbit
import pandas as pd
from dotenv import load_dotenv
from ta.utils import dropna
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import BollingerBands
from openai import OpenAI

load_dotenv()

def get_chart_with_indicators():
    # 일봉
    df_day = pyupbit.get_ohlcv("KRW-BTC", interval="day", count=30)
    df_day = dropna(df_day)

    rsi_day = RSIIndicator(close=df_day["close"])
    df_day["rsi"] = rsi_day.rsi()

    macd_day = MACD(close=df_day["close"])
    df_day["macd"] = macd_day.macd()
    df_day["macd_signal"] = macd_day.macd_signal()
    df_day["macd_diff"] = macd_day.macd_diff()

    bb_day = BollingerBands(close=df_day["close"])
    df_day["bb_bbm"] = bb_day.bollinger_mavg()
    df_day["bb_bbh"] = bb_day.bollinger_hband()
    df_day["bb_bbl"] = bb_day.bollinger_lband()

    # 시간봉
    df_hour = pyupbit.get_ohlcv("KRW-BTC", interval="minute60", count=24)
    df_hour = dropna(df_hour)

    rsi_hour = RSIIndicator(close=df_hour["close"])
    df_hour["rsi"] = rsi_hour.rsi()

    macd_hour = MACD(close=df_hour["close"])
    df_hour["macd"] = macd_hour.macd()
    df_hour["macd_signal"] = macd_hour.macd_signal()
    df_hour["macd_diff"] = macd_hour.macd_diff()

    bb_hour = BollingerBands(close=df_hour["close"])
    df_hour["bb_bbm"] = bb_hour.bollinger_mavg()
    df_hour["bb_bbh"] = bb_hour.bollinger_hband()
    df_hour["bb_bbl"] = bb_hour.bollinger_lband()

    # 최근 10개만 전송용으로 준비
    return {
        "day_chart": df_day.tail(10).to_dict(orient="records"),
        "hour_chart": df_hour.tail(10).to_dict(orient="records")
    }

def ai_trade():
    # 1. 차트 + 보조지표 데이터 구성
    chart_data = get_chart_with_indicators()

    # 2. AI 판단 요청
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "You are a bitcoin trading advisor. Based on the following candlestick charts and technical indicators (RSI, MACD, Bollinger Bands), "
                            "decide whether to 'buy', 'sell', or 'hold'. Return JSON only like:\n"
                            "{\"decision\": \"buy\", \"reason\": \"...\"}"
                        )
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": json.dumps(chart_data)
                    }
                ]
            }
        ],
        text={"format": {"type": "json_object"}},
        reasoning={},
        tools=[],
        temperature=1,
        max_output_tokens=2048,
        top_p=1,
        store=True
    )

    result = json.loads(response.output[0].content[0].text)
    print("### AI 판단:", result["decision"].upper(), "###")
    print("사유:", result["reason"])

    # 3. 자동매매
    access = os.getenv("UPBIT_ACCESS_KEY")
    secret = os.getenv("UPBIT_SECRET_KEY")
    upbit = pyupbit.Upbit(access, secret)

    if result["decision"] == "buy":
        krw = upbit.get_balance("KRW")
        if krw * 0.9995 > 5000:
            print("🟢 매수 실행")
            res = upbit.buy_market_order("KRW-BTC", krw * 0.9995)
            print(res)
        else:
            print("⚠️ 잔고 부족 (5000원 이하)")

    elif result["decision"] == "sell":
        btc = upbit.get_balance("KRW-BTC")
        ask_price = pyupbit.get_orderbook("KRW-BTC")["orderbook_units"][0]["ask_price"]
        if btc * ask_price > 5000:
            print("🔴 매도 실행")
            res = upbit.sell_market_order("KRW-BTC", btc)
            print(res)
        else:
            print("⚠️ 보유 코인 부족 (가치 5000원 이하)")

    elif result["decision"] == "hold":
        print("🟡 보유 상태 유지")

if __name__ == "__main__":
    while True:
        try:
            ai_trade()
        except Exception as e:
            print("⚠️ 예외 발생:", e)
        time.sleep(60)
