Это action, который можно вызывать по нажатию.
В него упаковываем информацию или информацию + кнопку, когда требуется возврат на вызывающую страницу.

## Еще
[[CallBack|Как передавать параметры в шторку и назад]]
[[Дизайн Bottom bar]]
## Вопросы
###  Можно ли сделать чтобы шторка вылазила на минимальный размер если нет или мало строк и расширялась до максимального по мере заполнения строк. и как если можно?
[A:](https://t.me/flutterflow_rus/12427/53580) у контейнера убери высоту, а у колонны дай мин размер, когда вызываешь шторку не ставь высоту.

[вариант2:](https://t.me/flutterflow_rus/12427/53582)
Сделать два контейнера. Верхний полностью прозрачный, который растягивается на всю допустимую ширину. А нижний расширяется под внутренний контент. И например на верхний контейнер повесить экшен Close Dialog.
И у нижнего задать min и max размеры.

[Вариант 3](https://t.me/flutterflow_chat/32670) (от поддержки)
Как скрыть Bottom bar при нажатии на пустое место
Почему bottom sheet не закрывается при нажатии на scrim?

Ответ поддержки:
Thanks for your question! 😊 Let's get straight to solving this potential behavior with "Show Bottom Sheet" and "Open Custom Dialogue." Based on your description, it seems the dismissible behavior is being influenced by the absence of a height definition in these components. Here's how you can resolve and optimize this:
1️⃣ Set Height for Your Bottom Sheet or Custom Dialog (Recommended Approach):

- When you don't set a height, the system may struggle to handle gestures like tapping on the scrim (the background outside the sheet/dialog), leading to non-dismissable behavior.

- For Bottom Sheet: Try setting the height proportionally like this:

MediaQuery.sizeOf(context).height * 0.6 // You can replace 0.6 with the percentage you'd like to use.


Alternatively, use a fixed height (e.g., 400 pixels) if consistent sizing fits your design better.

- For Dialogs:

You can set the height similarly. For instance:

dart
MediaQuery.sizeOf(context).height * 0.5


or a fixed height like 300 pixels. This ensures proper rendering and handling of interactions.
2️⃣ Add Manual Dismiss Action as a Backup:

- Create an invisible container that overlays the dialog/sheet area outside the component.

- Add the "On Tap" → "Close Dialog" or "Close Bottom Sheet" action to emulate the dismiss mechanism. While not ideal, this acts as a reliable fallback for certain edge cases.
3️⃣ Consider Using Scaffold-Level Overlays for Simplicity:

- For simple feedback messages or notifications, you can use "Show Snack Bar" instead of modals. They are lightweight and avoid interaction conflicts.

- For multi-step flows, navigating to a dedicated page might offer a cleaner user experience and avoid dismiss behavior issues.
4️⃣ Height Setting Examples for Clarity:

Bottom Sheet:

- Proportional: MediaQuery.sizeOf(context).height * 0.7

- Fixed pixels: 400
Dialog:

- Proportional: MediaQuery.sizeOf(context).height * 0.5

- Fixed pixels: 300
These adjustments should address your issue effectively. If this still feels inconsistent, there’s a slight chance it could be a bug (as you've suspected). If so, I'd recommend testing with different height values and even report the behavior if you can reproduce it consistently, we’ll dive deeper to ensure everything runs smoothly.
Keep on building amazing apps, and let me know how these solutions work out! 🤗
Best regards,
Richard

