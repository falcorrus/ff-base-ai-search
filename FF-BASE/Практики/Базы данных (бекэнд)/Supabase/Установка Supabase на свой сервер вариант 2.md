---
title: Установка Supabase на свой сервер
source: https://telegra.ph/Ustanovka-Supabase-na-svoj-server-02-21
author: 
published: 2023-02-21
created: 2024-11-25
description: Установка Supabase
tags:
  - инструкция
  - IT
dg-publish: true
---
February 21, 2023
Оригинал: [Установка Supabase на свой сервер – Telegraph](https://telegra.ph/Ustanovka-Supabase-na-svoj-server-02-21)

## Кто может помочь
[Telegram: Contact @Kosmorangers](https://t.me/Kosmorangers) 
[Telegram: Contact @jrustick](https://t.me/jrustick) 

# Установка Supabase на свой сервер
## Облако или свой сервер?
@Kosmorangers
В облаке приложение работало медленно, долго погружались данные. Для проверки, поднял сервер в РФ с супой, подключил к нему то же самое приложение. Загрузка данных стала почти мгновенной. Я вообще считаю что облачный вариант супы предназначен для тестирования и.т.д. Но когда приложение готово к релизу, его необходимо подключать к супе на своём сервере, и сервер должен располагаться в том регионе, для которого предназначено приложение.
## Инструкция для timeweb
[Как развернуть Supabase в облаке Timeweb Cloud: инструкция](https://timeweb.cloud/tutorials/cloud/kak-razvernut-supabase-v-oblake-timeweb-cloud)

## Инструкция общая
**Нам понадобятся**
Сервер с установленным Linux,
Docker и docker-compose,
Свой домен (я использовал reg.ru).


## Шаги установки:

#### Шаг 1: Копируем репозиторий:

```
git clone --depth 1 https://github.com/supabase/supabase
cd supabase/docker
cp .env.example .env
```

Далее заходим на сайт: [Supabase key generator](https://supabase.com/docs/guides/self-hosting#api-keys) и генерируем 3 ключа: JWT\_SECRET, ANON\_KEY и SERVICE\_KEY.

Далее открываем файл .env командой

```
 sudo nano .env
```

и вставляем ключи ANON\_KEY и SERVICE\_KEY в соответствующие поля.

Далее идём по пути "docker/volumes/api/" и открываем kong.yml:

```
cd volumes/api/
sudo nano kong.yml
```

и также прописываем эти два ключа в соответствующие поля.

Настройка ключей закончена.

Возвращаемся обратно в файл "/docker/.env" и находим там две строки:

API\_EXTERNAL\_URL=http://dropletipaddress:8000

SUPABASE\_PUBLIC\_URL=http://localhost:8000

и меняем значения на свой домен. **Обязательно** в "API\_EXTERNAL\_URL" **ставим https**, даже если у Вас нет SSL и **убираем ":8000"**, так как **FlutterFlow коннектится только по протоколу https и без портов**. Должно получиться как то так:

```
API_EXTERNAL_URL=https://my-domain.com
SUPABASE_PUBLIC_URL=http://my-domain.com:8000  
```

#### Шаг 2: Настройка домена (DNS зоны)

Далее идем на сайт [2IP](https://2ip.ru/) и копируем свой IP адрес сервера (если Вы подключились к нему **не** удалённо) и идём на сайт поставщика услуг доменов. Там щёлкаем по нашему купленному домену и создаём следующие DNS записи:

```
Тип: A
Subdomain: *
IP Address: your-server-ip-adress

Тип: A
Subdomain: @
IP Address: your-server-ip-adress

Тип: A
Subdomain: www
IP Address: your-server-ip-adress
```

Отлично! Теперь мы "сказали" сайту где находится Ваш сервер.

#### Шаг 3: Настройка HTTP Proxy

Дальше настроим HTTP proxy (используется caddy):

```
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https -y

curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg

curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list

sudo apt-get update
sudo apt-get install caddy -y
```

Когда установка завершится, открываем кофиг-файл caddy:

```
sudo nano /etc/caddy/Caddyfile
```

И вставляем данный код:

```
https://yourdomain.com {
        reverse_proxy /rest/v1/* localhost:8000
        reverse_proxy /auth/v1/* localhost:8000
        reverse_proxy /realtime/v1/* localhost:8000
        reverse_proxy /storage/v1/* localhost:8000
        reverse_proxy * localhost:3000
}
```

Сохраняем, закрываем и перезапускаем службу caddy:

```
sudo service caddy restart
```

#### Запуск:

Теперь осталось удостовериться, что Вы находитесь в /supabase/docker и запустить docker контейнеры:

```
docker-compose up
```

Через несколько минут на Вашем домене будет свой экземпляр Supabase.

**В FlutterFlow API\_URL будет "https://your-domain.com" , а ANON\_KEY - тот самый ANON\_KEY, который Вы генерировали в самом начале!**

### Спасибо за прочтение!

Использованные ресурсы: [https://www.safyah.com/blog/self-hosting-supabase-on-ubuntu-and-digital-ocean](https://www.safyah.com/blog/self-hosting-supabase-on-ubuntu-and-digital-ocean)