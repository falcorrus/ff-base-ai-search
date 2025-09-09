---
dg-publish: true
---

@iischenko нашёл решение как легко поменять цвет status bar в WEB приложении (PWA)
Скриншот - https://i.imgur.com/JaIopTC.png
[How to Change the Status Bar Color in a FlutterFlow App: A Step-by-Step Guide](https://community.flutterflow.io/community-tutorials/post/how-to-change-the-status-bar-color-in-a-flutterflow-app-a-step-by-step-YiSsfOvUB4Zehd0)

Был такой вопрос уже.
Я его себе в свою "базу знаний" записал.
Question:
Привет! А кто знает как можно цвет вот тут изменить?  Серая дефолтная шапка портит весь вид (см. приложенный скриншот).

Answer:
Создайте такой Custom action (см. код ниже) и закиньте его на запуск в main.dart (to Initial Actions).
import 'package:flutter/services.dart';
import 'package:flutter/material.dart';

Future<void> setTransparentStatusBar() async {
  SystemChrome.setSystemUIOverlayStyle(
    SystemUiOverlayStyle(
      statusBarColor: Colors.transparent, // Установка прозрачного фона
      statusBarIconBrightness: Brightness.dark, // Настройка цвета иконок (светлые или темные)
    ),
  ); 
}
📌 Note -
It will not work in test mode. So, test it on a real device or emulator.

Ссылка на видео на Youtube: https://www.youtube.com/watch?v=IHBIdadbIT0