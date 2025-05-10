import os
import time
import json
import requests
import pyupbit
import pandas as pd
from dotenv import load_dotenv
from ta.utils import dropna
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import BollingerBands
from openai import OpenAI

# 환경 변수 로드
load_dotenv()

# FNG API 호출 함수
def get_fear_and_greed():
    url = "https://api.alternative.me/fng/?limit=1"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()["data"][0]
            value = int(data["value"])
            label = data["value_classification"]
            return value, label
        else:
            print("❌ FNG API 요청 실패:", response.status_code)
            return None, None
    except Exception as e:
        print("❌ FNG API 예외:", e)
        return None, None

# 보조지표 포함한 차트 데이터 구성
def get_chart_with_indicators():
    # 30일 일봉
    df_day = pyupbit.get_ohlcv("KRW-BTC", interval="day", count=30)
    df_day = dropna(df_day)
    df_day["rsi"] = RSIIndicator(df_day["close"]).rsi()
    macd = MACD(df_day["close"])
    df_day["macd"] = macd.macd()
    df_day["macd_signal"] = macd.macd_signal()
    df_day["macd_diff"] = macd.macd_diff()
    bb = BollingerBands(df_day["close"])
    df_day["bb_bbm"] = bb.bollinger_mavg()
    df_day["bb_bbh"] = bb.bollinger_hband()
    df_day["bb_bbl"] = bb.bollinger_lband()

    # 24시간 시간봉
    df_hour = pyupbit.get_ohlcv("KRW-BTC", interval="minute60", count=24)
    df_hour = dropna(df_hour)
    df_hour["rsi"] = RSIIndicator(df_hour["close"]).rsi()
    macd_h = MACD(df_hour["close"])
    df_hour["macd"] = macd_h.macd()
    df_hour["macd_signal"] = macd_h.macd_signal()
    df_hour["macd_diff"] = macd_h.macd_diff()
    bb_h = BollingerBands(df_hour["close"])
    df_hour["bb_bbm"] = bb_h.bollinger_mavg()
    df_hour["bb_bbh"] = bb_h.bollinger_hband()
    df_hour["bb_bbl"] = bb_h.bollinger_lband()

    return {
        "day_chart": df_day.tail(10).to_dict(orient="records"),
        "hour_chart": df_hour.tail(10).to_dict(orient="records")
    }

# AI + FNG 기반 자동매매 함수
def ai_trade():
    # 1. 차트 + 보조지표 수집
    chart_data = get_chart_with_indicators()

    # 2. GPT-4 판단 요청
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
                            "You are a bitcoin trading advisor. Based on the candlestick chart and indicators (RSI, MACD, Bollinger Bands), "
                            "decide whether to 'buy', 'sell', or 'hold'. Respond only in JSON like:\n"
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
    print(f"🧠 GPT 판단: {result['decision'].upper()} | 이유: {result['reason']}")

    # 3. FNG 지표 확인
    fng_value, fng_label = get_fear_and_greed()
    print(f"📊 FNG 지수: {fng_value} ({fng_label})")

    # 4. 업비트 인증
    access = os.getenv("UPBIT_ACCESS_KEY")
    secret = os.getenv("UPBIT_SECRET_KEY")
    upbit = pyupbit.Upbit(access, secret)

    # 5. 판단 + FNG 조건에 따른 매매 실행
    if result["decision"] == "buy":
        if fng_value is not None and fng_value <= 40:
            krw = upbit.get_balance("KRW")
            if krw * 0.9995 > 5000:
                print("🟢 매수 실행")
                res = upbit.buy_market_order("KRW-BTC", krw * 0.9995)
                print(res)
            else:
                print("⚠️ 잔고 부족")
        else:
            print("⛔ 공포 상태 아님 → 매수 제한")

    elif result["decision"] == "sell":
        if fng_value is not None and fng_value >= 70:
            btc = upbit.get_balance("BTC")  # ✅ 'KRW-BTC' → 'BTC'

            if btc is None or float(btc) == 0.0:
                print("⚠️ BTC 보유 수량이 없습니다. 매도 스킵")
                return

            orderbook = pyupbit.get_orderbook("KRW-BTC")
            if not orderbook or "orderbook_units" not in orderbook[0]:
                print("❌ 오더북 조회 실패 또는 구조 오류")
                return

            ask_price = orderbook[0]["orderbook_units"][0]["ask_price"]
            if ask_price is None:
                print("❌ ask_price가 None입니다.")
                return

            if float(btc) * ask_price > 5000:
                print("🔴 매도 실행")
                res = upbit.sell_market_order("KRW-BTC", float(btc))
                print(res)
            else:
                print("⚠️ 보유 코인 가치가 5000원 미만입니다.")
        else:
            print("⛔ 탐욕 상태 아님 → 매도 제한")



    else:
        print("🟡 보유 유지 (HOLD)")

# 메인 루프: 60초 간격으로 실행
if __name__ == "__main__":
    while True:
        try:
            ai_trade()
        except Exception as e:
            print("❌ 예외 발생:", e)
        time.sleep(60)
