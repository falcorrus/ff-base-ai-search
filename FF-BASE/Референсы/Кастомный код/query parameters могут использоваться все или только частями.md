---
dg-publish: 
tags:
  - telegram
origin: telegram
author: "Broz"
---

Дата:  2025-01-25
**Forwarded from [Dmitriy K](https://t.me/kirilkindn)**
Источник: [Telegram: Contact @flutterflow\_rus](https://t.me/flutterflow_rus/12435/46635)

Q: как использовать API, в котором query parameters могут использоваться все, а могут только частями.

A: например есть 3 параметра 
- colour, 
- usage, 
- type.
Например, нужно использовать только 2 параметра из 3. 
URL будет примерно такой:
/resources?type=jacket&usage=casual (colour нет).  

1. Создаём API call URL.com/resources?[typeParam][usageParam][colourParam]

2. Создаём 3 переменных типа srting typeParam, usageParam, colourParam

3. В UI с помощью conditional and text combine передаем параметры: 
А) если параметр не используется, то передаем только символ &
Б) если используется, то в переменную вставляем text combine:
- название параметра, например colour= (обязательно знак равно)
- значение из какой-то переменной (например, widget state -> choice chips)
- & (на конце обязательно! Не забыть!)