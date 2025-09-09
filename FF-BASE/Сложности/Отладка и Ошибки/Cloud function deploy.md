---
title: "How To Fix: Cloud Function Deployment Errors (All Solutions Discussion)"
source: https://community.flutterflow.io/discussions/post/how-to-fix-cloud-function-deployment-errors-all-solutions-discussion-wgfMLgpLrBlmnUI?highlight=9qlSlZS0KQzXK0H
author: []
published: 2023-11-15
created: 2025-06-13
description: Deploy Cloud Functions w/ No Errors - Guide/Mega-thread Hello everyone, The FlutterFlow Cloud Functions launch was exciting and got us all hoping to test the feature, however many of us (me included) ...
tags:
  - статьи
---
# Облачные функции
[FlutterFlow Cloud Functions Masterclass Part 1 - YouTube](https://www.youtube.com/live/PkHZiBZQMUU)
.onCall - вызываются через action в FF
.on Request - вызываются через webhook https

# How To Fix Cloud Function Deployment Errors (All Solutions Discussion)

> [!TIP] В исходном посте есть картинки

## Deploy Cloud Functions w/ No Errors - Guide/Mega-thread

Hello everyone,

The FlutterFlow Cloud Functions launch was exciting and got us all hoping to test the feature, however many of us (me included) hadn't had the opportunity to try it. Why? Because no functions want to deploy!

Getting hit with **Error: Unknown Error. Please contact support@flutterflow.io** SUCKS!

This post collects all the solutions to this issue in one place. I've personally gone through and tested each step and explained it - I hope it helps you!

### Step-by-Step Guide

Go through each of the steps below (no matter how obvious):

1. **Make sure the project is on Blaze plan on Firebase**
2. **Ensure Firebase is connected to FlutterFlow and all rules and everything are deployed**
	1. Check all settings pages in FlutterFlow and check each is reflected in your firebase console
3. **Make sure there are no errors in your custom code for the cloud function**
	1. For now, just create a blank function with just the boilerplate code and try to deploy just that. If you can do that, then you can move on to your actual cloud function code.
4. **Check if any other cloud function deployment succeeds (push notification, stripe, etc)**
	1. Do this by checking the existing auto-created cloud functions by FlutterFlow in your Google Cloud Console.
	2. Page: *https://console.firebase.google.com/project/* ***\[PROJECT-NAME\]*** */functions*
	3. If they're there, you're fine. To double check, click on any and it'll tell you the deploy date.
		1. If they're not, either,
			1. you haven't set up any up - that's fine, move on.
			2. you haven't done Step 2 properly (e.g. you're expecting the deleting 
5. **Make sure the region is explicitly selected and is not left as \[default\] - on both Advance Firebase Settings, and in the Cloud Function deploy page**
	1. Ensure the Region is consistent not only between the two settings, but with the rest of your Firebase Project. I found which region the rest of my Firebase Project was set to by going to the 'Project Settings' in the Firebase Cloud Console. It'll be next to: 'Default GCP resource location'. Use that as your reference for everywhere else.
	2. Advanced Settings: Go FlutterFlow 'Settings' > 'Firebase' the scroll down to 'Advanced Settings'
	3. On the cloud deploy page
	4. Note: FlutterFlow's auto-created functions are in 'us-central1', don't worry about that if your project is in another region - use your region, not FlutterFlow's.
6. **Change the 'Memory Allocation' from \[Default\] to something else.**
	1. What number it *should* be obviously depends on your cloud function. Just choose 128MB for the sake of figuring out whether changing it allows you to deploy.
1. **Add *async* to your cloud function**
	1. add *async* in the same place as this code snippet (& remove the line break)
		```javascript
		https.onCall( async  (data, context)
		```
	2. Note: This will be something you will need to add manually every time you start writing a function and is easy to forget to do.
2. **Don't forget to reload the boilerplate code (green button, top right) whenever you change any settings (e.g. region/memory) before deploying - the code doesn't change dynamically.**
3. **Review package.json file**
	1. Found as a default file in the FlutterFlow Cloud Functions page underneath any Cloud Functions you've created.
	2. Ensure that the packages used in the cloud functions you want to deploy are included in the dependencies.
		1. Search for the latest package versions here: [https://www.npmjs.com/](https://www.npmjs.com/)
	3. Update the "node" engine from ">=18" to "18"
	4. Some accounts have this packages.json completely empty - like mine! If that's the case or you just want the fresh starter code with no errors, copy the code below:
		```json
		{
		  "name": "functions",
		  "description": "Firebase Custom Cloud Functions",
		  "engines":{
		    "node": "18"
		  },
		  "main": "index.js",
		  "dependencies": {
		    "firebase-admin": "^11.8.0",
		    "firebase-functions": "^4.3.0"
		  },
		  "private": true
		}
		```

### Final Boilerplate Check

After all the edits, your boilerplate code should look like this:

```javascript
const functions = require('firebase-functions');
const admin = require('firebase-admin');
// To avoid deployment errors, do not call admin.initializeApp() in your code

// Change Region to your GCP resource location and add async to the function
exports.yourFunctionName = functions.region('europe-west3').
    runWith({
        memory: '128MB'
  }).https.onCall( async  (data, context) => {
    // Write your code below!
   
    // Write your code above!
  }
);
```

---

## Post-Deployment Common Problems

If you can successfully deploy, but the cloud function doesn't work in run mode. Open the browser console to read the errors. Below are some I've tested to work.

### CORS Error

This happens sometimes with new Cloud Functions, regardless of whether you deploy them through FlutterFlow or not.

**Step 1**: Follow this official tutorial for general CORS set up: [https://docs.flutterflow.io/actions/actions/utilities/upload-data#types-of-upload](https://docs.flutterflow.io/actions/actions/utilities/upload-data#types-of-upload)

**Step 2**: Follow the steps below to specifically set up CORS for your functions

- Open Cloud Functions in your GCP project: [https://console.cloud.google.com/functions/list](https://console.cloud.google.com/functions/list)
- Open your function.
- Go to "Permissions".
- Check that there's a row with Principal="allUsers" and Role="Cloud Functions Invoker".
- If it's missing, click "Grant Access" and add that permission.
	- It'll ask if you're sure about making it public. Click Yes.
	- *Side Note: [Anton](https://community.flutterflow.io/member/3AsJZwm9ge) - [Inactive Member](https://community.flutterflow.io/member/rD3UZFPkvM), while this works, is there a more secure way? Not everyone will be comfortable with allUsers. Other functions use emails addresses (Google Accounts) or domains.*

---

## Deploy Functions Direct To Firebase

If FlutterFlow is *still* causing you issues or you just don't want to dance around the bugs, then you can just deploy your functions direct to firebase. Then all you need to do is trigger them via a FF API requests (or any way you want) to interact with them.

Google has an awesome tutorial playlist for anyone wanting to give it a go: [https://www.youtube.com/playlist?list=PLl-K7zZEsYLkPZHe41m4jfAxUi0JjLgSM](https://www.youtube.com/playlist?list=PLl-K7zZEsYLkPZHe41m4jfAxUi0JjLgSM)

I followed it myself and can confirm it's bulletproof.

## Ошибка 403 при облачной функции
см. с 9:10 [видео Игната](https://www.youtube.com/watch?v=a4hUsxS1RqQ) 


---
