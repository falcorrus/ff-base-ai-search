---
dg-publish: 
tags:
  - telegram
origin: telegram
author: "Мила Гендельман"
---
Дата:  2025-02-27
From [Мила Гендельман](https://t.me/MilaGendelman)**
Использование:
У меня, например, есть страничка с уведомлениями, при уходе с нее все уведомления становятся прочитанными, то есть там нужно еще одно действие, кроме navback. И если на иконку назад я могу что угодно повесить, то при нажатии на android back button произойдет только navback. Этот виджет позволяет это переписать



Custom Widget, который позволяет переписать действие AndroidBackButton:
1. конвертируем содержимое страницы в компонент
2. создаем custom widget PopScopeWrapper (код ниже)
3. добавляем его в scaffold страницы и в качестве параметра передаем в него компонент с содержимым, а также действие, которое должно заменить navigate back на Android Back Button
```
class PopScopeWrapper extends StatefulWidget {
  const PopScopeWrapper({
    super.key,
    this.width,
    this.height,
    required this.onBack,
    this.notifComponent, // Функция, возвращающая компонент
  });

  final double? width;
  final double? height;
  final Future Function() onBack;
  final Widget Function()?
      notifComponent; // Теперь можно передавать NotifComponent

  @override
  State<PopScopeWrapper> createState() => _PopScopeWrapperState();
}

class _PopScopeWrapperState extends State<PopScopeWrapper> {
  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: widget.width ?? double.infinity,
      height: widget.height ?? double.infinity,
      child: PopScope(
        canPop: false, // Отключаем стандартное поведение "Назад"
        onPopInvoked: (popAllowed) async {
          await widget.onBack.call(); // Вызываем кастомный обработчик
        },
        child: widget.notifComponent != null
            ? widget.notifComponent!() // Вставляем компонент
            : const SizedBox(), // Если компонента нет, просто пустой виджет
      ),
    );
  }
}
```