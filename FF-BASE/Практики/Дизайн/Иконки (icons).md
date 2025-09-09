---
dg-publish: true
---


## Коллекции
[Feather – Simply beautiful open source icons](https://feathericons.com/)


## Вопросы-ответы
#### Q: в каком формате нужны иконки, чтобы можно было их загрузить и потом менять цвет, размер. Где можно найти хороший выбор иконок, не стандартных. И иконки из Figma можно скачать и использовать, я скачал одну в формате svg но выдает ошибку и просит dart файл

A: вот FlutterFlow 5000+ Custom Icon Pack
https://amsarkar.gumroad.com/l/ficon

#### [Бесплатная коллекция из 1900+ 3D-иконок, сгенерированных ai](https://www.thiings.co/)
Также, можно генерировать свои


#### Q: как добавить 12982 красивых FontAwesome иконок в проект?
A: https://legacy-community.flutterflow.io/c/community-tutorials/how-to-add-fontawesome-pro-icon

А вот видео (https://youtu.be/fJ8tCE_767A?si=dm2LesjkC68IX4Pz)
И вот второе (https://youtu.be/zB9JyLSJGRU?si=FQaT0FLQ0hjRPCDb) 

## Проблемы
Q: пытаюсь через icomoon преобразовать иконки в шрифт, но половина иконок не конвертируется. Как справиться с этим?
![[Pasted image 20250107095851.png]]

A: 
[Convert SVG Strokes to Fills](https://iconly.io/tools/svg-convert-stroke-to-fill)

от @jrustick:
Сервис icomoon конвертирует svg в dart шрифт как иконки.
https://rutube.ru/video/c9491c48703f684062e89a8afaf1b019/?r=wd
Только иконка должна быть построена на fill а не stroke, мой совет- скачиваете такие иконки в хорошем png, конвертируете на любом сайте png в svg и повторяете

from [sabikrus](https://t.me/sabikrus)**
на самом деле все просто нужно в илюстраторе в бесплатной версии открыть иконку и сделать outline stroke ( то есть все обводки сделать кривыми). Это очень провсто в ютубе много уроков @IvanK7510 @momo_nut

from @brozaurus
подключайте в web версии Flutterflow. Через приложение выходит ерунда.
А ещё, пользуйтесь Вот - https://iconly.io

from [𝗺 𝗼 𝗺 𝗼](https://t.me/momo_nut)**
- Чтобы импортировать в iconmoon  (выполнить stroke to fill) надо или в Figma сделать vector path/union selection (если иконка простая) или в иллюстраторе object/expand strokes

- Проверьте уникальность шрифтового префикса, когда делаете download font в iconmoon. У каждого set он должен быть свой. После загрузите по новой
