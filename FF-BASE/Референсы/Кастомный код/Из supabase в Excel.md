---
dg-publish: 
tags:
  - telegram
origin: telegram
author: "Вахтанг"
---

Дата:  2025-02-23
**From [Вахтанг](https://t.me/hidden_account_1740339683)**

## Для чего
Код нужен для получения данных из supabase и формирования этих данных в формат для excel. 

В return value ничего не надо указывать, скачивание происходит автоматически. 
Код нужно немного доработать под ваш формат.

## Код
![[../temp/Код-для-загрузки-excel - 20250223.txt]]
```dart
// Automatic FlutterFlow imports
import '/backend/schema/structs/index.dart';
import '/backend/supabase/supabase.dart';
import '/actions/actions.dart' as action_blocks;
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/custom_code/actions/index.dart'; // Imports other custom actions
import '/flutter_flow/custom_functions.dart'; // Imports custom functions
import 'package:flutter/material.dart';
// Begin custom action code
// DO NOT REMOVE OR MODIFY THE CODE ABOVE!

import 'package:excel/excel.dart';
import 'package:universal_html/html.dart' as html;

Future downloadExcelCA(List<TransactionsRow> supabaseData) async {
  try {
    final excel = Excel.createExcel();
    final sheet = excel['Sheet1'];

    // 1. Добавляем заголовки для excel 
    sheet.appendRow([
      'Название 1 столбца',
      'Название 2 столбца',
      'И тд'
    ]);

    // 2. Добавляем данные напрямую через поля класса. Тут нужно указать названия ваших столбцов как в таблице supabase
    for (var row in supabaseData) {
      sheet.appendRow([
        row.id?.toString() ?? '', // ID
        row.data?.toString() ?? '', // Дата 
        row.summa?.toString() ?? '', // Сумма
        row.tip ?? '', // Тип
        row.komissia?.toString() ?? '', // Комиссия
        
        row.komment ?? '' // Комментарий
      ]);
    }

    // 3. Скачивание
    final bytes = excel.encode()!;
    final blob = html.Blob([bytes],
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
    final url = html.Url.createObjectUrlFromBlob(blob);
    html.AnchorElement(href: url)
      ..download = 'transactions_${DateTime.now().millisecondsSinceEpoch}.xlsx'
      ..click();
    html.Url.revokeObjectUrl(url);
  } catch (e) {
    print('Ошибка: $e');
  }
}
```