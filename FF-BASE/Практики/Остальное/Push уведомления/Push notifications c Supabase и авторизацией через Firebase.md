Источник: https://knowing-delivery-3b5.notion.site/Supabase-Push-notifications-with-Firebase-Auth-Supabase-Backend-1a585a4da689801482dbea5ae920e498
# Supabase Push notifications with Firebase Auth + Supabase Backend

This guide simplifies notifications in Flutterflow when using Supabase as a backend. This method allows you to use Flutterflow features like push notifications, Firebase authentication and normal Supabase actions.

## STEPS:

1. Create a Firebase project (with Blaze plan)
2. Connect our Firebase project to Flutterflow
3. Add custom code to Flutterflow
4. (do step 6 first if you already have Supabase users) Create cloud function to make JWT compatible
5. Connect Firebase to Supabase

You are now ready to use push notifications!

Existing Supabase projects: 

1. (optional) Create function to create existing Supabase users in Firebase

## 1. Create Firebase project

You can follow the Flutterflow steps for this. Nothing special, we just need a project on Blaze plan.

[https://docs.flutterflow.io/integrations/firebase/connect-to-firebase/](https://docs.flutterflow.io/integrations/firebase/connect-to-firebase/)

## 2. Connect project to Flutterflow

Same as step 1. Follow Flutterflow guides for this. We will not be using Firebase other than for Authentication and push notifications.

[https://docs.flutterflow.io/integrations/firebase/connect-to-firebase/](https://docs.flutterflow.io/integrations/firebase/connect-to-firebase/)

IMPORTANT: Ensure you have followed the steps to give [firebase@flutterflow.io](mailto:firebase@flutterflow.io) the correct permissions AND have enabled authentication, firestore and functions in your Firebase project. The 3 are required for notification setup (as per FF guides).

## 3. Add the following custom code to Flutterflow

### 3.1 Create an action called: updateSupabaseToken

```jsx
// Automatic FlutterFlow imports
import '/backend/backend.dart';
import '/backend/schema/structs/index.dart';
import '/backend/schema/enums/enums.dart';
import '/backend/supabase/supabase.dart';
import '/actions/actions.dart' as action_blocks;
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/custom_code/actions/index.dart'; // Imports other custom actions
import '/flutter_flow/custom_functions.dart'; // Imports custom functions
import 'package:flutter/material.dart';
// Begin custom action code
// DO NOT REMOVE OR MODIFY THE CODE ABOVE!

import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;
import 'package:supabase_flutter/supabase_flutter.dart';
import 'dart:async';

// We'll store the subscription at a global or static level
// so it persists beyond this function call.
StreamSubscription<firebase_auth.User?>? _authWatcher;

Future<void> updateSupabaseToken() async {
  try {
    // 1) If we haven't already set up the listener, do it now.
    if (_authWatcher == null) {
      _authWatcher = firebase_auth.FirebaseAuth.instance
          .userChanges()
          .listen((firebase_auth.User? user) async {
        if (user == null) {
          // User signed out
          // Optionally sign out from Supabase
          await SupaFlow.client.auth.signOut();
          debugPrint('Signed out of Supabase because Firebase user is null.');
        } else {
          // Update the token whenever the user logs in or refreshes
          await _fetchAndSetSupabaseToken(user);
        }
      });
      debugPrint('Auth watcher set up successfully.');
    } else {
      debugPrint('Auth watcher already set up.');
    }

    // 2) If a user is currently signed in, do an immediate token update.
    final user = firebase_auth.FirebaseAuth.instance.currentUser;
    if (user != null) {
      await _fetchAndSetSupabaseToken(user);
    } else {
      // If user == null, optionally sign out from Supabase right now
      // in case you want a truly "no user" state.
      await SupaFlow.client.auth.signOut();
      debugPrint('No user currently signed in; signed out from Supabase.');
    }
  } catch (e, st) {
    debugPrint('Error in updateSupabaseTokenAction: $e $st');
  }
}

// Helper to fetch the Firebase token and update Supabase
Future<void> _fetchAndSetSupabaseToken(firebase_auth.User user) async {
  try {
    // Get the Firebase JWT token directly.
    final firebaseToken = await user.getIdToken();

    // Update the Supabase client to use the Firebase token.
    Supabase.instance.client.headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $firebaseToken',
    };
    SupaFlow.client.rest.setAuth(firebaseToken);

    debugPrint('Supabase token updated successfully for user ${user.uid}.');
  } catch (e, st) {
    debugPrint('Error fetching/setting Supabase token: $e $st');
  }
}
```

### 3.2 Create an action called: forceRefreshToken

```jsx
// Automatic FlutterFlow imports
import '/backend/schema/structs/index.dart';
import '/backend/schema/enums/enums.dart';
import '/backend/supabase/supabase.dart';
import '/actions/actions.dart' as action_blocks;
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/custom_code/actions/index.dart'; // Imports other custom actions
import '/flutter_flow/custom_functions.dart'; // Imports custom functions
import 'package:flutter/material.dart';
// Begin custom action code
// DO NOT REMOVE OR MODIFY THE CODE ABOVE!

import 'package:firebase_auth/firebase_auth.dart';

Future forceRefreshToken() async {
  // Get the current user
  final user = FirebaseAuth.instance.currentUser;
  if (user == null) {
    return;
  }

  try {
    // Check if role is already set
    IdTokenResult tokenResult = await user.getIdTokenResult(false);
    Map<String, dynamic>? claims = tokenResult.claims;

    // If role is not set, force a token refresh
    if (claims == null || claims['role'] != 'authenticated') {
      // First attempt
      await user.getIdToken(true);

      // Wait briefly
      await Future.delayed(Duration(milliseconds: 1000));

      // Retry once more if needed
      final retryResult = await user.getIdTokenResult(false);
      if (retryResult.claims == null ||
          retryResult.claims!['role'] != 'authenticated') {
        // One final refresh attempt
        await user.getIdToken(true);
      }
    }

    // Function returns void, FlutterFlow will handle the refreshed token
    return;
  } catch (e) {
    print('Error in forceRefreshToken: $e');
    return;
  }
}
```

### 3.3 Add the updateSupabaseToken to final actions

In main.dart, add our newly created actions in the final actions.

![image.png](../temp/image.png)

## 4. Create cloud function to handle signups

Create the following cloud function named: processSignUp

This function will modify the JWT for a user when they are created in Firebase. It will also create the new user in a Supabase table named “users”. The ID column of our table will be the Firebase ID.

NOTE: Before saving the function, modify the section where it creates a user in Supabase to match your Supabase columns. In this example, the columns in table $<users>$ in Supabase were $<id>$, $<email>$, $<phone_number>$ and $<display_name>$. Note that in this example, the id is of type text

IMPORTANT: Add  "@supabase/supabase-js":  "^2.49.1" to the cloud function package.json.
![[image 1.png]]

```jsx
const functions = require('firebase-functions');
const admin = require('firebase-admin');
// To avoid deployment errors, do not call admin.initializeApp() in your code

const { getAuth } = require("firebase-admin/auth");
const { createClient } = require("@supabase/supabase-js");

// Logger implementation
const Logger = {
  timestamp: () => new Date().toISOString(),
  formatMessage: (level, message, meta = {}) => {
    return JSON.stringify({
      timestamp: Logger.timestamp(),
      level,
      message,
      ...meta
    });
  },
  info: (message, meta) => {
    console.log(Logger.formatMessage('INFO', message, meta));
  },
  error: (message, error, meta) => {
    console.error(Logger.formatMessage('ERROR', message, {
      ...meta,
      error: error ? {
        message: error.message,
        stack: error.stack,
        name: error.name
      } : undefined
    }));
  },
  debug: (message, meta) => {
    console.log(Logger.formatMessage('DEBUG', message, meta));
  }
};

async function createUserInSupabase(user, supabase) {
  Logger.debug('Creating user in Supabase', { 
    firebaseUid: user.uid 
  });

  try {      
    ///////////////////////////////////////////
    //Modify this to match your Supabase Schema
    const { data: newUser, error: insertError } = await supabase
      .from('users')
      .insert([{
        id: user.uid,
        email: user.email,
        display_name: user.displayName || null,
        phone_number: user.phoneNumber || null,
      }])
      .select()
      .single();

    if (insertError) {   
      throw insertError;
    }

    Logger.info('Successfully created user in Supabase', { 
      userId: newUser.id 
    });
    return newUser.id;

  } catch (error) {
    Logger.error('Failed to create user', error);
    throw error;
  }
}

// Define your function
exports.processSignUp = functions.auth.user().onCreate(async (user) => {
  Logger.debug('Processing new user signup', { 
    uid: user.uid,
    email: user.email 
  });

  try {
    // Set custom user claims
    Logger.debug('Setting custom user claims');
    await getAuth().setCustomUserClaims(user.uid, { role: "authenticated" });

    // Get Supabase config from environment variables
    const supabaseUrl = functions.config().supabase.url;
    const supabaseKey = functions.config().supabase.key;
    const supabase = createClient(supabaseUrl, supabaseKey);
    
    // Ensure user exists in Supabase
    const userId = await createUserInSupabase(user, supabase);
    
    Logger.info('Successfully processed user signup', { 
      userId,
      hasEmail: !!user.email,
      hasPhone: !!user.phoneNumber 
    });

    return { success: true };

  } catch (error) {
    Logger.error('Error in processSignUp', error);
    throw error;
  }
});
```

In order for your code to work with the supabase user creation, you must add some information manually in cloud console. Once your cloud function is deployed, follow the link below:

[https://console.cloud.google.com/functions](https://console.cloud.google.com/functions/list?inv=1&invt=Abqi1A&project=gympal-workout)

Make sure the correct project is selected (top left). Select your cloud function. Click on “Source” then select the .runtimeconfig.json file. Click “edit”.

Add the following with your service role key and your project url:

```jsx
"supabase": {
    "key": "",
    "url": ""
  }
```

## 5. Connect Firebase to Supabase

5.1 Go here:

https://supabase.com/dashboard/project/_/settings/auth

5.2 Select “Third party authentication

5.3 Add Firebase and connect


ALL DONE!

At this point you can use Supabase normally in your project. Supabase will verify your JWT tokens for validity. In order to enforce RLS policies, instead of using auth.uid() in your policies to get the user ID, you will need to use:

```jsx
auth.jwt() ->> 'sub'
```

This will give you the Firebase user ID.

## 6. Creating existing Supabase users in Firebase

If you already have an active Supabase project with users, you should create them in Firebase before completing step 4 (because creating them after would trigger our cloud function, which would try to create a row in Supabase).

1. In order to take all Supabase users and create them in Firebase, we can use [[Buildship]]. First, define 3 secrets:

SUPABASE_URL

SUPABASE_SERVICE_ROLE

FIREBASE_JSON

To get Firebase JSON, go to your firebase project. Click on Settings → Service Accounts → Generate new private key

Once the key is downloaded, open it with notepad. Copy the content and use that directly as the value for your FIREBASE_JSON secret in Buildship.

![[supa_image6.jpeg]]

1. Then in Buildship, create a new flow. We will not have an input or output node. Just add a “Starter Script” node in the middle of the flow

![[supa_image6 1.jpeg]]

1. Click on the </> button on the node to open the script. In there, delete the existing script and paste this:

```jsx
import { createClient } from "@supabase/supabase-js";
import admin from "firebase-admin";

export default async function (
  { SUPABASE_URL, SUPABASE_SERVICE_ROLE, FIREBASE_JSON }: NodeInputs, // Access values of node input parameters
  {
    logging, // Utility for logging during execution
  }: NodeScriptOptions,
): NodeOutput {
  /* Log execution start */
  logging.log("Starting user migration from Supabase to Firebase");
  
  logging.log("Initializing Supabase client");
  const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE);

	logging.log("Initializing Firebase client");
  admin.initializeApp({
    credential: admin.credential.cert(FIREBASE_JSON )
  });

  
  /* Fetch all users from Supabase */
  ///////////////////////////////////
  logging.log("Fetching users from Supabase");
  const { data: users, error } = await supabase
    .from('users')
    .select('*')
    .is('firebaseId', null); // Only select users without a Firebase ID
  
  if (error) {
    logging.error("Error fetching users from Supabase:", error);
    return "Error: Failed to fetch users from Supabase.";
  }
  
  logging.log(`Found ${users.length} users to migrate`);
  
  /* Migrate each user to Firebase */
  const results = {
    total: users.length,
    successful: 0,
    failed: 0,
    errors: []
  };
  
  for (const user of users) {
    try {
      // Create user in Firebase //
      ////////////////////////////
      const userRecord = await admin.auth().createUser({
        email: user.email,
        displayName: user.display_name,
        phoneNumber: user.phone_number,
        disabled: false,
      });
      
      //Add authenticated to the JWT token for Supabase compatibility
      await admin.auth().setCustomUserClaims(userRecord.uid, {
        role: 'authenticated'
      });
      
      // Update Supabase with Firebase ID //
      /////////////////////////////////////
      const { error: updateError } = await supabase
        .from('users')
        .update({ firebaseId: userRecord.uid })
        .eq('id', user.id);
      
      if (updateError) {
        logging.error(`Failed to update Supabase user ${user.id}:`, updateError);
        results.errors.push({
          user: user.email,
          stage: 'supabase_update',
          error: updateError.message
        });
        results.failed++;
      } 
    } catch (error) {
      logging.error(`Error migrating user ${user.email}:`, error);
      results.errors.push({
        user: user.email,
        stage: 'firebase_creation',
        error: error.message
      });
      results.failed++;
    }
  }
  
  /* Log summary */
  logging.log("Migration complete");
  logging.log(`Total users: ${results.total}`);
  logging.log(`Successfully migrated: ${results.successful}`);
  logging.log(`Failed migrations: ${results.failed}`);
  
  if (results.errors.length > 0) {
    logging.log("Errors encountered:", results.errors);
  }
}
```

In this code snippets, there are 3 pieces of code that you need to adapt to your Supabase table format. For each, ensure that the email, display_name, phone_number and id column match your actual Supabase table.

1. Still inside the node, go to the inputs tab and create the 3 inputs we need. Make them all caps (to match our code). They are all of type $<String>$

![[supa_image7.png]]

1. Save the modifications. Add the required keys to each field

![[supa_image8.png]]

![[supa_image9.png]]

1. Test the script wit the “Test” button in the top right corner. This should properly create all users in Firebase for you. You can debug the errors via “logs” at the bottom of the screen if things didn’t work
2. Now that your Supabase users have been created in Firebase, you can continue with step 4 and start creating your users in Firebase from now on.
3. 