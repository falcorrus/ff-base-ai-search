Иногда пишет "Ваше приложение не соответствует требованиям Google play к целевому уровню API"

[A:](https://t.me/flutterflow_rus/12427/57787)
Требование Google Play: target API 35
- В FlutterFlow:
  - Project Settings → Platforms → Android → Target SDK = 35.
  - Обновите проект до последней стабильной версии Flutter.
- Пересоберите именно Android AAB (Build → Android → AAB). Убедитесь, что versionCode увеличен.
- Проверьте AAB перед загрузкой:
  - bundletool dump manifest --bundle app.aab → убедитесь, что targetSdkVersion=35.
- Загрузите новый AAB в Play Console (хватит Internal testing/Closed testing). Ошибка исчезнет только после загрузки нового бандла.
- Если всё ещё ругается:
  - Убедитесь, что нет дополнительных модулей/динамических фич с target < 35. 🤷

[Также](https://t.me/flutterflow_rus/12427/57789),
Проверь все версии которые сейчас есть. У тебя могут версии со старым апи быть в тестировании. Отключи все ненужные. Оставь только продакшен