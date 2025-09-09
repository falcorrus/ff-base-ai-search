---
title: "Установка и настройка Flutter в Android Studio — Code Lab"
source: "https://codelab.pro/ustanovka-i-nastrojka-flutter-v-android-studio/"
author:
published:
created: 2025-01-22
description:
tags:
  - "статьи"
---
Flutter — это платформа для разработки мобильных приложений с открытым исходным кодом, созданная Google. Flutter завоевал огромную популярность среди разработчиков благодаря своей способности создавать кроссплатформенные мобильные приложения с единым кодом. Он быстр, прост в использовании и имеет большое сообщество разработчиков, которые вносят свой вклад в его разработку.

Если вы разработчик на Android и хотите начать работу с Flutter, вы можете использовать Android Studio для разработки приложений Flutter. В этой статье мы проведем вас через процесс настройки Flutter в Android Studio с нуля.

- [Установка Flutter в Android Studio](https://codelab.pro/ustanovka-i-nastrojka-flutter-v-android-studio/#%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0_Flutter_%D0%B2_Android_Studio "Установка Flutter в Android Studio")
- [Скачиваем Android Studio](https://codelab.pro/ustanovka-i-nastrojka-flutter-v-android-studio/#%D0%A1%D0%BA%D0%B0%D1%87%D0%B8%D0%B2%D0%B0%D0%B5%D0%BC_Android_Studio "Скачиваем Android Studio")
- [Устанавливаем Flutter SDK](https://codelab.pro/ustanovka-i-nastrojka-flutter-v-android-studio/#%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%B0%D0%B2%D0%BB%D0%B8%D0%B2%D0%B0%D0%B5%D0%BC_Flutter_SDK "Устанавливаем Flutter SDK")
- [Скачайте Flutter SDK](https://codelab.pro/ustanovka-i-nastrojka-flutter-v-android-studio/#%D0%A1%D0%BA%D0%B0%D1%87%D0%B0%D0%B9%D1%82%D0%B5_Flutter_SDK "Скачайте Flutter SDK")
- [Извлеките Flutter SDK](https://codelab.pro/ustanovka-i-nastrojka-flutter-v-android-studio/#%D0%98%D0%B7%D0%B2%D0%BB%D0%B5%D0%BA%D0%B8%D1%82%D0%B5_Flutter_SDK "Извлеките Flutter SDK")
- [Устанавливаем плагины Flutter и Dart](https://codelab.pro/ustanovka-i-nastrojka-flutter-v-android-studio/#%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%B0%D0%B2%D0%BB%D0%B8%D0%B2%D0%B0%D0%B5%D0%BC_%D0%BF%D0%BB%D0%B0%D0%B3%D0%B8%D0%BD%D1%8B_Flutter_%D0%B8_Dart "Устанавливаем плагины Flutter и Dart")
- [Настраиваем путь к Flutter SDK](https://codelab.pro/ustanovka-i-nastrojka-flutter-v-android-studio/#%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%B0%D0%B8%D0%B2%D0%B0%D0%B5%D0%BC_%D0%BF%D1%83%D1%82%D1%8C_%D0%BA_Flutter_SDK "Настраиваем путь к Flutter SDK")
- [Создаем новый проект Flutter](https://codelab.pro/ustanovka-i-nastrojka-flutter-v-android-studio/#%D0%A1%D0%BE%D0%B7%D0%B4%D0%B0%D0%B5%D0%BC_%D0%BD%D0%BE%D0%B2%D1%8B%D0%B9_%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82_Flutter "Создаем новый проект Flutter")
- [Запустите проект Flutter](https://codelab.pro/ustanovka-i-nastrojka-flutter-v-android-studio/#%D0%97%D0%B0%D0%BF%D1%83%D1%81%D1%82%D0%B8%D1%82%D0%B5_%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82_Flutter "Запустите проект Flutter")
- [Заключение](https://codelab.pro/ustanovka-i-nastrojka-flutter-v-android-studio/#%D0%97%D0%B0%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D0%B5 "Заключение")

## Скачиваем Android Studio

Первый шаг — это загрузить Android Studio. Вы можете скачать его с официального веб-сайта [Android Studio](https://developer.android.com/studio).

После того как вы скачали Android Studio, установите его в свою систему.

## Устанавливаем Flutter SDK

Установка Flutter SDK — это второй шаг к началу разработки на Flutter.

### Скачайте Flutter SDK

Первый шаг — загрузить Flutter SDK. Вы можете загрузить последнюю стабильную версию Flutter с [официального веб-сайта Flutter](https://docs.flutter.dev/get-started/install/windows).

### Извлеките Flutter SDK

После загрузки Flutter SDK распакуйте его в папку в вашей системе. Например, в Windows вы можете извлечь его в папку *C:\\frameworks*.

## Устанавливаем плагины Flutter и Dart

После установки Android Studio вам необходимо установить плагины Flutter и Dart. Для этого перейдите в *File -> Settings -> Plugins*.

В окне плагинов перейдите на вкладку *Marketplace* и найдите «Flutter» и «Dart». Нажмите на кнопку *Install*, чтобы установить оба плагина.

![](https://codelab.pro/wp-content/uploads/2023/03/4tnuqcs9.png)

После установке плагинов перезагрузите Android Studio

## Настраиваем путь к Flutter SDK

После того как вы установили плагины Flutter и Dart, вам необходимо настроить путь к Flutter SDK. Чтобы сделать это, перейдите в File -> Settings -> Языки и фреймворки -> Flutter. В поле путь к Flutter SDK нажмите на кнопку «…» и выберите каталог, в который вы установили Flutter SDK. Нажмите на *Ok*, чтобы сохранить изменения.

![](https://codelab.pro/wp-content/uploads/2023/03/d03unaoy.png)

## Создаем новый проект Flutter

Теперь, когда вы настроили Flutter в Android Studio, вы можете создать новый проект Flutter. Чтобы сделать это, перейдите в File -> New -> New Flutter Project.

![](https://codelab.pro/wp-content/uploads/2023/03/ibbcghwr.png)

В новом окне проекта Flutter выберите вкладку *Flutter* и нажмите *Next*. В следующем окне введите название проекта, местоположение проекта и другие сведения о проекте. Нажмите на кнопку *Finish*, чтобы создать проект.

## Запустите проект Flutter

После создания проекта Flutter вы можете запустить его на эмуляторе или физическом устройстве. Чтобы запустить проект, перейдите в меню Выполнить -> Запустить ‘main.dart’. Android Studio скомпилирует проект и запустит его на выбранном устройстве.

## Заключение

Настройка Flutter в Android Studio — это простой и понятный процесс. Следуя инструкциям, описанным в этой статье, вы можете быстро настроить Flutter в Android Studio и приступить к разработке кроссплатформенных мобильных приложений. Flutter — это мощный фреймворк, который может помочь вам с легкостью создавать высококачественные мобильные приложения.