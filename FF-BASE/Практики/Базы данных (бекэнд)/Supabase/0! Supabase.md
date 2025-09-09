---
dg-publish: true
title: Supabase
---
# Supabase
## Определение
Supabase — это платформа, ориентированная на разработчиков, которая предлагает **базу данных как услугу**, а также **дополнительные инструменты для создания бэкенда** для приложений.

Основные функции и возможности Supabase, для которых она используется:

1.  **База данных PostgreSQL**: Supabase основана на PostgreSQL, что делает ее реляционной базой данных с поддержкой SQL-запросов. Это позволяет работать со сложными запросами, связями между таблицами, транзакциями и строгой структурой данных.
2.  **Автоматические API**: Она автоматически генерирует REST API для каждой таблицы и функции в PostgreSQL, упрощая взаимодействие с базой данных.
3.  **Real-time обновления**: Поддерживает обновления данных в реальном времени через WebSockets, что полезно для приложений, требующих мгновенного отображения изменений.
4.  **Аутентификация**: Предоставляет сервис аутентификации (на базе GoTrue) с поддержкой OAuth (Google, GitHub, Facebook и др.), OTP (одноразовых паролей) и Magic Links.
5.  **Безопасность данных**: Использует Row-Level Security (RLS) PostgreSQL для создания гибких правил доступа к данным на уровне строк, таблиц или представлений на основе JWT-токенов.
6.  **Серверная логика (Функции)**: Поддерживает хранимые процедуры, триггеры и функции PostgreSQL для выполнения сложной логики на уровне базы данных, а также Edge Functions (на основе Deno) для серверной логики, выполняемой ближе к пользователям.
7.  **Файловое хранилище**: Предоставляет S3-совместимое хранилище через Storage API.
8.  **Расширенная аналитика**: Благодаря PostgreSQL, поддерживает сложные аналитические запросы и работу с большими наборами данных, а также расширения, такие как PostGIS для геопространственных запросов.
9.  **Гибкость развертывания**: Может быть развернута локально или на облачных платформах.
10. **Интеграция с GraphQL**: Поддерживает GraphQL, что позволяет эффективно запрашивать только необходимые данные и реализовывать real-time подписки.

**Supabase подходит, если:**
*   Вам нужна SQL-база данных со строгой структурой данных.
*   Ваше приложение требует транзакций, сложных запросов и реляционных связей.
*   Вы хотите использовать мощные real-time функции и Edge Functions.
*   Вам нужна гибкость в развертывании (облако или self-hosted).
*   Вы цените удобство просмотра данных в привычной табличной форме и возможность вынести часть логики из фронтенда.

#### Sources:

- [[Firebase Vs Supabase]]
- [[Appwrite]]
- [[GraphQL]]


## Обучение
[[Обучение и блогеры|Обучение и блогеры]]
[16. Databases Part 2: SQLite & Supabase | Обучающее видео](https://www.youtube.com/watch?v=f7bAWV6S32E)
[Общее и создание VIEW](https://www.youtube.com/watch?v=1dLSWYD2lso)

## Цены
[Актуальные цены](https://supabase.com/pricing) на облачную Supabase
А вот цены в виде скриншота
![[../../temp/PricingFeesSupabase.jpeg]]

## Развернуть (deploy) Supabase на свой сервер
[[Установка Supabase на свой сервер вариант 2]]
Также можно использовать [[Хранилище S3]]

## Общее, все упаковано
[[../Бекэнды backends|Что такое бэкэнд и с чем его едят]]
[База знаний от официального комьюнити FF](https://community.flutterflow.io/knowledge-base)
[Как найти индекс в appState](https://community.flutterflow.io/discussions/post/update-item-index-app-state-CY5XvdriZpnEHEY)
[Пагинация в Supa](https://community.flutterflow.io/community-tutorials/post/pagination-in-flutterflow-web-project-using-supabase-ENG9B092Un9oVsv)

[[SQL lite|SQLite-Альтернатива кешу для ускорения работы]]

[Проверка, что даты брони не внутри предыдущей брони - techn#2](https://www.youtube.com/watch?v=-l3iRV1WlEM)
[[Поиск в Supabase много]]

[[Делаем чат в Supabase]]

## Географические карты
[Геообъекты в радиусе от точки - technique4](https://www.youtube.com/watch?v=-l3iRV1WlEM)
[Как сделать онлайн трекинг по картам Google](https://blog.flutterflow.io/live-tracking-google-maps-driver/)
[Flutterflow - Custom Functions To Simplify Locations](https://www.youtube.com/watch?v=23NM9JyRjQg)
[FlutterFlow | Google Maps Search and Nearby Places - из текста показывает LatLong](https://www.youtube.com/watch?v=29Oz0LI8j68)

[Сделать как в Trello](https://www.youtube.com/watch?v=pmqZAkZv-to)
[как решить проблему с CORS в firebase и FF](https://docs.flutterflow.io/actions/actions/utilities/upload-data#web-access-for-pdfs-and-other-files)

## Компоненты и списки:
[Dynamic Selections in FlutterFlow: Create Your Custom Multi-Item Picker Component](https://www.youtube.com/watch?v=FV5Xw8LnpJE)
[Сделать интервал для календаря, удобно для фильтрации свободной недвиж, 4 способа, action на вызов диапазона дат](https://www.youtube.com/watch?v=kHUq8dIMy34)
[Как сохранить из API в пользовательский тип данных, техника2](https://www.youtube.com/watch?v=AzYHCgJrwmY)

[How to manually construct a Dynamic Link URL](https://www.youtube.com/watch?v=68yRbGtrWaE)
[Как в Suparbase подключить загрузку фото в bucket](https://www.youtube.com/watch?v=jM7OfHD8J6E)
[как в кастом коде получить доступ к локал стореджу](https://community.flutterflow.io/widgets-and-design/post/custom-widget-and-ffappstate-KEqkOSuiJE6B7W7)

[Универсальный триггер на обновление Supa](https://youtu.be/PhAI000IbBU?si=vOTz6VRoGEyqFE_6)

[Сохранение версий изменения ячеек в Supa, техника4](https://www.youtube.com/watch?v=YnjOl4sYYaY)



## chatGPT в Supa
[спрашиваешь в свободной форме о данных в твоей таблице, workflow2](https://www.youtube.com/watch?v=Q1M1e7FpuuU)


## Как подключить Google к Supabase
https://www.youtube.com/watch?v=_XM9ziOzWk4&t=1s

## Edge functions (в Supabase)
Разбор функции и и триггера для синхронизации изменений из Supa в Typesence 
см. с 31:49
[Build A Real App With FlutterFlow, Supabase, GraphQL and TypeSense (Step by Step From Scratch) - YouTube](https://www.youtube.com/watch?v=5ue32B5SYo8)

# Еще
[[Поиск в Supabase много]]
[[Установка Supabase на свой сервер вариант 2]]
[[Supabase realtime (обновление базы)]]
