---
dg-publish: true
---
Вкратце:
**Conditional Builder** показывает определённый виджет в зависимости от условий
**conditional visibility** виджета  показывает или прячет именно этот виджет виджет

## Q: как работает conditionals и conditional visibility?

A: (решение от @ArtemPlayback): 
https://telegra.ph/conditional-visibility-05-17
Q: как пользоваться conditionals и conditional visibility?
A: (от [@ArtemPlayback](https://t.me/artemplayback)): Что conditionals, что conditional visibility принимают на вход какое-то логическое значение (значение которое может быть либо true (верное), либо false (неверное). Значит вы можете либо использовать single condition (пример: textfield == 100, если действительно равен 100, то он вернет true, иначе false), combine conditions (тоже самое, но можно использовать либо and, либо or), либо использовать переменную типа boolean. 

Дальше везде логика одинаковая: 

1. Conditional visibility в дизайне: если на входе значение true, то виджет будет виден, если false, то нет.

2. В conditional action: если true, то одна цепочка действий, если false, то другая. 

3. В if then else та же логика: Если ваше условие или логическое значение == true, то сработает действие (настройка или еще что-то), которое укажете в then, а если == false, то другое, которое укажете.

Вроде все


## Еще:
[Conditional Builder vs Visibility | Best Practices](https://www.youtube.com/watch?v=REuYX-hqqiw&pp=ygUiY29uZGl0aW9uYWwgdmlzaWJpbGl0eSBmbHV0dGVyZmxvdw%3D%3D "Conditional Builder vs Visibility | Best Practices")
[Применительно к Choice chips](https://www.youtube.com/watch?v=nuKkxaW-fmY)


