---
dg-publish: 
tags:
  - telegram
origin: telegram
author: "Денис"
---

Дата:  2025-07-06
От: [Денис](https://t.me/Denis51111)**

## **Custom Reorderable ListView с виброткликами при долгом нажатии, в процессе перемещения и в конце перемещения.** 

**Параметры:**

1. items (Data Type List)** -** в моем случае это упражнения

2. OnReorder (Action c двумя параметрами : int oldIndex, int newIndex) - custom action "OnReorder", см. ниже

3.**** itemBuilder (Widget Builder с параметром exercise (Data Type)) - кастомизируете элемент списка так, как вам нужно. Вместо exercise указываете ваши данные.

Для понимания как работает custom action "OnReorder": https://www.youtube.com/watch?v=2Hm6jtU3504

## Код1
![[../temp/OnReorder.txt]]
```dart
// Automatic FlutterFlow imports
import '/backend/backend.dart';
import '/backend/schema/structs/index.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/custom_code/actions/index.dart'; // Imports other custom actions
import '/flutter_flow/custom_functions.dart'; // Imports custom functions
import 'package:flutter/material.dart';
// Begin custom action code
// DO NOT REMOVE OR MODIFY THE CODE ABOVE!

import 'package:flutter/services.dart';

Future<List<ExerciseStruct>> onReorder(
  int? oldIndex,
  int? newIndex,
  List<ExerciseStruct>? exercises,
) async {
  if (oldIndex == null || newIndex == null || exercises == null) {
    return exercises ?? [];
  }
  // Логика переупорядочивания
  if (oldIndex < newIndex) {
    newIndex -= 1;
  }
  final item = exercises.removeAt(oldIndex);
  exercises.insert(newIndex, item);

  return exercises;
}

```

## код2
![[../temp/VibratingReorderableListView.txt]]
```dart
// Automatic FlutterFlow imports
import '/backend/backend.dart';
import '/backend/schema/structs/index.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/custom_code/widgets/index.dart'; // Imports other custom widgets
import '/custom_code/actions/index.dart'; // Imports custom actions
import '/flutter_flow/custom_functions.dart'; // Imports custom functions
import 'package:flutter/material.dart';
// Begin custom widget code
// DO NOT REMOVE OR MODIFY THE CODE ABOVE!

import 'package:flutter/services.dart';
import 'package:flutter/gestures.dart';

class VibratingReorderableListView extends StatefulWidget {
  const VibratingReorderableListView({
    super.key,
    this.width,
    this.height,
    required this.items,
    required this.onReorder,
    required this.itemBuilder,
  });
  final double? width;
  final double? height;
  final List<ExerciseStruct> items;
  final Future Function(int oldIndex, int newIndex) onReorder;
  final Widget Function(ExerciseStruct exercise) itemBuilder;

  @override
  State<VibratingReorderableListView> createState() =>
      _VibratingReorderableListViewState();
}

class _VibratingReorderableListViewState
    extends State<VibratingReorderableListView> {
  // Для вибрации во время перетаскивания
  bool _isDragging = false;
  Offset? _lastPosition;
  final double _dragThreshold =
      35.0; // Увеличиваем порог для срабатывания вибрации
  int _draggedItemIndex = -1;
  GlobalKey _listKey = GlobalKey();
  Rect? _listBounds;

  @override
  void initState() {
    super.initState();
    // Запускаем обработчик событий после построения виджета
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _addPointerListener();
      _calculateListBounds();
    });
  }

  void _calculateListBounds() {
    // Получаем размеры виджета списка для ограничения области вибрации
    if (_listKey.currentContext != null) {
      final RenderBox renderBox =
          _listKey.currentContext!.findRenderObject() as RenderBox;
      final Offset position = renderBox.localToGlobal(Offset.zero);
      _listBounds = Rect.fromLTWH(position.dx, position.dy,
          renderBox.size.width, renderBox.size.height);
    }
  }

  void _addPointerListener() {
    // Добавляем глобальный обработчик перемещений указателя
    GestureBinding.instance.pointerRouter.addGlobalRoute(_handlePointerEvent);
  }

  void _handlePointerEvent(PointerEvent event) {
    // Только если идет перетаскивание
    if (!_isDragging) return;

    if (event is PointerMoveEvent) {
      // Проверяем, находится ли указатель в пределах списка
      if (_listBounds != null && !_listBounds!.contains(event.position)) {
        // Если указатель вышел за пределы списка, не выполняем вибрацию
        return;
      }

      // Если это первое событие движения
      if (_lastPosition == null) {
        _lastPosition = event.position;
        return;
      }

      // Вычисляем расстояние, на которое переместился указатель
      final double distance = (_lastPosition! - event.position).distance;

      // Если перемещение достаточно большое, добавляем вибрацию
      if (distance > _dragThreshold) {
        // Используем более легкую вибрацию
        HapticFeedback.selectionClick();
        _lastPosition = event.position; // Обновляем позицию
      }
    }
  }

  void _handleReorder(int oldIndex, int newIndex) async {
    // Вибрация при завершении перетаскивания
    HapticFeedback.mediumImpact();

    // Сбрасываем состояние перетаскивания
    _isDragging = false;
    _lastPosition = null;

    // Вызываем переданный колбэк
    await widget.onReorder(oldIndex, newIndex);
  }

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;

    // Перерасчет границ списка при каждом построении
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _calculateListBounds();
    });

    return SizedBox(
      width: screenWidth,
      key: _listKey,
      child: ReorderableListView(
        shrinkWrap: true,
        physics:
            NeverScrollableScrollPhysics(), // Убирает скролл, если список внутри ScrollView
        onReorderStart: (index) {
          // Активируем вибрацию при начале перетаскивания
          HapticFeedback.heavyImpact();

          // Устанавливаем флаг перетаскивания и сбрасываем позицию
          _isDragging = true;
          _lastPosition = null;
          _draggedItemIndex = index;

          // Рассчитываем границы списка при начале перетаскивания
          _calculateListBounds();
        },
        buildDefaultDragHandles: true,
        onReorder: _handleReorder,

        /// Кастомизация внешнего вида перетаскиваемого элемента
        proxyDecorator: (child, index, animation) {
          return Material(
            elevation: 6,
            borderRadius: BorderRadius.circular(10),
            clipBehavior: Clip.antiAlias,
            child: child,
          );
        },
        children: List.generate(widget.items.length, (index) {
          final exercise = widget.items[index];
          return KeyedSubtree(
            key: ValueKey(exercise.exerciseRef?.id ?? index),
            child: widget.itemBuilder(exercise),
          );
        }),
      ),
    );
  }

  @override
  void dispose() {
    GestureBinding.instance.pointerRouter
        .removeGlobalRoute(_handlePointerEvent);
    super.dispose();
  }
}
```