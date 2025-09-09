---
dg-publish: true
---
## Подборка видео
https://m.youtube.com/watch?v=ML6MpNVmoBQ&feature=emb_logo
https://www.youtube.com/watch?v=V1D0MfFQlSo&t=3s (Jorge)
https://community.flutterflow.io/c/community-tutorials/how-to-create-a-simple-shopping-cart
https://www.youtube.com/watch?v=vhbaTpkG8bg (c 15:43)? много полезного кода для функций


## Решение от  [Telegram: Contact @flutterflow\_rus](https://t.me/flutterflow_rus/24030/49702)
Custom action для переноса всех данных с корзины "cart" в заказы "orders"(supabase).
Cправа в колонке "arguments" включаем return value. Type: bool; is list, nullable оставляем пустыми. 
В define arguments; arguments 1 пишем в name: orderid; в type: integer; is list, nullable оставляем пустыми. 
Очень быстро нежели циклом loop.
```
Future<bool> moveCartToOrders(int orderId) async {
  try {
    final supabaseClient = SupaFlow.client; //  Подключение к Supabase
    final userId = supabaseClient.auth.currentUser?.id;
    if (userId == null) {
      print(" Ошибка: Пользователь не авторизован.");
      return false;
    }
    print(" Функция moveCartToOrders вызвана!");
    print(" orderId, который передаём: $orderId");
    // 1️ Загружаем все товары из cart_items пользователя
    final response =
        await supabaseClient.from('cart_items').select().eq('user_id', userId);
    if (response.isEmpty) {
      print(" Корзина пуста, нечего переносить.");
      return false;
    }
    print(" Товары в корзине перед переносом: $response");
    // 2️ Формируем данные для order_items
    final orderItems = response
        .map((item) => {
              'order_id': orderId, //  Передаём правильный order_id
              'user_id': userId,
              'product_id': item['product_id'],
              'price': item['price'], //  Цена товара
            })
        .toList();

    print(" Данные для вставки в order_items: $orderItems");

    // 3️ Вставляем данные в order_items
    await supabaseClient.from('order_items').insert(orderItems);

    print(" Товары успешно перенесены в order_items!");

    // 4️ Считаем сумму заказа (сумма всех price)
    final totalPriceResponse = await supabaseClient
        .from('order_items')
        .select('price')
        .eq('order_id', orderId);

    // Считаем сумму
    double totalSum = totalPriceResponse.fold(
        0, (prev, item) => prev + (item['price'] as num));

    print(" Общая сумма заказа: $totalSum");

    // 5️ Обновляем summ_price в orders
    await supabaseClient
        .from('orders')
        .update({'summ_price': totalSum}).eq('id', orderId);

    print("summ_price обновлён в orders!");

    // 6️ Удаляем товары из cart_items
    await supabaseClient.from('cart_items').delete().eq('user_id', userId);

    print("Корзина очищена!");

    return true;
  } catch (error) {
    print(" Ошибка при переносе данных: $error");
    return false;
  }
}
```