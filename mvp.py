import os
from dotenv import load_dotenv
load_dotenv()

# 1. 업비트 차트 가져오기(30일 일봉)
import pyupbit

df = pyupbit.get_ohlcv("KRW-BTC", interval="day", count=30)
#print(df.to_json())

# 2. AI에게 차트 주고 투자 판단 받기(buy, sell, hold)
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
  model="gpt-4.1",
  input=[
      # 역할 설정
    {
      "role": "system",
      "content": [
        {
          "type": "input_text",
          "text": "You are the ultimate Bitcoin investing expert. Tell me whether to buy, sell, or hold at the moment based on the chart data provided. response in json format\n\nResponse Example:\n{\"decision\": \"buy\",  \"reason\": \"some technical reason\"}\n{\"decision\": \"sell\",  \"reason\": \"some technical reason\"}\n{\"decision\": \"hold\",  \"reason\": \"some technical reason\"}"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": df.to_json()      # 실제데이터를 JSON데이터를 받아와 GPT가 판단을 하는 코드드
        }
      ]
    }
  ],
  text={
    "format": {
      "type": "json_object"
    }
  },
  reasoning={},
  tools=[],
  temperature=1,
  max_output_tokens=2048,
  top_p=1,
  store=True
)
result = response.output[0].content[0].text
# 3. 받은 데이터로 자동매매 하기
import json
result  = json.loads(result)
access = os.getenv("UPBIT_ACCESS_KEY")          # 본인 값으로 변경
secret = os.getenv("UPBIT_SECRET_KEY")          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

if result["decision"] == "buy":
    # 매수
    print(upbit.buy_market_order("KRW-BTC", upbit.get_balance("KRW")))
    print(result["reason"])
elif result["decision"] == "sell":
    # 매도
    print(upbit.sell_market_order("KRW-BTC", upbit.get_balance("KRW-BTC")))
    print(result["reason"])
elif result["decision"] == "hold":
    # 지나감
    print(result["reason"])