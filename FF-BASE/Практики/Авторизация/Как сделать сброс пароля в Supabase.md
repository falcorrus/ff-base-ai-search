---
dg-publish: true
---
## Вариант1
[Creating a User-Friendly Password Update Experience - YouTube](https://www.youtube.com/watch?v=uiZl-UliiH4)


## Подробный разбор про сброс пароля в Supabase
[Источник: Master Forgot and Reset Password in FlutterFlow and Supabase (2025) - YouTube](https://www.youtube.com/watch?v=EB5xtsf9pIw)
### Код sendRecoveryEmail (это Custom ACTION!)
Аргумент1 - email
Аргумент2 - redirectTo
Оба String, НЕ null

```dart
// Automatic FlutterFlow imports
import '/backend/supabase/supabase.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/custom_code/actions/index.dart'; // Imports other custom actions
import '/flutter_flow/custom_functions.dart'; // Imports custom functions
import 'package:flutter/material.dart';

// Begin custom action code
// DO NOT REMOVE OR MODIFY THE CODE ABOVE!

import 'package:supabase_flutter/supabase_flutter.dart';

Future<String?> sendRecoveryEmail(
String email,
String? redirectTo,
) async {
// Add your function code here!
// Get a reference your Supabase client
final supabase = SupaFlow.client;

// Try to send password recovery email
try {
await supabase.auth.resetPasswordForEmail(email, redirectTo: redirectTo);
return null;
} catch (e) {
// If failed (i.e. email address not found), return error
return e.toString();
}
}
```
### код updatePassword (это Custom ACTION!)
Аргумент1 - newPassword
Аргумент2 - confirmNewPassword
Оба String, НЕ null
```dart
// Automatic FlutterFlow imports
import '/backend/supabase/supabase.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/custom_code/actions/index.dart'; // Imports other custom actions
import '/flutter_flow/custom_functions.dart'; // Imports custom functions
import 'package:flutter/material.dart';
// Begin custom action code
// DO NOT REMOVE OR MODIFY THE CODE ABOVE!

import 'package:supabase_flutter/supabase_flutter.dart';

Future<String?> updatePassword(
String newPassword,
String confirmNewPassword,
) async {
// Add your function code here!
// Get a reference your Supabase client

final supabase = SupaFlow.client;

// Check if passwords match
if (newPassword != confirmNewPassword) {
return "Passwords do not match!";
}
try {
await supabase.auth.updateUser(UserAttributes(password: newPassword));
// Return null if the user has successfully reset their password
return null;
} catch (e) {
// Return the error as to why reset password failed
return e.toString();
}
}
```

### Пример красивого письма в Supa, который получает пользователь

	в нем поменяйте https://baonline.ru/passreset на url страницы, где у пользователя запрашивается новый пароль.
	поменяйте ttps://nvodtxeehqnreyjuijsl.supabase.co на адрес своей Supa

```html
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Сброс пароля</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
<div style="max-width: 600px; margin: auto; background: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
<h2 style="color: #333333;">Сброс пароля</h2>
<p style="color: #555555;">Вы запросили сброс пароля для вашего аккаунта.</p>
<p style="color: #555555;">Нажмите на кнопку ниже, чтобы задать новый пароль:</p>
<p style="text-align: center; margin: 30px 0;">
<a href="https://nvodtxeehqnreyjuijsl.supabase.co/auth/v1/verify?token={{ .TokenHash }}&type=recovery&redirect_to=https://baonline.ru/passreset"
style="background-color: #2f40fb; color: white; padding: 14px 28px; text-decoration: none; font-size: 16px; border-radius: 6px; display: inline-block;">
Сбросить пароль

</a>
</p>
<p style="color: #999999; font-size: 12px;">
Если вы не запрашивали сброс пароля, просто проигнорируйте это письмо.

</p>
</div>
</body>
</html>
```
## Советы
От https://t.me/skripov_channel
С нормальным бэком сброс пароля и аналогичные действия делаются так:
1. Пользователь говорит что забыл пароль и указывает свой emal или телефон.
2. Находим этого пользователя, если его нет то показываем ошибку. 
3. В отдельной табличке с одноразовыми кодами (сессии сброса пароля) создаем новую запись в неё сохраняем id пользователя и отправленный (на email или телефон) код, возвращаем пользователю с бэка ответ, что код отправили и сообщаем id созданной сессии на сброс пароля.
4. Пользователь вводит полученный код и новый пароль - отправляем их на бэк вместе с id сессии.
5. На бэке берем запись по id из таблички сессий, сравниваем полученный от пользователя код с тем который отправляли. Если все ок, то меняем пользователю указанному в сессии пароль на тот, который он прислал вместе с кодом.
6. Если ок, то сообщаем пользователю об успешной смене пароля и отправляем его на форму входа.

Надеюсь понятно написал 🙂