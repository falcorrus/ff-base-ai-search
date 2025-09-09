---
title: "Using FlutterFlow Libraries to build Adapty<>FlutterFlow integration"
source: "https://blog.flutterflow.io/using-flutterflow-libraries-to-build-adapty-flutterflow-integration/"
author:
  - "[[Alexey Goncharov]]"
published: 2024-12-19
created: 2025-02-05
description: "Why We Built a FlutterFlow Integration and How You Can Create One Using an Existing Flutter/Dart SDKA few months ago, FlutterFlow introduced an exciting new feature: Libraries. In FlutterFlow, a library is a type of project that can include many of the same resources as other FlutterFlow projects—"
tags:
  - "статьи"
---
## Интеграция с Adapty (перевод)
### Оригинал: 
https://blog.flutterflow.io/using-flutterflow-libraries-to-build-adapty-flutterflow-integration/

## Вводная часть
[[Работа с Library (библиотека)]]

## Почему мы создали библиотеку Adapty FlutterFlow

В Adapty мы сразу увидели потенциал библиотек FlutterFlow, которые помогут нам создать мощную интеграцию между Adapty и FlutterFlow. [Adapty](https://adapty.io/?utm_source=FlutterFlow-blog&utm_medium=referral&utm_campaign=FlutterFlow-blog) — это комплексная платформа для управления и оптимизации подписок в приложении. Благодаря надежному SDK для покупок в приложении, аналитике в реальном времени, возможностям A/B-тестирования и прогнозированию доходов интеграция Adapty с FlutterFlow показалась нам идеальным способом помочь разработчикам приложений увеличить свой доход, а также расширить наш собственный охват.

Мы решили создать библиотеку, которая охватывает многие функции, предоставляемые нашим существующим Flutter SDK, упрощая для пользователей FlutterFlow добавление управления подписками в приложениях в свои проекты.

![](https://blog.flutterflow.io/content/images/2024/12/x4_FlutterFlow-article_banner1_v3.png)

**Adapty позволяет разработчикам приложений интегрировать покупки внутри приложения, настраивать платный доступ и проводить A/B-тесты — без обновлений приложения**

#### Библиотека FlutterFlow Adapty

Библиотека [Adapty FlutterFlow](https://marketplace.flutterflow.io/item/Mf1oFJcqngHzERZSPNA8?ref=blog.flutterflow.io) позволяет создавать и запускать платные и A/B-тесты на разных этапах пути пользователя к мобильному приложению — например, во время регистрации, в настройках или в других ключевых точках.

Эти этапы известны как Placements. Placement в вашем приложении может управлять несколькими платными доступами или A/B-тестами одновременно, каждый из которых предназначен для определенных групп пользователей, которые мы называем Аудиториями.

Благодаря библиотеке Adapty пользователи FlutterFlow могут легко экспериментировать с различными платными доступами с течением времени, заменяя один на другой без необходимости выпускать новую версию своего приложения.

![](https://blog.flutterflow.io/content/images/2024/12/adapty_docs_flutterflow_1.jpg)

Разработчики FlutterFlow могут использовать библиотеку Adapty для  [вызова серии действий](https://adapty.io/docs/ff-getting-started?utm_source=FlutterFlow-blog-1&utm_medium=referral&utm_campaign=FlutterFlow-blog) , чтобы определить, какой платный контент должен отображаться в определенном месте размещения. Затем они могут отображать соответствующий пользовательский интерфейс с помощью условных строителей в FlutterFlow. Наконец, разработчики могут регистрировать события отображения и покупки для просмотра аналитики и внесения корректировок в Adapty.

#### Как библиотека работает изнутри

Ядро библиотеки — это набор действий, представленных в FlutterFlow. Однако нам нужно было предпринять дополнительные шаги для правильной инициализации SDK и обработки передачи данных между действиями. 

1. **Добавление** [**adaptationy\_flutter**](https://pub.dev/packages/adapty_flutter?ref=blog.flutterflow.io) **в качестве зависимости**

Пользовательский код в нашей библиотеке использует наш существующий Flutter SDK, поэтому мы сначала добавили наш пакет Dart как зависимость. Вы можете управлять всеми зависимостями pub для пакета FlutterFlow на странице Project Dependencies.

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXdAgaXbwXQ6_Npc8NvcO-7goEZuNbyw21-xyvMcZGLdv0P2R-FixLW29HwrmeNweggt15m55Kb5DiPct6zCx-IbU8j8f4s5CRguZJFaYqbAoa6kbncTV6K_7FFulg9T-B4nPI8Oug?key=1Kd7-K-bIwxCqr1zC_y3_ZP_)

**Примечание: лучше всего импортировать определенную версию пакета. Если вы этого не сделаете, FlutterFlow будет использовать последнюю версию пакета, что может привести к неожиданным критическим изменениям.**

2. **Получение API-ключа пользователя**

Нам нужен был способ запрашивать у пользователей их ключ API, который мы используем при инициализации SDK. Это стало возможным благодаря [значениям библиотеки FlutterFlow](https://docs.flutterflow.io/resources/projects/libraries/?ref=blog.flutterflow.io#library-values) . В нашем проекте библиотеки мы создали новое значение библиотеки под названием AdaptyAPIKey.

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXfDMKJ8cKFbim5XG2VlxTh1ic_Wf26PYbClRB0p9pvadO7HEhClvgHK9fUO9laqXNsQ_9ZOF5pz-_RQhnEjA5pCpYySeraQpvqE5FfLe5qWFmNyFqYCjmoMetGcWWYcPrpkckHi4g?key=1Kd7-K-bIwxCqr1zC_y3_ZP_)

Когда пользователи импортируют библиотеку в свой проект, они могут указать свой ключ API в пользовательском интерфейсе.

3. **Инициализация Adapty SDK**

Чтобы использовать наш SDK, первым шагом является инициализация класса Adapty путем вызова Adapty().activate. Мы добились этого, создав пользовательское действие, которое пользователи могут вызывать при инициализации своего приложения в main.dart.

Код для действия инициализации также использует упомянутое выше значение библиотеки (FFLibraryValues().AdaptyApiKey).

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXd03_NPZXXwBzKANE4wlbxUxpPMMISmyrvGa5vwFse6Ei1YHX3ZW_mcAP6o5qC8BJ9q31iEBNccafE1EgN2VaCqzQhRwpfGgcFQ8g7gt_m96sesdYWCXDaNj70QxYVyweRM5NAz8w?key=1Kd7-K-bIwxCqr1zC_y3_ZP_)

4. **Создание пользовательских типов данных и перечислений**

Многие методы нам нужно было выставлять, принимать и возвращать классы, определенные в нашем базовом SDK. Однако FlutterFlow не распознает произвольные классы Dart, поэтому мы создали [пользовательские типы данных](https://docs.flutterflow.io/resources/data-representation/custom-data-types/?ref=blog.flutterflow.io) и [перечисления](https://docs.flutterflow.io/resources/data-representation/enums/?ref=blog.flutterflow.io) , которые отражают поля в классах из нашего SDK.

Мы также создали расширения для преобразования между типами, ожидаемыми нашим SDK, и структурами, используемыми FlutterFlow.

Хотя этот процесс был немного ручным и утомительным, он не был слишком сложным. Мы рады, что FlutterFlow в конечном итоге сможет распознавать пользовательские классы Dart непосредственно из кода, что сделает этот процесс намного более плавным. 

5. **Создание пользовательских действий**

Имея классы данных, мы создали [пользовательские действия](https://docs.flutterflow.io/concepts/custom-code/custom-actions?ref=blog.flutterflow.io) для каждого метода, который мы хотели предоставить пользователям в пользовательском интерфейсе FlutterFlow. Эти действия принимают входные данные, настроенные пользователем, и могут возвращать значения, используемые во всем приложении.

For example, the getPaywall action calls Adapty().getPaywall() under the hood, which returns an AdaptyPaywall object. We then use an extension to convert this object into a struct that can be returned from actions within FlutterFlow.

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXf0ZrXLDA1dKjrlBxJiiIRp2KiN3wYmT3VTYbbjmk_O7Gdh2-RIfpqOOjdzo1oKs3zZ08GW1lSAZNox659AuPvei4nT0rP4-zylsMlDwFu_KOlrr2bOiNK0iTOOe0AbscufwB67QQ?key=1Kd7-K-bIwxCqr1zC_y3_ZP_)

**Note: we found it easier to leverage the** [**VSCode extension**](https://docs.flutterflow.io/concepts/custom-code/vscode-extension/?ref=blog.flutterflow.io) **than the built in custom code editor for writing these custom actions.**

6. **Testing the Library**

To test the library, we created a sample project that imports the Library as a dependency. During active development, it's helpful to use the "current" version rather than a static version.

This sample project was not only useful for testing the complete user flow, but can also be made public to share with the community as a demo of how to use the library.

7. **Creating Documentation for the Library**

Once the Library was tested and made available to users, we created [documentation](https://adapty.io/docs/flutterflow?utm_source=FlutterFlow-blog-1&utm_medium=referral&utm_campaign=FlutterFlow-blog) to provide step-by-step instructions for using it. Depending on the integration you're building, you may need to guide users on changing OS permissions or highlight limitations, such as platform support.

#### What's Next for the Adapty Library

This week, FlutterFlow announced Marketplace support for Libraries. This exciting update will allow more FlutterFlow users to discover our Library, along with many others. Now, users can find Adapty in the FlutterFlow marketplace, access our documentation, and add it to their projects.

In addition to listing our library in the marketplace, we'll continue to add new features based on updates to our SDK. With [robust version control](https://docs.flutterflow.io/resources/projects/libraries/?ref=blog.flutterflow.io#library-versioning), we're able to upgrade the package dependency version in our Library project, add new features, test them, and publish them for FlutterFlow users.

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXc3fsgx2QF4J7RvYj1CfxxnY1OwcJy8q-28jM9l1R9XFWiC3xkQgaeUCZD_UmYGKXOBLyfe8jCVnS6ETEQZhzi50oI-7MP4B-as4CrXdBSEkSImTZaLZQ3-OYlIhcNWnW7hLL_HnA?key=1Kd7-K-bIwxCqr1zC_y3_ZP_)

**Adapty Library is now available on the FlutterFlow Marketplace**

#### The Benefits of Building a FlutterFlow Integration

Developing a FlutterFlow integration offers numerous advantages: providing FlutterFlow users easy access to your product's features, expanding your audience, making your SDK more accessible, and creating new revenue streams through monetizing your Library in the FlutterFlow marketplace. We hope our journey inspires you to explore the potential of building your own integration.

If you're curious about building a library in FlutterFlow, check out the [FlutterFlow documentation](https://docs.flutterflow.io/resources/projects/libraries/?ref=blog.flutterflow.io#importance-of-libraries) for more details. And if you want to learn more about our integration or try it out for yourself, see the [Adapty documentation](https://adapty.io/docs/ff-getting-started?utm_source=FlutterFlow-blog-2&utm_medium=referral&utm_campaign=FlutterFlow-blog).

![](https://blog.flutterflow.io/content/images/2024/12/x3_FlutterFlow-article_banner2.png)

[**Start using Adapty with FlutterFlow and get 3 months for free!**](https://app.adapty.io/flutterflow-offer/?ref=blog.flutterflow.io)