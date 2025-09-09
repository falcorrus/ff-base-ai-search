---
dg-publish: false
tags:
  - telegram
origin: telegram
author: Сергей
---
## Фильтрация по значению
Дата:  2025-03-16
**Forwarded from [Сергей](https://t.me/ssmorodin)**

Вот код чтения из Supabase (по api) таблицы *classes* с фильтрацией по значению поля *tenantid* с выдачей результата в виде DataType Classes (поля соответствуют полям в базе данных), в конце дополнительная функция *parseDateTime* для преобразования формата времени :
## Код
```dart
import 'package:http/http.dart' as http;
import 'dart:convert';
Future<List<ClassesStruct>> readRowsClasses(String? tenantid,) async {
  final baseUrl = FFAppState().baseUrl;
  final headers = Map<String, String>.from(json.decode(FFAppState().headers));
  final url = tenantid != null && tenantid.isNotEmpty ? '$baseUrl/classes?tenantid=eq.$tenantid' : '$baseUrl/classes';
  try {
    final response = await http.get(Uri.parse(url), headers: headers);
    if (response.statusCode == 200) {
      final data = json.decode(response.body) as List;
      return data
          .map((item) => ClassesStruct(
                id: item['id'] as int?,
                createdAt: _parseDateTime(item['created_at'] as String?),
                tenantid: item['tenantid'] as String?,
                trainerId: item['trainer_id'] as int?,
                name: item['name'] as String?,
                time: _parseDateTime(item['time'] as String?),
                capaciti: item['capaciti'] as int?,
              ))
          .toList();
    } else {
      throw Exception('Failed to load data: ${response.statusCode}');
    }
  } catch (e) {throw Exception('Failed to load data: $e');}
}
DateTime? _parseDateTime(String? dateString) => dateString != null ? DateTime.tryParse(dateString) : null;
```

Чтобы вывести в интерфейс сохраняем выходные данные в State и делаем по ним Generating Children from Variable


## Еще
**Рекомендация:**
Хорошей практикой является, при создании таблиц и колонок в PostgreSQL (включая Supabase) использовать только **строчные буквы и подчеркивания** (snake_case), например: `service_name`, `categoria_num_ref`, `is_verified`. В этом случае вам никогда не понадобятся двойные кавычки, и имена будут обрабатываться без учета регистра по умолчанию.


## Общий формат запроса в Supa (по API)
curl --get 'https://gkeanrtwzbzfsecpkmhw.supabase.co/rest/v1/users' \

-H "apikey: SUPABASE_CLIENT_ANON_KEY" \
-H "Authorization: Bearer SUPABASE_CLIENT_ANON_KEY" \
-H "Range: 0-9" \
-d "select=*" \

Т.е. в Header запроса пишем:
	apikey:   `ваш key` ( он же anon public)
	Authorization: Bearer `ваш anon-key`