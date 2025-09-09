---
dg-publish: true
---
## Обучающие видео
Много про RLS (права на строки, на столбцы, MFA/multi-factor auth)
[Supabase Is A LOT More POWERFUL Than You Thought! - YouTube](https://www.youtube.com/watch?v=Jipdn8SLwAI)

## Права в Supa
Подробное видео: [A Crash Course In Row-Level Security (RLS) For FlutterFlow Users - YouTube](https://www.youtube.com/watch?v=Fqre21bcxlo)

Надо прописывать в **policies** к каждой таблице. Пишет одну или несколько политик. Надо, чтобы условие срабатывало **в любой** из них.

### дать админский доступ определённому ID (666..)
((( SELECT auth.uid() AS uid) = id) OR (auth.uid() = '666408b4-1566-447b-a36c-0e36c9ebc96d'::uuid))
### Доступ, если совпадает столбец в двух таблицах
// myShopN в таблице users и shopIDRef в таблице productos
(EXISTS ( SELECT 1
FROM (users u
JOIN productos p ON ((u."myShopN" = p."shopIDRef")))
WHERE (u.id = auth.uid())))

## Разрешаем только пользоватям, чьё id в таблице users совпадает с uuid_owner в orders
В таблице *order* заводим столбец *uuid_owner*
В таблице *users* нужен столбец *id*
Делаем, что доступ только, если данные в них совпадают

```
(EXISTS ( SELECT 1
FROM (users u
JOIN orders o ON ((u.id = o.uuid_owner)))
WHERE (u.id = auth.uid())))
```

## Доступ к таблице для Админа.
В таблице *users* в столбце *tariff* должно быть *admin*
```
(EXISTS ( SELECT 1
FROM users
WHERE ((users.id = auth.uid()) AND (users.tariff = 'admin'::text))))
```


## Все возможные варианты. Выберите нужный
CREATE TABLE companies (
 id SERIAL PRIMARY KEY,
 name TEXT NOT NULL
);

CREATE TABLE users (
 id UUID PRIMARY KEY,
 email TEXT NOT NULL UNIQUE,
 company_id INTEGER REFERENCES companies(id),
 role TEXT CHECK (role IN ('User', 'Admin')) DEFAULT 'User'
);

CREATE TABLE todos (
 id SERIAL PRIMARY KEY,
 title TEXT NOT NULL,
 description TEXT,
 completed BOOLEAN DEFAULT FALSE,
 company_id INTEGER REFERENCES companies(id),
 user_id UUID REFERENCES users(id),
 created_at TIMESTAMP DEFAULT now() 
 );

INSERT INTO companies (name) VALUES ('Company A'), ('Company B');

ALTER TABLE todos ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Company-based select access"
ON todos
FOR SELECT
USING (
 company_id = (SELECT company_id FROM users WHERE id = auth.uid()) 
);

CREATE POLICY "Company-based insert access"
ON todos
FOR INSERT
WITH CHECK (
 company_id = (SELECT company_id FROM users WHERE id = auth.uid()) 
);

CREATE POLICY "Role-based update access"
 ON todos
 FOR UPDATE
 USING (
 company_id = (SELECT company_id FROM users WHERE id = auth.uid())
 AND (
 user_id = auth.uid() OR
 (SELECT role FROM users WHERE id = auth.uid()) = 'Admin'
 ) 
 )
 WITH CHECK (
 company_id = (SELECT company_id FROM users WHERE id = auth.uid())
 AND (
 user_id = auth.uid() OR
 (SELECT role FROM users WHERE id = auth.uid()) = 'Admin'
 ) 
 );

CREATE POLICY "Role-based delete access"
ON todos
FOR DELETE
USING (
 company_id = (SELECT company_id FROM users WHERE id = auth.uid())
 AND (
 user_id = auth.uid() OR
 (SELECT role FROM users WHERE id = auth.uid()) = 'Admin'
 ) 
);



## Из документации
Источник: [Tables and Data \| Supabase Docs](https://supabase.com/docs/guides/database/tables?queryGroups=language&language=dart)
### View security[#](https://supabase.com/docs/guides/database/tables?queryGroups=language&language=dart#view-security)

By default, views are accessed with their creator's permission ("security definer"). If a privileged role creates a view, others accessing it will use that role's elevated permissions. To enforce row level security policies, define the view with the "security invoker" modifier.
```dart alter a security_definer view to be security_invoker
alter view <view name>
set (security_invoker = true);

-- create a view with the security_invoker modifier
create view <view name> with(security_invoker=true) as (
  select * from <some table>
);
```