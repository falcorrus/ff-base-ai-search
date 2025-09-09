Подробная инструкция в документации
[FFAppState \| FlutterFlow Documentation](https://docs.flutterflow.io/generated-code/ff-app-state/)




# FFAppState
Русский перевод

Предпосылки

В этом руководстве используется пример сгенерированного кода **[демонстрационного приложения EcommerceFlow](https://bit.ly/ff-docs-demo-v1)** . Чтобы просмотреть сгенерированный код напрямую, посетите **[репозиторий Github](https://github.com/FlutterFlow/sample-apps/tree/main/ecommerce_flow)** .

Класс `FFAppState`в FlutterFlow действует как центральный узел для управления глобальным состоянием приложения. Он разработан как синглтон, что означает, что существует только один экземпляр этого класса на протяжении всего жизненного цикла приложения. Этот класс расширяет [**ChangeNotifier**](https://api.flutter.dev/flutter/foundation/ChangeNotifier-class.html) , позволяя виджетам прослушивать и реагировать на изменения состояния.

Он включает в себя методы инициализации и обновления постоянного состояния приложения, а также определяет различные переменные состояния с соответствующими **геттерами и сеттерами** для манипулирования этими значениями.

Вот базовый шаблон класса, взятый из сгенерированного кода [**демонстрационного приложения eCommerceFlow**](https://bit.ly/ff-docs-demo-v1) :

```
class FFAppState extends ChangeNotifier {  static FFAppState _instance = FFAppState._internal();  factory FFAppState() {    return _instance;  }  FFAppState._internal();  static void reset() {    _instance = FFAppState._internal();  }  void update(VoidCallback callback) {    callback();    notifyListeners();  }   // App State variable of primitive type with a getter and setter    bool _enableDarkMode = false;    bool get enableDarkMode => _enableDarkMode;    set enableDarkMode(bool value) {    _enableDarkMode = value;   }}
```

Это `_enableDarkMode`переменная состояния приложения, созданная разработчиком, которая создает свои собственные соответствующие геттер и сеттер.

### Пересоздать при обновлении [AppState](https://docs.flutterflow.io/generated-code/ff-app-state#rebuild-on-updating-appstate "Прямая ссылка на Rebuild при обновлении AppState")

При обновлении `AppState`переменной из редактора потока действий вам будет представлено несколько вариантов **[типа обновления](https://docs.flutterflow.io/resources/data-representation/app-state#update-type)** , таких как **Rebuild All Pages** , **Rebuild Current Page** и **No Rebuild** в настройках действия. Давайте посмотрим, как изменится сгенерированный код при выборе этих параметров.

#### Перестроить текущую [страницу](https://docs.flutterflow.io/generated-code/ff-app-state#rebuild-current-page "Прямая ссылка на перестройку текущей страницы")

Когда разработчик выбирает обновление App State с типом обновления **Rebuild Current Page**`setter` , вызывается соответствующий . Сразу после этого `setState((){});`вызывается , который обновляет только текущую страницу.

Вот пример сгенерированного кода, когда мы обновляем состояние приложения `enableDarkMode`в `onInitialization`триггере действия `ProductListPage`.

```
SchedulerBinding.instance.addPostFrameCallback((_) async {  FFAppState().enableDarkMode = !(FFAppState().enableDarkMode ?? true);  setState(() {});});
```

#### Перестроить все [страницы](https://docs.flutterflow.io/generated-code/ff-app-state#rebuild-all-pages "Прямая ссылка на перестройку всех страниц")

В этом случае тип обновления установлен на **Rebuild All Pages** , что означает, что `setter`вызывается , за которым следует `update()`метод . Этот метод внутренне вызывает `notifyListeners()`, что имеет решающее значение для обновления любых виджетов, зависящих от этой переменной.

```
SchedulerBinding.instance.addPostFrameCallback((_) async {  FFAppState().enableDarkMode = !(FFAppState().enableDarkMode ?? true);  FFAppState().update(() {});});
```

Обновление состояния приложения из пользовательского кода

При обновлении переменных App State из пользовательского кода, например, Custom Actions, крайне важно вызвать функцию обновления, чтобы гарантировать, что изменения будут отражены на всех страницах. Например, следует использовать:

```
FFAppState().update(() => FFAppState().enableDarkMode = !(FFAppState().enableDarkMode ?? true));
```

#### Нет [перестройки](https://docs.flutterflow.io/generated-code/ff-app-state#no-rebuild "Прямая ссылка на No Rebuild")

Вызывается только сеттер без последующего вызова setState или метода update. Это означает, что обновляется только переменная, а состояние не изменяется после обновления данных.

### смотреть FFAppState (https://docs.flutterflow.io/generated-code/ff-app-state#watchffappstate "Прямая ссылка на просмотр FFAppState")

При добавлении действия [**«Обновить состояние приложения»**](https://docs.flutterflow.io/resources/data-representation/app-state#update-app-state-action) с помощью редактора потока действий соответствующие страницы будут включать эту строку в метод сборки:

```
 @overrideWidget build(BuildContext context) {    context.watch<FFAppState>();    ...
```

Используя `context.watch<FFAppState>()`, виджет эффективно подписывается на любые изменения в `FFAppState`классе. Всякий раз, когда происходит изменение объекта `FFAppState`, этот виджет автоматически перестраивается, чтобы отразить эти изменения. Это гарантирует, что ваш виджет всегда отображает самые последние данные и состояние приложения, поддерживая актуальный и отзывчивый пользовательский интерфейс.

### Управление AppState [*List*](https://docs.flutterflow.io/generated-code/ff-app-state#managing-appstatelist "Прямая ссылка на Управление AppState<List>")

Когда вы добавляете переменную App State `List`типа в FlutterFlow, автоматически генерируется несколько служебных функций, которые помогут вам управлять этим списком. Эти функции включают геттер, сеттер и методы для добавления, удаления и обновления элементов в списке. Такая настройка гарантирует, что вы можете легко взаимодействовать со списком, сохраняя при этом состояние приложения согласованным и отзывчивым. Ниже приведено объяснение этих сгенерированных функций с использованием конкретного примера LatLngList.

```
late LoggableList<LatLng> _LatLngList =    LoggableList([LatLng(37.4071594, -122.0775312), LatLng(40.7358633, -73.9910835)]);List<LatLng> get LatLngList => _LatLngList?..logger = () => debugLogAppState(this);set LatLngList(List<LatLng> value) {    if (value != null) {        _LatLngList = LoggableList(value);    }    debugLogAppState(this);}void addToLatLngList(LatLng value) {    LatLngList.add(value);}void removeFromLatLngList(LatLng value) {    LatLngList.remove(value);}void removeAtIndexFromLatLngList(int index) {    LatLngList.removeAt(index);}void updateLatLngListAtIndex(    int index,    LatLng Function(LatLng) updateFn,) {    LatLngList[index] = updateFn(_LatLngList[index]);}void insertAtIndexInLatLngList(int index, LatLng value) {    LatLngList.insert(index, value);}
```

Эти функции генерируются автоматически, чтобы обеспечить удобный и последовательный способ управления переменными состояния приложения в виде списка, что упрощает поддержание состояния приложения:

- Список `LatLngList`инициализируется как частная переменная `_LatLngList`типа `LoggableList`, что помогает управлять списком с помощью дополнительных возможностей ведения журнала.
- Метод get `LatLngList`позволяет другим частям приложения получать доступ к `LatLngList`.
- Метод set `LatLngList`позволяет заменить все `LatLngList`на новое. Когда назначается новый список, он обновляет частную переменную `_LatLngList`и регистрирует это изменение с помощью `debugLogAppState`.
- Функция `addToLatLngList`добавляет новый `LatLng`объект в LatLngList, динамически обновляя список по мере работы приложения.
- Функция `removeFromLatLngList`удаляет определенный `LatLng`объект из списка `LatLngList`, гарантируя, что список останется точным и актуальным.
- Функция `removeAtIndexFromLatLngList`удаляет `LatLng`объект из списка на основе его индексной позиции.
- Функция `updateLatLngListAtIndex`позволяет обновить `LatLng`объект по определенному индексу, применив к нему функцию обновления ( `updateFn`).
- Функция `insertAtIndexInLatLngList`вставляет новый `LatLng`объект в массив `LatLngList`по указанному индексу, при необходимости сдвигая существующие элементы.

Как создать переменные состояния приложения

Чтобы узнать больше о создании и использовании переменных состояния приложения в пользовательском интерфейсе FlutterFlow, ознакомьтесь с руководством [**по состоянию приложения**](https://docs.flutterflow.io/resources/data-representation/app-state) .[](https://docs.flutterflow.io/resources/data-representation/app-state)

Была ли эта статья полезной?