## Вводная часть
На вход надо дать List из значений в формате Int
на выходе получает сумму всех значений, тоже в Int

Если нужна не вся колонка, то регулируем это фильтром на более раннем этапе, когда делаем запрос в БД
## Картинка
![[2025-03-02_sum.jpeg]]
## Код
```
import 'dart:convert';
import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';
import 'package:timeago/timeago.dart' as timeago;
import '/flutter_flow/custom_functions.dart';
import '/flutter_flow/lat_lng.dart';
import '/flutter_flow/place.dart';
import '/flutter_flow/uploaded_file.dart';
import '/backend/backend.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '/backend/schema/structs/index.dart';
import '/backend/schema/enums/enums.dart';
import '/backend/supabase/supabase.dart';
import '/auth/supabase_auth/auth_util.dart';

int? sumOfList(List<int> inputField) {
  /// MODIFY CODE ONLY BELOW THIS LINE

  int sum = 0;
  for (int value in inputField) {
    sum += value;
  }
  return sum;

  /// MODIFY CODE ONLY ABOVE THIS LINE
}
```

> [!INFO] а можно вот так красиво сделать, только:
> return inputField.reduce((a,b)=>a+b);
