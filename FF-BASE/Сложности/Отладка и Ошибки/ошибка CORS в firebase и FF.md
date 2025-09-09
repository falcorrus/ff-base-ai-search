Варианты:
1. https://docs.flutterflow.io/actions/actions/utilities/upload-data#web-access-for-pdfs-and-other-files

2. [Почему не прогружаются изображения из FB? Ни в тест мод, ни в ран мод. Даже в веб версии не грузятся. А вот если APK собрать то все работает. Почему так происходит?](https://chatgpt.com/share/67c06b82-5910-8011-8b9b-2b7c4430b76a)

3. Можно почитать про официальные решения

4. Для ошибки "https request. Status code: 0": [Resolving CORS for stored files](https://www.youtube.com/watch?v=txeFCNKqyzk)
5. [Fix CORS issue in 2 mins! FlutterFlow x Firebase Storage](https://www.youtube.com/watch?v=uZRIzAHpLDQ)
6. Решение проблемы лета 2025 https://t.me/flutterflow/28858
7.  

## Пользователь авторизуется, но не сохраняется в Firebase

Док: [Connect to Firebase \| FlutterFlow Documentation](https://docs.flutterflow.io/integrations/firebase/connect-to-firebase/#enable-firestore-for-database-access)
Надо добавить две роли для firebase@flutterflow.io
- *Service Account User*
- *Cloud Functions Admin*

