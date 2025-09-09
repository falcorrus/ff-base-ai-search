---
dg-publish: true
---
[17. API Development | Part 1 | FlutterFlow University Expert Training - YouTube](https://www.youtube.com/watch?v=4XDappFZeqk)
[Безопасная передача ключей api](https://docs.flutterflow.io/securing-your-api-keys-in-private-api-calls)

# Вопросы и ответы
## как использовать API, в котором query parameters могут использоваться все, а могут только частями.
Q: как использовать API, в котором query parameters могут использоваться все, а могут только частями.

A (от @kirilkindn): например есть 3 параметра 
- colour, 
- usage, 
- type.
Например, нужно выводить только 2 параметра из 3. 
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


## API Interseptors
[FlutterFlow's MOST INNOVATIVE Features of 2024 - Feature 6](https://www.youtube.com/watch?v=aLg-sQ83Cqg)

## Возможные проблемы
### В Test все ок, но результат не выводится
A: Убедитесь, что запрос возвращает *List*, даже если вы фильтруете так, что точно возвращается 1 (одно) значение. Например, если возвращаете в DataType, то поставьте у него галочку *List*.
Будете получать *List*, но не страшно, берите из него по индексу *First* значение.