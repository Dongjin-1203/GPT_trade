import os
import pyupbit
import json
from dotenv import load_dotenv
load_dotenv()

def ai_trade():
    # 1. 업비트 차트 가져오기 (30일 일봉)
    df_30d = pyupbit.get_ohlcv("KRW-BTC", interval="day", count=30)
    print("최근 30일 일봉 차트 데이터:")
    print(df_30d.tail())

    # 2. 24시간 시간봉 차트 가져오기
    df_24h = pyupbit.get_ohlcv("KRW-BTC", interval="minute60", count=24)
    print("최근 24시간 시간봉 차트 데이터:")
    print(df_24h.tail())

    # 3. 현재 투자 상태 조회
    access = os.getenv("UPBIT_ACCESS_KEY")          # 본인 값으로 변경
    secret = os.getenv("UPBIT_SECRET_KEY")          # 본인 값으로 변경
    upbit = pyupbit.Upbit(access, secret)

    krw_balance = upbit.get_balance("KRW")  # 원화 잔고
    btc_balance = upbit.get_balance("KRW-BTC")  # BTC 보유량

    print(f"현재 KRW 잔고: {krw_balance}")
    print(f"현재 BTC 보유량: {btc_balance}")

    # 4. 오더북 (호가 데이터) 조회
    orderbook = pyupbit.get_orderbook(ticker="KRW-BTC")
    ask_price = orderbook['orderbook_units'][0]['ask_price']  # 최우선 매도 호가
    bid_price = orderbook['orderbook_units'][0]['bid_price']  # 최우선 매수 호가

    print(f"최우선 매도 호가: {ask_price}")
    print(f"최우선 매수 호가: {bid_price}")

    # # 5. AI에게 차트 주고 투자 판단 받기 (buy, sell, hold)
    # from openai import OpenAI
    # client = OpenAI()

    # response = client.responses.create(
    #     model="gpt-4.1",
    #     input=[{
    #         "role": "system",
    #         "content": [
    #             {
    #                 "type": "input_text",
    #                 "text": "You are the ultimate Bitcoin investing expert. Tell me whether to buy, sell, or hold at the moment based on the chart data provided. response in json format\n\nResponse Example:\n{\"decision\": \"buy\",  \"reason\": \"some technical reason\"}\n{\"decision\": \"sell\",  \"reason\": \"some technical reason\"}\n{\"decision\": \"hold\",  \"reason\": \"some technical reason\"}"
    #             }
    #         ]
    #     },
    #     {
    #         "role": "user",
    #         "content": [
    #             {
    #                 "type": "input_text",
    #                 "text": df_30d.to_json()      # 실제데이터를 JSON데이터로 받아와 GPT가 판단을 하는 코드
    #             }
    #         ]
    #     }],
    #     text={
    #         "format": {
    #             "type": "json_object"
    #         }
    #     },
    #     reasoning={},
    #     tools=[],
    #     temperature=1,
    #     max_output_tokens=2048,
    #     top_p=1,
    #     store=True
    # )

    # # 6. 결과 파싱 및 자동매매
    # result = response.output[0].content[0].text
    # result = json.loads(result)

    # print("### AI Decision: ", result["decision"].upper(), "###")
    # print(f"### Reason: {result['reason']} ###")

    # if result["decision"] == "buy":
    #     # 매수
    #     my_balance = upbit.get_balance("KRW")
    #     if my_balance * 0.9995 > 5000:
    #         print("### Buy Order Executed ###")
    #         print(upbit.buy_market_order("KRW-BTC", my_balance * 0.9995))
    #         print("buy:", result["reason"])
    #     else:
    #         print("잔고가 5000원 미만입니다. ")
    # elif result["decision"] == "sell":
    #     # 매도
    #     my_coin = upbit.get_balance("KRW-BTC")
    #     current_price = pyupbit.get_orderbook(ticker="KRW-BTC")["orderbook_units"][0]["ask_price"]

    #     if my_coin * current_price > 5000:
    #         print("### Sell Order Executed ###")
    #         print(upbit.sell_market_order("KRW-BTC"))
    #         print("sell", result["reason"])
    #     else:
    #         print("보유 코인이 5000원 미만입니다. ")
    # elif result["decision"] == "hold":
    #     # 지나감
    #     print("hold: ", result["reason"])

# while True:
#     import time
#     time.sleep(60)
ai_trade()
