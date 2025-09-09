---
dg-publish: true
author: "@sabikrus"
---
от @sabikrus
функция возврат ссылки на изображение из path (он не является сслыкой!, многие путают и передают его как ссылка, но это неверно. Если нужна ссылка то вот вам функция.
можно вернуть ссылку из трех видов изображение, видео и аудио.> [!example]

> [!INFO] можно вернуть ссылку из трех видов: изображение, видео и аудио.

```dart
import 'dart:convert'; import 'dart:math' as math;`
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
import '/backend/schema/structs/index.dart';

String imageUrl(
String? imagePath,
String? videoPath,
String? audioPath,
) {
/// MODIFY CODE ONLY BELOW THIS LINE

// Проверяем, какой из аргументов не равен null
final path = imagePath ?? videoPath ?? audioPath;

// Если все пути равны null, возвращаем пустую строку
if (path == null) {
return '';
}

// Разделяем путь на части
List<String> parts = path.split('/');

// Ищем часть, начинающуюся с http:// или https://
for (int i = parts.length - 1; i >= 0; i--) {
if (parts[i].startsWith('http://') || parts[i].startsWith('https://')) {
return parts[i];
}
}

// Если не найдено, возвращаем оригинальный путь
return path;

/// MODIFY CODE ONLY ABOVE THIS LINE
}
```

