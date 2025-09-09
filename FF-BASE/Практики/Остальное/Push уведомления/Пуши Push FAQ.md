---
dg-publish: true
---
## OneSignal, Push для Supabase
https://community.flutterflow.io/discussions/post/onesignal-integration-for-notifications---notifications-for-supabase-yd2c5sa4jzoQr1W

[OneSignal integration for notifications - Notifications for Supabase](https://community.flutterflow.io/discussions/post/onesignal-integration-for-notifications---notifications-for-supabase-yd2c5sa4jzoQr1W)
[Realtime обновление базы](https://www.youtube.com/watch?v=3wvXtIgWUF4&t=391s)
[Пуши в Supa, без FB](https://www.youtube.com/watch?v=jfkE4_frL_c)
[[Push notifications c Supabase и авторизацией через Firebase|Push notifications на Supabase и авторизации через Firebase Auth]]

## Подборка видео
1. Сделать чат и push (https://www.youtube.com/watch?v=jfkE4_frL_c)
2. push через onesignal (https://www.youtube.com/watch?v=DJaFai5hJn8&t=23s)
3. push с supabase auth (https://medium.com/@a.ayremlou/flutterflow-push-notifications-without-firebase-auth-low-code-e6456605af33)
4. push от Dimitar (https://www.youtube.com/watch?v=YcnKiZpo8ro)
5. push от Ali Ayremlou текстом (https://medium.com/@a.ayremlou/flutterflow-push-notifications-without-firebase-auth-low-code-e6456605af33)
6. Через oneSignal (https://www.youtube.com/watch?v=6QSAMaRT1a0)
7. [пуши по расписанию](https://www.youtube.com/watch?v=cHPC8EH8U-M)
8. [[Оповещение при изменении в Supabase|Оповещение при изменении в Supabase]]

Q: в какой момент и как делать этот запрос на refreshToken внутри flutterflow
A (от @anton_k8):
Нужно создать interception и в нем проверять актуальность accessToken, если не актуален то запрашивать новый с помощью refresh

> Когда вы заводите идентификатор на про картинки в apple, *будьте внимательны, когда пишите bindleID*. 
>там в конце через точку надо писать ImageNotification и мой косяк был, что я букву I написал маленьку. Если что обращайте на это внимания, дабы экономить время))
 мало ли кому важно будет).