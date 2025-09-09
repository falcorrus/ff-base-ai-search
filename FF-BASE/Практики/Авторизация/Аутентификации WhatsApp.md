От @Djonua
https://t.me/flutterflow_rus/12427/54235

1. Регистрируешься на Whapi.cloud.
2. Меняешь язык на русский (появится возможность оплачивать рф картами да и цена совсем другая). Можно на тестовом периоде попробовать в принципе.
3. Создаешь новый канал и сканируешь QR код. копируешь API токен.
4. В FlutterFlow в разделе API создаешь Post запрос с параметрами:

URL: https://gate.whapi.cloud/messages/text

Headers:
authorization: Bearer [apiKey]
accept: application/json
content-type: application/json

Body: 
{
  "typing_time": 0,
  "body": "<body>",
  "to": "<to>"
}

Ну и создаешь нужные переменные.