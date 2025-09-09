---
dg-publish: true
---
# Подборка
1. Simple search (можно подробно прочитать в документации)
2. когда нужен поиск по одному полю) - API (https://www.youtube.com/watch?v=yExwJg1Kz0s&list=PLsGKm9PeeQyIHA00PFyuh7-VEZHLNl_Jo)
3. Algolia (быстрый и бесплатный поиск (до 1000 позиций)
4. Поиск по всей таблице (https://www.youtube.com/watch?v=gb7aKhDuZ4w)
5. Поиск по примерному описанию/по смыслу. см. технику №3 (https://www.youtube.com/watch?v=-l3iRV1WlEM) )
6. [Поиск в Supabase через API](https://www.youtube.com/watch?v=1n4UGyNDAis) примерно 1ч30мин
7. [SIMPLEST way to make Simple Search in FlutterFlow and Supabase (2025) - YouTube](https://www.youtube.com/watch?v=VZovcmjNGQc) 

[Поиск по всей таблице от Digital Pro, c 22:51 в одно API](https://www.youtube.com/watch?v=gb7aKhDuZ4w)

6. от [Kosmorangers](https://t.me/Kosmorangers). Источник: [Telegram: Contact @flutterflow\_rus](https://t.me/flutterflow_rus/12427/34747)
   Я использую простую кастомную функцию, в которой если в аргументе пусто, то она просто возвращает знак &. Если возвращать null, выйдет ошибка. А символ & не вызывает ошибок. Короче функция примерно так выглядит:

```dart
String? idCommentFiltr(int? id) {

  // если в аргументе id есть число, то вернуть comid=eq.[id]&
  if (id != null) {
    if (id is int) {
      return 'comid=eq.$id&';
    }
  }
  return '&';
```


[FlutterFlow and like filtering using Supabase](https://medium.com/@thomas.mcneill_82427/flutterflow-and-filtering-queries-using-supabase-cfc35936ac3f)
[Короткое видео про SimpleSearch от человека](https://www.loom.com/share/fcbe0ef5c01e488f95b49b52bf9d1700) и [второе](https://www.loom.com/share/c80819672668420495bf3f531fc4a8ae)

# Пример строки API в Supa для поиска и фильтрации по нескольким параметрам
```
https://nvodtxeehqreyjuijsl.supabase.co/rest/v1/productos?&select=*&isAvailable=true&name=[name]&shopIDRef=eq.[shop]&order=myIndex.asc
```

Поиск в нескольких столбцах Supa. Так как стоит OR, то в *любом из них*.
Ищет в таблица Services, во всех трёх столбцах: serviceName, dopName, description 
https://nvodtxeehqnreyjuijsl.supabase.co/rest/v1/services?or=(serviceName.[name],dopName.[name],description.[name])
[name сделать как ниже]
а лучше в photos "supabase"

> [!done] [[Поиск в Supa по одному столбцу|Поиск через API по одному полю с выводом в ListView]]

# Сложный поиск
## Вариант 1
от https://t.me/gotorain
Источник: https://t.me/flutterflow_rus/24030/48975
I. Метод. Поиск по таблице supabase, текст запроса должен быть в той же последовательности, что и в supabase.
Например: нам нужно найти "Красивый зеленый дом, с бассейном". Тогда для запроса подойдет "Красив зелен басс"
![[../../temp/image_supa1.jpg]]

1. Выбираем таблицу поиска
2. Колонку поиска
3. Метод поиска (не чувствителен к регистру)
4. Code Expression
5. Создаем аргумент var1, который берем из TextField
6. И вставляем код (Полностью, с одинарными кавычками:
```
'%${var1.split(' ').map((word) => '%$word%').join()}%'
```

Ну и жмем Check Errors - Confirm


## Вариант 2
от https://t.me/gotorain
Источник: https://t.me/flutterflow_rus/24030/48975
II. Метод. Поиск по таблице supabase, НЕ обязательно в той же последовательности , что и в supabase.
Например: нам нужно найти "Красивый зеленый дом, с бассейном". Тогда для запроса подойдет "басс зелен красив"
![[../../temp/image_supaSearch2.jpg]]
Для этого нужно:
1. два (или более фильтра) - это количество слов разделенных пробелами, В нашем случае до 3х слов с оператором AND. (Скриншот 1).
2. так же используем метод Like (Case-insensitive), и Code-Exprssion для всех трех фильтров, НО код у всех отличается:

**Первый**: 
```
'%${var1.split(' ')[0]}%' 
```
**Второй**: 
```
'%${var1.split(' ').length > 1 ? var1.split(' ')[1] : ''}%'
```
**Третий**: 
```
'%${var1.split(' ').length > 2 ? var1.split(' ')[2] : ''}%'  
```
(Не забываем - одинарные кавычки тоже нужно копировать)

Где var1 - наша переменная, которую отправляем в запрос
и с каждым новым фильтром в code expression нужно изменить два числа в формуле +1

## Прочее
[[SQL_что это такое|Что такое SQL которое используем в запросах]]
 [Arrays In Supabase - YouTube](https://www.youtube.com/watch?v=w_6UKxiDBxc)
 