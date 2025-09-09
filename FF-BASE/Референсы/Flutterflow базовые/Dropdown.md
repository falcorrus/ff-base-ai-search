---
title: Dropdown | FlutterFlow Documentation
source: https://docs.flutterflow.io/resources/forms/dropdown/
author: 
published: 
created: 2025-02-04
description: Learn how to add Dropdown widget in your FlutterFlow app.
tags: []
---
## Официальное объяснение
Источник: https://docs.flutterflow.io/resources/forms/dropdown/

Виджет DropDown позволяет пользователям выбирать из списка вариантов. Он требует набор элементов для отображения и начальное значение для указания текущего выбора. Когда пользователь выбирает элемент из раскрывающегося списка, значение обновляется, чтобы отразить выбранный элемент.

Вы можете использовать этот виджет в любой ситуации, когда вы хотите, чтобы пользователи могли выбирать из набора опций, например, выбирать страну, язык или цвет.

Состояние виджета

Прежде чем углубляться в виджеты форм, ознакомьтесь с нашим руководством по [**состояниям виджетов,**](https://docs.flutterflow.io/concepts/state-management/widget-state) чтобы эффективно управлять состоянием и поведением элементов формы.

Давайте посмотрим, как добавить виджет *DropDown* и создать пример, который показывает выбранное значение на виджете Text. Вот как это выглядит:

1. Добавьте виджет **DropDown** , перейдите на **панель свойств > Определить параметры >** нажмите **Добавить параметры,** чтобы добавить элементы.
2. Чтобы отобразить значение по умолчанию, перейдите в раздел **«Начальная конфигурация»** и введите значение. Убедитесь, что оно соответствует одному из параметров, добавленных на предыдущем шаге.
3. Выбранное значение раскрывающегося списка можно получить через *Widget State > DropDown* . Чтобы отобразить его в виджете *Text* , добавьте виджет [**Text**](https://docs.flutterflow.io/resources/ui/widgets/text) , перейдите на панель свойств, нажмите **Set from Variable** и выберите **Widget State > DropDown** (т. е. имя вашего раскрывающегося списка).

### Установка начального [значения](https://docs.flutterflow.io/resources/forms/dropdown#setting-initial-value "Прямая ссылка на установку начального значения")

Установка значения по умолчанию или начального значения для DropDown является общим требованием для многих приложений. Это может обеспечить лучший пользовательский опыт, предварительно выбрав наиболее вероятный вариант.

Чтобы установить начальное значение:

1. Выберите виджет **DropDown** > перейдите на **панель свойств** > **Начальная конфигурация** .
2. В поле **«Начальное значение параметра** » введите имя параметра, который вы хотите установить в качестве параметра по умолчанию.
3. Чтобы задать это значение динамически, откройте меню **«Установить из переменной»** и выберите переменную.
1. Например, чтобы установить это значение из Firebase, убедитесь, что у вас есть доступ к документу Firebase, содержащему поле, которое вы хотите установить.
2. Откройте меню **«Задать из переменной»** > выберите **документ \[имя\_коллекции\]** > выберите **поле** .
4. Если вы не установите начальное значение, будет отображен **текст подсказки .**

### Сохранение значения DropDown при [изменении](https://docs.flutterflow.io/resources/forms/dropdown#saving-dropdown-value-on-selection-change "Прямая ссылка на сохранение значения DropDown при изменении выбора")

Вы можете захотеть сохранить значение раскрывающегося списка сразу после изменения выбора. Этот подход полезен, когда вы хотите гарантировать, что выбор пользователя будет немедленно сохранен, не дожидаясь отправки формы. Таким образом, вы можете обеспечить лучший пользовательский опыт и снизить риск потери данных в случае любого прерывания.

Это можно сделать, добавив действие, например, [обновить состояние приложения](https://docs.flutterflow.io/resources/data-representation/app-state#update-app-state-action) или [обновить запись Firestore](https://docs.flutterflow.io/integrations/database/cloud-firestore/firestore-actions#update-document-action) , которое [срабатывает при изменении выбора](https://docs.flutterflow.io/resources/ui/widgets/widget-commonalities#trigger-action-on-selection-change) в этом виджете.

![Сохранение значения DropDown при изменении выбора](https://docs.flutterflow.io/assets/images/saving-dp-value-on-selection-change-650062acd9356949bfbd767de51af87e.webp)
### [Настройка](https://docs.flutterflow.io/resources/forms/dropdown#customizing "Прямая ссылка на настройку")Вы можете настроить внешний вид и поведение этого виджета, используя различные свойства, доступные на панели свойств.

### Отображение [метки](https://docs.flutterflow.io/resources/forms/dropdown#showing-option-label "Прямая ссылка на отображение метки параметра")

Виджет раскрывающегося списка позволяет вам показывать метку, а не фактическое значение опции. Добавив метку опции, вы можете получить простое/короткое имя или аббревиатуру (которую довольно легко сравнивать и обрабатывать в бэкэнде) вместо сложного имени (например, Фолклендские острова \[Мальвинские острова\]).

Например, в раскрывающемся списке «Страна» вы можете иметь разные *значения* *параметров* для хранения в бэкэнде и *метки параметров* для отображения в раскрывающемся списке. Как показано ниже:

| Значения параметров | Метки опций |
| --- | --- |
| США | Соединенные Штаты |
| В | Индия |
| ФК | Фолклендские острова (Мальвинские острова) |

Чтобы показать метку параметра:

1. Выберите виджет **DropDown** , перейдите на панель свойств и включите переключатель **«Добавить метки параметров»** .
2. Введите значение в полях **Define Option Values** ​​и **Define Options Labels** . Нажмите **Add Option** (под *Define Option Values* ), чтобы добавить больше значений и меток.
3. Вам также необходимо задать **Тип данных** для значений. Например, если значения, которые вы собираетесь хранить, являются числами, такими как 1,2,3, установите его на *Integer* .

### [Раскрывающийся список](https://docs.flutterflow.io/resources/forms/dropdown#searchable-dropdown "Прямая ссылка на раскрывающийся список поиска") с возможностью поискаВиджет *DropDown* — хороший выбор, когда у вас небольшое количество вариантов (около 10–20). Однако если у вас больше вариантов, рассмотрите возможность использования раскрывающегося списка с возможностью поиска.

Поисковый раскрывающийся список позволяет пользователям искать и фильтровать параметры, вводя текст в строке поиска. По мере ввода текста раскрывающийся список динамически фильтруется, чтобы показывать только соответствующие параметры. Это особенно полезно при работе с длинными списками параметров и может улучшить пользовательский опыт, сокращая время, необходимое для поиска и выбора параметра.

Чтобы сделать выпадающий виджет доступным для поиска:

1. Select the **DropDown** widget, move to the **Properties Panel > DropDown Search >** enable **Is Searchable** option.
2. You can also customize the **Search Hint Text** property.

![Создание раскрывающегося списка с возможностью поиска](https://docs.flutterflow.io/assets/images/making-dd-searchable-f1de9e328ba77af1b6c50fbb028e23b0.png)

### Disable dropdown[​](https://docs.flutterflow.io/resources/forms/dropdown#disable-dropdown "Прямая ссылка на раскрывающийся список «Отключить»")

You might need to disable a dropdown when certain conditions are not yet met or need to be fulfilled. For example, when the dropdown options are dependent on other fields, and those fields are not filled yet.

To disable the dropdown:

1. Select the **DropDown** widget, move to the **Properties Panel > DropDown Search >** enable **Disable Dropdown** option.
2. Click on **Unset** and select the source that returns the boolean value (i.e., True or False), such as boolean variable, [Conditions](https://docs.flutterflow.io/resources/functions/conditional-logic), [Code Expression](https://docs.flutterflow.io/resources/functions/utility#code-expressions).

![Отключение выпадающего списка](https://docs.flutterflow.io/assets/images/disabling-dropdown-05e5d82e8c412f1ae7cc909623b9e693.png)

### Allow multi select[​](https://docs.flutterflow.io/resources/forms/dropdown#allow-multi-select "Прямая ссылка на Разрешить множественный выбор")

You might want to allow users to select multiple options from the dropdown list. For example, on an e-commerce app, users might want to filter products based on multiple attributes, such as t-shirts in both 'blue' and 'red' colors.

To allow multi-select, select the **Dropdown** widget, move to the properties panel, find the **Allow Multi Select** property, and enable it.

info

To clear the selection, you can use the [Reset Form Fields](https://docs.flutterflow.io/resources/forms/reset-form-field) action and choose the **Reset Dropdown Fields** option. Then, simply select the name of the dropdown widget you wish to reset.

### Changing dropdown size[​](https://docs.flutterflow.io/resources/forms/dropdown#changing-dropdown-size "Прямая ссылка на изменение размера раскрывающегося списка")

To change the height and width of the dropdown, select the **DropDown** widget, move to the **Properties Panel > DropDown Properties > enter the Width and Height value**.

### Set max height[​](https://docs.flutterflow.io/resources/forms/dropdown#set-max-height "Прямая ссылка на установку максимальной высоты")

If needed, you can also control the dropdown height using the **Max Height** property.

### Adding margin[​](https://docs.flutterflow.io/resources/forms/dropdown#adding-margin "Прямая ссылка на добавление маржи")

Margin adds a space between the DropDown's text and its border. To change the margin, select the **DropDown** widget, move to the **Properties Panel > DropDown Properties >** find the **Margin** property, and change the values.

### Changing background color[​](https://docs.flutterflow.io/resources/forms/dropdown#changing-background-color "Прямая ссылка на Изменение цвета фона")

To change the background color, move to the **Properties Panel > DropDown Style > set the Fill Color**.

![Изменение цвета фона](https://docs.flutterflow.io/assets/images/changing-background-color-2522beea0239fb73d5746b2a33cb77ac.png)

Menu elevation adds a shadow to the dropdown, giving it a sense of depth and making it appear above the surface it is placed on.

To change the menu elevation (depth or Z-axis), move the **Properties Panel >** enter the **Menu** **Elevation** value.

info

Чем больше значение, тем больше размер тени.

### Добавление [границы](https://docs.flutterflow.io/resources/forms/dropdown#adding-border "Прямая ссылка на добавление границы")

Посмотрите, как [добавить границу](https://docs.flutterflow.io/resources/ui/widgets/widget-commonalities#adding-border) .

### Показать/скрыть [подчеркивание](https://docs.flutterflow.io/resources/forms/dropdown#showhide-underline "Прямая ссылка на Показать/скрыть подчеркивание")

Чтобы отобразить или скрыть подчеркивание раскрывающегося списка, переместите **Панель свойств >** **Стиль раскрывающегося списка** > используйте переключатель **Скрыть подчеркивание** .

### Исправить [положение](https://docs.flutterflow.io/resources/forms/dropdown#fix-position "Прямая ссылка на исправление позиции")

По умолчанию параметры раскрывающегося списка отображаются над/над кнопкой раскрывающегося списка. Чтобы отобразить под/под кнопкой, переместите переключатель **Properties Panel >** **DropDown Style** > на переключатель **Fix Position** .

![Исправлено положение раскрывающихся вариантов](https://docs.flutterflow.io/assets/images/fix-position-44942cedca06778938f5864d54a1a709.webp)

Запустить действие при изменении

# Видео
## [FlutterFlow Tip #3: Dropdown Menus in FlutterFlow (custom dialogs от Kaleo Design)](https://www.youtube.com/watch?v=7Qc7qLrdYj4)
## [Dynamic DropDown](https://www.youtube.com/watch?v=Ur6rr2uXq-c&t=394s)
## [How to create Supabase Dropdowns in FlutterFlow](https://www.youtube.com/watch?v=TTmwR-QnHrc)



