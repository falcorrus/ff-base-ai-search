от [Memet](https://t.me/arpadzhy)

ссылка проекта 
https://app.flutterflow.io/project/test2-tv5n2n?tab=widgetTree&component=timeliner
расположен на странице page2
![[../temp/image_timeline.jpg]]

## custom action для получения высоты компонента 

`// Automatic FlutterFlow imports`
`import '/flutter_flow/flutter_flow_theme.dart';`
`import '/flutter_flow/flutter_flow_util.dart';`
`import '/custom_code/actions/index.dart'; // Imports other custom actions`
`import '/flutter_flow/custom_functions.dart'; // Imports custom functions`
`import 'package:flutter/material.dart';`
`// Begin custom action code`
`// DO NOT REMOVE OR MODIFY THE CODE ABOVE!`

`import 'dart:async';`
`import 'package:flutter/widgets.dart'; // Для WidgetsBinding`
`import 'package:flutter/rendering.dart'; // Для RenderObject и RenderBox`

`Future<double> getHeight(BuildContext context) async {`
  `Completer<double> completer = Completer<double>();`

  `// Первый обратный вызов после первого кадра`
  `WidgetsBinding.instance.addPostFrameCallback((_) {`
    `// Второй обратный вызов после второго кадра`
    `WidgetsBinding.instance.addPostFrameCallback((_) {`
      `final RenderObject? renderObject = context.findRenderObject();`
      `if (renderObject is RenderBox) {`
        `double height = renderObject.size.height;`
        `completer.complete(height);`
        `print("Высота виджета: $height"); // Выводим высоту в консоль`
      `} else {`
        `completer.complete(0.0); // Возвращаем 0.0, если RenderBox не найден`
        `print(`
            `"RenderBox не найден. Возвращается высота: 0.0"); // Выводим сообщение в консоль`
      `}`
    `});`
  `});`

  `return completer.future;`
`}`



### Важно
> [!NOTE] Важно
> поставить галочку include BuildContext и добавить Boilerplate code, тогда в функцию будет включен параметр BuildContext context. 
> 
> Так как экшен стоит при инициализации компонента, то стоит задать дефолтную высоту для timeline иначе получите ошибку null, после отрисовки компоненты примут высоту самого виджета