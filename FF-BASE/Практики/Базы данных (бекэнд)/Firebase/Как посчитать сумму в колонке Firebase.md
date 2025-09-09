---
title: Firebase суммирование
source: https://community.flutterflow.io/c/community-custom-widgets/post/firebase-aggregation-query-alternative-using-custom-code-CGkIfbGS3JX4hoZ
author:
  - "[[Sachin Saini]]"
published: 2024-01-14
created: 2024-12-19
description: "Hello, FlutterFlow community! 👋 Are you looking to perform Firebase Aggregation Queries in FlutterFlow and wondering about alternatives? Well, you're in the right place! 🚀 Problem: As of now, FlutterFlow..."
dg-publish: true
---
## Ещё 
[Суммировать значения в списке в AppState (action)](https://rapidmvp.co/how-to-sum-values-of-flutterflow-variables/)
[Суммировать значения в списке в AppState (видео)](https://www.youtube.com/watch?v=VYC5vwnIpzQ)


## Основное
**Проблема:**
На данный момент FlutterFlow не предоставляет прямой возможности выполнять запросы агрегации (суммирования) Firebase. Но не переживайте – если есть желание, всегда найдется способ!

  
**Решение:**
Я нашел удобный обходной путь, используя Data Query и пользовательский код. В этом посте я покажу вам пошагово, как реализовать запросы агрегации Firebase в FlutterFlow.

_Вы также можете следовать этому_ [видео-уроку на YouTube](https://www.youtube.com/@NoCodeFluttter).

*You can also follow the* [Youtube Tutorial](https://www.youtube.com/@NoCodeFluttter)

## Steps to Follow:

**Шаги, которые нужно выполнить:**
**Шаг 1: Создайте пользовательскую функцию:** sumFirebaseQuery
**Шаг 2: Определите аргументы:** **_(Список double)_** amountRef
**Шаг 3: Возвращаемое значение:** **_Double_**
**Шаг 4: Скопируйте и вставьте следующий код в редактор кода:****

```dart
import 'dart:convert';
import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';
import 'package:timeago/timeago.dart' as timeago;
import '/flutter_flow/lat_lng.dart';
import '/flutter_flow/place.dart';
import '/flutter_flow/uploaded_file.dart';
import '/flutter_flow/custom_functions.dart';
import '/backend/backend.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '/auth/firebase_auth/auth_util.dart';

double sumFirebaseQuery(List<double> amountRef) {
  double sum = 0.0;
  for (double amount in amountRef) {
    sum += amount;
  }
  return sum;
}
```

![](https://tribe-s3-production.imgix.net/539inLvruR6NwMOv27WMA?auto=compress,format&dl)

> **Step 5: Create a Page State (Double):**
> 
> ![](https://tribe-s3-production.imgix.net/zEYNkHk84oyBMuGmnfXp9?auto=compress,format&dl)

> **Step 6: On Page load Create two Actions:**
> 
> **a) Query the Collection: (Make sure to use the filters)**
> 
> ![](https://tribe-s3-production.imgix.net/FvoBI0OZRKAGhPhu7HiIT?auto=compress,format&dl)

> Make Sure to Name the Action Output
> 
> ![](https://tribe-s3-production.imgix.net/SH77miFc6EfooqO8raHY7?auto=compress,format&dl)
> 
> b) Update Page State: Set Value
> 
> Now, Get the value from the Custom Function

![](https://tribe-s3-production.imgix.net/TwuM1d4HzM47UPeFsXrYm?auto=compress,format&dl)

## Quick Steps:  

1. Get the Values from the Action Variable
2. Map List Item
3. Under Map List item Select the Field which you wan to Sum.

> **Step 7: Display the Data from Page State in the Text Widget**

![](https://tribe-s3-production.imgix.net/it9VANgzj7toSXfZoRa6E?auto=compress,format&dl)

That's All!

If you need any help in Integration you can Get help via [1:1 Session](http://bit.ly/Avaraniya)

## Функция для вычисления общей суммы всех чисел из списка
от [Sabikrus](https://t.me/flutterflow_rus/24030/54961)
На вход List Double.
На выходе Double
```dart
double totalsumm(List<double>? list) {
  /// MODIFY CODE ONLY BELOW THIS LINE

  if (list == null || list.isEmpty) {
    return 0.00;
  }
  return list.fold(0.00, (sum, num) => sum + num);

  /// MODIFY CODE ONLY ABOVE THIS LINE
}

```
