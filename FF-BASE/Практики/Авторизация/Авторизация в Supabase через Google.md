---
dg-publish: true
---

# Авторизация в Supabase через Google
Инструкция от @brozaurus
## 1. Сначала читаем [офиц.документацию](https://docs.flutterflow.io/integrations/authentication/supabase/google)
Настраиваем все credentials, как написано. Должно работать для WEB. 
Для Android см. [[Авторизация в Supabase через Google#Настройка входа в приложении Android|раздел ниже]]

## 2. Процесс в FF
В FF на кнопке "Войти с Google" создаём действие Supabase authentication - Log In. Все действия **для WEB** после него не работают (нюансы именно этого процесса), поэтому нам надо создать в FF *промежуточную страницу*.
Но для **Android** всё-таки после действия Log In добавляем действие navigate to *MAIN*.

Создаём промежуточную страницу, и в ней на автозагрузке делаем логику
![[image_Аутентификация Supabase.jpg]]
В этой логике проверяем, есть ли в в таблице public.users нашей Supa строка с пользователем или он новый новый.
Если **новый**, то идём по левой ветке и создаём запись в Supa и дальше идём на страницу заполнения профиля *editProfile* (или другую, по желанию).
Если **старый**, то сразу отправляем на Главную страницу *main*. А перед этим сохраняем все данные пользователя в State, это удобно для дальнейшего использования по всему приложению. 

!! В Supa настраиваем переход на *промежуточную страницу* (authentication - URL configuration - Site URL)


**О настройке разрешений** в Google cloud, см. с 11:30: [Supercharge Your Apps With These Advanced Supabase Authentication Techniques - YouTube](https://www.youtube.com/watch?v=XCbSBXzMZzg)
13:00 Настройка Oauth
Создать включи для всех платформ и вставить эти ключи в Supa

## Настройка входа в приложении Android

### Получите SHA-ключи из Google Play Console:
Это нужно, так как после выкладывания в Play Store он подписывает приложении своими ключами (заменяет ваши!)
- Откройте **Google Play Console** и выберите ваше приложение.
- В левом меню перейдите в раздел **"Настройка" (Setup)** → **"Целостность приложения" (App integrity)**.
- Выберите вкладку **"Подписание приложения" (App signing)**.
- На этой странице вам нужны **SHA-1** и **SHA-256** отпечатки из секции **"Сертификат ключа подписи приложения" (App signing key certificate)**. Это **ключевой момент**! Google Play переподписывает ваше приложение своим собственным ключом, и именно его отпечатки нужны Firebase.

### Добавьте эти SHA-ключи в Firebase Console:

- Откройте **Firebase Console** и выберите ваш проект.
- Перейдите в **"Настройки проекта" (Project settings)** (иконка шестеренки рядом с "Project overview").
- На вкладке **"Общие" (General)** прокрутите до раздела **"Ваши приложения" (Your apps)** и выберите ваше Android-приложение (по названию пакета, например, `com.yourcompany.yourapp`).
- В самом низу этого блока, под названием пакета, вы увидите "Отпечатки сертификатов SHA" (SHA certificate fingerprints).
- Нажмите **"Добавить отпечаток" (Add fingerprint)** и вставьте сначала SHA-1, а затем повторите то же самое для SHA-256, которые вы скопировали из Google Play Console.
- **Обязательно сохраните изменения!**

### Обновите конфигурационный файл Firebase 
в FF Настройки - Firebase - Regenerate config files

### Обновите приложение в play market
FF - Настройки - Mobile deployment - Deploy to play store

Через 1 - 3 часа приложение должно обновиться.




## Кастом action для анонимного входа supabase
от [Telegram: View @flutterflow\_rus](https://t.me/flutterflow_rus/24030/54660)
```dart
// Automatic FlutterFlow imports
import '/backend/schema/structs/index.dart';
import '/backend/supabase/supabase.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/custom_code/actions/index.dart'; // Imports other custom actions
import '/flutter_flow/custom_functions.dart'; // Imports custom functions
import 'package:flutter/material.dart';
// Begin custom action code
// DO NOT REMOVE OR MODIFY THE CODE ABOVE!

import 'package:supabase_flutter/supabase_flutter.dart';

/// Custom action: Кастом action для анонимного входа supabase

Future<bool> signInAnonymously() async {
  // Получаем клиент Supabase
  final supabase = Supabase.instance.client;

  try {
    // Выполняем анонимный вход
    final AuthResponse res = await supabase.auth.signInAnonymously();

    // Если сессия есть — вход успешен
    return res.session != null;
  } on AuthException catch (e) {
    // Ошибки аутентификации Supabase
    print('Auth exception: ${e.message}');
    return false;
  } catch (error) {
    // Любые другие ошибки
    print('Unexpected error: $error');
    return false;
  }
}
```