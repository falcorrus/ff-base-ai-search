---
tags:
  - supabase
---

от @flutterzer0
Источник: https://t.me/flutterflow_rus/12429/55697
Видео: https://www.youtube.com/watch?v=pQ1eJn0LGF8

## Код 1 (custom action!)
![[../temp/code_custom1.jpg]]
```dart
// Automatic FlutterFlow imports
import '/backend/supabase/supabase.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/custom_code/actions/index.dart'; // Imports other custom actions
import '/flutter_flow/custom_functions.dart'; // Imports custom functions
import 'package:flutter/material.dart'; // Imports flutter material

// Begin custom action code
// DO NOT REMOVE OR MODIFY THE CODE ABOVE!

import 'package:supabase_flutter/supabase_flutter.dart';

Future getPhoneOtp(String phone) async {
  // Add your function code here!

  // Get a reference your Supabase client
  final supabase = Supabase.instance.client;

  await supabase.auth.signInWithOtp(
    phone: phone,
    shouldCreateUser: true,
  );
}

// Set your action name, define your arguments and return parameter,
// and then add the boilerplate code using the green button on the right!
```


## Код 2 (custom action!)

![[../temp/code_2.png]]

```dart
// Automatic FlutterFlow imports
import '/backend/supabase/supabase.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/custom_code/actions/index.dart'; // Imports other custom actions
import '/flutter_flow/custom_functions.dart'; // Imports custom functions
import 'package:flutter/material.dart';

// Begin custom action code
// DO NOT REMOVE OR MODIFY THE CODE ABOVE!

import 'package:supabase_flutter/supabase_flutter.dart';

Future<bool> verifyPhoneOtp(
  String phone,
  String? token,
) async {
  // Instantiate Supabase client
  final supabase = Supabase.instance.client;

  try {
    // Call the supabase verifyOTP function for phone authentication
    // If successful, a response with the user and session is returned
    final AuthResponse res = await supabase.auth.verifyOTP(
      type: OtpType.sms,
      token: token ?? "",
      phone: phone,
    );

    // Return true if session is not null (i.e., user is authenticated)
    return res.session != null;
  } on AuthException catch (e) {
    // Catch any authentication errors and print the message
    print('Auth exception: ${e.message}');
    return false;
  } catch (error) {
    // Catch any other errors
    print('Unexpected error: $error');
    return false;
  }
}

// Set your action name, define your arguments and return parameter,
// and then add the boilerplate code using the green button on the right!
```