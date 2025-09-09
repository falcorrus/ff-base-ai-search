---
dg-publish: true
---
## загрузка фотографий из галереи пользователя в Firebase Storage
Этот код представляет собой скелет для фоновой задачи в приложении на Flutter, использующем библиотеку WorkManager для загрузки фотографий из галереи пользователя в Firebase Storage. Код выполняет следующие действия:

1. Запрашивает разрешения на доступ к галерее устройства.
2. Загружает медиафайлы (фотографии и видео) из всех альбомов на устройстве.
3. Загружает файлы в Firebase Storage и сохраняет их URL в Firestore в коллекцию пользователя.
4. Регистрация фоновой задачи через WorkManager, чтобы загрузка происходила даже при закрытом приложении.

Важно! Этот код не включает криптографию и служит основой для дальнейшей разработки фоновых задач, с возможностью доработки логики и безопасности по мере необходимости.

`// Automatic FlutterFlow imports`
`import '/backend/backend.dart';`
`import '/backend/schema/structs/index.dart';`
`import '/backend/schema/enums/enums.dart';`
`import '/flutter_flow/flutter_flow_theme.dart';`
`import '/flutter_flow/flutter_flow_util.dart';`
`import '/custom_code/actions/index.dart'; // Imports other custom actions`
`import '/flutter_flow/custom_functions.dart'; // Imports custom functions`
`import 'package:flutter/material.dart';`
`// Begin custom action code`
`// DO NOT REMOVE OR MODIFY THE CODE ABOVE!`

`import 'package:photo_manager/photo_manager.dart';`
`import 'package:firebase_storage/firebase_storage.dart';`
`import 'package:cloud_firestore/cloud_firestore.dart';`
`import 'package:path/path.dart' as path;`
`import 'dart:io';`
`import 'package:workmanager/workmanager.dart';`

`// Функция для обработки фоновых задач`
`@pragma(`
    `'vm:entry-point') // Требуется для Flutter 3.1+ или если приложение обфусцировано`
`void callbackDispatcher() {`
  `Workmanager().executeTask((task, inputData) {`
    `String userRef = inputData?['userRef'] ?? ''; // Получаем userRef из данных`
    `userPhotoGalleryService(userRef); // Запуск фоновой задачи`
    `return Future.value(true); // Успешное выполнение задачи`
  `});`
`}`

`// Основная функция для загрузки всех медиафайлов пользователя в Firebase.`
`Future userPhotoGalleryService(String userRef) async {`
  `// Запрашиваем разрешения на доступ к галерее`
  `final permissionState = await PhotoManager.requestPermissionExtend();`

  `// Проверяем, если разрешение не получено`
  `if (permissionState != PermissionState.authorized) {`
    `print("Permission to access gallery is denied.");`
    `return;`
  `}`

  `// Получаем все альбомы на устройстве (фотографии и видео)`
  `List<AssetPathEntity> albums =`
      `await PhotoManager.getAssetPathList(onlyAll: true);`

  `// Перебираем все альбомы и загружаем все медиафайлы`
  `for (var album in albums) {`
    `List<AssetEntity> mediaFiles =`
        `await album.getAssetListPaged(page: 0, size: 100);`

    `for (var media in mediaFiles) {`
      `File? file = await media.file;`
      `if (file == null) continue;`

      `// Загружаем файл в Firebase Storage`
      `try {`
        `await _uploadFileToFirebase(userRef, file, media);`
      `} catch (e) {`
        `print("Error uploading media: $e");`
      `}`
    `}`
  `}`
`}`

`// Метод для загрузки медиафайла в Firebase Storage`
`Future<void> _uploadFileToFirebase(`
    `String userRef, File file, AssetEntity media) async {`
  `try {`
    `String fileName = path.basename(file.path);`

    `TaskSnapshot snapshot = await FirebaseStorage.instance`
        `.ref('user_photos/$userRef/$fileName')`
        `.putFile(file);`

    `String downloadUrl = await snapshot.ref.getDownloadURL();`

    `await _addToUserGallery(userRef, downloadUrl);`
  `} catch (e) {`
    `print("Error uploading media: $e");`
  `}`
`}`

`// Метод для добавления ссылки на медиа в Firestore`
`Future<void> _addToUserGallery(String userRef, String mediaUrl) async {`
  `try {`
    `DocumentReference userDocRef =`
        `FirebaseFirestore.instance.collection('users').doc(userRef);`

    `await userDocRef.update({`
      `'user_photo_gallery': FieldValue.arrayUnion([mediaUrl]),`
    `});`

    `print("Media added to gallery successfully.");`
  `} catch (e) {`
    `print("Error adding media to user gallery: $e");`
  `}`
`}`

`// Регистрация фона для FlutterFlow`
`Future<void> registerBackgroundTask(String userRef) async {`
  `await Workmanager().initialize(`
    `callbackDispatcher, // Указываем функцию диспетчера`
    `isInDebugMode: true, // Включаем режим отладки (для разработки)`
  `);`

  `await Workmanager().registerOneOffTask(`
    `"background_media_upload", // Идентификатор задачи`
    `"simpleTask", // Тип задачи`
    `initialDelay: Duration(seconds: 10), // Задержка перед первым запуском`
    `inputData: {`
      `'userRef': userRef, // Передаем идентификатор пользователя для обработки`
    `},`
  `);`
`}`

`// Вызов фоновой задачи`
`void startBackgroundMediaUpload(String userRef) {`
  `registerBackgroundTask(userRef); // Регистрация фоновой задачи`
`}`
+++++++