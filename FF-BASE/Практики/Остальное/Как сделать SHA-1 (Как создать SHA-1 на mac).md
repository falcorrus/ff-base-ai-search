## Сделать SHA-1 (Как создать SHA-1 на mac)
[Если Google auth работает везде, кроме андроида](https://community.flutterflow.io/authentication/post/google-sign-in-not-working-on-android-but-is-working-on-web-and-ios-Rl77YRP9AApWDT2)
[Док офиц](https://developers.google.com/android/guides/client-auth)

### вар1
В терминал: keytool -printcert -jarfile *app.apk*
	запускать из папки приложения
	*app.apk* поменять на имя своего приложения
### путь 2
Хотел бы уточнить, а как сгенерировать SHA-1 ? 🤔 С того что я нашёл нужно в коммандную строку вписать  keytool -exportcert -list -v -alias `<your-key-name>` -keystore `<path-to-production-keystore>`
pass: android.  
🥲Но здесь есть появляется несколько вопросов где взять этот ключ и что за  path-to-production-keystore.                                  
Кто то с этим уже сталкивался, нашли решение этой задачи ?

обычно достаточно ключей в гугл сторе, которые генерятся сами + фб ключи
но если не заводится гугл вход, то вот команда для мака, для винды, думаю, можно поискать самостоятельно

keytool -list -v -keystore ~/.android/debug.keystore -alias androiddebugkey -storepass android -keypass android

https://stackoverflow.com/questions/30070264/get-sha1-fingerprint-certificate-in-android-studio-for-google-maps

Большое спасибо, проблема решена !💋  

1. Как и что делать показано вот здесь, https://www.youtube.com/watch?v=fqtom3ove_U , но нужно иметь Visual Studio

2. Потом у меня появлялась ошибка в терминале: keytool : Имя "keytool" не распознано как имя командлета, функции, файла сценария или выполняемой программы. Проверьте правильность написания имени, а также наличие и правильность пути, после чего повторите попытку.

3. Решение нашлось вот здесь, нужно было скачать Java отсюда https://www.java.com/en/download/  и добавить в переменные среды, путь к Java/bin, а как это сделать показано здесь https://www.youtube.com/watch?v=zzfHPGyjoWw 

и Вуаля! ключ Sha1 у меня =)🔥

### Путь 3
[https://developers.google.com/android/guides/client-auth](https://developers.google.com/android/guides/client-auth)

Найти дорогу у keystore:
keytool -list -v \
-alias androiddebugkey -keystore ~/debug.keystore
After **enter key password:** write **android** and press **enter** (you won't see the password while you type in).
keytool -list -v \
-alias androiddebugkey -keystore ~/.android/debug.keystore


[Вариант отсюда](https://www.youtube.com/watch?v=uV9PQcg0qLI):
в терминале: keytool -printcert -jarfile имя файла.apk

Google auth:
Вставить в Firestore: ff-debug-service-free-ygxkweukma-uc.a.run-app


## Вариант 4
Дата:  2025-04-18
**Forwarded from [Евгений Шевцов](https://t.me/Evgeny_Shevtsov_Blag)**

keytool -printcert -jarfile Monter-release.apk - ввести команду в папке с файлом apk

Roman Levchenkov, [01.06.2024 4:58]
Привет! Если кому интересно делюсь своим опытом.  Проект на FF. Авторизация Google. SHA1 ключ сгенерирован и прописан согласно докам. Версии Web и тест авторизация работает отлично отлично как на симуляторе/ реальном устройстве так и при публикации Web. Формируем APK, заливаем на реальное. Авторизация Google перестает работать.

Roman Levchenkov, [01.06.2024 4:59]
Оказалось FF при генерации APK использует Codemagic который подписывает APK своим сертификатом который нигде в FF не виден. В доках FF об этом ничего нет.

появятся подписи их вставить в firebase

Roman Levchenkov, [01.06.2024 5:01]
В итоге решение: В терминале в папке с APK вводим команду keytool -printcert -jarfile [copy apk file location here]

Roman Levchenkov, [01.06.2024 5:02]
Она выводит нам SHA1 и SHA256  которыми подписал Codemagic этот APK

Roman Levchenkov, [01.06.2024 5:03]
Их прописываем по инструкции в Firebase и все работает. При следующих генерациях APK ключи эти вроде не меняются

Roman Levchenkov, [01.06.2024 5:05]
Надеюсь сэкономит кому то время. Вот ссылка на обсуждение этой темы https://community.flutterflow.io/authentication/post/google-sign-in-not-working-on-android-but-is-working-on-web-and-ios-Rl77YRP9AApWDT2 
**вот нашел у себя в базе инструкцию**

## вариант 5
в терминал: 
```
keytool -list -v -keystore ~/.android/debug.keystore -alias androiddebugkey -storepass android -keypass android
```