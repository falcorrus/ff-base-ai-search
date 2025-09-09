Офиц документация: https://docs.flutterflow.io/integrations/google-analytics/
Видео курс: [GA4: что такое события? Как подключить DebugView #3(10) - YouTube](https://www.youtube.com/watch?v=tpdfHl9Z2DM&list=PLeDR6lYFEHWHr7rznfkgPiq63yLhhYgbZ&index=3) 
[Инструкция для новичков](https://support.jmango360.com/portal/en/kb/articles/beginners-guide-firebase-analytics#:~:text=The%20Analytics%20section%20of%20Firebase,app%2Dversion%20adoption%2C%20etc) 
# Подробно

> [!INFO] Google Analytics интегрирован в Firebase. Это означает, что вам необходимо настроить Firebase, чтобы включить отслеживание аналитики и регистрировать события из вашего приложения FlutterFlow.

## Для начала необходимо включить
1. Google Analytics в Firebase 
2. в FlutterFlow в разделе «Настройки» - «Интеграции» - "Google Analytics". 
FlutterFlow начнёт автоматически регистрировать события, такие как загрузка страниц, взаимодействие с виджетами и действия аутентификации. Кроме того, можно отслеживать пользовательские события с параметрами для записи определенных действий пользователей, относящихся к целям приложения, например, покупок продуктов в приложении электронной коммерции. 

Автоматически логируется следующее:
- **On Page Load**: Logs an event when a user opens a page, recorded with the Firebase-recommended name `screen_view`. The actual screen name is accessible within the `screen_name` parameter.

> [!INFO]
> Используем для анализа открытия страниц. У события есть встроенные параметры (нет необходимости свои делать), т.е. можно отслеживать все, что происходит при открытии.

- **On Action Start**: Captures events when users interact with widgets that trigger actions. Events are logged in the format `{WIDGET_NAME}_{TRIGGER_TYPE}`. For instance, if a user taps a button that navigates to another page, the event is logged as `Button_navigate_to`.
- **On Each Individual Action**: This logs an event for every individual action or action chain for a given widget. It will be logged as `{WIDGET_NAME}_{TRIGGER_TYPE}` For example, when the user taps on a button and adds the _Upload Media_ action followed by the _Update App State_ action, the event will be logged as `Button_upload_media` and `Button_update_local_state`.
- **On Authentication**: Logs events for authentication-related actions such as sign-up, login, logout, password reset, or account deletion. Events are logged using the action type, e.g., `sign_up` or `login`.
## Отслеживаем 
В [Гугл аналитике](https://analytics.google.com/) идёте в Администратор - Просмотр данных - События и видите множество событий. Ищите то, по которому хотите отслеживать.
##  переходы
- MAIN_PAGE_ContainerCard_ON_TAP -
	на странице с названием *MAIN* **нажат** контейнер с названием *ContainerCard*
- MAIN_PAGE_navigate_to_event_ON_TAP
	со страницы с названием *MAIN* **перешли** на страницу *Event*

## открытия страниц
Нам нужно событие screen_view (оно срабатывает при открытии экрана приложения)

> [!NOTE] Для понимания, какая именно страница приложения открылась, нам нужно добавить пользовательский параметр

Например. У нас есть страница *Event*. Хотим видеть, сколько раз её открыли.
В самый верхний виджет добавляем action (в On Page Load) - Google analytics event
	В event name пишем название события. У нас это *screen_view*
	Добавляем параметр. Лучше его называть понятно, например *eventID* (по нему можно будет фильтровать). 
	В *eventID* либо зашиваем цифру, если у нас на каждое событие свой экран или просто будем помнить, что эта цифра значит, что открывали именно экран Event. Или вносим параметр, по которому хотим идентифицировать именно этот экран. Например, если при входе зашьем данные о пользователе, который входит.

> [!info]
> 1. Обновляем приложение
> 2. Нажимаем в приложении на это действие
> 3. Ждём до 24 часов, чтобы наш пользовательский параметр стал виден в Аналитике.

Открываем в аналитике "Администратор - Просмотр данных - Специальные определения"
![[image_event.jpeg]]

Нажимаем синюю кнопку "Создать специальный параметр", в нем в "параметр события" должен появиться наш eventID.
Если не появился, значит или не прошло 24 часа, или вы в программе ни разу ни открыли этот экран.

## Анализ
Теперь можем видеть, что экран Event открывался два раза, c параметром eventID 26 и 70 (в моем случае в *специальный параметр* передавался *page parameter* FF (https://baonline.ru/event?id=26)
Что screen_view касается именно нашего экрана Event мы знаем, посколько только в нем передавался параметр eventID).
![[image_Google Analytics_event-1.jpg]]

# Разное
## DebugView как пользоваться (отладка онлайн только за тобой)
[Документация](https://support.google.com/analytics/answer/7201382?hl=ru&utm_id=ad)
- в Chrome установить *Google Analytics Debugger*
- Когда вы включите на устройствах режим отладки, откройте страницу [Администратор](https://analytics.google.com/analytics/web/#/?pagename=admin&utm_source=gahc&utm_medium=dlinks) и в разделе _Просмотр данных_ выберите **DebugView**. Начните пользоваться сайтом или приложением и отслеживайте активируемые события.


