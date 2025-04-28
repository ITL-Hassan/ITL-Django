import requests
import json

def getWeatherData():
  api_url = "https://weather.tsukumijima.net/api/forecast/city/400010"

  response = requests.get(api_url)
  data = response.json()

  forecast = {
    'date' : data["forecasts"][0]["date"].replace( '-', '/' ),
    'telop' : data["forecasts"][0]["telop"],
    'image' : data["forecasts"][0]["image"]["url"],
    'max' : data["forecasts"][0]["temperature"]["max"]["celsius"],
    'min' : data["forecasts"][0]["temperature"]["min"]["celsius"],
  }
  
  return forecast


  if response.status_code == 200:
    # データをJSON形式で解析
    data = response.json()

    # 取得したデータを表示
    print(json.dumps(data, indent=4))

    return response

  else:
    print(f"Error: {response.status_code}")
    print(f"Error Message: {response.text}")