---
dg-publish: true
---
# Специальные техники 

[Выложить на свой домен](https://t.me/flutterflow_chat/24784)
[Выложить на свой домен_вариант с Amazon S3 (смотрим с 1:11:24)](https://www.youtube.com/watch?v=PtOS1sFumLs)
[Селфхостинг на DigitalOcean](https://www.youtube.com/watch?v=dDhy6pk282U)

[Удобное удаление строки с подтверждением, техника1](https://www.youtube.com/watch?v=YnjOl4sYYaY)
[Одновременная работа с текстом, техника2](https://www.youtube.com/watch?v=YnjOl4sYYaY)
[Сохранение версий текста и возврат их, техника3](https://www.youtube.com/watch?v=YnjOl4sYYaY)

## Перевод
[Перевод через Google и API](https://www.youtube.com/watch?v=xCTEdacOxwE)

## Проблемы 
[Не работает скрол -> выключить Primary у ListView](https://t.me/flutterflow_rus/12427/21576)
## Свайпы
[Горизонтальный свайп](https://www.youtube.com/watch?v=WqY8lfmj7Bk)
 




## Приятный кастомный BottomPicker с Dev 
https://www.youtube.com/watch?v=yl2LOhJl964
## Q: Где найти много полезных хаков и кода в одном месте?
A: Мы собрали это в telegra.ph:
https://telegra.ph/Oglavlenie-poleznyh-hakov-FlutterFlow-01-25

Официальный сборник ответов
https://intercom.help/flutterflow/en/



## Фильтрация по чекбоксу
https://www.youtube.com/watch?v=Xw_Axw-GIkE

## Dropdown
[Видео подробное. Как использовать через Custom dialog](https://www.youtube.com/watch?v=7Qc7qLrdYj4)


Q: Как вытащить значение из DropDown для фильтрации дальше
A: Экшеном записывать можно
## Как подключить график
https://community.flutterflow.io/c/community-custom-widgets/fl-chart-integration


## перевести список на другой язык
@antonperviy (https://t.me/antonperviy) а с днями недели можно сделать лист дней в локалстейте, его плодить через чилдренов, по клику на один итем добавлять его в локалстейт «выбранный день», как автоперевод сделать не подскажу, но как костыль можно на кондишнах передавать данные, типо если итем равен понедельник, то запиши в выбранный день monday, если среда - wednesday и тд
## Выделение карточки цветом
https://www.youtube.com/watch?v=vHfStbW-jt8&t=2413s
## Функция посчитать разницу дней (для тестового периода)
https://www.youtube.com/watch?v=jf8i4ZjyYO4

##  Фильтр в фильтре (у Тренера только его занятия)
https://www.youtube.com/watch?v=Me1ryBHQvbY (см.Tip3)
## Как добавить свой элемент после каждого 3го элемента списка
https://www.youtube.com/watch?v=HY7k_KPEl7Q (tip1)
## Возможность выбирать (работать) нужный элемент из списка
https://www.youtube.com/watch?v=HY7k_KPEl7Q (tip2)
## Динамическая навигация на нужную страницу
https://www.youtube.com/watch?v=HY7k_KPEl7Q (tip3)
## Как вытащить значение из Custom widget
Использовать FFAppState().scan, где *scan* это имя AppState

```
setState(() {
this.code = code;
});
// Проверка на null перед обновлением значения
String codeResult = this.code ?? "";
FFAppState().update(() {
FFAppState().scan = codeResult;
});
```

Смотреть: https://www.youtube.com/watch?v=_ik4paDX6VI

### вариант 2
There is a new way to this using this code as January 2023 FFAppState().update(() {setState(() => FFAppState().[LOCAL-STATE-NAME] = data); });


## получаю на входе String True, надо переделать в Bool
https://www.youtube.com/watch?v=HY7k_KPEl7Q (tip4)
сделать expression: var1=="true"?true:false


## Примеры функций с объяснением
https://community.flutterflow.io/c/community-tutorials/10-incredibly-useful-flutterflow-custom-functions-examples
## как кодом вынимать значения из Firebase
https://www.youtube.com/watch?v=JH_tdlJen_k
## Примеры функций с объяснением
https://community.flutterflow.io/c/community-tutorials/10-incredibly-useful-flutterflow-custom-functions-examples

[[Как сделать SHA-1 (Как создать SHA-1 на mac)]]

## Настройки базы FireBase для FlutterFlow
### Текстовая инструкция:
https://docs.flutterflow.io/data-and-backend/firebase/firebase-setup#2.2-enable-access-to-your-project
Cloud functions admin (administrador de cloud functions)
Service account user  (usuario de cuenta de servicio)

### **Видео:**
https://youtu.be/XkHP17QJy20?t=570 JamesNoCode
https://youtu.be/O-qPEkKW1rM?t=88
https://youtu.be/6ibJXbVpUXY?t=3303 Игнат (2 отличные части на рус)

## How to Self host FlutterFlows webapp with Custom domain For Free
https://community.flutterflow.io/community-tutorials/post/how-to-self-host-flutterflows-webapp-with-custom-domain-for-free-w3TIBKoQVb8DB4w
вар2: Q: как задеплоить в web свой проект бесплатно?
A: https://youtu.be/dpoVucT9xng?si=0ySIUoYSbQecm_G2
### Cloud functions
[Отправка email используя SendGrid из приложения (техника4)](https://www.youtube.com/watch?v=AzYHCgJrwmY)

> [!NOTE]
> Дальше почему-то не вставляется

