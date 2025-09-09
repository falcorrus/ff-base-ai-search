
от [Sabikrus](https://t.me/flutterflow_rus/24030/52503)

## Описание

> [!NOTE] функция для обновления локации у пользователя если он в приложении 
>  в main нужно загрузить ( но в функции мои названия коллекций) нужно поменять на ваши

Q: Класс, а сколько стоит такой стрим в firebase? Все пугают, а интересно получить реальные данные.
A: 2 миллиона бесплатно, это подписка на изменения каждые 500 метров если проехал курьер 5 км это 10 запросов для отправки данных. И так же 10 запросов на получение если клиент смотрит локацию. Если не смотрит 0 )
## Как выглядит
![[photo_2025-04-01_16-37-05.jpg]]

## Код
```dart
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:geolocator/geolocator.dart';
import 'package:firebase_auth/firebase_auth.dart' as auth;

Future startLocationUpdates() async {
  // Проверяем, включена ли опция отслеживания
  if (!FFAppState().PositionUser.courier) return;

  // Проверяем разрешения на геолокацию
  LocationPermission permission = await Geolocator.checkPermission();
  if (permission == LocationPermission.denied) {
    permission = await Geolocator.requestPermission();
    if (permission == LocationPermission.denied 
        permission == LocationPermission.deniedForever) {
      return; // Разрешение не выдано
    }
  }

  auth.User? user = auth.FirebaseAuth.instance.currentUser;
  if (user == null) return;

  DocumentReference? companyRef = FFAppState().User.company;
  if (companyRef == null) return;
  String companyId = companyRef.id;
  // Определяем ссылку на подколлекцию курьеров
  CollectionReference couriersRef = FirebaseFirestore.instance
      .collection('companies')
      .doc(companyId)
      .collection('couriers');

  // Ищем документ курьера по idUser
  QuerySnapshot querySnapshot =
      await couriersRef.where('idUser', isEqualTo: user.uid).limit(1).get();

  DocumentReference courierDoc;
  if (querySnapshot.docs.isNotEmpty) {
    // Если документ найден, используем его
    courierDoc = querySnapshot.docs.first.reference;
  } else {
    // Если документ не найден, создаем новый
    courierDoc = couriersRef.doc();
    await courierDoc.set({
      'idUser': user.uid,
      'latitude': null,
      'longitude': null,
      'timestamp': FieldValue.serverTimestamp(),
    });
  }

  // Запускаем поток обновления местоположения
  Geolocator.getPositionStream(
    locationSettings: const LocationSettings(
      accuracy: LocationAccuracy.best,
      distanceFilter: 500, // Обновление только при изменении на 500 м
    ),
  ).listen((Position position) {
    List<double> newLocation = [position.latitude, position.longitude];

    // Проверяем, изменилась ли локация по сравнению с последней сохраненной
    if (FFAppState().lastLocation.isEmpty 
        (FFAppState().lastLocation[0] - newLocation[0]).abs() > 0.0001 ||
        (FFAppState().lastLocation[1] - newLocation[1]).abs() > 0.0001) {
      // Обновляем Firestore
      courierDoc.set({
        'latitude': position.latitude,
        'longitude': position.longitude,
        'timestamp': FieldValue.serverTimestamp(),
      }, SetOptions(merge: true));

      // Обновляем локальное состояние
      FFAppState().lastLocation = newLocation;
    }
  });
}
```

## Предложение по улучшению
[Источник](https://t.me/flutterflow_rus/12427/52516)
```
FFAppState().lastLocation[0] !=newLocation[0])||
        (FFAppState().lastLocation[1] 0!newLocation[1])
```   
Так будет проще