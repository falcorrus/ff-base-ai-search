---
sharenote_link: https://share.note.sx/cl71zk9n#qX4aGxjxgLUGCsO/7GsfCFP+lTfxSfWUOjUW1BMtmiw
sharenote_updated: 2025-06-15T14:19:03-03:00
---
# Облачная функция для Firebase

> [!NOTE] Часть инструкции по yooKassa: [Подключаем Юкассу (yookassa)](Платежи%20и%20денежные%20вопросы/Подключаем%20Юкассу%20(yookassa).md)
> Не факт, что работает..

## Для чего:
При получении уведомления от yooKassa ищет в коллекции ***payments*** запись с таким же ***id платежа*** и ***суммой платежа*** и обновляет в ней статус на актуальный

## Код функции "webhook"

> [!INFO] Параметров нет

```js
// 1. Импортируем Firebase Functions SDK и Firestore
const functions = require('firebase-functions');
const admin = require('firebase-admin');

// Инициализируем Firebase Admin SDK (если еще не инициализирован)
if (!admin.apps.length) {
    admin.initializeApp();
}

const db = admin.firestore();

// Валидация входных параметров (Остается без изменений, она универсальна)
function validateWebhookPayload(body) {
    const errors = [];
    
    if (!body || typeof body !== 'object') {
        errors.push('Тело запроса отсутствует или имеет неверный формат.');
        return errors;
    }

    if (!body.type) {
        errors.push('Отсутствует поле "type"');
    } else if (body.type !== 'notification') {
        errors.push('Неверное значение поля "type", ожидается "notification"');
    }
    
    if (!body.event) {
        errors.push('Отсутствует поле "event"');
    }
    
    if (!body.object) {
        errors.push('Отсутствует поле "object"');
        // Возвращаем ошибки, если нет объекта, т.к. дальнейшие проверки бессмысленны без него
        return errors; 
    }
    
    const paymentObject = body.object;
    
    if (!paymentObject.id) {
        errors.push('Отсутствует поле "object.id"');
    }
    
    // Добавлена проверка на status, т.к. вы его теперь явно используете
    if (!paymentObject.status) {
        errors.push('Отсутствует поле "object.status"');
    }

    // Проверка amount только для payment.succeeded, как в вашей первоначальной логике
    if (body.event === 'payment.succeeded') {
        if (!paymentObject.amount) {
            errors.push('Отсутствует поле "object.amount" для payment.succeeded');
        } else {
            if (typeof paymentObject.amount.value === 'undefined') { // Проверяем на undefined, а не на falsy
                errors.push('Отсутствует поле "object.amount.value" для payment.succeeded');
            }
            if (!paymentObject.amount.currency) {
                errors.push('Отсутствует поле "object.amount.currency" для payment.succeeded');
            }
        }
    }
    
    return errors;
}

exports.webhook = functions.https.onRequest(async (req, res) => {
    // Устанавливаем Content-Type для всех ответов
    res.set('Content-Type', 'application/json');

    try {
        // Для Firebase Cloud Functions (HTTP-триггер) тело запроса находится в req.body.
        // Firebase автоматически парсит JSON, если Content-Type
```

