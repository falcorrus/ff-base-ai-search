
> [!tip] Недописано! 

от @Brozaurus
В отличие от других подходов, здесь сортировка делается в DataType, что позволяет красиво/быстро обновлять список

```dart
// Automatic FlutterFlow imports
import '/backend/backend.dart';
import '/backend/schema/structs/index.dart';
import '/backend/schema/enums/enums.dart';
import '/backend/supabase/supabase.dart';
import '/actions/actions.dart' as action_blocks;
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/custom_code/actions/index.dart'; // Imports other custom actions
import '/flutter_flow/custom_functions.dart'; // Imports custom functions
import 'package:flutter/material.dart';
// Begin custom action code
// DO NOT REMOVE OR MODIFY THE CODE ABOVE!

import '/backend/schema/structs/productos_struct.dart';

Future<List<ProductosStruct>> onReorderCopy(
  int? oldIndex,
  int? newIndex,
  List<ProductosStruct>? productos,
) async {
  // Проверка на null
  if (oldIndex == null || newIndex == null || productos == null) {
    throw Exception('Invalid parameters');
  }
  // Корректировка newIndex, если oldIndex меньше newIndex
  if (oldIndex < newIndex) {
    newIndex -= 1;
  }
  // Создание копии списка
  List<ProductosStruct> updatedProductos = List.from(productos);
  // Перемещение элемента в копии списка
  final ProductosStruct item = updatedProductos.removeAt(oldIndex);
  updatedProductos.insert(newIndex, item);

  // Обновление индексов в DataType с использованием map
  return updatedProductos
      .asMap()
      .entries
      .map((entry) => ProductosStruct(
            sortIndex: entry.key,
            // Копирование других полей из entry.value
          ))
      .toList();
}

// Set your action name, define your arguments and return parameter,
// and then add the boilerplate code using the green button on the right!
```
