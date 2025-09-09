---
dg-publish: true
---

## Обзор возможностей анимации (официальное видео)
[11. Animation | FlutterFlow University Expert Training - YouTube](https://www.youtube.com/watch?v=B0qz4JRYy7U)
[Офиц видео](https://www.youtube.com/watch?v=jlY_h0lJUEQ)
Полезные нюансы: [Micro Interactions, animations and transitions in FlutterFlow Apps - YouTube](https://www.youtube.com/watch?v=aMU5sjZdg7k)

## Инструменты для анимации

Для интеграции сторонней анимации во FlutterFlow доступны два основных инструмента:

1. **Lottie-анимация:** Подробности можно найти в официальной документации: [https://docs.flutterflow.io/concepts/animations/lottie-animation/](https://docs.flutterflow.io/concepts/animations/lottie-animation/
   и в видео: [How To Use Lottie Animations in Flutterflow - YouTube](https://www.youtube.com/watch?v=vTn9NU_nkZw&pp=ugUEEgJlbg%3D%3D)

Подборка lottie-файлов (анимаций) от @brozaurus:
[LottieFiles – Google Диск](https://drive.google.com/drive/folders/1ycPMq4xlMX2EgzBkczm81w_sY2_xxXxJ?usp=sharing)
[A micro-animations library](https://useanimations.com/#explore)


2. **Rive-анимация:** Документация доступна по ссылке: [https://docs.flutterflow.io/concepts/animations/rive-animation](https://docs.flutterflow.io/concepts/animations/rive-animation)


## как сделать анимацию на скрытие элемента

Q: https://t.me/flutterflow_rus/12427/45245
Как сделать анимацию на скрытие элемента, допустим в компонент стейте есть булево значение по которому отображается виджет, при смене значения - виджет анимированно выезжает, а как сделать, чтоб он так же анимированно сваливал?

A: Результат выглядит [так-см. в телеге](https://t.me/flutterflow_chat/27022).
![[../temp/anim1.jpg]]
![[../temp/anim2.jpg]]

**Пояснение:**
Для реализации анимации скрытия необходимо добавить обратную анимацию в On Action Trigger. Затем добавьте экшен, который вызывает эту анимацию. Важно, чтобы второй экшен после него имел статус Reset.

**Таким образом:**
- При появлении виджета срабатывает анимация, заданная в `On Page Load`.
- При скрытии виджета активируется анимация, настроенная через триггер.

