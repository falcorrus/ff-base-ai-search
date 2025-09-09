от [@brozaurus](https://t.me/brozaurus)

# Дано
Есть таблица в Supabase (например, с товарами). 
Таблица называется **productos**.
# Надо
- вытащить данные из таблицы productos
- отфильтровать, чтобы столбец shopIDRef был равен параметру shopid
- сохранить результат на компьютер пользователя в .csv
# Решение

## 1. Создаём Custom action "exportProductosToCsv"
```dart
// Automatic FlutterFlow imports
import '/backend/backend.dart';
import '/backend/schema/structs/index.dart';
import '/backend/schema/enums/enums.dart';
import '/backend/supabase/supabase.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/custom_code/actions/index.dart'; // Imports other custom actions
import '/flutter_flow/custom_functions.dart'; // Imports custom functions
import 'package:flutter/material.dart';
// Begin custom action code
// DO NOT REMOVE OR MODIFY THE CODE ABOVE!

import '/custom_code/actions/index.dart';
import '/flutter_flow/custom_functions.dart';

import 'dart:convert';
import 'dart:typed_data';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:file_saver/file_saver.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:csv/csv.dart';

Future<void> exportProductosToCsv(int shopid) async {
  try {
    final supabase = Supabase.instance.client;
    final response =
        await supabase.from('productos').select('*').eq('shopIDRef', shopid);

    final data = List<Map<String, dynamic>>.from(response);

    if (data.isEmpty) {
      print('No data found for export');
      return;
    }

    // Заголовки и строки
    final headers = data.first.keys.toList();
    final rows = <List<dynamic>>[
      headers,
      ...data.map(
          (item) => headers.map((key) => item[key]?.toString() ?? '').toList()),
    ];

    final csv = const ListToCsvConverter().convert(rows);

    await FileSaver.instance.saveFile(
      name: 'productos.csv',
      bytes: Uint8List.fromList(utf8.encode(csv)),
      mimeType: MimeType.csv,
    );

    print('CSV export completed successfully');
  } catch (e) {
    print('Error during export: $e');
  }
}
// Set your action name, define your arguments and return parameter,
// and then add the boilerplate code using the green button on the right!
```

### Settings как здесь![[../../temp/image_Как сохранить таблицу в csv_settings.jpg]]

## 2. Вызываем action из интерфейса
Вешаем на любую кнопку custom action "exportProductosToCsv". 
При нажатии будет вызываться окно сохранения файла csv.

> [!INFO] Работает только в WEB, т.к. было лень настраивать права для моб.

-=-=-
