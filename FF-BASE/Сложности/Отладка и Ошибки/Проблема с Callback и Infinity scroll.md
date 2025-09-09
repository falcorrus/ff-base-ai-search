---
dg-publish: true
tags:
  - telegram
origin: telegram
author: Dmitriy K
---
Q:
А кто-нибудь сталкивался с таким багом, когда ставишь инфинит скролл на Апи-вызов, но есть разные компоненты-фильтры для этого апи, которые при изменениях запускают экшн Execute callback с рефрешем Апи-реквеста, но после этого зацикливаются Апи-вызовы и начинают загружать данные до бесконечности (шагая всё дальше и дальше по страницам). Причём ставил после экшена рефреша Апи-реквеста алерт и сам экшен, похоже, не зацикливается.

a (@jrustick):
С infinity scroll вечно какие то проблемы, делал аналог используя библиотеку visibility_detector (как кастомный виджет с вызываемым action при видимости ) ставил ее за 2-3 элемента до конца загруженных элементов и получилось сделать бесшовный infinity scroll, тут описал работу библеотки на примере с изображениями (https://t.me/flutterflow_rus/24030/45808)

A: [Telegram: Contact @kirilkindn](https://t.me/kirilkindn)
Да, у меня было. 
Вот мой пост. 
https://community.flutterflow.io/ask-the-community/post/why-does-infinite-scroll-call-api-regardless-of-user-scroll-GhRTR4aFBllgjdx
В нем же есть решение, там есть скриншот