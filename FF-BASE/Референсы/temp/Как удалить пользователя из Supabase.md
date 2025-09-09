---
dg-publish: 
tags:
  - telegram
origin: telegram
author: "Dmitriy K"
---

Дата:  2025-03-31
From [Dmitriy K](https://t.me/kirilkindn)**

## Q: Как удалить пользователя из Supabase (реального пользователя из таблицы auth.users)
Вот [первый вариант](https://t.me/flutterflow_rus/12435/52466), а ниже улучшенный
A: Использовать Edge function (более улучшенный и более безопасный вариант). 

1. Supabase. в AI Assistant пишем запрос
```
create the edge function and deploy it <text function>
``` 
Делаем деплой функции.

2. FF. Создаем API
POST https://<PROJECT_NAME>.supabase.co/functions/v1/delete-user-account
Headers: Authorization: Bearer $[jwt]$, API KEY - не нужно.
Body: $<пусто>$
Variables: создаем jwt - string

3. FF - Actions. Вызываем API, задаем переменную jwt = Authenticated User -> id token (jwt token)

Код функции - во вложении.
### Код функции:
```
В функции ничего не нужно менять.

import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";
import { corsHeaders } from '../_shared/cors.ts';

console.log("Функция удаления учетной записи пользователя");

Deno.serve(async (request) => {
  // Это необходимо, если вы планируете вызывать вашу функцию из браузера.
  if (request.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    // Создание экземпляра SupabaseClient
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? '',
      { global: { headers: { Authorization: request.headers.get('Authorization')! } } }
    );

    // Создание объекта пользователя, который содержит данные для идентификации user.id
    const {
      data: { user },
    } = await supabaseClient.auth.getUser();

    // Выбрасывание ошибки, если не удается идентифицировать пользователя по токену
    if (!user) throw new Error('Пользователь не найден для JWT!');

    // Создание клиента supabaseAdmin, который использует Service Role Key
    const supabaseAdmin = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    );

    // Вызов метода deleteUser на клиенте supabaseAdmin и передача user.id
    const { data: deletion_data, error: deletion_error } = await supabaseAdmin.auth.admin.deleteUser(user.id);

    // Логирование ошибки удаления для отладки. Удалите, если не требуется! 
    console.log(deletion_error);

    // Возврат ответа с информацией о пользователе, который был удален
    return new Response('Пользователь удален: ' + JSON.stringify(deletion_data, null, 2), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 200,
    });
  } catch (error) {
    // Возврат ошибки с сообщением об ошибке в случае возникновения проблем
    return new Response(JSON.stringify({ error: error.message }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 400,
    });
  }
});
```

![[txt_Как удалить пользователя из Supabase_.txt]]