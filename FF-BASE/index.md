---
dg-publish: true
dg-home: true
tags:
---

Здесь **база знаний** от чата телеграма  [@Flutterflow_rus](https://t.me/flutterflow_rus) 

[[Общая информация о Базе знаний]]
[Официальная документация](https://docs.flutterflow.io/)

```dataview
TABLE WITHOUT ID file.link AS "Заметки",
dateformat(file.mtime, "dd.MM.yyyy") AS "Последнее посещение"
FROM -"temp" // НЕ включать папку "temp"
WHERE file.name != "index" // И по-прежнему исключать файл "index"
SORT file.mtime DESC
LIMIT 7
```

