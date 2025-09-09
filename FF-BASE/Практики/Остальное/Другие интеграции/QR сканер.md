от [Sabikrus](https://t.me/flutterflow_rus/24030/52503)

> [!NOTE]
> Сканер который работает в веб (я интегрировал только для веб этот) а для мобилки тот который в FF

пакет qrcode_scanner_dialog: ^1.0.0
```
import 'dart:async';
import 'package:qrcode_scanner_dialog/qr_bar_code_scanner_dialog.dart';

final QrBarCodeScannerDialog _scanner = QrBarCodeScannerDialog();

Future<String?> scanBarcodeAndReturn(
  BuildContext context,
  String? title,
) async {
  try {
    Completer<String?> completer = Completer<String?>();

    _scanner.getScannedQrBarCode(
      context: context,
      cameraFacing: CameraFacing.back,
      onCode: (rawCode) {
        if (rawCode != null && rawCode.trim().isNotEmpty) {
          // Удаляем префикс "Code scanned = " если он есть
          final cleaned =
              rawCode.replaceFirst(RegExp(r'^Code scanned =\s*'), '').trim();
          completer.complete(cleaned);
        } else {
          completer.complete(null);
        }
      },
    );

    return completer.future;
  } catch (e) {
    debugPrint('❌ Ошибка при сканировании: $e');
    return null;
  }
}
```
