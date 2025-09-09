
от  @nitemin
[Telegram: View @flutterflow\_rus](https://t.me/flutterflow_rus/12427/58709) 

```dart
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

Future<DateTime?> showCustomCupertinoDatePicker(BuildContext context) async {
  DateTime? selectedDate;

  // Принудительная локализация на русский
  await showModalBottomSheet(
    context: context,
    builder: (BuildContext context) {
      return Localizations.override(
        context: context,
        locale: const Locale('ru', 'RU'), // Русская локализация
        child: Container(
          height: 250,
          child: CupertinoDatePicker(
            mode: CupertinoDatePickerMode.dateAndTime,
            use24hFormat: true, // 24-часовой формат без AM/PM
            initialDateTime: DateTime.now(),
            onDateTimeChanged: (DateTime newDate) {
              selectedDate = newDate;
            },
          ),
        ),
      );
    },
  );

  return selectedDate;
}
```

## Формат показа
Можно и только дату - CupertinoDatePickerMode.date ставим 
значения которые можем задавать по документации:
time
date
dateAndTime
monthYear

---
