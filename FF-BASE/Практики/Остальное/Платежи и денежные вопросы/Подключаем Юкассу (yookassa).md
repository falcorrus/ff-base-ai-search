---
dg-publish: true
---
НЕДОПИСАНО
## Вариант1 от @Brozaurus

[[../webhook cloud function|Код для облачной функции для получения webhook]]

### API для инициации платежа
> [!INFO] Если работает в тесте, но не работает в web, то сделайте Deploy private API

```json
{
  "amount": {
    "value": "<amount>",
    "currency": "RUB"
  },
  "payment_method_data": {
    "type": "yoo_money"
  },
  "confirmation": {
    "type": "redirect",
    "return_url": "https://pamiatka.flutterflow.app/paymentStatus"
  },
  "capture": true,
  "description": "Заказ <Idempotence-Key> от <userEmail>"
}
```
## Подключить Юкассу к FF (Общее)
Вот гайд для юкассы от Игната  (https://www.youtube.com/watch?v=a4hUsxS1RqQ)
вот еще: [Добавляем онлайн оплату в интернет магазин. Платежная система на сайт для разработчиков по API - YouTube](https://www.youtube.com/watch?v=jNWq7pPLGcA)

### Быстрый старт

API ЮKassa позволяет принимать платежи онлайн — в вебе и на мобильных устройствах. Эта статья поможет вам принять первый платеж, при этом вашим покупателям будут доступны все способы оплаты, которые вы подключили.
[Документация Юкассы](https://yookassa.ru/developers/payment-acceptance/getting-started/quick-start)

> [!TIP] Нужна помощь с подключением? 
> @brozaurus
> @z3rus (Philippe)

## Документация по тестовый режим Юкассы
https://yookassa.ru/developers/payment-acceptance/testing-and-going-live/testing
https://yookassa.ru/developers/payment-acceptance/getting-started/quick-start


### подробности с сайта ЮКасса

**Ссылка для оплаты выглядит примерно так:**
https://yoomoney.ru/payments/external/confirmation?orderId=2fc6f003-000f-5000-b000-1cd01469b710

**Тестовая карта:**
5555555555554444, дата любая из будущего

const authorization = "Basic MTA5NDg3ODp0ZXN0X0F1aGd3cHRFTVU3SFlVNTNzclNpXzVhSFRQcEhsOENXNnBYZmJLbnRQbGs="; // Ваш Authorization token

## Вариант2 от Игната

Видео: https://www.youtube.com/watch?v=a4hUsxS1RqQ 


Зашифровываем ключ в base64 (используется для авторизации в тест.режиме Yoo):
https://onlinestringtools.com/convert-string-to-base64
### Облачная функция из видео Игната:
!Сотрите 2 верхние строки, они уже есть (но проверьте!)
```js
const functions = require("firebase-functions");
const admin = require('firebase-admin');
const { v4: uuidv4 } = require('uuid');
const axios = require('axios');
admin.initializeApp();

const authorization = "Basic ВАШ ТОКЕН";
const initial_payment_msg = "Списываем оплату за заказ";
const my_url = "https://www.instagram.com/sprestay/";

exports.initialPayment = functions.https.onRequest(async (request, response) => {
    try {
        const url = "https://api.yookassa.ru/v3/payments";

        // получаем заказ из БД и цену заказа
        var order_id = request.body.order_id;
        const orders = admin.firestore().collection('orders');
        var order_snapshot = await orders.doc(order_id).get();
        var order = order_snapshot.data();
        var price = order['price'];

        // параметры для запроса
        var headers = {
            "Authorization": authorization,
            "Idempotence-Key": uuidv4().toString(),
            "Content-Type": 'application/json'
        };
        var params = {
            "amount": {
                "value": price.toString(),
                "currency": "RUB"
            },
            "payment_method_data": {
                "type": "bank_card"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": my_url
            },
            "description": initial_payment_msg,
            "save_payment_method": "false"
        };

        // запрос к юкассе
        axios.post(url, params, {
            headers: headers,
        }).then((res) => {
            return res.data;
        })
            .then(async (res) => {
                if (res.status == "pending") {
                    await orders.doc(order_id).update({"payment_id": res.payment_method.id});
                    response.send({
                        "url": res.confirmation.confirmation_url, 
                    });
                }
            })
            .catch((err) => {
                functions.logger.log("ERROR", err);
                response.send({
                    "status": "error",
                    "body": err,
                });
            });
    } catch (e) {
        functions.logger.log("ERROR");
        functions.logger.log(e.message);
        response.send({
            "status": "error",
            "body": e.message
        });
    }
});


exports.UkassaWebHook = functions.https.onRequest(async (request, response) => {
    if (request.body.event == "payment.waiting_for_capture") {
        let payment_id = request.body.object.id;
        let status = request.body.object.status;
        if (status == "waiting_for_capture") {
            // сюда попадаем, если клиент оплатил
            await confirmPayment(payment_id);
            await getPayment(payment_id);
        }
    }
    response.send("OK");
});




const confirmPayment = async (payment_id) => {
    await admin.firestore().collection('orders').where("payment_id", "==", payment_id)
    .limit(1)
    .get()
    .then(snapshot => {
        if (snapshot.size > 0) {
            const firstDoc = snapshot.docs[0].ref;
            firstDoc.update({paid: true}).then(() => {
                console.log('Документ успешно обновлен');
              })
              .catch(err => {
                console.log('Ошибка обновления документа', err);
              });
          } else {
            console.log("документы не найдены");
          }
    })
    .catch(err => {
        console.log('Ошибка получения документа', err);
        return null
    });
}

const getPayment = async (payment_id) => {
    const url = `https://api.yookassa.ru/v3/payments/${payment_id}/capture`;

    var headers = {
        "Authorization": authorization,
        "Idempotence-Key": uuidv4().toString(),
        "Content-Type": 'application/json'
    };

    return await axios.post(url, {}, {
        headers: headers,
    }).then((res) => res.data).then(async (res) => {
        functions.logger.log("Платеж успешно подтвержден", res);
        return true;
    }).catch((err) => {
        functions.logger.log("Ошибка при подтверждении платежа", err);
        return false;
    });
}

const cancelPayemnt = async (payment_id) => {
    const url = `https://api.yookassa.ru/v3/payments/${payment_id}/cancel`;

    var headers = {
        "Authorization": authorization,
        "Idempotence-Key": uuidv4().toString(),
        "Content-Type": 'application/json'
    };

    return await axios.post(url, {}, {
        headers: headers,
    }).then((res) => res.data).then(async (res) => {
        functions.logger.log("Платеж успешно отменен", res);
        return true;
    }).catch((err) => {
        functions.logger.log("Ошибка при отмене платежа", err);
        return false;
    });
}

exports.getPaymentApi = functions.https.onRequest(async (request, response) => {
    var payment_id = request.body.payment_id;
    await getPayment(payment_id);
    response.status(200);
});

exports.cancelPaymentApi = functions.https.onRequest(async (request, response) => {
    var payment_id = request.body.payment_id;
    await cancelPayemnt(payment_id);
    response.status(200);
})
```