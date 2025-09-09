от [Telegram: View @flutterflow\_rus](https://t.me/flutterflow_rus/24030/54957)

На вход надо дать:
	  DateTime date - например текущую дату
	  String name - любой string
На выходе получаем String
```dart
String newCustomID(
  DateTime date,
  String name,
) {
  /// MODIFY CODE ONLY BELOW THIS LINE
/// Кастом для формирования уникального ID
  String year = date.year.toString().substring(2, 4); // последние 2 цифры года
  String month =
      date.month.toString().padLeft(2, '0'); // месяц в формате "01", "02"
  String day = date.day.toString().padLeft(2, '0'); // день в формате "01", "02"
  String hours = date.hour.toString().padLeft(2, '0'); // часы
  String minutes = date.minute.toString().padLeft(2, '0'); // минуты
  String milliseconds =
      date.millisecond.toString().padLeft(3, '0'); // миллисекунды

  // Убираем все неалфавитные символы из имени
  String nameLetters = name.replaceAll(RegExp(r'[^A-Za-z]'), '');

  // Берем первые 3 буквы имени, если меньше - заполняем 'X'
  String namePart = (nameLetters.length >= 3
          ? nameLetters.substring(0, 3)
          : nameLetters.padRight(3, 'X'))
      .toUpperCase();

  // Склеиваем части: год + месяц + день + миллисекунды + имя
  String customID = '$year$month$day$milliseconds$namePart';

  // Ограничиваем длину до 16 символов, если ID длиннее
  return customID.length > 16 ? customID.substring(0, 16) : customID;

  /// MODIFY CODE ONLY ABOVE THIS LINE
}
	```
