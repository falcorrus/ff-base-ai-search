
# Как исправить ошибку NULL
[How to fix null errors in Flutterflow](https://www.youtube.com/watch?v=x47oMgD4cvo)


## Null при API или результат API не хочет сохраняться в DataType
от @brozaurus
Бывают ситуации, когда мы забираем данные по API и сохраняем в DataType, прилетает NULL.
![[../temp/image_null.jpg]]

> [!NOTE] В основном проблемы бывают с картинками и датами.

В **настройках JSON path** результатов api выбираем:
1. Даты сохраняем на String
2. Картинки как String или Image Path

В **настройках DataType** выбираем:
1. Даты сохраняем как String
2. Картинки как Image path
С датами будет проблема, если в Supa вы сохраняете их не в DateTime, а как Date. Date воспринимается API как String. Если String ok, то нормально. А если вы планируете использовать в FF как дату, то нужна конвертация с Custom Action.

Все это можно сохранить в State. Ему присваиваем наш DataType.
[How to use custom data types with supabase?](https://community.flutterflow.io/ask-the-community/post/how-to-use-custom-data-types-with-supabase-zRfInAjSK7nyXvO)
## Полезно
[Power of JSON and Supabase and Datatype - Full Walkthrough - YouTube](https://www.youtube.com/live/0StIoln3gVU)
Сохраняем jsonb в ячейку supabase
## Ещё 
[DataType](../Flutterflow/DataType.md)