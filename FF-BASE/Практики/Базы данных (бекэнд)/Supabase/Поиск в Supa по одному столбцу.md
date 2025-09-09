# Пример строки API в Supa для поиска и фильтрации по одному столбцу, с Code Expression
Источник: [Поиск через API, решена проблема пустого вывода, с 54:00](https://www.youtube.com/watch?v=QikTDU4DDAU)
От: @brozaurus

> [!TIP] Удобен тем, что проверяется и null  и iLike работает (поиск по буквам в середине слова)


## Создаём API. В нем меняем на ваши:
 - название своей `базы` `nvo..` 
 - название таблицы `productos` на имя таблице, где будем искать
```dart
https://nvodtxeehqreyjuijsl.supabase.co/rest/v1/productos?&select=*
```


## Добавляем в variable параметр fullName и его в Query 
![[../../temp/image_SearchAPISupa.jpg]]



## Cоздаём page state `SearchPS` 
## В Actions: 

- в строке поиска, на `on change` назначаем значение для `SearchPS`  из `widget state` ![[../../temp/image_SearchAPISupa2.jpg]]

## На ListView создаём API-запрос
![[../../temp/image_SearchAPISupa3.jpg]]

## В inline-функции пишем:
![[../../temp/image_SearchAPISupa4.jpg]]

В `SearchString`  берём значение из нашего page state `SearchPS` 

```dart
searchString !=null ? "ilike.*$searchString*" : "ilike.**"
```

**ГОТОВО!**