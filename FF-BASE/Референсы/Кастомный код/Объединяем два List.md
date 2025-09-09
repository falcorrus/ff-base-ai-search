
Решение от https://t.me/paritel99

На вход даём 2 List Strings. На выходе 1 List String.
```dart
List<String>? sumlistitems(
  List<String>? list1,
  List<String>? list,
) {
  /// MODIFY CODE ONLY BELOW THIS LINE

  // Combine 2 lists of pictures
// combine two lists of pictures
  if (list1 == null || list == null) {
    return null;
  }
  final combinedList = [...list1, ...list];
  return combinedList;

  /// MODIFY CODE ONLY ABOVE THIS LINE
}
```

